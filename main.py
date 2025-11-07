import logging
import os
from src.pdf_processor import PDFProcessor, TextBlock  
from src.translator import TranslationAgent
from src.pdf_builder import PDFBuilder
from src.font_manager import FontManager

def translate_complete_pdf(input_pdf: str, target_lang: str, output_pdf: str = None):
    """
    Complete PDF translation pipeline
    """
    logging.basicConfig(level=logging.INFO)
    
    
    processor = PDFProcessor()
    translator = TranslationAgent()
    pdf_builder = PDFBuilder()
    font_manager = FontManager()
    
    print(f"🚀 Starting translation: {input_pdf} → {target_lang}")
    
    print("📄 Extracting text from PDF...")
    blocks = processor.extract_text_blocks(input_pdf)
    print(f"✅ Extracted {len(blocks)} text blocks")
    

    print(f"🌍 Translating to {target_lang}...")
    translated_blocks = []
    
    for i, block in enumerate(blocks):
        if block.text.strip():  
            translated_text = translator.translate_text(block.text, target_lang)
            translated_block = TextBlock(
                text=translated_text,
                bbox=block.bbox,
                page_num=block.page_num,
                font_size=block.font_size,
                font_name=font_manager.get_font_for_language(target_lang)
            )
            translated_blocks.append(translated_block)
        
        
        if (i + 1) % 50 == 0:
            print(f"   Translated {i + 1}/{len(blocks)} blocks...")
    
    
    if output_pdf is None:
        base_name = os.path.splitext(input_pdf)[0]
        output_pdf = f"{base_name}_{target_lang}_translated.pdf"
    
    
    print("📝 Rebuilding PDF with translations...")
    result_path = pdf_builder.rebuild_pdf_with_translations(
        input_pdf, translated_blocks, output_pdf
    )
    
    print(f"✅ TRANSLATION COMPLETE!")
    print(f"📁 Output: {result_path}")
    print(f"📊 Stats: {len(blocks)} blocks translated to {target_lang}")
    
    return result_path

def main():
    
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in current directory.")
        return
    
    print("Available PDFs:")
    for i, pdf in enumerate(pdf_files):
        print(f"  {i + 1}. {pdf}")
    

    input_pdf = pdf_files[0]
    
    
    print(f"\n{'='*50}")
    translate_complete_pdf(input_pdf, 'es')  
    
    print(f"\n🎉 TRANSLATION COMPLETED!")

if __name__ == "__main__":
    main()
