from markitdown import MarkItDown
import time
import os
import logging
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    OpenAI = None
    openai_available = False

# Configure logger
logger = logging.getLogger(__name__)

class ConversionService:
    def __init__(self):
        # Initialize with OpenAI client if API key is available for image OCR
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("MODEL", "gpt-4o")  # Default to gpt-4o, gpt-4-turbo recommended
        
        if api_key and openai_available:
            client = OpenAI(api_key=api_key)
            self.converter = MarkItDown(llm_client=client, llm_model=model)
            logger.info(f"MarkItDown ready with OpenAI ({model})")
        else:
            self.converter = MarkItDown()
            if not api_key:
                logger.info("MarkItDown ready (no OpenAI API key)")
            else:
                logger.warning("MarkItDown ready (openai package missing)")
    
    def convert_file(self, file_path: str) -> tuple[str, Dict[str, Any], float]:
        """
        Convert a file to markdown using MarkItDown
        
        Args:
            file_path: Path to the file to convert
            
        Returns:
            tuple: (markdown_content, metadata, conversion_time)
        """
        file_name = os.path.basename(file_path)
        file_extension = self.get_file_extension(file_name)
        file_size = os.path.getsize(file_path)
        
        logger.info(f"Converting {file_name} ({file_extension}, {file_size} bytes)")
        start_time = time.time()
        
        try:
            result = self.converter.convert(file_path)
            conversion_time = time.time() - start_time
            
            metadata = {
                "file_size": file_size,
                "converted_at": time.time()
            }
            
            logger.info(f"Converted {file_name} in {conversion_time:.2f}s")
            return result.text_content, metadata, conversion_time
            
        except Exception as e:
            logger.error(f"Failed to convert {file_name}: {str(e)}")
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