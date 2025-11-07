import os
import logging

class FontManager:
    LANG_FONT_MAPPING = {
        'es': 'Helvetica',  # Spanish - Latin script
        'fr': 'Helvetica',  # French - Latin script  
        'de': 'Helvetica',  # German - Latin script
        'it': 'Helvetica',  # Italian - Latin script
        'pt': 'Helvetica',  # Portuguese - Latin script
        'ru': 'Helvetica',  # Russian - Cyrillic (basic)
        'hi': 'Helvetica',  # Hindi - Devanagari (basic)
        'ar': 'Helvetica',  # Arabic (basic)
        'zh': 'Helvetica',  # Chinese (basic)
        'ja': 'Helvetica',  # Japanese (basic)
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_font_for_language(self, lang_code: str) -> str:
        return self.LANG_FONT_MAPPING.get(lang_code, 'Helvetica')