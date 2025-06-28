import sqlite3
import os
from typing import Optional

class DatabaseManager:
    """
    Clase para manejar la base de datos del inventario.
    Proporciona métodos para conectar, crear tablas y ejecutar operaciones.
    """
    
    def __init__(self, db_name: str = "inventario.db"):
        """
        Inicializa el manejador de base de datos.
        
        Args:
            db_name: Nombre del archivo de base de datos
        """
        self.db_name = db_name
        self.create_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            Conexión a la base de datos SQLite
        """
        return sqlite3.connect(self.db_name)
    
    def create_database(self) -> None:
        """
        Crea la base de datos y la tabla productos si no existen.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Crear tabla productos
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        descripcion TEXT,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        categoria TEXT
                    )
                ''')
                
                conn.commit()
                print("Base de datos creada exitosamente.")
                
        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[list]:
        """
        Ejecuta una consulta SQL.
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta
            
        Returns:
            Resultados de la consulta (para SELECT) o None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                
                # Si es una consulta SELECT, devolver resultados
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                
                conn.commit()
                return None
                
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None
    
    def close(self) -> None:
        """
        Cierra la conexión a la base de datos.
        """
        # SQLite se cierra automáticamente con el context manager
        pass 