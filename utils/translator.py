from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)
async def translate_description(text, target_lang='ru'):
    try:
        if not text or len(text) < 10:
            return None
        
        if any(ord(char) > 127 for char in text[:100]):
            return None
        
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text[:5000])
        return translated
    except Exception as e:
        logger.error(f"Ошибка перевода: {e}")
        return None