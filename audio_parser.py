"""Class for handling audio tasks."""
from google import genai
from utils import load_credential


class AudioParser:
    def __init__(self):
        self.client = genai.Client(api_key=load_credential("gemini_api_key"))    

    def summarize_daily_log(self, file_path):
        """
        Summarize the content of an audio file using Gemini AI.
        """
        myfile = self.client.files.upload(file=file_path)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                "This audio clip contains a log of the day's activities. \
                Please summarize it, using bullet points and sections where applicable. \
                Make sure to write it in markdown format." \
                "If something is not clear, ask for clarification." \
                "If it does not contain any relevant information, say nothing was found.", 
                myfile
            ]
        )
        return response.text