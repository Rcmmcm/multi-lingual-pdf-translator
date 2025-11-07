from transformers import pipeline
import torch
import logging
from typing import Dict, Optional, List
import threading

class TranslationAgent:
    def __init__(self, preload_languages: List[str] = None):
        self.cache_dir = "./model_cache"
        self.logger = logging.getLogger(__name__)
        self._pipelines = {}
        self._loading = {}
        
        # Pre-load common languages in background
        if preload_languages:
            self._preload_languages(preload_languages)
    
    def _preload_languages(self, languages: List[str]):
        """Pre-load translation models in background thread"""
        def load_models():
            for lang in languages:
                if lang not in self._pipelines and lang not in self._loading:
                    self._loading[lang] = True
                    try:
                        self.logger.info(f"🔄 Pre-loading {lang} model...")
                        self.get_translator(lang)  # This loads the model
                        self.logger.info(f"✅ Pre-loaded {lang} model")
                    except Exception as e:
                        self.logger.error(f"❌ Failed to pre-load {lang}: {e}")
                    finally:
                        self._loading[lang] = False
        
        # Start pre-loading in background
        thread = threading.Thread(target=load_models, daemon=True)
        thread.start()
    
    def get_translator(self, target_lang: str):
        if target_lang in self._pipelines:
            return self._pipelines[target_lang]
        
        model_name = f"Helsinki-NLP/opus-mt-en-{target_lang.lower()}"
        
        try:
            self.logger.info(f"📥 Loading: {model_name}")
            translator = pipeline(
                "translation",
                model=model_name,
                device=0 if torch.cuda.is_available() else -1,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            self._pipelines[target_lang] = translator
            return translator
            
        except Exception as e:
            self.logger.warning(f"❌ Failed to load {model_name}: {e}")
            # Fallback strategy
            fallback_model = "Helsinki-NLP/opus-mt-en-mul"
            self.logger.info(f"🔄 Using fallback: {fallback_model}")
            translator = pipeline(
                "translation",
                model=fallback_model,
                device=0 if torch.cuda.is_available() else -1
            )
            self._pipelines[target_lang] = translator
            return translator
    
    def translate_text(self, text: str, target_lang: str) -> str:
        translator = self.get_translator(target_lang)
        if translator:
            result = translator(text)[0]['translation_text']
            return result
        return text
    
    def batch_translate_with_progress(self, texts: List[str], target_lang: str, progress_callback=None) -> List[str]:
        """Translate multiple texts with progress updates"""
        results = []
        total = len(texts)
        
        for i, text in enumerate(texts):
            translated = self.translate_text(text, target_lang)
            results.append(translated)
            
            if progress_callback:
                progress_callback((i + 1) / total)
        
        return results
    
    def is_model_loaded(self, target_lang: str) -> bool:
        """Check if model is already loaded"""
        return target_lang in self._pipelines
