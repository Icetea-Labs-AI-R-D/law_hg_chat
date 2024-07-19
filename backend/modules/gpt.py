from openai import OpenAI, AsyncOpenAI
from typing import Optional, Any, List, Dict
from lm import LM

class SyncGPT(LM):
    """Wrapper around OpenAI's GPT API.
    Default:
        model is "gpt-4o-mini".
        temperature is 0.5.
        stream is False.
        
    Args:
        model (str, optional): OpenAI supported LLM model to use. Defaults to "gpt-4o-mini".
        api_key (Optional[str], optional): API provider Authentication token. use Defaults to None.
        response_format (Optional[str], optional): Format of the response from the API. Defaults to None.
        **kwargs: Additional arguments to pass to the API provider.
    """
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ):
        super().__init__(model)
        if api_key:
            self.api_key = api_key
        else:
            raise ValueError("API Key is required for OpenAI API.")

        if response_format:
            self.response_format = {"type": response_format}

        self.kwargs = {
            **self.kwargs,
            **kwargs,
        }

        self.client = OpenAI(api_key=self.api_key)
    
    def _request(self, 
        messages: List[Dict[str, str]],
        **kwargs
    ):
        response = self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        return response

    def chat(self, 
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
        ):
        """Chat with the GPT language model.

        Args:
            system_prompt (Optional[str], optional): system prompt. Defaults to None.
            user_prompt (Optional[str], optional): user prompt. Defaults to None.
            response_format (Optional[str], optional): format for response. Defaults to None.
        """
        
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        
        kwargs = {**self.kwargs, **kwargs}
        
        if response_format:
            kwargs["response_format"] = {"type": response_format}
        
        response = self._request(messages, **kwargs)
            
        return response
    
class AsyncGPT(LM):
    """Wrapper around OpenAI's GPT API.
    Default:
        model is "gpt-4o-mini".
        temperature is 0.5.
        stream is False.
        
    Args:
        model (str, optional): OpenAI supported LLM model to use. Defaults to "gpt-4o-mini".
        api_key (Optional[str], optional): API provider Authentication token. use Defaults to None.
        response_format (Optional[str], optional): Format of the response from the API. Defaults to None.
        **kwargs: Additional arguments to pass to the API provider.
    """
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
    ):
        super().__init__(model)
        if api_key:
            self.api_key = api_key
        else:
            raise ValueError("API Key is required for OpenAI API.")

        if response_format:
            self.response_format = {"type": response_format}

        self.kwargs = {
            **self.kwargs,
            **kwargs,
        }

        self.client = AsyncOpenAI(api_key=self.api_key)
        
    async def _request(self,
        messages: List[Dict[str, str]] = [],
        **kwargs
    ):
        response = await self.client.chat.completions.create(
            messages=messages,
            **kwargs
        )
        return response
        
    async def chat(self, 
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        response_format: Optional[str] = None,
        **kwargs
        ):
        """Chat with the GPT language model.

        Args:
            system_prompt (Optional[str], optional): system prompt. Defaults to None.
            user_prompt (Optional[str], optional): user prompt. Defaults to None.
            response_format (Optional[str], optional): format for response. Defaults to None.
        """
        
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        
        kwargs = {**self.kwargs, **kwargs}
        
        if response_format:
            kwargs["response_format"] = {"type": response_format}
            
        response = await self._request(messages, **kwargs)
            
        return response
    
def get_choice_text(
    choice: dict,
    stream: bool = False 
) -> str:
    if not stream:
        return choice["message"]["content"]
    return choice["delta"]["content"]