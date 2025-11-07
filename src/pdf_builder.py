import fitz
import logging
from typing import List
from .pdf_processor import TextBlock

class PDFBuilder:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def rebuild_pdf_with_translations(self, original_pdf_path: str, 
                                    translated_blocks: List[TextBlock],
                                    output_path: str) -> str:
        """
        Create new PDF with translated text while preserving layout
        """
        try:
            # Open original PDF
            doc = fitz.open(original_pdf_path)
            
            for block in translated_blocks:
                page = doc[block.page_num]
                
                # Remove original text by drawing white rectangle
                page.draw_rect(block.bbox, color=(1, 1, 1), fill=(1, 1, 1))
                
                # Add translated text at same position
                page.insert_text(
                    point=(block.bbox[0], block.bbox[3] - 2),  # Slightly above bottom
                    text=block.text,
                    fontsize=block.font_size,
                    fontname=block.font_name
                )
            
            # Save the new PDF
            doc.save(output_path)
            doc.close()
            
            self.logger.info(f"Translated PDF saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error rebuilding PDF: {e}")
            raise