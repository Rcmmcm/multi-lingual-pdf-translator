import logging
import os
from src.pdf_processor import PDFProcessor, TextBlock
from src.pdf_builder import PDFBuilder
from src.font_manager import FontManager

# REMOVED the circular import from app

def translate_complete_pdf(input_pdf: str, target_lang: str, output_pdf: str = None, progress_callback=None, translator_agent=None):
    """
    Complete PDF translation pipeline - pass translator as parameter
    """
    logging.basicConfig(level=logging.INFO)
    
    # Initialize components
    processor = PDFProcessor()
    pdf_builder = PDFBuilder()
    font_manager = FontManager()
    
    if progress_callback:
        progress_callback(0.1, "📄 Extracting text from PDF...")
    
    # Step 1: Extract text
    blocks = processor.extract_text_blocks(input_pdf)
    
    if progress_callback:
        progress_callback(0.3, f"✅ Extracted {len(blocks)} text blocks")
    
    # Step 2: Prepare texts for translation
    texts_to_translate = [block.text for block in blocks if block.text.strip()]
    
    if progress_callback:
        progress_callback(0.4, f"🌍 Translating {len(texts_to_translate)} blocks...")
    
    # Step 3: Translate with progress (using passed translator)
    def translation_progress(progress):
        if progress_callback:
            current_progress = 0.4 + (progress * 0.5)
            progress_callback(current_progress, f"Translating... {int(progress*100)}%")
    
    translated_texts = translator_agent.batch_translate_with_progress(
        texts_to_translate, target_lang, translation_progress
    )
    
    if progress_callback:
        progress_callback(0.9, "📝 Rebuilding PDF with translations...")
    
    translated_blocks = []
    text_index = 0
    
    for block in blocks:
        if block.text.strip():
            translated_block = TextBlock(
                text=translated_texts[text_index],
                bbox=block.bbox,
                page_num=block.page_num,
                font_size=block.font_size,
                font_name=font_manager.get_font_for_language(target_lang)
            )
            translated_blocks.append(translated_block)
            text_index += 1
        else:
            translated_blocks.append(block)
    
    if output_pdf is None:
        base_name = os.path.splitext(input_pdf)[0]
        output_pdf = f"{base_name}_{target_lang}_translated.pdf"
    
    result_path = pdf_builder.rebuild_pdf_with_translations(
        input_pdf, translated_blocks, output_pdf
    )
    
    if progress_callback:
        progress_callback(1.0, "✅ Translation complete!")
    
    return result_path
