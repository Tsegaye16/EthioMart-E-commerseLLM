import re
import json
import os
from typing import List, Dict
from nltk.tokenize import word_tokenize
from langdetect import detect

class DataPreprocessor:
    def __init__(self, input_folder: str, output_folder: str):
        self.input_folder = input_folder
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def process_file(self, input_file: str) -> List[Dict]:
        """Process a single file and return the processed data."""
        with open(input_file, "r", encoding="utf-8") as f:
            messages = json.load(f)

        processed_messages = [self.preprocess_message(msg) for msg in messages]
        return processed_messages

    def preprocess_message(self, message: Dict) -> Dict:
        """Clean and preprocess a single message."""
        text = message.get("text", "")

        if text:
            text = self._normalize_text(text)
            tokens = self._tokenize_text(text)
            message["cleaned_text"] = " ".join(tokens)

        return message

    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing special characters, extra spaces, etc."""
        text = text.strip()  # Remove leading/trailing spaces
        text = re.sub(r"[^\w\s፡።፣፤፥፦፧፨᎐᎑᎒]", "", text)  # Remove non-Amharic special characters
        text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
        return text

    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into words."""
        try:
            if detect(text) == "am":  # Check if text is Amharic
                return word_tokenize(text)
        except:
            pass
        return text.split()  # Fallback simple split
