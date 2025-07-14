"""Class for handling audio tasks."""
import os
import shutil
import subprocess
from google import genai
from utils import load_config
from datetime import datetime


class AudioParser:
    def __init__(self):
        self.config = load_config("config.yaml")
        self.vault_path = self.config["vault_path"]

        if self.config["options"]["ai_used"] == "gemini":
            self.client = genai.Client(api_key=self.config["genai"]["gemini"]["api_key"])

    def summarize_daily_log(self, file_path):
        """
        Summarize the content of an audio file using Gemini AI.
        """
        myfile = self.client.files.upload(file=file_path)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[
                f"Your job is to summarize a log of the day's activities. \
                Please make it's concise but comprehensive. \
                Make sure to put emphasis on the key points by using markdown syntax. \
                Make sure to write it in markdown format. \
                If something is not clear, ask for clarification. \
                If no relevant information is seen, say nothing was found. \
                Also start the summary with a title including the date. \
                Today is {datetime.now().strftime('%Y-%m-%d')}", 
                myfile
            ]
        )
        self.save_to_vault(f"log_{datetime.now().strftime('%Y-%m-%d')}", response.text, "Daily Logs")

        return response.text
    
    def save_to_vault(self, name, contents, vault_dir):
        """
        Save the content to a file in the specified vault directory and update git.
        """
        # Ensure the vault directory exists
        full_dir_path = os.path.join(self.vault_path, vault_dir)
        os.makedirs(full_dir_path, exist_ok=True)
        
        # Write the content to file
        file_path = os.path.join(full_dir_path, f"{name}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(contents)
        
        # Run terminal command to update the vault
        command = f"cd '{self.vault_path}' && git add . && git diff --staged --quiet || (git commit -m 'Update audio vault: {name}' && git push)"
        
        # Use subprocess to capture both stdout and stderr
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"Vault updated successfully with file: {name}.md")
        except subprocess.CalledProcessError as e:
            print(f"Git command failed with return code {e.returncode}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            print(f"Command was: {command}")
            raise RuntimeError(f"Failed to update the vault with the new file: {name}.md. Error: {e.stderr}")
