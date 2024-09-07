from langdetect import detect
from transformers import pipeline, MarianMTModel, MarianTokenizer

translate_models = {
    "es": {
        "ru": "Helsinki-NLP/opus-mt-ru-es",  
        "ar": "Helsinki-NLP/opus-mt-ar-es",  
        "he": "Helsinki-NLP/opus-mt-he-es",  
        "en": "Helsinki-NLP/opus-mt-en-es",  
        "fr": "Helsinki-NLP/opus-mt-fr-es", 
    },
    "en": {
        "ru": "Helsinki-NLP/opus-mt-ru-en",  
        "ar": "Helsinki-NLP/opus-mt-ar-en",  
        "he": "Helsinki-NLP/opus-mt-he-en",  
        "en": "Helsinki-NLP/opus-mt-en-en",  
        "fr": "Helsinki-NLP/opus-mt-fr-en", 
        
    }
}

def detect_language(texto):
    try:
        return detect(texto)
    except:
        return "Idioma no detectado"

def translate(texto, language):
    detected_language = detect_language(texto)
    if detected_language in translate_models[language]:
        model_name = translate_models[language][detected_language]
    else:
        return None
    
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    inputs = tokenizer(texto, return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    translated = tokenizer.decode(translated[0], skip_special_tokens=True)

    return translated
