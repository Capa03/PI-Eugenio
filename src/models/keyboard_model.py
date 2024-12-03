
import codecs
import re


class KeyboardModel:
    def __init__(self) -> None:
        pass

    def _create_keyboard(self, matrix, keyboard_name, image_ids):
        """
        Creates a .tec file using the matrix and downloaded images.
        """
        keyboard_file = f"{keyboard_name}.tec"
        try:
            with codecs.open(keyboard_file, "w", "cp1252") as file:
                for row in matrix:
                    file.writelines(["LINHA ?\n", "GRUPO ?\n"])
                    words = self._split_row(row)
                    for word in words:
                        if word.startswith("[") and word.endswith("]"):
                            clean_word = word[1:-1]
                            if not image_ids:
                                print(f"Warning: No more image IDs available for '{clean_word}'.")
                                file.write(f"TECLA TECLA_NORMAL {clean_word} {clean_word} {clean_word};;; 1 -1 -1\n")
                                continue

                            image_id = image_ids.pop(0)
                            file.write(
                                f"TECLA TECLA_IMAGEM CAT_IMG_{keyboard_name}\\{image_id}.bmp:{clean_word} ? {clean_word};;; 1 -1 -1\n"
                            )
                        else:
                            file.write(f"TECLA TECLA_NORMAL {word} {word} {word};;; 1 -1 -1\n")
            print(f"Keyboard file created: {keyboard_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to create keyboard file: {e}")
        
    def _edit_keyboard(self, keyboard_name):
        """
        Creates a .tec file using the matrix and downloaded images.
        """
        f = open(keyboard_name + ".tec", "r")
        #print(f.read())
        return f.read()

        
        
    @staticmethod
    def _split_row(row):
        """
        Splits a string row into words and bracketed terms, removing unwanted characters.
        """
        # Extract bracketed terms or sequences of alphanumeric characters
        return re.findall(r'\[[^\]]+\]|\b\w+\b', row)