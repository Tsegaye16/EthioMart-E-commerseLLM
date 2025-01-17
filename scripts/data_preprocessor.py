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

    def preprocess_all(self):
        """Process all JSON files in the input folder."""
        for file_name in os.listdir(self.input_folder):
            if file_name.endswith(".json"):
                input_file = os.path.join(self.input_folder, file_name)
                output_file = os.path.join(self.output_folder, file_name)
                
                with open(input_file, "r", encoding="utf-8") as f:
                    messages = json.load(f)

                processed_messages = [self.preprocess_message(msg) for msg in messages]
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(processed_messages, f, ensure_ascii=False, indent=4)
                
                print(f"Processed data saved to {output_file}")

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

