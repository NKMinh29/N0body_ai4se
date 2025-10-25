# AI Assistant with OCR and RAG

Hệ thống AI Assistant tích hợp OCR và RAG (Retrieval-Augmented Generation) để xử lý và truy vấn tài liệu.

## 🎯 Tính năng

### 1. **OCR Module** (`core/OCR/OCR.py`)
- Trích xuất văn bản từ ảnh (PNG, JPG, etc.)
- Trích xuất văn bản từ PDF (tự động chuyển đổi thành ảnh)
- Lưu ảnh từ PDF vào thư mục `temp/`
- Hỗ trợ tiếng Việt và tiếng Anh
- Tiền xử lý ảnh để cải thiện độ chính xác

### 2. **RAG Assistant** (`core/AIssistance/AIssistance.py`)
- Sử dụng Gemini AI làm core chatbot
- Vector hóa tài liệu với ChromaDB
- Embeddings với Sentence Transformers
- Truy vấn ngữ nghĩa (semantic search)
- Tích hợp RAG để trả lời câu hỏi dựa trên tài liệu

## 📦 Cài đặt

### 1. Cài đặt system dependencies (Arch Linux)
```bash
sudo pacman -S tesseract tesseract-data-eng tesseract-data-vie
```

### 2. Cài đặt Python packages
```bash
pip install -r requirements.txt
```

### 3. Thiết lập Gemini API Key
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Hoặc tạo file `.env`:
```
GEMINI_API_KEY=your-api-key-here
```

## 🚀 Sử dụng

### Ví dụ 1: OCR cơ bản
```python
from core.OCR.OCR import OCRProcessor

# Khởi tạo OCR
ocr = OCRProcessor(lang='vie+eng')

# Trích xuất text từ ảnh
text = ocr.extract_text_from_image('document.png')
print(text)

# Trích xuất text từ PDF (tự động lưu ảnh vào temp/)
text = ocr.extract_text_from_pdf('document.pdf')
print(text)
```

### Ví dụ 2: RAG Assistant cơ bản
```python
from core.AIssistance.AIssistance import GeminiRAGAssistant

# Khởi tạo assistant
assistant = GeminiRAGAssistant()

# Thêm tài liệu vào knowledge base
documents = [
    "Python là ngôn ngữ lập trình bậc cao.",
    "Machine Learning là nhánh của AI.",
    "FastAPI là framework hiện đại cho Python."
]
assistant.add_documents_to_knowledge_base(documents)

# Truy vấn
result = assistant.query("Python là gì?")
print(result['answer'])
```

### Ví dụ 3: Tích hợp OCR + RAG
```python
from core.OCR.OCR import OCRProcessor
from core.AIssistance.AIssistance import GeminiRAGAssistant

# Khởi tạo
ocr = OCRProcessor(lang='vie+eng')
assistant = GeminiRAGAssistant(collection_name="my_documents")

# Trích xuất text từ PDF
text = ocr.extract_text_from_pdf('document.pdf')

# Thêm vào knowledge base
metadata = {'filename': 'document.pdf', 'type': 'pdf'}
assistant.add_documents_to_knowledge_base(text, [metadata])

# Truy vấn
result = assistant.query("Tóm tắt nội dung tài liệu")
print(result['answer'])
```

### Ví dụ 4: Chạy demo đầy đủ
```bash
python example_ocr_rag.py
```

## 📁 Cấu trúc thư mục

```
Ai4SE/
├── core/
│   ├── OCR/
│   │   └── OCR.py              # Module OCR
│   └── AIssistance/
│       └── AIssistance.py      # Module RAG Assistant
├── temp/                        # Ảnh từ PDF
│   └── {pdf_name}/
│       ├── {pdf_name}_page_1.png
│       └── {pdf_name}_page_2.png
├── chroma_db/                   # Vector database
├── example_ocr_rag.py          # Demo tích hợp
├── requirements.txt
└── README_AI.md                # File này
```

## 🔧 API Reference

### OCRProcessor

#### `__init__(lang='vie+eng')`
Khởi tạo OCR processor

#### `extract_text_from_image(image_source, preprocess=True)`
Trích xuất text từ ảnh hoặc PDF (tự động phát hiện)

#### `extract_text_from_pdf(pdf_source, save_images=True, temp_dir="temp")`
Trích xuất text từ PDF với tùy chọn lưu ảnh

#### `extract_data(image_source)`
Trích xuất text chi tiết với confidence và bounding boxes

### DocumentVectorizer

#### `__init__(collection_name, persist_directory, embedding_model)`
Khởi tạo vectorizer

#### `add_document(text, metadata, doc_id)`
Thêm 1 tài liệu

#### `add_documents(texts, metadatas, doc_ids)`
Thêm nhiều tài liệu

#### `add_document_from_file(file_path, chunk_size, chunk_overlap)`
Thêm tài liệu từ file text với chunking

#### `search(query, n_results)`
Tìm kiếm tài liệu liên quan

#### `get_collection_stats()`
Lấy thống kê collection

### GeminiRAGAssistant

#### `__init__(api_key, model_name, vectorizer, collection_name)`
Khởi tạo RAG assistant

#### `add_documents_to_knowledge_base(texts, metadatas)`
Thêm tài liệu vào knowledge base

#### `add_documents_from_directory(directory, pattern, chunk_size)`
Thêm tất cả file text từ thư mục

#### `query(question, n_context_docs, temperature, max_tokens)`
Truy vấn với RAG, trả về answer + sources

#### `chat(message, use_rag, n_context_docs)`
Chat đơn giản

#### `get_knowledge_base_stats()`
Lấy thống kê knowledge base

## 🎨 Workflow đầy đủ

```python
import os
from pathlib import Path
from core.OCR.OCR import OCRProcessor
from core.AIssistance.AIssistance import GeminiRAGAssistant

# 1. Khởi tạo
os.environ['GEMINI_API_KEY'] = 'your-key'
ocr = OCRProcessor(lang='vie+eng')
assistant = GeminiRAGAssistant(collection_name="documents")

# 2. Xử lý tài liệu
documents_path = Path("documents")

for file_path in documents_path.glob("**/*.pdf"):
    # Trích xuất text
    text = ocr.extract_text_from_pdf(str(file_path))
    
    # Thêm metadata
    metadata = {
        'filename': file_path.name,
        'path': str(file_path),
        'type': 'pdf'
    }
    
    # Lưu vào knowledge base
    assistant.add_documents_to_knowledge_base(text, [metadata])

# 3. Truy vấn
questions = [
    "Tóm tắt các tài liệu",
    "Có những thông tin gì về AI?",
    "Giải thích về Machine Learning"
]

for q in questions:
    result = assistant.query(q, n_context_docs=5)
    print(f"Q: {q}")
    print(f"A: {result['answer']}\n")
```

## 🔑 Lấy Gemini API Key

1. Truy cập: https://makersuite.google.com/app/apikey
2. Tạo API key mới
3. Copy và set vào environment variable

## ⚙️ Cấu hình nâng cao

### Thay đổi embedding model
```python
from core.AIssistance.AIssistance import DocumentVectorizer

vectorizer = DocumentVectorizer(
    embedding_model="paraphrase-multilingual-MiniLM-L12-v2"  # Tốt hơn cho tiếng Việt
)
```

### Thay đổi Gemini model
```python
assistant = GeminiRAGAssistant(
    model_name="gemini-1.5-pro"  # Model mạnh hơn
)
```

### Chunking strategy
```python
# Chunk nhỏ hơn cho văn bản ngắn
vectorizer.add_document_from_file(
    "document.txt",
    chunk_size=500,
    chunk_overlap=100
)
```

## 📊 Performance Tips

1. **OCR**: Sử dụng `dpi=300` cho PDF chất lượng cao
2. **Embeddings**: Model nhỏ hơn = nhanh hơn nhưng ít chính xác hơn
3. **ChromaDB**: Tự động persist, không cần save thủ công
4. **Chunking**: Chunk lớn = context tốt, chunk nhỏ = tìm kiếm chính xác

## 🐛 Troubleshooting

### Lỗi "GEMINI_API_KEY not found"
```bash
export GEMINI_API_KEY="your-key"
```

### Lỗi Tesseract
```bash
# Cài đặt lại
sudo pacman -S tesseract tesseract-data-vie
```

### Lỗi ChromaDB
```bash
# Xóa và tạo lại
rm -rf chroma_db/
```

## 📝 License

MIT License

## 👥 Contributors

- Your Name

## 🔗 Links

- Gemini API: https://ai.google.dev/
- ChromaDB: https://www.trychroma.com/
- Pytesseract: https://github.com/madmaze/pytesseract
