"""Script para probar si el servidor responde"""
import requests
import sys

try:
    print("🔍 Probando conexión a http://127.0.0.1:5000...")
    response = requests.get('http://127.0.0.1:5000', timeout=5)
    print(f"✅ Status Code: {response.status_code}")
    print(f"✅ Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print(f"✅ Content Length: {len(response.text)} caracteres")
    print(f"\n📄 Primeros 500 caracteres de la respuesta:")
    print("=" * 80)
    print(response.text[:500])
    print("=" * 80)
except requests.exceptions.ConnectionError:
    print("❌ ERROR: No se pudo conectar al servidor")
    print("💡 Asegúrate de que el servidor Flask esté corriendo")
    sys.exit(1)
except requests.exceptions.Timeout:
    print("❌ ERROR: Timeout al conectar")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    sys.exit(1)
