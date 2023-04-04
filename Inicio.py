import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana
ventana = tk.Tk()
ventana.title("Ventana de inicio")
ventana.geometry("500x550")  # Ajustar tamaño de la ventana

# Cambiar color de fondo de la ventana
ventana.configure(bg="#F2F2F2")

# Cargar imagen del logo y redimensionarla
logo_imagen = Image.open("Logo/logo.png")
logo_redimensionado = logo_imagen.resize((200, 200))
logo = ImageTk.PhotoImage(logo_redimensionado)

# Crear etiquetas
bienvenido_etiqueta = tk.Label(ventana, text="¡Bienvenido al Traductor de señas!",
                               font=("Helvetica", 22, "bold"), fg="#000000")
titulo_etiqueta = tk.Label(ventana, text="Donde tu comunicación nos importa",
                           font=("Helvetica", 16), fg="#696969")

# Crear botón personalizado
def abrir_archivo():
    import Resultado

def abrir_y_cerrar():
    ventana.destroy()
    abrir_archivo()

boton = tk.Button(ventana, text="Ingresar", command=abrir_y_cerrar,
                  bg="#19A7CE", font=("Helvetica", 18, "bold"), fg="#FFFFFF", border=0, padx=50, pady=10)

# Personalizar el botón

def on_enter(event):
    boton.configure(bg='#2EC4B6')


def on_leave(event):
    boton.configure(bg='#19A7CE')


boton.bind('<Enter>', on_enter)
boton.bind('<Leave>', on_leave)

# Agregar elementos a la ventana
logo_etiqueta = tk.Label(ventana, image=logo, bg="#F2F2F2")
logo_etiqueta.pack(pady=20)
bienvenido_etiqueta.pack(pady=10)
titulo_etiqueta.pack(pady=10)
boton.pack(pady=20)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
