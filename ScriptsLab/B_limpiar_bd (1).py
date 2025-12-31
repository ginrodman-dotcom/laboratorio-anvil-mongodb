import pymongo
from pymongo import MongoClient


URI = "mongodb+srv://ginrodman_db_user:X5xxELI2pqUdM3Va@tiendas.9gabutg.mongodb.net/?retryWrites=true&w=majority&appName=Tiendas"

try:
    client = pymongo.MongoClient(URI)
    print(" Conectado para formateo...")
except Exception as e:
    print(f" Error al conectar: {e}")
    exit()

db = client["Tienda"]


col_productos = db["Productos"]
col_empleados = db["Empleados"]
col_clientes = db["Clientes"]
col_ventas = db["Ventas"]

def formatear_todo():
    print("\n⚠️  ATENCIÓN: Se borrarán TODOS los datos de la base de datos 'Tienda'.")
    confirmacion = input("¿Estás seguro? Escribe 'SI' para continuar: ")

    if confirmacion.upper() == "SI":
        print("\n Iniciando limpieza...")
        
        # Borrando todo
        p = col_productos.delete_many({})
        e = col_empleados.delete_many({})
        c = col_clientes.delete_many({})
        v = col_ventas.delete_many({})

        print(f"   -> Productos eliminados: {p.deleted_count}")
        print(f"   -> Empleados eliminados: {e.deleted_count}")
        print(f"   -> Clientes eliminados: {c.deleted_count}")
        print(f"   -> Ventas eliminadas: {v.deleted_count}")
        
        print("\n ¡Base de datos formateada y vacía! ")
    else:
        print("\n Operación cancelada. No se borró nada.")

if __name__ == "__main__":
    formatear_todo()