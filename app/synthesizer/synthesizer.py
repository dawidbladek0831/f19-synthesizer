from enum import Enum
import threading
import os
import io

import torch
from transformers import VitsModel, AutoTokenizer
import soundfile

# import scipy

models_folder_path = "./models"

class Language(Enum):
    ENG = "ENG"
    POL = "POL"

class ModelNotFoundError(Exception):
    def __init__(self, model_id: str, language: Language):
        super().__init__(f"Model not found: '{model_id}' - '{language}'.")


class TextToSpeechModel:
    def __init__(self, model_id: str, language: Language, model_path: str):
        self.model_id = model_id
        self.language = language
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.lock = threading.Lock() 

    def _is_model_loaded(self) -> bool:
        return self.model is not None and self.tokenizer is not None

    def _load_model_from_disk(self):
        print(f"Loading model: {self.model_path}")
        self.model = VitsModel.from_pretrained(
            pretrained_model_name_or_path=self.model_path, 
            local_files_only=True
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.model_path, 
            local_files_only=True
        )

    def _load_model(self): # Double-checked locking 
        if not self._is_model_loaded():
            with self.lock: 
                if not self._is_model_loaded():
                    self._load_model_from_disk()

    def _cleare_text(self, text: str) -> str:
        return text.replace("(", "").replace(")", "")

    def synthesize(self, text: str) -> io.BytesIO:
        print(f"synthesize: {text}")
        self._load_model()
        cleared_text = self._cleare_text(text)
        inputs = self.tokenizer(cleared_text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output = self.model(**inputs).waveform.cpu().numpy()

        buffer = io.BytesIO()
        soundfile.write(buffer, output.squeeze(), self.model.config.sampling_rate, format='WAV')
        buffer.seek(0)

        print(f"synthesized: {text}")
        return buffer

models = {
    Language.POL: {
        "vits": TextToSpeechModel("vits", Language.POL, models_folder_path + "/local_vits"),
    },
    Language.ENG: {
        "vits": TextToSpeechModel("vits", Language.ENG, models_folder_path + "/local_vits"),
    }
}

def get_model(model_id: str, language: Language):
    if not (language in models) or not (model_id in models[language]):
        raise ModelNotFoundError(model_id, language)
    return models[language][model_id]
