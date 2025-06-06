# Image conversion tests with OCR

# Test JPG image conversion
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.jpg; filename="sample.jpg"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.jpg"
jsonpath "$.original_format" == ".jpg"
jsonpath "$.markdown_content" exists
jsonpath "$.metadata" exists
jsonpath "$.conversion_time" exists

# Test PNG image conversion if available
POST http://localhost:8000/api/v1/convert
[MultipartFormData]
file: file,sample.png; filename="sample.png"
HTTP 200
[Asserts]
jsonpath "$.filename" == "sample.png"
jsonpath "$.original_format" == ".png"
jsonpath "$.markdown_content" exists

# Test image download
POST http://localhost:8000/api/v1/convert?download=true
[MultipartFormData]
file: file,sample.jpg; filename="sample.jpg"
HTTP 200
[Asserts]
header "Content-Type" contains "text/markdown"
header "Content-Disposition" contains "attachment"
header "Content-Disposition" contains "sample.md"