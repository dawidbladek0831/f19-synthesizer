import threading
from datasets import load_dataset, load_from_disk
import torch

from app.utils.decorators import log_execution_time

class SpeakerEmbeddingsManager:
    def __init__(self, datasets_folder_path):
        self.dataset = None
        self.datasets_folder_path = datasets_folder_path
        self.lock = threading.Lock()
        self._load_dataset()
    
    @log_execution_time("Loaded dataset")
    def _load_dataset(self) -> None: 
        if not self._is_dataset_loaded():
            with self.lock: 
                if not self._is_dataset_loaded():
                    self._load_dataset_from_disk()

    def _is_dataset_loaded(self) -> bool:
        return self.dataset is not None
    
    def _load_dataset_from_disk(self) -> None:
        self.dataset = load_from_disk(self.datasets_folder_path)

    @log_execution_time("Fetched speaker embedding")
    def get_speaker_embedding(self, index:int) -> torch.Tensor:
        while(not self._is_dataset_loaded()):
            pass
        return torch.tensor(self.dataset[index]["xvector"]).unsqueeze(0)

_speaker_embeddings_manager = None
_speaker_embeddings_manager_lock = threading.Lock()

def get_speaker_embeddings_manager() -> SpeakerEmbeddingsManager:
    global _speaker_embeddings_manager
    if _speaker_embeddings_manager is None:
        with _speaker_embeddings_manager_lock:  
            if _speaker_embeddings_manager is None:  
                _speaker_embeddings_manager = SpeakerEmbeddingsManager("./datasets/embeddings_dataset")
    return _speaker_embeddings_manager