"""
OCR Module using Pytesseract
Provides text extraction from images and PDFs
"""

import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import Union, Optional, List
import io
import fitz  # PyMuPDF
import os
from pathlib import Path


class OCRProcessor:
    """OCR processor using Pytesseract"""
    
    def __init__(self, lang: str = 'vie+eng'):
        """
        Initialize OCR processor
        
        Args:
            lang: Language(s) for OCR (default: 'vie+eng' for Vietnamese and English)
                  Use 'eng' for English only, 'vie' for Vietnamese only
        """
        self.lang = lang
    
    @staticmethod
    def is_pdf(file_source: Union[str, bytes]) -> bool:
        """
        Check if the file is a PDF
        
        Args:
            file_source: File path or bytes data
            
        Returns:
            True if file is PDF, False otherwise
        """
        if isinstance(file_source, str):
            # Check file extension
            if file_source.lower().endswith('.pdf'):
                return True
            # Check file header
            try:
                with open(file_source, 'rb') as f:
                    header = f.read(4)
                    return header == b'%PDF'
            except:
                return False
        elif isinstance(file_source, bytes):
            # Check bytes header
            return file_source[:4] == b'%PDF'
        return False
    
    @staticmethod
    def pdf_to_images(
        pdf_source: Union[str, bytes], 
        dpi: int = 300,
        save_to_temp: bool = True,
        temp_dir: str = "temp"
    ) -> List[np.ndarray]:
        """
        Convert PDF pages to images using PyMuPDF
        
        Args:
            pdf_source: PDF file path or bytes data
            dpi: Resolution for conversion (default: 300)
            save_to_temp: Whether to save images to temp directory (default: True)
            temp_dir: Temporary directory path (default: "temp")
            
        Returns:
            List of images as numpy arrays (one per page)
        """
        images = []
        saved_paths = []
        
        try:
            # Open PDF
            if isinstance(pdf_source, str):
                pdf_document = fitz.open(pdf_source)
                pdf_name = Path(pdf_source).stem  # Get filename without extension
            elif isinstance(pdf_source, bytes):
                pdf_document = fitz.open(stream=pdf_source, filetype="pdf")
                pdf_name = "document"  # Default name for bytes input
            else:
                raise ValueError("PDF source must be file path or bytes")
            
            # Create temp directory if saving is enabled
            if save_to_temp:
                temp_path = Path(temp_dir) / pdf_name
                temp_path.mkdir(parents=True, exist_ok=True)
            
            # Convert each page to image
            zoom = dpi / 72  # Default PDF DPI is 72
            mat = fitz.Matrix(zoom, zoom)
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=mat)
                
                # Convert to numpy array
                img_data = pix.samples
                img = np.frombuffer(img_data, dtype=np.uint8).reshape(
                    pix.height, pix.width, pix.n
                )
                
                # Convert RGBA to BGR if needed
                if pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                elif pix.n == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                images.append(img)
                
                # Save to temp directory if enabled
                if save_to_temp:
                    img_filename = f"{pdf_name}_page_{page_num + 1}.png"
                    img_path = temp_path / img_filename
                    cv2.imwrite(str(img_path), img)
                    saved_paths.append(str(img_path))
                    print(f"Saved: {img_path}")
            
            pdf_document.close()
            
            if save_to_temp:
                print(f"All {len(images)} pages saved to: {temp_path}")
            
            return images
            
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Apply thresholding to get binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised
    
    def extract_text_from_image(
        self, 
        image_source: Union[str, bytes, np.ndarray, Image.Image],
        preprocess: bool = True,
        config: str = '--psm 6'
    ) -> str:
        """
        Extract text from image
        
        Args:
            image_source: Can be:
                - str: Path to image file
                - bytes: Image data as bytes
                - np.ndarray: Image as numpy array (OpenCV format)
                - Image.Image: PIL Image object
            preprocess: Whether to preprocess image (default: True)
            config: Pytesseract configuration (default: '--psm 6')
                   PSM modes:
                   0 = Orientation and script detection (OSD) only
                   1 = Automatic page segmentation with OSD
                   3 = Fully automatic page segmentation (default)
                   6 = Assume a single uniform block of text
                   11 = Sparse text. Find as much text as possible
                   
        Returns:
            Extracted text as string
        """
        try:
            # Check if it's a PDF first
            if isinstance(image_source, (str, bytes)) and self.is_pdf(image_source):
                return self.extract_text_from_pdf(image_source, preprocess, config)
            
            # Load image based on source type
            if isinstance(image_source, str):
                # File path
                image = cv2.imread(image_source)
                if image is None:
                    raise ValueError(f"Could not load image from path: {image_source}")
            elif isinstance(image_source, bytes):
                # Bytes data
                nparr = np.frombuffer(image_source, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif isinstance(image_source, np.ndarray):
                # Numpy array
                image = image_source
            elif isinstance(image_source, Image.Image):
                # PIL Image
                image = cv2.cvtColor(np.array(image_source), cv2.COLOR_RGB2BGR)
            else:
                raise ValueError("Unsupported image source type")
            
            # Preprocess if requested
            if preprocess:
                image = self.preprocess_image(image)
            
            # Convert to PIL Image for pytesseract
            pil_image = Image.fromarray(image)
            
            # Extract text
            text = pytesseract.image_to_string(pil_image, lang=self.lang, config=config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error during OCR processing: {str(e)}")
    
    def extract_text_from_pdf(
        self,
        pdf_source: Union[str, bytes],
        preprocess: bool = True,
        config: str = '--psm 6',
        dpi: int = 300,
        save_images: bool = True,
        temp_dir: str = "temp"
    ) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_source: PDF file path or bytes data
            preprocess: Whether to preprocess images (default: True)
            config: Pytesseract configuration
            dpi: Resolution for PDF to image conversion (default: 300)
            save_images: Whether to save extracted images to temp directory (default: True)
            temp_dir: Temporary directory path (default: "temp")
            
        Returns:
            Extracted text from all pages combined
        """
        try:
            # Convert PDF to images
            images = self.pdf_to_images(pdf_source, dpi=dpi, save_to_temp=save_images, temp_dir=temp_dir)
            
            # Extract text from each page
            all_text = []
            for page_num, image in enumerate(images, 1):
                text = self.extract_text_from_image(image, preprocess=preprocess, config=config)
                if text.strip():
                    all_text.append(f"--- Page {page_num} ---\n{text}")
            
            return "\n\n".join(all_text)
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_data(
        self,
        image_source: Union[str, bytes, np.ndarray, Image.Image],
        preprocess: bool = True
    ) -> dict:
        """
        Extract detailed data from image including text, confidence, and bounding boxes
        
        Args:
            image_source: Image source (same formats as extract_text_from_image)
            preprocess: Whether to preprocess image
            
        Returns:
            Dictionary containing:
                - text: Full extracted text
                - words: List of detected words with confidence and position
        """
        try:
            # Check if it's a PDF
            if isinstance(image_source, (str, bytes)) and self.is_pdf(image_source):
                return self.extract_data_from_pdf(image_source, preprocess)
            
            # Load and preprocess image
            if isinstance(image_source, str):
                image = cv2.imread(image_source)
            elif isinstance(image_source, bytes):
                nparr = np.frombuffer(image_source, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            elif isinstance(image_source, np.ndarray):
                image = image_source
            elif isinstance(image_source, Image.Image):
                image = cv2.cvtColor(np.array(image_source), cv2.COLOR_RGB2BGR)
            else:
                raise ValueError("Unsupported image source type")
            
            if preprocess:
                image = self.preprocess_image(image)
            
            pil_image = Image.fromarray(image)
            
            # Get detailed data
            data = pytesseract.image_to_data(pil_image, lang=self.lang, output_type=pytesseract.Output.DICT)
            
            # Extract full text
            text = pytesseract.image_to_string(pil_image, lang=self.lang)
            
            # Parse word-level information
            words = []
            n_boxes = len(data['text'])
            for i in range(n_boxes):
                if int(data['conf'][i]) > 0:  # Only include words with positive confidence
                    word_info = {
                        'text': data['text'][i],
                        'confidence': float(data['conf'][i]),
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    }
                    words.append(word_info)
            
            return {
                'text': text.strip(),
                'words': words
            }
            
        except Exception as e:
            raise Exception(f"Error during OCR data extraction: {str(e)}")
    
    def extract_data_from_pdf(
        self,
        pdf_source: Union[str, bytes],
        preprocess: bool = True,
        dpi: int = 300,
        save_images: bool = True,
        temp_dir: str = "temp"
    ) -> dict:
        """
        Extract detailed data from PDF
        
        Args:
            pdf_source: PDF file path or bytes data
            preprocess: Whether to preprocess images
            dpi: Resolution for PDF to image conversion
            save_images: Whether to save extracted images to temp directory (default: True)
            temp_dir: Temporary directory path (default: "temp")
            
        Returns:
            Dictionary containing:
                - text: Full extracted text from all pages
                - pages: List of page data with words and confidence
        """
        try:
            images = self.pdf_to_images(pdf_source, dpi=dpi, save_to_temp=save_images, temp_dir=temp_dir)
            
            all_text = []
            pages_data = []
            
            for page_num, image in enumerate(images, 1):
                page_data = self.extract_data(image, preprocess=preprocess)
                page_data['page_number'] = page_num
                pages_data.append(page_data)
                all_text.append(page_data['text'])
            
            return {
                'text': '\n\n'.join(all_text),
                'pages': pages_data
            }
            
        except Exception as e:
            raise Exception(f"Error extracting data from PDF: {str(e)}")
    
    def is_text_present(
        self,
        image_source: Union[str, bytes, np.ndarray, Image.Image],
        min_confidence: float = 60.0
    ) -> bool:
        """
        Check if text is present in the image
        
        Args:
            image_source: Image source
            min_confidence: Minimum confidence threshold (0-100)
            
        Returns:
            True if text is detected with sufficient confidence
        """
        try:
            data = self.extract_data(image_source)
            # Check if any word has confidence above threshold
            for word in data['words']:
                if word['confidence'] >= min_confidence and len(word['text'].strip()) > 0:
                    return True
            return False
        except:
            return False


# Convenience functions
def extract_text(
    image_source: Union[str, bytes, np.ndarray, Image.Image],
    lang: str = 'vie+eng',
    preprocess: bool = True
) -> str:
    """
    Quick function to extract text from image
    
    Args:
        image_source: Image source (file path, bytes, numpy array, or PIL Image)
        lang: Language for OCR (default: 'vie+eng')
        preprocess: Whether to preprocess image
        
    Returns:
        Extracted text
    """
    ocr = OCRProcessor(lang=lang)
    return ocr.extract_text_from_image(image_source, preprocess=preprocess)


def extract_text_from_file(file_path: str, lang: str = 'vie+eng') -> str:
    """
    Extract text from image file
    
    Args:
        file_path: Path to image file
        lang: Language for OCR
        
    Returns:
        Extracted text
    """
    ocr = OCRProcessor(lang=lang)
    return ocr.extract_text_from_image(file_path)


if __name__ == "__main__":
    # Example usage
    ocr = OCRProcessor(lang='vie+eng')
    
    # Example 1: Extract text from image
    # text = ocr.extract_text_from_image('./core/08888419.pdf')
    # print("Extracted text:", text)
    
    # Example 2: Extract text from PDF
    text = ocr.extract_text_from_pdf('./core/08888419.pdf')
    print("PDF text:", text)
    
    # Example 3: Extract text (auto-detect PDF or image)
    # text = ocr.extract_text_from_image('path/to/file.pdf')  # Works with both PDF and images
    # print("Extracted text:", text)
    
    # Example 4: Extract detailed data
    # data = ocr.extract_data('path/to/file.jpg')
    # print("Full text:", data['text'])
    # print("Number of words detected:", len(data['words']))
    
    # Example 5: Check if text is present
    # has_text = ocr.is_text_present('path/to/image.jpg')
    # print("Text present:", has_text)
    
    print("OCR module loaded successfully!")
    print("Supported languages: vie (Vietnamese), eng (English), vie+eng (both)")
    print("Supported formats: Images (PNG, JPG, etc.) and PDF files")
