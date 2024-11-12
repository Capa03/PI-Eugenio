import requests
import os
from PIL import Image
from io import BytesIO
import codecs


class DataModel:
    def __init__(self):
        self.base_url = 'https://api.arasaac.org/v1'
        self.matrix = [[]]

    def search_images(self, matrix, keyboard_name):
        self.matrix = matrix
        self.keyboard_name = keyboard_name 
        response = []

        # Loop through each word in the input list
        for word in matrix:
            for w in word:
                print(f"Searching for images related to: {w}")
                try:
                    # Make the API request
                    request = requests.get(f"{self.base_url}/pictograms/pt/search/{w}")

                    # Check if the request was successful
                    if request.status_code == 200:
                        # Append each word's response as a separate sublist
                        response.append(request.json())
                    else:
                        print(f"No image data found for the word: {w}")
                        response.append([])  # Append an empty list if no data is found

                except requests.exceptions.RequestException as e:
                    print(f"An error occurred during the request for '{w}': {e}")
                    response.append([])  # Append an empty list in case of an error
            
        return self.proccess_search(response)  # Process the response data
    

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
        bmp_path = f"CAT_IMG_{self.keyboard_name}/{image_id}.bmp"
        image.save(bmp_path, "BMP")  # Save as BMP
        print(f"Image with ID {image_id} saved as BMP in 200x200 size.")



    def download_image(self, response):
        if not os.path.exists(f"CAT_IMG_{self.keyboard_name}"):
            os.makedirs(f"CAT_IMG_{self.keyboard_name}")
        
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

        self.create_keyboard(response) 

        #Access matrix by self.matrix
        #[['Ola', 'adeus'], ['sim', 'nao']]
    def create_keyboard(self, response):
        with codecs.open(f"{self.keyboard_name}.tec", "w", "cp1252") as file: # cp1252 -> ANSI encoding or "utf-8"
            x = 0 # keep track of the image id is in the array
            for arr in self.matrix: # [['Ola', 'adeus'], ['sim', 'nao']] -> self.matrix ['Ola', 'adeus'] -> arr
                l1 = "LINHA ?\n"
                l2 = "GRUPO ?\n"
                l3 = f"TECLA TECLA_IMAGEM CAT_IMG_Teste\{response[x]}.bmp:{arr[0]} ? {arr[0]} 1 -1 -1\n" # Syntax Warninng here (because of the \{)
                l4 = f"TECLA TECLA_IMAGEM CAT_IMG_Teste\{response[x+1]}.bmp:{arr[1]} ? {arr[1]} 1 -1 -1\n" # Syntax Warninng here
                x = x + 2 
                file.writelines([l1,l2,l3,l4]) # write lines in file
            file.close()

