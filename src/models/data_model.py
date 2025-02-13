import requests
import os
from PIL import Image
from io import BytesIO
import codecs
import re

from models import keyboard_model


class DataModel:
    def __init__(self, base_url="https://api.arasaac.org/v1"):
        self.base_url = base_url
        self.keyboard = keyboard_model.KeyboardModel()

    def search_and_process_images(self, matrix, keyboard_name):
        """
        Orchestrates searching, downloading, and processing images.
        """
        try:
            responses, errors = self._search_images(matrix)
            if errors:
                print(f"Errors found while searching images for: {', '.join(errors)}")

            filtered_ids, invalid_words = self._process_image_responses(matrix, responses)
            if invalid_words:
                print(f"No valid images found for: {', '.join(invalid_words)}")

            self._download_images(filtered_ids, keyboard_name)
            
            self.keyboard._create_keyboard(matrix, keyboard_name, filtered_ids)
        except Exception as e:
            raise RuntimeError(f"Error in processing images: {e}")

    def _read_file(self, path):
        return self.keyboard._edit_keyboard(path)


    def _search_images(self, matrix):
        """
        Searches for images in the API for bracketed words.
        """
        responses = []
        errors = []
        for row in matrix:
            words = self._split_row(row)
            for word in words:
                if word.startswith("[") and word.endswith("]"):  # Check for bracketed words
                    clean_word = word[1:-1]  # Remove brackets
                    try:
                        response = requests.get(f"{self.base_url}/pictograms/pt/search/{clean_word}")
                        if response.status_code == 200:
                            responses.append((clean_word, response.json()))
                        else:
                            errors.append(clean_word)
                    except requests.exceptions.RequestException as e:
                        errors.append(clean_word)
        return responses, errors

    def _download_images(self, image_ids, keyboard_name):
        """
        Downloads and saves images.
        """
        appdata_dir = os.getenv('APPDATA')  # This fetches the path to %APPDATA%
        output_dir = os.path.join(appdata_dir, f"LabSI2-INESC-ID/Eugénio 3.0/CAT_IMG_{keyboard_name}")
        os.makedirs(output_dir, exist_ok=True) 

        for image_id in image_ids:
            try:
                response = requests.get(f"{self.base_url}/pictograms/{image_id}?download=true")
                if response.status_code == 200:
                    self._save_image(response, image_id, output_dir)

            except Exception as e:
                print(f"Failed to download image {image_id}: {e}")

    def _save_image(self, response, image_id, output_dir):
        """
        Saves an image in BMP format.
        """
        try:
            image = Image.open(BytesIO(response.content))
            image = image.convert("RGB")
            image = image.resize((200, 200))
            image_path = os.path.join(output_dir, f"{image_id}.bmp")
            image.save(image_path, "BMP")
            print(f"Saved image: {image_path}")
        except Exception as e:
            print(f"Failed to save image ID {image_id}: {e}")

    def _process_image_responses(self, matrix, responses):
        """
        Filters IDs for valid images from API responses.
        """
        filtered_ids = []
        invalid_words = []
        word_response_map = {word: response for word, response in responses}

        for row in matrix:
            words = self._split_row(row)
            for word in words:
                if word.startswith("[") and word.endswith("]"):  # Process bracketed words
                    clean_word = word[1:-1]
                    response = word_response_map.get(clean_word, [])
                    valid_images = [item for item in response if not item.get("schematic", False)]
                    if valid_images:
                        filtered_ids.append(str(valid_images[0]["_id"]))  # Use valid image ID
                    else:
                        invalid_words.append(clean_word)
        return filtered_ids, invalid_words
    
    def _split_row(row):
        """
        Splits a string row into words and bracketed terms, removing unwanted characters.
        """
        # Extract bracketed terms or sequences of alphanumeric characters
        return re.findall(r'\[[^\]]+\]|\b\w+\b', row)





