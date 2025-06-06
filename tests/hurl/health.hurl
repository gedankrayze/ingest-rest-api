# Health check endpoints

# Test root endpoint
GET http://localhost:8000/
HTTP 200
[Asserts]
jsonpath "$.message" == "MarkItDown REST API"
jsonpath "$.status" == "running"

# Test health endpoint
GET http://localhost:8000/health
HTTP 200
[Asserts]
jsonpath "$.status" == "healthy"