import os
import tkinter as tk
from PIL import Image, ImageTk
from controllers.main_controller import MainController  

def show_splash_screen(app):
    """Displays a responsive splash screen."""
    splash_root = tk.Tk()
    splash_root.overrideredirect(True) 


    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    splash_label = tk.Label(splash_root, text="Editor de Teclados para o Eugénio V3", font=("Arial", 24))
    splash_label.pack(pady=20)

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))  
        image_path = os.path.join(script_dir, "assets", "image", "eugenio.png")

        print(f"Loading image from: {image_path}")  

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        original_image = Image.open(image_path)

        max_width = int(screen_width * 0.5)
        max_height = int(screen_height * 0.5)
        original_width, original_height = original_image.size

        scale_factor = min(max_width / original_width, max_height / original_height)
        if scale_factor < 1:
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        else:
            resized_image = original_image

        splash_image = ImageTk.PhotoImage(resized_image)  

        image_label = tk.Label(splash_root, image=splash_image)
        image_label.image = splash_image 
        image_label.pack()

    except FileNotFoundError as e:
        print(e)
        error_label = tk.Label(splash_root, text="Image not found", fg="red")
        error_label.pack()
    except Exception as e:
        print(f"Error loading image: {e}")
        error_label = tk.Label(splash_root, text=f"Error: {e}", fg="red")
        error_label.pack()

    def destroy_splash():
        splash_root.destroy()
        app.run()  


    splash_root.update_idletasks()  
    width = splash_root.winfo_width()
    height = splash_root.winfo_height()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    splash_root.geometry(f"{width}x{height}+{x}+{y}")  

    splash_root.after(2000, destroy_splash) 
    splash_root.mainloop()

if __name__ == "__main__":
    app = MainController()  
    show_splash_screen(app)  
