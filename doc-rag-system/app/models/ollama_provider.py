import ollama

class OllamaProvider:

    def __init__(self, model="phi3:mini", host="http://ollama:11434"):
        self.client = ollama.Client(host=host)
        self.model = model

    def chat(self, messages, temperature=0.7, max_tokens=1):
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        return response["message"]["content"]
