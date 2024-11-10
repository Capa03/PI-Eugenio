# src/models/data_model.py
import requests
import os

class DataModel:
    def __init__(self):
        self.base_url = 'https://api.arasaac.org/v1'
        self.matrix = [[]]

    def search_images(self, matrix):
        self.matrix = matrix
        # This will hold the image data from API responses as a multidimensional list
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

        # Iterate through each word's response data
        for word_data in response:
            # Check if there is valid data and filter out items where 'schematic' is True
            filtered_data = [item for item in word_data if item.get('schematic', False) is False]

            # Append the first item's '_id' from the filtered list, if any items remain after filtering
            if filtered_data:
                word_list.append(filtered_data[0]['_id'])

        print(f"Word list: {word_list}")
        return self.download_image(word_list)  # Download the images


    def download_image(self, response):
        # Ensure the 'CAT_IMG_TEST' directory exists
        if not os.path.exists("CAT_IMG_TEST"):
            os.makedirs("CAT_IMG_TEST")
        
        # Loop through each image data
        for id in response:
            try:
                # Make the API request to get the image data
                request = requests.get(f"{self.base_url}/pictograms/{id}?download=true")
                
                # Check if the request was successful
                if request.status_code == 200:
                    # Get the content type from the response headers (e.g., image/png, image/jpeg)
                    content_type = request.headers.get('Content-Type', '')
                    # Set the file extension based on the content type
                    if 'image' in content_type:
                        file_extension = content_type.split('/')[-1]  # e.g., 'jpeg', 'png'
                    else:
                        file_extension = 'bmp'  # Default to bmp if the content type is not an image
                    
                    # Save the image to a file
                    with open(f"CAT_IMG_TEST/{id}.{file_extension}", "wb") as file:
                        file.write(request.content)
                    print(f"Image with ID {id} saved successfully.")
                else:
                    print(f"Failed to download image with ID: {id} (Status code: {request.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request for image ID '{id}': {e}")

        #Access matrix by self.matrix
        #[['Ola', 'adeus'], ['sim', 'nao']]
