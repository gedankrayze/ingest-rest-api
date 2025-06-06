# Batch file conversion tests

# Test batch conversion with multiple files
POST http://localhost:8000/api/v1/convert/batch
[MultipartFormData]
files: file,sample.pdf; filename="sample.pdf"
files: file,sample.docx; filename="sample.docx"
files: file,sample.txt; filename="sample.txt"
HTTP 200
[Asserts]
jsonpath "$.total_files" == 3
jsonpath "$.successful" >= 0
jsonpath "$.failed" >= 0
jsonpath "$.successful_conversions" exists
jsonpath "$.errors" exists

# Test batch with mixed supported and unsupported files
POST http://localhost:8000/api/v1/convert/batch
[MultipartFormData]
files: file,sample.pdf; filename="sample.pdf"
files: file,unsupported.xyz; filename="unsupported.xyz"
HTTP 200
[Asserts]
jsonpath "$.total_files" == 2
jsonpath "$.successful" == 1
jsonpath "$.failed" == 1
jsonpath "$.errors[0].filename" == "unsupported.xyz"