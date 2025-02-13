import os
import tkinter as tk
from PIL import Image, ImageTk
from controllers.main_controller import MainController  

CONFIG_FILE = "config.txt"  

def should_show_intro():
    return not (os.path.exists(CONFIG_FILE) and "skip_intro=True" in open(CONFIG_FILE).read())

def save_user_preference(skip_intro):
    with open(CONFIG_FILE, "w") as file:
        file.write(f"skip_intro={'True' if skip_intro else 'False'}")

def show_intro_screen():
    """Displays an introduction screen and returns if it should continue to the main app."""
    intro_root = tk.Tk()
    intro_root.title("Bem-vindo ao Editor Eugénio")

    screen_width = intro_root.winfo_screenwidth()
    screen_height = intro_root.winfo_screenheight()

    frame = tk.Frame(intro_root, padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Bem-vindo ao Editor de Teclados", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(frame, text="Este software permite criar e editar teclados personalizados para o Eugénio.",
             wraplength=400, justify="left", font=("Arial", 12)).pack(pady=10)

    show_intro_var = tk.BooleanVar(value=False)  
    check_btn = tk.Checkbutton(frame, text="Não mostrar mais", variable=show_intro_var, font=("Arial", 10))
    check_btn.pack(pady=5)
    
    def continue_to_app():
        save_user_preference(show_intro_var.get())  
        intro_root.destroy()  

    def close_app():
        """Close the entire application if the X button is clicked."""
        os._exit(0)  
        
    tk.Button(frame, text="Continuar", command=continue_to_app, font=("Arial", 12, "bold"), bg="#3498DB", fg="white").pack(pady=10)

    intro_root.protocol("WM_DELETE_WINDOW", close_app)
    
    intro_root.update_idletasks()
    width, height = 450, 250  
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    intro_root.geometry(f"{width}x{height}+{x}+{y}")

    intro_root.mainloop()  # This keeps the window open until "Continuar" is clicked

def show_splash_screen():
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
        if should_show_intro():
            show_intro_screen()  # Show the introduction screen
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
    show_splash_screen()
