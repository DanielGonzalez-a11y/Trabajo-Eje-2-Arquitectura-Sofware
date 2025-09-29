# models/entities.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Material:
    id_material: int
    nombre_categoria: str
    nombre_material: str
    descripcion: str
    tiempo_descomposicion: str

    def __str__(self):
        return f"{self.nombre_material} - {self.descripcion}"


@dataclass
class CentroReciclaje:
    id_centro: int
    nombre_centro: str
    direccion: str
    telefono: str
    horario_atencion: str
    latitud: float
    longitud: float
    materiales: Optional[List[Material]] = None

    def __post_init__(self):
        if self.materiales is None:
            self.materiales = []


@dataclass
class Noticia:
    id_noticia: int
    titulo: str
    resumen: str
    contenido: str
    fecha_publicacion: str
    fuente: str

    def __str__(self):
        return f"{self.titulo} - {self.fecha_publicacion}"


@dataclass
class Recordatorio:
    id_recordatorio: int
    titulo: str
    descripcion: str
    fecha_recordatorio: str
    hora_recordatorio: str
    repetir_semanal: bool
    activo: bool

    def __str__(self):
        return f"{self.titulo} - {self.fecha_recordatorio}"