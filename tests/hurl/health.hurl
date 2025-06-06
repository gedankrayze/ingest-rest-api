# Health check endpoints

# Test root endpoint
GET http://localhost:8000/
HTTP 200
[Asserts]
header "Content-Type" contains "text/html"
body contains "MarkItDown REST API"

# Test health endpoint
GET http://localhost:8000/health
HTTP 200
[Asserts]
jsonpath "$.status" == "healthy"