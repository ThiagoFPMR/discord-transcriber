import openai


class ChatGPT:
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
