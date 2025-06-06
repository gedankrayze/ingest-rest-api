# Single file conversion tests

# Test PDF conversion
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.pdf; filename="sample.pdf"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.pdf"
jsonpath "$.original_format" == ".pdf"
jsonpath "$.markdown_content" exists
jsonpath "$.metadata" exists
jsonpath "$.conversion_time" exists

# Test DOCX conversion
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.docx; filename="sample.docx"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.docx"
jsonpath "$.original_format" == ".docx"
jsonpath "$.markdown_content" exists

# Test TXT conversion
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.txt; filename="sample.txt"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.txt"
jsonpath "$.original_format" == ".txt"
jsonpath "$.markdown_content" exists

# Test image (JPG) conversion with OCR
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.jpg; filename="sample.jpg"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.jpg"
jsonpath "$.original_format" == ".jpg"
jsonpath "$.markdown_content" exists
jsonpath "$.metadata" exists

# Test with download option
POST http://localhost:8000/api/v1/convert?download=true
[MultipartFormData]
file: file,sample.txt; filename="sample.txt"
HTTP 200
[Asserts]
header "Content-Type" contains "text/markdown"
header "Content-Disposition" contains "attachment"

# Test unsupported format
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,unsupported.xyz; filename="unsupported.xyz"
HTTP 400
[Asserts]
jsonpath "$.detail" contains "Unsupported file format"