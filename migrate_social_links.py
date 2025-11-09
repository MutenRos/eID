"""
Script de migración para actualizar la tabla social_links
- Elimina columna icon
- Añade columna updated_at
- Añade índice para (user_id, platform)
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def migrate():
    print("="*60)
    print(" Migración de tabla social_links")
    print("="*60)
    
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'eid')
        )
        cursor = connection.cursor()
        
        print("\n✓ Conectado a la base de datos 'eid'")
        
        # 1. Verificar si existe la columna icon
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_schema = %s 
              AND table_name = 'social_links' 
              AND column_name = 'icon'
        """, (os.getenv('DB_NAME', 'eid'),))
        
        if cursor.fetchone()[0] > 0:
            print("\n→ Eliminando columna 'icon'...")
            cursor.execute("ALTER TABLE social_links DROP COLUMN icon")
            print("✓ Columna 'icon' eliminada")
        else:
            print("\n○ Columna 'icon' ya no existe")
        
        # 2. Verificar si existe la columna updated_at
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_schema = %s 
              AND table_name = 'social_links' 
              AND column_name = 'updated_at'
        """, (os.getenv('DB_NAME', 'eid'),))
        
        if cursor.fetchone()[0] == 0:
            print("\n→ Añadiendo columna 'updated_at'...")
            cursor.execute("""
                ALTER TABLE social_links 
                ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """)
            print("✓ Columna 'updated_at' añadida")
        else:
            print("\n○ Columna 'updated_at' ya existe")
        
        # 3. Añadir índice para (user_id, platform) si no existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.statistics 
            WHERE table_schema = %s 
              AND table_name = 'social_links' 
              AND index_name = 'idx_platform'
        """, (os.getenv('DB_NAME', 'eid'),))
        
        if cursor.fetchone()[0] == 0:
            print("\n→ Creando índice 'idx_platform'...")
            cursor.execute("""
                CREATE INDEX idx_platform ON social_links(user_id, platform)
            """)
            print("✓ Índice 'idx_platform' creado")
        else:
            print("\n○ Índice 'idx_platform' ya existe")
        
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ Migración completada exitosamente!")
        print("="*60)
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Error: {err}")
        return False
    
    return True

if __name__ == '__main__':
    migrate()
