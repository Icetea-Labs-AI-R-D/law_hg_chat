import openai
from backend.modules.lm import LM

class GPT4(LM):
    """Wrapper around OpenAI's GPT API.

    Args:
        model (str, optional): OpenAI supported LLM model to use. Defaults to "gpt-4o".
        api_key (Optional[str], optional): API provider Authentication token. use Defaults to None.
        api_provider (Literal["openai"], optional): The API provider to use. Defaults to "openai".
        model_type (Literal["chat", "text"], optional): The type of model that was specified. Mainly to decide the optimal prompting strategy. Defaults to "text".
        **kwargs: Additional arguments to pass to the API provider.
    """