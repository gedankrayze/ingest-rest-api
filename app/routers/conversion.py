from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import Response
import tempfile
import os
from typing import Optional

from app.models.conversion import ConversionResponse, ErrorResponse
from app.services.converter import ConversionService

router = APIRouter(tags=["conversion"])
converter_service = ConversionService()

@router.post("/convert", response_model=ConversionResponse)
async def convert_file(
    file: UploadFile = File(...),
    download: Optional[bool] = False
):
    """
    Convert uploaded file to Markdown format
    
    Args:
        file: File to convert
        download: If True, return markdown as downloadable file
        
    Returns:
        ConversionResponse with markdown content
    """
    
    if not converter_service.is_supported_format(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. File: {file.filename}"
        )
    
    temp_file_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            temp_file_path = tmp_file.name
            content = await file.read()
            tmp_file.write(content)
        
        markdown_content, metadata, conversion_time = converter_service.convert_file(temp_file_path)
        
        if download:
            markdown_filename = os.path.splitext(file.filename)[0] + ".md"
            return Response(
                content=markdown_content,
                media_type="text/markdown",
                headers={
                    "Content-Disposition": f"attachment; filename={markdown_filename}"
                }
            )
        
        return ConversionResponse(
            filename=file.filename,
            original_format=converter_service.get_file_extension(file.filename),
            markdown_content=markdown_content,
            metadata=metadata,
            conversion_time=conversion_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.post("/convert/batch")
async def convert_files_batch(
    files: list[UploadFile] = File(...)
):
    """
    Convert multiple files to Markdown format
    
    Args:
        files: List of files to convert
        
    Returns:
        List of ConversionResponse objects
    """
    results = []
    errors = []
    
    for file in files:
        try:
            result = await convert_file(file=file)
            results.append(result)
        except HTTPException as e:
            errors.append({
                "filename": file.filename,
                "error": e.detail
            })
    
    return {
        "successful_conversions": results,
        "errors": errors,
        "total_files": len(files),
        "successful": len(results),
        "failed": len(errors)
    }