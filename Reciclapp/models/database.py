# models/database.py
import psycopg2
from typing import List, Optional
from .entities import Material, CentroReciclaje, Noticia, Recordatorio


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
            self.connection = None

    def get_materiales(self) -> List[Material]:
        if not self.connection:
            return []

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
            resultados = cursor.fetchall()
            cursor.close()

            materiales = []
            for fila in resultados:
                material = Material(
                    id_material=fila[0],
                    nombre_categoria=fila[1],
                    nombre_material=fila[2],
                    descripcion=fila[3],
                    tiempo_descomposicion=fila[4]
                )
                materiales.append(material)

            return materiales
        except Exception as e:
            print(f"Error al obtener materiales: {e}")
            return []

    def get_material_by_id(self, id_material: int) -> Optional[Material]:
        if not self.connection:
            return None

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
            resultado = cursor.fetchone()
            cursor.close()

            if resultado:
                return Material(*resultado)
            return None
        except Exception as e:
            print(f"Error al obtener material: {e}")
            return None

    def get_centros_reciclaje(self) -> List[CentroReciclaje]:
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT id_centro, nombre_centro, direccion, telefono, 
                   horario_atencion, latitud, longitud
            FROM centros_reciclaje
            ORDER BY nombre_centro
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            centros = []
            for fila in resultados:
                centro = CentroReciclaje(
                    id_centro=fila[0],
                    nombre_centro=fila[1],
                    direccion=fila[2],
                    telefono=fila[3],
                    horario_atencion=fila[4],
                    latitud=float(fila[5]),
                    longitud=float(fila[6])
                )
                centros.append(centro)

            return centros
        except Exception as e:
            print(f"Error al obtener centros: {e}")
            return []

    def get_materiales_por_centro(self, id_centro: int) -> List[Material]:
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT tm.id_material, cr.nombre_categoria, tm.nombre_material, 
                   tm.descripcion, tm.tiempo_descomposicion
            FROM centros_materiales cm
            JOIN tipos_material tm ON cm.id_material = tm.id_material
            JOIN categorias_reciclaje cr ON tm.id_categoria = cr.id_categoria
            WHERE cm.id_centro = %s
            """
            cursor.execute(query, (id_centro,))
            resultados = cursor.fetchall()
            cursor.close()

            materiales = []
            for fila in resultados:
                material = Material(*fila)
                materiales.append(material)

            return materiales
        except Exception as e:
            print(f"Error al obtener materiales del centro: {e}")
            return []

    def get_noticias(self) -> List[Noticia]:
        """Obtiene noticias sobre reciclaje en Bogotá"""
        if not self.connection:
            # Datos de ejemplo si no hay conexión
            return self._get_noticias_ejemplo()

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT id_noticia, titulo, resumen, contenido, fecha_publicacion, fuente
            FROM noticias_reciclaje
            ORDER BY fecha_publicacion DESC
            LIMIT 10
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            noticias = []
            for fila in resultados:
                noticia = Noticia(*fila)
                noticias.append(noticia)

            return noticias
        except Exception as e:
            print(f"Error al obtener noticias: {e}")
            return self._get_noticias_ejemplo()

    def _get_noticias_ejemplo(self) -> List[Noticia]:
        """Noticias de ejemplo sobre reciclaje en Bogotá"""
        return [
            Noticia(
                1,
                "Bogotá incrementa en 15% el reciclaje en 2024",
                "La ciudad alcanzó nuevas metas en reciclaje gracias a programas de concientización",
                "Bogotá ha logrado un incremento del 15% en las tasas de reciclaje durante el primer trimestre de 2024...",
                "2024-03-15",
                "Alcaldía de Bogotá"
            ),
            Noticia(
                2,
                "Nuevos puntos ecológicos en TransMilenio",
                "Instalación de 50 nuevos puntos de reciclaje en estaciones principales",
                "El sistema TransMilenio incorporó 50 puntos ecológicos para facilitar el reciclaje a los ciudadanos...",
                "2024-03-10",
                "Secretaría de Ambiente"
            ),
            Noticia(
                3,
                "Campana 'Recicla por Bogotá' supera expectativas",
                "Más de 100.000 familias participaron en la iniciativa",
                "La campaña de reciclaje municipal logró la participación récord de 100.000 familias bogotanas...",
                "2024-03-05",
                "UAESP"
            ),
            Noticia(
                4,
                "Bogotá implementa recolección diferenciada de residuos",
                "Nuevo sistema de recolección por colores se expande a 5 localidades más",
                "El programa de recolección diferenciada llegará a Usaquén, Suba, Engativá, Fontibón y Kennedy...",
                "2024-02-28",
                "Alcaldía de Bogotá"
            )
        ]

    def get_recordatorios(self) -> List[Recordatorio]:
        """Obtiene recordatorios del usuario"""
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT id_recordatorio, titulo, descripcion, fecha_recordatorio, 
                   hora_recordatorio, repetir_semanal, activo
            FROM recordatorios_reciclaje
            WHERE activo = true
            ORDER BY fecha_recordatorio
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()

            recordatorios = []
            for fila in resultados:
                recordatorio = Recordatorio(*fila)
                recordatorios.append(recordatorio)

            return recordatorios
        except Exception as e:
            print(f"Error al obtener recordatorios: {e}")
            return []

    def guardar_recordatorio(self, recordatorio: Recordatorio) -> bool:
        """Guarda un nuevo recordatorio"""
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO recordatorios_reciclaje 
            (titulo, descripcion, fecha_recordatorio, hora_recordatorio, repetir_semanal, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                recordatorio.titulo,
                recordatorio.descripcion,
                recordatorio.fecha_recordatorio,
                recordatorio.hora_recordatorio,
                recordatorio.repetir_semanal,
                recordatorio.activo
            ))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error guardando recordatorio: {e}")
            return False

    def get_centro_by_id(self, id_centro: int) -> Optional[CentroReciclaje]:
        """Obtiene un centro específico por ID"""
        if not self.connection:
            return None

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT id_centro, nombre_centro, direccion, telefono, 
                   horario_atencion, latitud, longitud
            FROM centros_reciclaje
            WHERE id_centro = %s
            """
            cursor.execute(query, (id_centro,))
            resultado = cursor.fetchone()
            cursor.close()

            if resultado:
                centro = CentroReciclaje(
                    id_centro=resultado[0],
                    nombre_centro=resultado[1],
                    direccion=resultado[2],
                    telefono=resultado[3],
                    horario_atencion=resultado[4],
                    latitud=float(resultado[5]),
                    longitud=float(resultado[6])
                )
                return centro
            return None
        except Exception as e:
            print(f"Error al obtener centro por ID: {e}")
            return None

    def eliminar_recordatorio(self, id_recordatorio: int) -> bool:
        """Elimina un recordatorio por ID"""
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM recordatorios_reciclaje WHERE id_recordatorio = %s"
            cursor.execute(query, (id_recordatorio,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error eliminando recordatorio: {e}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión a BD cerrada")