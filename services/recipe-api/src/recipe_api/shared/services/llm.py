from openai import OpenAI

from recipe_api.shared.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.vllm_base_url,
            api_key=settings.vllm_api_key or "EMPTY",
        )
        self.model = settings.vllm_model

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system_prompt: str | None = None,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content or ""

    async def generate_async(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        system_prompt: str | None = None,
    ) -> str:
        # TODO: Use AsyncOpenAI for true async support
        return self.generate(prompt, max_tokens, temperature, system_prompt)


def get_llm_service() -> LLMService:
    return LLMService()
