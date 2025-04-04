from enum import Enum
import threading

from app.synthesizer.text_to_speech_models import Language, TextToSpeechSpeechT5Model, TextToSpeechVitsModel


class ModelNotFoundError(Exception):
    def __init__(self, model_id: str, language: Language):
        super().__init__(f"Model not found: '{model_id}' - '{language}'.")

class TextToSpeechModelsManager:
    def __init__(self, models_folder_path):
        self.models_folder_path = models_folder_path
        self.models = { 
            Language.POL: {
                "vits": TextToSpeechVitsModel("vits", Language.POL, models_folder_path + "/local_vits"),
            },
            Language.ENG: {
                "vits": TextToSpeechVitsModel("vits", Language.ENG, models_folder_path + "/speecht5"),
                "speecht5": TextToSpeechSpeechT5Model("speecht5", Language.ENG,models_folder_path + "/speecht5/model", models_folder_path + "/speecht5/processor", models_folder_path + "/hifigan/vocoder"),
            }
        }
    def get_model(self, model_id: str, language: Language):
        if not (language in self.models) or not (model_id in self.models[language]):
            raise ModelNotFoundError(model_id, language)
        return self.models[language][model_id]
    
_text_to_speech_models_manager = None
_text_to_speech_models_manager_lock = threading.Lock()

def get_text_to_speech_models_manager() -> TextToSpeechModelsManager:
    global _text_to_speech_models_manager
    if _text_to_speech_models_manager is None:
        with _text_to_speech_models_manager_lock:  
            if _text_to_speech_models_manager is None:  
                _text_to_speech_models_manager = TextToSpeechModelsManager("./models")
    return _text_to_speech_models_manager
