# models/__init__.py
from .entities import Material, CentroReciclaje
from .database import DatabaseManager

__all__ = ['Material', 'CentroReciclaje', 'DatabaseManager']