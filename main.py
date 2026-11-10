import customtkinter as ctk
from datetime import datetime, date
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, text

# Configuración del tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Cadena de conexión a tu BD local
PG_URI = "postgresql+psycopg2://postgres:Asus2026@localhost:5432/CRM-Ventas?client_encoding=utf8"

class MainWindow(ctk.CTk):
    def __init__(self, usuario_actual="admin"):
        super().__init__()

        self.title("CRM de Ventas - Panel Principal")
        self.geometry("1100x650")
        self.minsize(900, 550)

        # Configuración del Grid Principal (1 fila, 2 columnas)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -------------------------------------------------------------------
        # 1. PANEL LATERAL (SIDEBAR)
        # -------------------------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # Logotipo / Título CRM
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CRM VENTAS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Botones de Navegación
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="📊 Dashboard", command=self.mostrar_dashboard, anchor="w")
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_proyectos = ctk.CTkButton(self.sidebar_frame, text="🏗️ Proyectos / Cotiz.", command=self.mostrar_proyectos, anchor="w")
        self.btn_proyectos.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_clientes = ctk.CTkButton(self.sidebar_frame, text="👥 Clientes", command=self.mostrar_clientes, anchor="w")
        self.btn_clientes.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Info del Usuario y Cerrar Sesión (al final del panel)
        self.user_label = ctk.CTkLabel(self.sidebar_frame, text=f"Usuario: {usuario_actual}", font=ctk.CTkFont(size=12))
        self.user_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="s")

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Cerrar Sesión", fg_color="transparent", border_width=1, command=self.cerrar_sesion)
        self.btn_logout.grid(row=6, column=0, padx=20, pady=(10, 20), sticky="s")

        # -------------------------------------------------------------------
        # 2. ÁREA DE CONTENIDO CENTRAL
        # -------------------------------------------------------------------
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(1, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Título de la vista activa
        self.header_label = ctk.CTkLabel(self.main_content_frame, text="Bienvenido al CRM", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Sub-contenedor dinámico donde se cargarán los módulos
        self.view_container = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.view_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)

        # Cargar vista por defecto
        self.mostrar_dashboard()

    # -------------------------------------------------------------------
    # MÉTODOS DE NAVEGACIÓN Y VISTAS
    # -------------------------------------------------------------------
    def limpiar_vista(self):
        for widget in self.view_container.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self.header_label.configure(text="📊 Resumen General")
        self.limpiar_vista()

        # Tarjetas de resumen rápido
        frame_cards = ctk.CTkFrame(self.view_container, fg_color="transparent")
        frame_cards.pack(fill="x", pady=10)

        card1 = ctk.CTkFrame(frame_cards, width=200, height=100)
        card1.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card1, text="Clientes Totales", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        ctk.CTkLabel(card1, text="--", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=5)

        card2 = ctk.CTkFrame(frame_cards, width=200, height=100)
        card2.pack(side="left", expand=True, fill="both", padx=5)
        ctk.CTkLabel(card2, text="Proyectos Activos", font=ctk.CTkFont(size=14)).pack(pady=(15, 5))
        ctk.CTkLabel(card2, text="--", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=5)

    def mostrar_clientes(self):
        self.header_label.configure(text="👥 Gestión de Clientes")
        self.limpiar_vista()

        # Botón de acción rápido
        btn_nuevo = ctk.CTkButton(self.view_container, text="+ Nuevo Cliente", width=150)
        btn_nuevo.pack(anchor="w", pady=(0, 10))

        # Tabla de Clientes (Usando Treeview de Tkinter para mostrar datos)
        tree_frame = ctk.CTkFrame(self.view_container)
        tree_frame.pack(fill="both", expand=True)

        columns = ("id", "nombre", "empresa", "telefono", "email")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre / Contacto")
        tree.heading("empresa", text="Empresa")
        tree.heading("telefono", text="Teléfono")
        tree.heading("email", text="Correo")

        tree.column("id", width=50, anchor="center")
        tree.column("nombre", width=200)
        tree.column("empresa", width=200)
        tree.column("telefono", width=120)
        tree.column("email", width=200)

        tree.pack(fill="both", expand=True)

    def mostrar_proyectos(self):
            self.header_label.configure(text="🏗️ Gestión de Proyectos y Cotizaciones")
            self.limpiar_vista()

            # Contenedor principal de la vista
            container = ctk.CTkFrame(self.view_container, fg_color="transparent")
            container.pack(fill="both", expand=True)

            # ------------------------------------------------------------------
            # BARRA DE FILTROS SUPERIOR (Selector por Status)
            # ------------------------------------------------------------------
            filter_frame = ctk.CTkFrame(container, fg_color="transparent")
            filter_frame.pack(fill="x", pady=(0, 10))

            lbl_filtro = ctk.CTkLabel(filter_frame, text="Filtrar por Status:", font=ctk.CTkFont(size=12, weight="bold"))
            lbl_filtro.pack(side="left", padx=(0, 10))

            # Opciones de status disponibles (puedes ajustar según tus datos de Access)
            opciones_status = ["Todos", "Estudio", "Adjudicado", "Perdido", "En Ejecución"]
            
            # Selector desplegable (CTkComboBox)
            self.status_combobox = ctk.CTkComboBox(
                filter_frame, 
                values=opciones_status, 
                command=self.filtrar_proyectos_por_status,
                width=180
            )
            self.status_combobox.pack(side="left")
            self.status_combobox.set("Estudio")  # Por defecto arranca mostrando los "Estudio" como pediste

            # ------------------------------------------------------------------
            # CONTENEDOR DE LA TABLA (TREEVIEW)
            # ------------------------------------------------------------------
            tree_frame = ctk.CTkFrame(container)
            tree_frame.pack(fill="both", expand=True)

            # Definición de las 14 columnas solicitadas
            columns = [
                "item", "n_negocio", "cliente", "proyecto", "ubicacion", 
                "responsable", "peso_tm", "fecha_cotizacion", "producto", 
                "mercado", "tipo_oferta", "fabricacion", "montaje", "status"
            ]

            # Scrollbars (Vertical y Horizontal)
            tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
            tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")

            # Guardamos el tree en self para poder actualizarlo desde el filtro
            self.tree_proyectos = ttk.Treeview(
                tree_frame, 
                columns=columns, 
                show="headings", 
                yscrollcommand=tree_scroll_y.set, 
                xscrollcommand=tree_scroll_x.set
            )

            tree_scroll_y.config(command=self.tree_proyectos.yview)
            tree_scroll_x.config(command=self.tree_proyectos.xview)

            # Empaquetar scrollbars y tabla
            tree_scroll_y.pack(side="right", fill="y")
            tree_scroll_x.pack(side="bottom", fill="x")
            self.tree_proyectos.pack(side="left", fill="both", expand=True)

            # Configurar títulos de las columnas
            headers_name = [
                "Item", "N° Negocio", "Cliente", "Proyecto", "Ubicación", 
                "Responsable", "Peso TM", "F. Cotización", "Producto", 
                "Mercado", "Tipo Oferta", "Fabricación?", "Montaje?", "Status"
            ]

            for col, name in zip(columns, headers_name):
                self.tree_proyectos.heading(col, text=name, anchor="center")
                self.tree_proyectos.column(col, width=110, anchor="w", stretch=True)

            # Ajustar anchos específicos para columnas clave
            self.tree_proyectos.column("item", width=50, anchor="center")
            self.tree_proyectos.column("peso_tm", width=80, anchor="e")
            self.tree_proyectos.column("status", width=90, anchor="center")

            # Configuración de colores para el semáforo (Tags)
            self.tree_proyectos.tag_configure("verde", background="#d4edda", foreground="#155724")      # Verde suave
            self.tree_proyectos.tag_configure("amarillo", background="#fff3cd", foreground="#856404")   # Amarillo suave
            self.tree_proyectos.tag_configure("rojo", background="#f8d7da", foreground="#721c24")       # Rojo suave

            # Cargar datos iniciales (por defecto "Estudio")
            self.cargar_datos_proyectos(status_filtro="Estudio")

    def cargar_datos_proyectos(self, status_filtro="Todos"):
            # Limpiar registros actuales de la tabla
            for row in self.tree_proyectos.get_children():
                self.tree_proyectos.delete(row)

            try:
                engine = create_engine(PG_URI)
                with engine.connect() as connection:
                    
                    # Prefijando con proyectos. y manteniendo comillas dobles para las mayúsculas
                    if status_filtro == "Todos":
                        query = text("""
                            SELECT proyectos."Correlativo", proyectos."Negocio", proyectos."NombreCliente", 
                                proyectos."NombreProyecto", proyectos."Ubicacion", proyectos."Responsable", 
                                proyectos."PesoTM", proyectos."FechaEntregacotizacion", proyectos."Rubro", 
                                proyectos."Destino", proyectos."TipoCotizacion", proyectos."OpFabricacion", 
                                proyectos."OpMontaje", proyectos."Status" 
                            FROM public.proyectos
                        """)
                        result = connection.execute(query)
                    else:
                        query = text("""
                            SELECT proyectos."Correlativo", proyectos."Negocio", proyectos."NombreCliente", 
                                proyectos."NombreProyecto", proyectos."Ubicacion", proyectos."Responsable", 
                                proyectos."PesoTM", proyectos."FechaEntregacotizacion", proyectos."Rubro", 
                                proyectos."Destino", proyectos."TipoCotizacion", proyectos."OpFabricacion", 
                                proyectos."OpMontaje", proyectos."Status" 
                            FROM public.proyectos 
                            WHERE LOWER(proyectos."Status") = LOWER(:estatus)
                        """)
                        result = connection.execute(query, {"estatus": status_filtro})
                    
                    hoy = date.today()

                    for row in result:
                        f_cot = row[7]  # FechaEntregacotizacion
                        tag = "verde"

                        # Aplicar lógica de semáforo de fechas
                        if f_cot:
                            if isinstance(f_cot, str):
                                try:
                                    f_cot = datetime.strptime(f_cot[:10], "%Y-%m-%d").date()
                                except:
                                    pass
                            
                            if isinstance(f_cot, (date, datetime)):
                                if isinstance(f_cot, datetime):
                                    f_cot = f_cot.date()
                                
                                dias_restantes = (f_cot - hoy).days

                                if dias_restantes >= 7:
                                    tag = "verde"
                                elif 5 <= dias_restantes < 7:
                                    tag = "amarillo"
                                else:
                                    tag = "rojo"

                        # Insertar fila con su respectivo semáforo
                        self.tree_proyectos.insert("", "end", values=row, tags=(tag,))

            except Exception as e:
                print(f"Error al consultar proyectos reales: {e}")

    def filtrar_proyectos_por_status(self, seleccion):
        # Método que se ejecuta automáticamente al cambiar el valor del ComboBox
        self.cargar_datos_proyectos(status_filtro=seleccion)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas salir?"):
            self.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()