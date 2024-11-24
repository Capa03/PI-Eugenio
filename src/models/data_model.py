import requests
import os
from PIL import Image
from io import BytesIO
import codecs


class DataModel:
    def __init__(self, base_url="https://api.arasaac.org/v1"):
        self.base_url = base_url

    def search_and_process_images(self, matrix, keyboard_name):
        """
        Orquestra a pesquisa, download e processamento das imagens.
        """
        try:
            # Mapeia palavras para os resultados da API
            responses, errors = self._search_images(matrix)
            if not responses:
                raise ValueError("No responses received from the API.")
            
            if errors:
                raise ValueError(f"Errors found while searching images for: {', '.join(errors)}")

            filtered_ids, invalid_words = self._process_image_responses(matrix, responses)
            if invalid_words:
                raise ValueError(f"Invalid inputs with no images found: {', '.join(invalid_words)}")

            if not filtered_ids:
                raise ValueError("No valid images found for the given input.")

            self._download_images(filtered_ids, keyboard_name)
            self._create_keyboard(matrix, keyboard_name, filtered_ids)
        except Exception as e:
            raise RuntimeError(f"Error in processing images: {e}")

    def _search_images(self, matrix):
        """
        Busca imagens na API para cada palavra da matriz e identifica erros.
        """
        responses = []
        errors = []
        for row in matrix:
            for word in row:
                try:
                    response = requests.get(f"{self.base_url}/pictograms/pt/search/{word}")
                    if response.status_code == 200:
                        responses.append((word, response.json()))
                    else:
                        errors.append(word)
                        print(f"No data found for: {word} (Status code: {response.status_code})")
                except requests.exceptions.RequestException as e:
                    errors.append(word)
                    print(f"API request error for '{word}': {e}")
        return responses, errors

    def _process_image_responses(self, matrix, responses):
        """
        Filtra IDs de imagens relevantes e retorna palavras inválidas.
        """
        filtered_ids = []
        invalid_words = []

        word_response_map = {word: response for word, response in responses}

        for row in matrix:
            for word in row:
                response = word_response_map.get(word, [])
                valid_images = [item for item in response if not item.get("schematic", False)]
                if valid_images:
                    filtered_ids.append(valid_images[0]["_id"])
                else:
                    invalid_words.append(word)

        return filtered_ids, invalid_words

    def _download_images(self, image_ids, keyboard_name):
        """
        Faz o download e salva imagens.
        """
        output_dir = f"CAT_IMG_{keyboard_name}"
        os.makedirs(output_dir, exist_ok=True)

        for image_id in image_ids:
            try:
                response = requests.get(f"{self.base_url}/pictograms/{image_id}?download=true")
                if response.status_code == 200:
                    self._save_image(response, image_id, output_dir)
                else:
                    print(f"Failed to download image ID {image_id}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to download image {image_id}: {e}")

    def _save_image(self, response, image_id, output_dir):
        """
        Salva uma imagem no formato BMP.
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

    def _create_keyboard(self, matrix, keyboard_name, image_ids):
        """
        Cria o arquivo .tec com as configurações do teclado.
        """
        keyboard_file = f"{keyboard_name}.tec"
        try:
            with codecs.open(keyboard_file, "w", "cp1252") as file:
                for row in matrix:
                    file.writelines(["LINHA ?\n", "GRUPO ?\n"])
                    for word in row:
                        image_id = image_ids.pop(0) if image_ids else "MISSING"
                        if image_id == "MISSING":
                            print(f"Warning: No image found for '{word}' while creating keyboard.")
                        file.write(
                            f"TECLA TECLA_IMAGEM CAT_IMG_{keyboard_name}\\{image_id}.bmp:{word} ? {word};;; 1 -1 -1\n"
                        )
            print(f"Keyboard file created: {keyboard_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to create keyboard file: {e}")
