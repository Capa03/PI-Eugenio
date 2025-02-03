
import codecs
import re
import os


class KeyboardModel:
    PASSED_GROUP_LINE = 2

    def __init__(self) -> None:
        pass

    def _create_keyboard(self, matrix, keyboard_name, image_ids):
        """
        Creates a .tec file using the matrix and downloaded images.
        
        Args:
            matrix (list): A 2D list of words representing the keyboard layout.
            keyboard_name (str): The name of the keyboard to create.
            image_ids (list): A list of image IDs for pictogram keys.
        """
        try:
            with codecs.open(self._get_eugenio_path(keyboard_name), "w", "cp1252") as file:
                for row in matrix:
                    file.writelines(["LINHA ?\n", "GRUPO ?\n"])
                    words = self._split_row(row)
                    for word in words:
                        if word.startswith("[") and word.endswith("]"):
                            clean_word = word[1:-1]
                            if not image_ids: 
                                file.write(f"TECLA TECLA_NORMAL {clean_word} {clean_word} {clean_word};;; 1 -1 -1\n")
                                continue
                            image_id = image_ids.pop(0)
                            file.write(f"TECLA TECLA_IMAGEM CAT_IMG_{keyboard_name}\\{image_id}.bmp:{clean_word} ? CAT_IMG_{keyboard_name}\\{image_id}.bmp 1 -1 -1\n")
                        else:
                            file.write(f"TECLA TECLA_NORMAL {word} {word} {word};;; 1 -1 -1\n")
        except Exception as e:
            raise RuntimeError(f"Failed to create keyboard file: {e}")
        
    def _edit_keyboard(self, keyboard_name):
        """
        Edits a .tec file using the matrix and downloaded images.
        
        Args:
            keyboard_name (str): The name of the keyboard to edit.

        Returns:
            str: A string representation of the keyboard layout.
        """
        file = open(self._get_eugenio_path(keyboard_name), "r") 
        lines = list(file) # list of lines in file
        keys = list() # list of keys from keyboard
        count = 0 # regular count in order to count the first two lines that are just for create another line
        try:
            is_new_line = False # this boolean is here in order to check if the first two lines from a line from the keyboard. So we can apply /n to write in the program so the user can see we are in another line
            for line in lines:
                if(line.startswith("LINHA") or line.startswith("GRUPO")):
                    if(count > self.PASSED_GROUP_LINE):
                        is_new_line = True
                else:
                    if(is_new_line):
                        if "TECLA_NORMAL" in line: # -> To Acess Normal key
                            words_in_line = line.split() # Splits the line into words
                            keys.append("\n" + words_in_line[words_in_line.index("TECLA_NORMAL") + 1]) # this line takes the word in index and adds 1 is the word in front of the index word
                            is_new_line = False
                        else: # -> To Acess Pictogram Key
                            start = line.find(":") + 1 # -> + 1 in order to just take the word
                            end = line.find("?") - 1 # -> -1 in order to just take the word
                            keys.append("\n[" + line[start:end] + "]") # in the line takes the specific place [] in line start and end and writes the word is between
                            is_new_line = False
                    else:
                        if "TECLA_NORMAL" in line:
                            words_in_line = line.split()
                            keys.append(words_in_line[words_in_line.index("TECLA_NORMAL") + 1])
                        else:
                            start = line.find(":") + 1
                            end = line.find("?") - 1
                            keys.append("[" + line[start:end] + "]")
                count = count + 1

            return_string = ""
            for key in keys:
                return_string = return_string + key + " "

            return return_string
        
        except Exception as e:
            raise RuntimeError(f"Failed to create keyboard file: {e}")
    
    def _get_eugenio_path(self, keyboard_name):
        """
        Returns the path to the Eugénio 3.0 keyboard file.

        Returns:
            str: The path to the keyboard file.
        """
        appdata_dir = os.getenv('APPDATA')  # This fetches the path to %APPDATA%
        keyboard_file = os.path.join(appdata_dir, f"LabSI2-INESC-ID/Eugénio 3.0/{keyboard_name}.tec")
        return keyboard_file


    @staticmethod
    def _split_row(row):
        """
        Splits a string row into words and bracketed terms, removing unwanted characters.

        Args:
            row (str): The input string to split.

        Returns:
            list: A list of words and bracketed terms.
        """
        # Extract bracketed terms or sequences of alphanumeric characters
        return re.findall(r'\[[^\]]+\]|\b\w+\b', row)