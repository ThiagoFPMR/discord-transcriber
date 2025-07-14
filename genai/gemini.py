from google import genai


class Gemini:
    def __init__(self, model, api_key):
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def process_audio(self, prompt, file_path):
        """
        Summarize the content of an audio file using Gemini AI.
        """
        myfile = self.client.files.upload(file=file_path)
        response = self.client.models.generate_content(
            model=self.model, 
            contents=[
                prompt,
                myfile
            ]
        )
        return response.text