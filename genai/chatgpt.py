from openai import OpenAI


class ChatGPT:
    def __init__(self, chat_model: str, transcribe_model: str, api_key: str):
        """
        Initializes the ChatGPT client with the specified model and API key.

        Args:
            chat_model (str): The model to use for generating responses.
            transcribe_model (str): The model to use for transcribing audio files.
            api_key (str): The API key for authenticating with the OpenAI service.
        """
        self.client = OpenAI(api_key=api_key)
        self.chat_model = chat_model
        self.transcribe_model = transcribe_model

    def speech_to_text(self, audio_path: str):
        """
        Converts speech from an audio file to text using the specified model.

        Args:
            audio_path (str): The path to the audio file to be processed.
        Returns:
            str: The transcribed text from the audio file.
        """
        with open(audio_path, "rb") as file:
            response = self.client.audio.transcriptions.create(
                model=self.transcribe_model, file=file, response_format="text"
            )
        return response

    def generate_response(self, prompt: str):
        """
        Generates a response to the given prompt using the specified model.

        Args:
            prompt (str): The input prompt for which a response is to be generated.

        Returns:
            str: The generated response from the model.
        """
        response = self.client.chat.completions.create(
            model=self.chat_model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    import yaml

    with open("../config.yaml", "r") as file:
        config = yaml.safe_load(file)
        chatgpt_config = config["genai"]["openai"]
    chatgpt = ChatGPT(
        chat_model=chatgpt_config["chat_model"],
        transcribe_model=chatgpt_config["transcribe_model"],
        api_key=chatgpt_config["api_key"],
    )
    # prompt = "What is the capital of France?"
    # response = chatgpt.generate_response(prompt)
    audio_path = "../test_audio.m4a"
    transcription = chatgpt.speech_to_text(audio_path)
    response = chatgpt.generate_response(
        f"Summarize the transcription below in a daily log format using markdown syntax.\n\n{transcription}"
    )
    print(response)
