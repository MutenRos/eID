"""
Gestor de conexiones MySQL para eID
"""

import mysql.connector
from mysql.connector import Error
import os

class Database:
    """Clase para manejar la conexión a MySQL"""
    
    def __init__(self):
        self.host = os.environ.get('DB_HOST', 'localhost')
        self.port = os.environ.get('DB_PORT', '3306')
        self.user = os.environ.get('DB_USER', 'root')
        self.password = os.environ.get('DB_PASSWORD', '')
        self.database = os.environ.get('DB_NAME', 'eid')
        self.connection = None
    
    def connect(self):
        """Establecer conexión con MySQL usando pool de conexiones"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci',
                autocommit=False
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None
    
    def disconnect(self):
        """Cerrar conexión"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Ejecutar query (INSERT, UPDATE, DELETE)"""
        cursor = self.connection.cursor(buffered=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error ejecutando query: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def fetch_one(self, query, params=None):
        """Obtener un solo resultado"""
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error en fetch_one: {e}")
            return None
        finally:
            cursor.close()
    
    def fetch_all(self, query, params=None):
        """Obtener todos los resultados"""
        cursor = self.connection.cursor(dictionary=True, buffered=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error en fetch_all: {e}")
            return []
        finally:
            cursor.close()

# Instancia global
db = Database()
