from sqlalchemy import create_engine, text

# Tu conexión local actual
PG_URI = "postgresql+psycopg2://postgres:Asus2026@localhost:5432/CRM-Ventas?client_encoding=utf8"

engine = create_engine(PG_URI)

with engine.connect() as conn:
    print("--- 1. LISTANDO LAS TABLAS DE TU BD ---")
    tablas = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    for t in tablas:
        print(t[0])

    print("\n--- 2. PROBANDO CONSULTA A LA TABLA DE PROYECTOS ---")
    try:
        # Intentamos ver los primeros registros de la tabla proyectos
        res = conn.execute(text("SELECT * FROM proyectos LIMIT 1;"))
        for row in res:
            print("¡Tabla encontrada con éxito! Columnas:", row._mapping.keys())
    except Exception as e:
        print("La tabla 'proyectos' dio un error (quizás se llama distinto, ej: 'Proyecto', 'tbl_proyectos'):", e)