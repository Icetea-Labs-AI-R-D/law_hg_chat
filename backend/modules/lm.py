from abc import ABC, abstractmethod

class LM(ABC):
    """Abstract class for language models."""
    
    def __init__(self, model, temperature: float = 0.0, json_format: str = None, stream: bool = False) -> None:
        self.kwargs = {
            "model": model,
            "temperature": temperature,
            "json_format": {"type": json_format},
            "stream": stream
        }
        
        self.provider = "openai"
        
        self.history = []
        
    @abstractmethod
    def _basic_request(self, prompt, **kwargs):
        pass
    
    def request(self, prompt, **kwargs):
        return self._basic_request(prompt, **kwargs)
    
    
    @abstractmethod
    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        pass
    
    def copy(self, **kwargs):
        """Returns a copy of the language model with the same parameters."""
        kwargs = {**self.kwargs, **kwargs}
        model = kwargs.pop("model")

        return self.__class__(model=model, **kwargs)