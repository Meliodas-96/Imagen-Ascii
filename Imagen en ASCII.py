import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import random

# Conjunto de caracteres ASCII posibles
ASCII_CHARS = "@%#*+=-:. "

def generate_random_ascii_chars(length=len(ASCII_CHARS)):
    """Genera una lista de caracteres ASCII aleatorios."""
    chars = list(ASCII_CHARS)
    random.shuffle(chars)  # Mezclar caracteres
    return chars[:length]  # Retornar solo el número deseado de caracteres

def resize_image(image, new_width=100):  # Aumenta el ancho por defecto
    width, height = image.size
    ratio = height / width / 1.65  # Ajuste para que se vea mejor
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")  # Convertir a escala de grises

def pixels_to_ascii(image, ascii_chars):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        # Mapeo de píxeles a caracteres ASCII aleatorios
        ascii_str += ascii_chars[pixel * (len(ascii_chars) - 1) // 255]
    return ascii_str

def convert_image_to_ascii(image_path, width):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return

    image = resize_image(image, width)
    image = grayify(image)

    ascii_chars = generate_random_ascii_chars()  # Generar caracteres aleatorios
    ascii_str = pixels_to_ascii(image, ascii_chars)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join(ascii_str[i:i + img_width] for i in range(0, ascii_str_len, img_width))

    return ascii_img

def open_file():
    file_path = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        try:
            width = int(width_entry.get())
            ascii_image = convert_image_to_ascii(file_path, width)
            text_box.delete(1.0, tk.END)  # Limpiar el cuadro de texto
            text_box.insert(tk.END, ascii_image)  # Insertar la imagen ASCII
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un ancho válido.")

def save_to_file():
    ascii_content = text_box.get(1.0, tk.END).strip()
    if not ascii_content:
        messagebox.showwarning("Advertencia", "No hay contenido ASCII para guardar.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(ascii_content)
        messagebox.showinfo("Éxito", "Archivo guardado con éxito.")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversor de Imagen a ASCII")

# Crear un cuadro de entrada para el ancho
width_label = tk.Label(root, text="Ancho de imagen ASCII:")
width_label.pack()
width_entry = tk.Entry(root)
width_entry.pack()
width_entry.insert(0, "100")  # Ancho predeterminado aumentado

# Crear un botón para abrir el explorador de archivos
open_button = tk.Button(root, text="Abrir imagen", command=open_file)
open_button.pack()

# Crear un botón para guardar el resultado
save_button = tk.Button(root, text="Guardar como TXT", command=save_to_file)
save_button.pack()

# Crear un cuadro de texto para mostrar la imagen ASCII
text_box = tk.Text(root, width=100, height=30, font=("Courier", 6))
text_box.pack()

root.mainloop()
