from markitdown import MarkItDown
import time
import os
from typing import Optional, Dict, Any

class ConversionService:
    def __init__(self):
        self.converter = MarkItDown()
    
    def convert_file(self, file_path: str) -> tuple[str, Dict[str, Any], float]:
        """
        Convert a file to markdown using MarkItDown
        
        Args:
            file_path: Path to the file to convert
            
        Returns:
            tuple: (markdown_content, metadata, conversion_time)
        """
        start_time = time.time()
        
        try:
            result = self.converter.convert(file_path)
            conversion_time = time.time() - start_time
            
            metadata = {
                "file_size": os.path.getsize(file_path),
                "converted_at": time.time()
            }
            
            return result.text_content, metadata, conversion_time
            
        except Exception as e:
            raise Exception(f"Conversion failed: {str(e)}")
    
    def get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        return os.path.splitext(filename)[1].lower()
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported by MarkItDown"""
        supported_extensions = {
            '.pdf', '.pptx', '.docx', '.xlsx', '.xls',
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff',
            '.mp3', '.wav', '.m4a', '.ogg',
            '.html', '.htm', '.xml', '.csv', '.json',
            '.txt', '.md', '.rtf', '.epub', '.zip'
        }
        
        ext = self.get_file_extension(filename)
        return ext in supported_extensions