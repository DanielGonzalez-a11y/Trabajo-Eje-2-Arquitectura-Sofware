
import psycopg2
from psycopg2 import sql


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="reciclapp",
                user="postgres",
                password="ROOT",
                port="5432"
            )
            print("Conexión exitosa a PostgreSQL")
        except Exception as e:
            print(f"Error de conexión: {e}")

    def get_materiales(self):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT tm.id_material, cr.nombre_categoria, tm.nombre_material, 
                   tm.descripcion, tm.tiempo_descomposicion
            FROM tipos_material tm
            JOIN categorias_reciclaje cr ON tm.id_categoria = cr.id_categoria
            ORDER BY cr.nombre_categoria, tm.nombre_material
            """
            cursor.execute(query)
            materiales = cursor.fetchall()
            cursor.close()
            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {e}")
            return []

    def get_material_by_id(self, id_material):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT tm.id_material, cr.nombre_categoria, tm.nombre_material, 
                   tm.descripcion, tm.tiempo_descomposicion
            FROM tipos_material tm
            JOIN categorias_reciclaje cr ON tm.id_categoria = cr.id_categoria
            WHERE tm.id_material = %s
            """
            cursor.execute(query, (id_material,))
            material = cursor.fetchone()
            cursor.close()
            return material
        except Exception as e:
            print(f"Error al obtener material: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()


