"""
Script de migración para añadir friend_code a usuarios
"""

import mysql.connector
from dotenv import load_dotenv
import os
import secrets
import string

load_dotenv()

def generate_friend_code():
    """Generar código de amigo único (8 caracteres alfanuméricos en mayúsculas)"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))

def migrate():
    print("="*60)
    print(" Migración: Añadir friend_code a usuarios")
    print("="*60)
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'eid')
        )
        cursor = connection.cursor()
        
        print("\n✓ Conectado a la base de datos 'eid'")
        
        # 1. Verificar si existe la columna friend_code
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_schema = %s 
              AND table_name = 'users' 
              AND column_name = 'friend_code'
        """, (os.getenv('DB_NAME', 'eid'),))
        
        if cursor.fetchone()[0] == 0:
            print("\n→ Añadiendo columna 'friend_code'...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN friend_code VARCHAR(12) AFTER password_hash
            """)
            print("✓ Columna 'friend_code' añadida")
            
            # Generar códigos únicos para usuarios existentes
            cursor.execute("SELECT id FROM users")
            users = cursor.fetchall()
            
            if users:
                print(f"\n→ Generando códigos para {len(users)} usuarios existentes...")
                for (user_id,) in users:
                    while True:
                        code = generate_friend_code()
                        # Verificar que sea único
                        cursor.execute("SELECT COUNT(*) FROM users WHERE friend_code = %s", (code,))
                        if cursor.fetchone()[0] == 0:
                            cursor.execute("UPDATE users SET friend_code = %s WHERE id = %s", (code, user_id))
                            print(f"  ✓ Usuario {user_id}: {code}")
                            break
            
            # Hacer la columna NOT NULL y UNIQUE
            cursor.execute("""
                ALTER TABLE users 
                MODIFY COLUMN friend_code VARCHAR(12) NOT NULL UNIQUE
            """)
            
            # Añadir índice
            cursor.execute("""
                CREATE INDEX idx_friend_code ON users(friend_code)
            """)
            print("✓ Índice 'idx_friend_code' creado")
            
        else:
            print("\n○ Columna 'friend_code' ya existe")
        
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
