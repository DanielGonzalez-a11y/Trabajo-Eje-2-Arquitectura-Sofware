# controllers/app_controller.py
import folium
from folium.plugins import MarkerCluster
import os
from datetime import datetime, timedelta
from typing import List, Optional, Callable
from models.database import DatabaseManager
from models.entities import Material, CentroReciclaje, Noticia, Recordatorio


class AppController:
    def __init__(self):
        self.db = DatabaseManager()
        self._on_materiales_loaded = None
        self._on_centros_loaded = None
        self._on_noticias_loaded = None
        self._on_recordatorios_loaded = None
        self._materiales_cache = []
        self._centros_cache = []
        self._noticias_cache = []
        self._recordatorios_cache = []

    # === MATERIALES ===
    def cargar_materiales(self):
        """Notifica al controlador para cargar materiales"""
        self._materiales_cache = self.db.get_materiales()
        if self._on_materiales_loaded:
            self._on_materiales_loaded(self._materiales_cache)

    def set_on_materiales_loaded(self, callback: Callable[[List[Material]], None]):
        """Establece callback para cuando los materiales se carguen"""
        self._on_materiales_loaded = callback

    def get_material_by_id(self, id_material: int) -> Optional[Material]:
        """Obtiene un material específico por ID"""
        if not self._materiales_cache:
            return self.db.get_material_by_id(id_material)
        return next((m for m in self._materiales_cache if m.id_material == id_material), None)

    def get_materiales_agrupados(self) -> dict:
        """Retorna materiales agrupados por categoría"""
        agrupados = {}
        for material in self._materiales_cache:
            if material.nombre_categoria not in agrupados:
                agrupados[material.nombre_categoria] = []
            agrupados[material.nombre_categoria].append(material)
        return agrupados

    # === CENTROS DE RECICLAJE ===
    def cargar_centros_reciclaje(self):
        """Notifica al controlador para cargar centros"""
        self._centros_cache = self.db.get_centros_reciclaje()

        # Cargar materiales para cada centro
        for centro in self._centros_cache:
            centro.materiales = self.db.get_materiales_por_centro(centro.id_centro)

        if self._on_centros_loaded:
            self._on_centros_loaded(self._centros_cache)

    def set_on_centros_loaded(self, callback: Callable[[List[CentroReciclaje]], None]):
        """Establece callback para cuando los centros se carguen"""
        self._on_centros_loaded = callback

    def get_centro_by_id(self, id_centro: int) -> Optional[CentroReciclaje]:
        """Obtiene un centro específico por ID con sus materiales"""
        # Buscar en la caché primero (más eficiente)
        if self._centros_cache:
            for centro in self._centros_cache:
                if centro.id_centro == id_centro:
                    return centro

        # Si no está en caché, buscar en la base de datos
        try:
            centro = self.db.get_centro_by_id(id_centro)
            if centro:
                # Cargar materiales para este centro específico
                centro.materiales = self.db.get_materiales_por_centro(id_centro)
            return centro
        except Exception as e:
            print(f"Error obteniendo centro por ID: {e}")
            return None

    # === NOTICIAS ===
    def cargar_noticias(self):
        """Notifica al controlador para cargar noticias"""
        self._noticias_cache = self.db.get_noticias()
        if self._on_noticias_loaded:
            self._on_noticias_loaded(self._noticias_cache)

    def set_on_noticias_loaded(self, callback: Callable[[List[Noticia]], None]):
        """Establece callback para cuando las noticias se carguen"""
        self._on_noticias_loaded = callback

    def get_noticia_by_id(self, id_noticia: int) -> Optional[Noticia]:
        """Obtiene una noticia específica por ID"""
        return next((n for n in self._noticias_cache if n.id_noticia == id_noticia), None)

    # === RECORDATORIOS ===
    def cargar_recordatorios(self):
        """Notifica al controlador para cargar recordatorios"""
        self._recordatorios_cache = self.db.get_recordatorios()
        if self._on_recordatorios_loaded:
            self._on_recordatorios_loaded(self._recordatorios_cache)

    def set_on_recordatorios_loaded(self, callback: Callable[[List[Recordatorio]], None]):
        """Establece callback para cuando los recordatorios se carguen"""
        self._on_recordatorios_loaded = callback

    def guardar_recordatorio(self, titulo: str, descripcion: str, fecha: str, hora: str, repetir: bool) -> bool:
        """Guarda un nuevo recordatorio"""
        nuevo_recordatorio = Recordatorio(
            id_recordatorio=0,  # Se asignará automáticamente
            titulo=titulo,
            descripcion=descripcion,
            fecha_recordatorio=fecha,
            hora_recordatorio=hora,
            repetir_semanal=repetir,
            activo=True
        )

        resultado = self.db.guardar_recordatorio(nuevo_recordatorio)
        if resultado:
            # Recargar recordatorios
            self.cargar_recordatorios()
        return resultado

    # === MAPA CON FOLIUM ===
    def generar_mapa_centros(self, centros: List[CentroReciclaje]) -> str:
        """Genera un mapa HTML con los centros de reciclaje y retorna la ruta del archivo"""
        try:
            # Centro del mapa en Bogotá
            mapa = folium.Map(
                location=[4.6097, -74.0817],  # Coordenadas de Bogotá
                zoom_start=11,
                tiles='OpenStreetMap'
            )

            # Agrupar marcadores para mejor visualización
            marker_cluster = MarkerCluster().add_to(mapa)

            # Agregar cada centro al mapa
            for centro in centros:
                # Crear lista de materiales para el popup
                materiales_lista = ""
                for material in centro.materiales[:5]:  # Mostrar máximo 5 materiales
                    materiales_lista += f"• {material.nombre_material}<br>"

                if len(centro.materiales) > 5:
                    materiales_lista += f"• ... y {len(centro.materiales) - 5} más<br>"

                # Crear popup con información
                popup_html = f"""
                <div style="width: 300px; font-family: Arial, sans-serif;">
                    <h3 style="color: #2e7d32; margin-bottom: 10px;">{centro.nombre_centro}</h3>
                    <p><b>📍 Dirección:</b> {centro.direccion}</p>
                    <p><b>📞 Teléfono:</b> {centro.telefono}</p>
                    <p><b>🕒 Horario:</b> {centro.horario_atencion}</p>
                    <p><b>♻️ Materiales aceptados ({len(centro.materiales)}):</b></p>
                    <div style="max-height: 100px; overflow-y: auto; background: #f5f5f5; padding: 5px; border-radius: 3px;">
                        {materiales_lista}
                    </div>
                </div>
                """

                folium.Marker(
                    location=[centro.latitud, centro.longitud],
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f"Click para ver detalles de {centro.nombre_centro}",
                    icon=folium.Icon(
                        color='green',
                        icon='recycle',
                        prefix='fa'
                    )
                ).add_to(marker_cluster)

            # Agregar título al mapa
            title_html = '''
                 <h3 align="center" style="font-size:20px"><b>🗺️ Centros de Reciclaje - Bogotá</b></h3>
                 <p align="center">♻️ Puntos verdes para reciclar correctamente</p>
                 '''
            mapa.get_root().html.add_child(folium.Element(title_html))

            # Guardar mapa como HTML
            mapa_dir = "mapas"
            if not os.path.exists(mapa_dir):
                os.makedirs(mapa_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mapa_path = os.path.join(mapa_dir, f"mapa_centros.html")
            mapa.save(mapa_path)

            print(f"Mapa generado exitosamente: {mapa_path}")
            return mapa_path

        except Exception as e:
            print(f"Error generando mapa: {e}")
            return None

    def get_ruta_mapa_actual(self) -> str:
        """Retorna la ruta del mapa más reciente"""
        mapa_path = "mapas/mapa_centros.html"
        if os.path.exists(mapa_path):
            return mapa_path
        return None

    # === GESTIÓN DE LA APLICACIÓN ===
    def cerrar_aplicacion(self):
        """Cierra recursos de la aplicación"""
        self.db.close()

    def verificar_conexion(self) -> bool:
        """Verifica si hay conexión a la base de datos"""
        return self.db.connection is not None

    def eliminar_recordatorio(self, id_recordatorio: int) -> bool:
        """Elimina un recordatorio y actualiza la caché"""
        resultado = self.db.eliminar_recordatorio(id_recordatorio)
        if resultado:
            # Actualizar la caché
            self._recordatorios_cache = [r for r in self._recordatorios_cache if r.id_recordatorio != id_recordatorio]
            # Notificar a los observers
            if self._on_recordatorios_loaded:
                self._on_recordatorios_loaded(self._recordatorios_cache)
        return resultado