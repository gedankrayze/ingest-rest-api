# MarkItDown REST API

A FastAPI-based REST API service that converts various file formats to Markdown using Microsoft's MarkItDown library.

## Features

- Convert single files to Markdown format
- Batch conversion support
- Download converted files or get JSON response
- Support for multiple file formats:
  - Documents: PDF, DOCX, PPTX, XLSX
  - Images: PNG, JPG, JPEG, GIF, BMP, TIFF
  - Audio: MP3, WAV, M4A, OGG
  - Web: HTML, XML
  - Data: CSV, JSON
  - Text: TXT, MD, RTF
  - Other: EPUB, ZIP

## Installation

1. Create virtual environment and install dependencies:
```bash
task install
```

Or manually:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Convert Single File
```bash
POST /api/v1/convert
```

Upload a file to convert to Markdown. Optional query parameter `download=true` to download the result as a .md file.

Example:
```bash
curl -X POST "http://localhost:8000/api/v1/convert" \
  -F "file=@document.pdf"
```

### Batch Convert Files
```bash
POST /api/v1/convert/batch
```

Convert multiple files in a single request.

Example:
```bash
curl -X POST "http://localhost:8000/api/v1/convert/batch" \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.docx"
```

### Health Check
```bash
GET /health
```

## API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker

Build and run with Docker:

```bash
# Build the image
docker build -t markitdown-api .

# Run the container
docker run -p 8000:8000 markitdown-api
```

## Response Format

### Single File Conversion
```json
{
  "filename": "document.pdf",
  "original_format": ".pdf",
  "markdown_content": "# Converted content...",
  "metadata": {
    "file_size": 12345,
    "converted_at": 1234567890.123
  },
  "conversion_time": 0.234
}
```

### Batch Conversion
```json
{
  "successful_conversions": [...],
  "errors": [...],
  "total_files": 3,
  "successful": 2,
  "failed": 1
}
```