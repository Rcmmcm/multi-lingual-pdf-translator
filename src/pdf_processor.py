import fitz
import logging
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class TextBlock:
    text: str
    bbox: Tuple[float, float, float, float]
    page_num: int
    font_size: float
    font_name: str

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text_blocks(self, pdf_path: str) -> List[TextBlock]:
        text_blocks = []
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")
                for block in blocks["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["text"].strip():
                                    text_blocks.append(TextBlock(
                                        text=span["text"].strip(),
                                        bbox=span["bbox"],
                                        page_num=page_num,
                                        font_size=span["size"],
                                        font_name=span["font"]
                                    ))
            doc.close()
            return text_blocks
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise