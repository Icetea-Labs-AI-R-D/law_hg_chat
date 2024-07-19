from abc import ABC, abstractmethod

class LM(ABC):
    """Abstract class for language models."""
    
    def __init__(self, model, temperature: float = 0.5, stream: bool = False) -> None:
        self.kwargs = {
            "model": model,
            "temperature": temperature,
            "stream": stream
        }
        
        self.provider = "openai"