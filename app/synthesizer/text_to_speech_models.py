from enum import Enum
import threading
import io

import torch
from transformers import VitsModel, AutoTokenizer, SpeechT5ForTextToSpeech, SpeechT5Processor, SpeechT5HifiGan
import soundfile

from app.synthesizer.speaker_embeddings_manager import SpeakerEmbeddingsManager, get_speaker_embeddings_manager
from app.utils.decorators import log_execution_time

class Language(Enum):
    ENG = "ENG"
    POL = "POL"

class TextToSpeechModel:
    def __init__(self, model_id: str, language: Language, model_path: str):
        self.model_id = model_id
        self.language = language
        self.model_path = model_path

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.lock = threading.Lock() 

        self.model = None

    def _is_model_loaded(self) -> bool:
        return self.model is not None

    def _load_model(self): # Double-checked locking 
        if not self._is_model_loaded():
            with self.lock: 
                if not self._is_model_loaded():
                    self._load_model_from_disk()

    def _cleare_text(self, text: str) -> str:
        return text.replace("(", "").replace(")", "")

    def _load_model_from_disk(self):
        pass

    def synthesize(self, text: str, speaker_id: int) -> io.BytesIO:
        pass

class TextToSpeechVitsModel(TextToSpeechModel):
    def __init__(self, model_id: str, language: Language, model_path: str):
        super().__init__(model_id, language, model_path)
        self.tokenizer = None

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

    def synthesize(self, text: str, speaker_id: int) -> io.BytesIO:
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

class TextToSpeechSpeechT5Model(TextToSpeechModel):
    def __init__(self, model_id: str, language: Language, model_path: str,
                 processor_model_path: str, vocoder_model_path: str):
        super().__init__(model_id, language, model_path)
        self.vocoder_model_path = vocoder_model_path
        self.processor_model_path = processor_model_path
        self.processor = None
        self.vocoder = None
        
    @log_execution_time("Loaded model")
    def _load_model_from_disk(self):
        self.model = SpeechT5ForTextToSpeech.from_pretrained(pretrained_model_name_or_path=self.model_path, local_files_only=True).to(self.device)
        self.processor = SpeechT5Processor.from_pretrained(pretrained_model_name_or_path=self.processor_model_path, local_files_only=True)
        self.vocoder = SpeechT5HifiGan.from_pretrained(pretrained_model_name_or_path=self.vocoder_model_path, local_files_only=True)
    
    @log_execution_time("Synthesized text")
    def synthesize(self, text: str, speaker_id: int) -> io.BytesIO:
        self._load_model()
        cleared_text = self._cleare_text(text)
        
        inputs = self.processor(text=cleared_text, return_tensors="pt")
        
        speaker_embeddings = get_speaker_embeddings_manager().get_speaker_embedding(speaker_id)
        
        speech = self.model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=self.vocoder)
  
        buffer = io.BytesIO()
        soundfile.write(buffer, speech.squeeze(), 16000, format='WAV')
        buffer.seek(0)
        return buffer
 