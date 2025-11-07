import gradio as gr
import os
from src.utils import translate_complete_pdf
from src.translator import TranslationAgent

# Initialize translator
translator_agent = TranslationAgent(preload_languages=["es"])

def gradio_translate_pdf(input_pdf, target_lang, progress=gr.Progress()):
    try:
        if input_pdf is None:
            return None, "Please upload a PDF file"
        
        base_name = os.path.splitext(os.path.basename(input_pdf))[0]
        output_pdf = f"{base_name}_{target_lang}.pdf"
        
        def update_progress(percent, message=""):
            progress(percent, desc=message)
        
        result_path = translate_complete_pdf(
            input_pdf, target_lang, output_pdf, update_progress, translator_agent
        )
        
        return result_path, "✅ Translation complete! Click the file above to download."
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

with gr.Blocks(title="PDF Translator") as demo:
    gr.Markdown("# PDF Translation Bot")
    gr.Markdown("**Upload PDF → Select Language → Download Translated PDF**")
    
    with gr.Row():
        with gr.Column():
            pdf_input = gr.File(
                label="📄 Upload PDF File",
                file_types=[".pdf"]
            )
            
            lang_dropdown = gr.Dropdown(
                choices=[
                    ("🇪🇸 Spanish", "es"),
                    ("🇫🇷 French", "fr"), 
                    ("🇩🇪 German", "de"),
                    ("🇮🇹 Italian", "it"),
                    ("🇵🇹 Portuguese", "pt"),
                    ("🇷🇺 Russian", "ru"),
                    ("🇮🇳 Hindi", "hi"),
                    ("🇦🇪 Arabic", "ar"),
                    ("🇨🇳 Chinese", "zh"),
                    ("🇯🇵 Japanese", "ja")
                ],
                label="🌐 Select Target Language",
                value="es"
            )
            
            translate_btn = gr.Button("🚀 Translate PDF", variant="primary", size="lg")
        
        with gr.Column():
            gr.Markdown("### 📥 Download Translated PDF")
            
            pdf_output = gr.File(
                label="Your translated file will appear here",
                interactive=False
            )
            
            gr.Markdown("**⬆️ Click the file above to download**")
            
            status_output = gr.Textbox(
                label="📊 Status",
                value="🟢 Ready - Upload a PDF and click Translate",
                interactive=False
            )
    
    translate_btn.click(
        fn=gradio_translate_pdf,
        inputs=[pdf_input, lang_dropdown],
        outputs=[pdf_output, status_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
