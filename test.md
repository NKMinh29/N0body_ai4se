1. Upload PDF file thành công
- *Input:* sample.pdf (chứa "Hello AI")
- *Request:* POST /api/upload/pdf
- *Expected Result:*
  ```json
  { "status": "success", "content": "Hello AI" }
2. Upload image file thành công
Input: sample.png (ảnh chứa "AI4SE")
Request: POST /api/upload/image
Expected Result:
  { "status": "success", "text": "AI4SE" }
3. Upload PDF không hợp lệ
Input: corrupt.pdf
Request: POST /api/upload/pdf
Expected Result:
{ "status": "error", "message": "Invalid PDF file" }
4. Upload image không hợp lệ
Input: corrupt.png
Request: POST /api/upload/image
Expected Result:
{ "status": "error", "message": "Invalid image file" }
5. Upload file không đúng định dạng
Input: sample.txt
Request: POST /api/upload/pdf
Expected Result:
{ "status": "error", "message": "Unsupported file type" }
6. Upload PDF lớn hơn 10MB
Input: large.pdf (>10MB)
Request: POST /api/upload/pdf
Expected Result:
{ "status": "error", "message": "File too large" }
7. Upload image lớn hơn 10MB
Input: large.png (>10MB)
Request: POST /api/upload/image
Expected Result:
{ "status": "error", "message": "File too large" }
8. Upload PDF không có nội dung
Input: empty.pdf
Request: POST /api/upload/pdf
Expected Result:\{ "status": "error", "message": "File too large" }
9. Upload image không có text
Input: blank.png
Request: POST /api/upload/image
Expected Result:
{ "status": "success", "text": "" }
10. FE: Hiển thị nội dung PDF sau upload
Input: sample.pdf (chứa "Hello AI")
Expected UI: Trang web hiển thị: Nội dung file: Hello AI
11. FE: Hiển thị text trích xuất từ ảnh
Input: sample.png (ảnh chứa "AI4SE")
Expected UI: Trang web hiển thị: Text trích xuất: AI4SE
12. FE: Hiển thị lỗi khi upload file không hợp lệ
Input: corrupt.pdf
Expected UI: Thông báo lỗi: Invalid PDF file
13. FE: Upload nhiều file PDF cùng lúc
Input: file1.pdf, file2.pdf
Expected UI: Hiển thị nội dung cả hai file
14. FE: Upload nhiều ảnh cùng lúc
Input: img1.png, img2.png
Expected UI: Hiển thị text trích xuất từ cả hai ảnh
15. FE: Upload file khi chưa đăng nhập (nếu có auth)
Input: sample.pdf
Expected UI: Thông báo: Bạn cần đăng nhập để upload file
