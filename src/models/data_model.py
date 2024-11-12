import requests
import os
from PIL import Image
from io import BytesIO

class DataModel:
    def __init__(self):
        self.base_url = 'https://api.arasaac.org/v1'

    def search_images(self, words):
        response = []

        for word in words:
            print(f"Searching for images related to: {word}")
            try:
                request = requests.get(f"{self.base_url}/pictograms/pt/search/{word}")

                if request.status_code == 200:
                    response.append(request.json())
                else:
                    print(f"No image data found for the word: {word}")
                    response.append([])

            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request for '{word}': {e}")
                response.append([])
        
        return self.proccess_search(response)

    def proccess_search(self, response):
        word_list = []
        if not response:
            print("No image data found for any of the words.")
            return word_list

        for word_data in response:
            filtered_data = [item for item in word_data if item.get('schematic', False) is False]

            if filtered_data:
                word_list.append(filtered_data[0]['_id'])

        print(f"Word list: {word_list}")
        return self.download_image(word_list)
    
    def convert_img(self, request, image_id):
        image = Image.open(BytesIO(request.content))
        image = image.convert("RGB")  # Convert to RGB if needed
        image = image.resize((200, 200))  # Resize to 200x200
        bmp_path = f"CAT_IMG_TEST/{image_id}.bmp"
        image.save(bmp_path, "BMP")  # Save as BMP
        print(f"Image with ID {image_id} saved as BMP in 200x200 size.")



    def download_image(self, response):
        if not os.path.exists("CAT_IMG_TEST"):
            os.makedirs("CAT_IMG_TEST")
        
        for id in response:
            try:
                request = requests.get(f"{self.base_url}/pictograms/{id}?download=true")

                if request.status_code == 200:
                    self.convert_img(request, id)
                else:
                    print(f"Failed to download image with ID: {id} (Status code: {request.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request for image ID '{id}': {e}")
            except IOError as e:
                print(f"An error occurred while processing the image with ID '{id}': {e}")
