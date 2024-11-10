# src/models/data_model.py
import requests
import os

class DataModel:
    def __init__(self):
        self.base_url = 'https://api.arasaac.org/v1'

    def search_images(self, words):
        # This will hold the image data from API responses
        response = []

        # Loop through each word in the input list
        for word in words:
            print(words)
            try:
                print(f"Searching for images related to: {word}")

                # Make the API request
                request = requests.get(f"{self.base_url}/pictograms/pt/search/{word}")

                # Check if the request was successful
                if request.status_code == 200:
                    response.append(request.json())  # Append the JSON data to the response list
                else:
                    print(f"No image data found for the word: {word}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request for '{word}': {e}")

        return self.proccess_request(response)  # Process the response data
    

    def proccess_request(self, response):
        # A set to store unique first keyword values (from keyword[0].keyword)
        unique_keywords = set()
        
        # List to hold characters after filtering the response
        characters = []
        
        # Loop through each word's result in the response
        for word_results in response:
            # Loop through each individual result (image data)
            for image_data in word_results:
                # Ensure 'schematic' is not True
                if not image_data.get('schematic', False):
                    # Check if there is at least one keyword (looking at keyword[0])
                    if image_data.get('keywords') and len(image_data['keywords']) > 0:
                        # Focus on the first keyword in the list (keyword[0])
                        first_keyword = image_data['keywords'][0].get('keyword')
                        
                        # If the first keyword is not already in the set, add it and add the image_data to characters
                        if first_keyword and first_keyword not in unique_keywords:
                            unique_keywords.add(first_keyword)
                            characters.append(image_data)
                    
        # If there are characters that meet the criteria, process them
        if characters:
            return characters
        else:
            # If no characters were found, set the error message
            self.errorMessage = 'No pictograms found.'

    def download_image(self, response):
        # Ensure the 'CAT_IMG_TEST' directory exists
        if not os.path.exists("CAT_IMG_TEST"):
            os.makedirs("CAT_IMG_TEST")
        
        # Loop through each image data
        for image_data in response:
            try:
                # Make the API request to get the image data
                request = requests.get(f"{self.base_url}/pictograms/{image_data['_id']}?download=true")
                
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
                    with open(f"CAT_IMG_TEST/{image_data['_id']}.{file_extension}", "wb") as file:
                        file.write(request.content)
                    print(f"Image with ID {image_data['_id']} saved successfully.")
                else:
                    print(f"Failed to download image with ID: {image_data['_id']} (Status code: {request.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred during the request for image ID '{image_data['_id']}': {e}")
