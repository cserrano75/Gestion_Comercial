# LTvd58cD9pBtOUXg
from main import MainWindow
import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy import create_engine, text

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

# Cadena de conexión a tu PostgreSQL local
# (Reemplaza 'nombre_de_tu_bd' por el nombre real de tu base de datos migrada)
PG_URI = "postgresql+psycopg2://postgres:Asus2026@localhost:5432/CRM-Ventas"

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CRM - Iniciar Sesión")
        self.geometry("400x350")
        self.resizable(False, False)

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Bienvenido al CRM", font=ctk.CTkFont(size=22, weight="bold"))
        self.label_titulo.pack(pady=(40, 20))

        # Campo Usuario
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", width=250, height=40)
        self.entry_usuario.pack(pady=10)

        # Campo Contraseña
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250, height=40)
        self.entry_password.pack(pady=10)

        # Botón de Login
        self.btn_login = ctk.CTkButton(self, text="Ingresar", command=self.verificar_login, width=250, height=40)
        self.btn_login.pack(pady=(20, 10))

    def verificar_login(self):
            usuario = self.entry_usuario.get()
            password = self.entry_password.get()

            if not usuario or not password:
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
                return

            try:
                uri_segura = PG_URI + "?client_encoding=utf8"
                engine = create_engine(uri_segura)
                
                with engine.connect() as connection:
                    if usuario == "admin" and password == "Admin123*":
                        messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
                        self.destroy()

                        # Abro la ventana principal del CRM
                        main_app = MainWindow(usuario_actual=usuario)
                        main_app.mainloop()
                    else:
                        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            
            except Exception as e:
                # Imprimimos el error real en la terminal para diagnosticarlo de inmediato
                print("--- ERROR REAL DE CONEXIÓN ---")
                print(repr(e))
                print("------------------------------")
                
                # Mostramos un mensaje limpio en la ventanita sin errores de codecs
                messagebox.showerror("Error de Conexión", "No se pudo conectar a la BD local.\nRevisa la terminal para ver el detalle.")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()