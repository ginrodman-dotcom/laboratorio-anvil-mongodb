import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from bson.objectid import ObjectId

URI = "mongodb+srv://ginrodman_db_user:X5xxELI2pqUdM3Va@tiendas.9gabutg.mongodb.net/?retryWrites=true&w=majority&appName=Tiendas"
DATABASE_NAME = "Tienda"
COLLECTIONS = ["Productos", "Empleados", "Clientes", "Ventas"]

_client = None
_db = None

def conectar_mongodb():
    """Conecta a MongoDB Atlas (patrón singleton)"""
    global _client, _db
    
    if _client is None:
        try:
            _client = MongoClient(URI, serverSelectionTimeoutMS=10000)

            # Verificar conexión

            _client.admin.command('ping')
            _db = _client[DATABASE_NAME]
            print("✅ Conexión exitosa a MongoDB Atlas")
            return _db
        except ConnectionFailure as e:
            print(f"❌ Error de conexión: {e}")
            return None
        except Exception as e:
            print(f"⚠️  Error inesperado: {e}")
            return None
    return _db

def obtener_coleccion(nombre_coleccion):

    """Obtiene una colección específica"""

    db = conectar_mongodb()
    if db is None:
        return None
    if nombre_coleccion not in COLLECTIONS:
        print(f"⚠️  Advertencia: Colección '{nombre_coleccion}' no está en la lista oficial")
    return db[nombre_coleccion]

#  FUNCIONES CRUD GENÉRICAS 

def crear_documento_generico(nombre_coleccion, datos):

    """
    Crea un documento en cualquier colección
    """

    try:
        coleccion = obtener_coleccion(nombre_coleccion)
        if coleccion is None:
            return {"success": False, "error": "No se pudo conectar a la BD"}
        if not isinstance(datos, dict):
            return {"success": False, "error": "Los datos deben ser un diccionario"}
        if len(datos) < 3:
            return {"success": False, "error": "Se requieren al menos 3 campos (sin contar _id)"}
        
        resultado = coleccion.insert_one(datos)
        return {
            "success": True, 
            "id": str(resultado.inserted_id),
            "message": f"Documento creado en '{nombre_coleccion}'"
        }
    except PyMongoError as e:
        return {"success": False, "error": f"Error de MongoDB: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {e}"}

def leer_documentos_generico(nombre_coleccion, filtro=None, sort_campo=None, orden="asc", limite=None, skip=0):
    
    """
    Lee documentos con filtros avanzados
    """

    try:
        coleccion = obtener_coleccion(nombre_coleccion)
        if coleccion is None:
            return []
        
        filtro = filtro or {}
        
        # Configurar orden

        orden_valor = 1 if orden == "asc" else -1
        
        # Construir consulta

        cursor = coleccion.find(filtro)
        
        # Aplicar ordenamiento

        if sort_campo:
            cursor = cursor.sort(sort_campo, orden_valor)
        
        # Aplicar skip (paginación)

        if skip > 0:
            cursor = cursor.skip(skip)
        
        # Aplicar límite

        if limite and isinstance(limite, int) and limite > 0:
            cursor = cursor.limit(limite)
        
        documentos = list(cursor)
        
        # Convertir ObjectId a string para serialización

        for doc in documentos:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
        
        return documentos
    except PyMongoError as e:
        print(f"❌ Error al leer documentos: {e}")
        return []
    except Exception as e:
        print(f"⚠️  Error inesperado: {e}")
        return []

def actualizar_documento_generico(nombre_coleccion, filtro, nuevos_datos):

    """
    Actualiza documentos
    """

    try:
        coleccion = obtener_coleccion(nombre_coleccion)
        if coleccion is None:
            return {"success": False, "error": "No se pudo conectar a la BD"}
        
        if not filtro:
            return {"success": False, "error": "Se requiere un filtro para actualizar"}
        if not nuevos_datos:
            return {"success": False, "error": "Se requieren datos nuevos para actualizar"}
        
        resultado = coleccion.update_one(filtro, {"$set": nuevos_datos})
        
        if resultado.modified_count > 0:
            return {
                "success": True,
                "modified": resultado.modified_count,
                "message": f"Documento actualizado en '{nombre_coleccion}'"
            }
        else:
            return {
                "success": False,
                "error": "No se encontraron documentos que coincidan con el filtro"
            }
    except PyMongoError as e:
        return {"success": False, "error": f"Error de MongoDB: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {e}"}

def eliminar_documento_generico(nombre_coleccion, filtro, confirmar=True):

    """
    Elimina documentos
    """

    try:
        coleccion = obtener_coleccion(nombre_coleccion)
        if coleccion is None:
            return {"success": False, "error": "No se pudo conectar a la BD"}
        
        if not filtro:
            return {"success": False, "error": "Se requiere un filtro para eliminar"}
        
        # Confirmación 

        if confirmar:
            print(f"\n⚠️  ATENCIÓN: Se eliminarán documentos de '{nombre_coleccion}'")
            print(f"   Filtro: {filtro}")
            respuesta = input("   ¿Continuar? (s/n): ")
            if respuesta.lower() != 's':
                return {"success": False, "error": "Eliminación cancelada por el usuario"}
        
        resultado = coleccion.delete_one(filtro)
        
        if resultado.deleted_count > 0:
            return {
                "success": True,
                "deleted": resultado.deleted_count,
                "message": f"Documento eliminado de '{nombre_coleccion}'"
            }
        else:
            return {
                "success": False,
                "error": "No se encontraron documentos que coincidan con el filtro"
            }
    except PyMongoError as e:
        return {"success": False, "error": f"Error de MongoDB: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Error inesperado: {e}"}

#  FUNCIONES ESPECÍFICAS POR COLECCIÓN 

#  PRODUCTOS 

def buscar_productos_por_genero(genero, limite=5):

    """Busca productos por género musical"""

    filtro = {"genero": genero}
    return leer_documentos_generico("Productos", filtro=filtro, sort_campo="nombre", limite=limite)

def obtener_productos_ordenados_por_precio(orden="asc", limite=10):

    """Busca productos ordenados por precio"""

    return leer_documentos_generico("Productos", sort_campo="precio", orden=orden, limite=limite)

def actualizar_precio_producto(nombre_producto, nuevo_precio):

    """Actualiza el precio de un producto"""

    filtro = {"nombre": nombre_producto}
    nuevos_datos = {"precio": nuevo_precio}
    return actualizar_documento_generico("Productos", filtro, nuevos_datos)

def buscar_productos_con_stock_bajo(umbral=10):

    """Busca productos con stock bajo"""

    filtro = {"stock": {"$lt": umbral}}
    return leer_documentos_generico("Productos", filtro=filtro, sort_campo="stock")

# EMPLEADOS 

def buscar_empleados_por_cargo(cargo, limite=None):

    """Busca empleados por cargo"""

    filtro = {"cargo": cargo}
    return leer_documentos_generico("Empleados", filtro=filtro, sort_campo="identificador", limite=limite)

def obtener_empleados_ordenados_por_sueldo(orden="asc"):

    """Obtiene empleados ordenados por sueldo"""

    return leer_documentos_generico("Empleados", sort_campo="sueldo", orden=orden)

#  CLIENTES 
def buscar_clientes_vip(es_vip="SÍ"):

    """Busca clientes VIP"""

    filtro = {"vip": es_vip}
    return leer_documentos_generico("Clientes", filtro=filtro)

def obtener_clientes_por_edad_rango(min_edad=18, max_edad=65):

    """Obtiene clientes dentro de un rango de edad"""

    filtro = {"edad": {"$gte": min_edad, "$lte": max_edad}}
    return leer_documentos_generico("Clientes", filtro=filtro, sort_campo="edad")

#  VENTAS 
def buscar_ventas_por_metodo_pago(metodo_pago):

    """Busca ventas por método de pago"""

    filtro = {"metodo_pago": metodo_pago}
    return leer_documentos_generico("Ventas", filtro=filtro, sort_campo="total", orden="desc")

def obtener_ventas_mayores_a(monto_minimo=100):

    """Obtiene ventas mayores a un monto"""

    filtro = {"total": {"$gt": monto_minimo}}
    return leer_documentos_generico("Ventas", filtro=filtro, sort_campo="total", orden="desc")

#  FUNCIONES DE ESTADÍSTICAS 

def obtener_estadisticas_productos():

    """Obtiene estadísticas de productos"""

    productos = leer_documentos_generico("Productos")
    
    if not productos:
        return {"total": 0, "promedio_precio": 0, "total_stock": 0}
    
    total_productos = len(productos)
    total_precio = sum(p.get('precio', 0) for p in productos)
    total_stock = sum(p.get('stock', 0) for p in productos)
    
    return {
        "total_productos": total_productos,
        "promedio_precio": total_precio / total_productos if total_productos > 0 else 0,
        "total_stock": total_stock,
        "producto_mas_caro": max(productos, key=lambda x: x.get('precio', 0)) if productos else None,
        "producto_menor_stock": min(productos, key=lambda x: x.get('stock', 9999)) if productos else None
    }

#  MENÚ INTERACTIVO 

def mostrar_menu():
    print("\n" + "="*60)
    print("🧪 MENÚ DE PRUEBAS - CRUD COMPLETO")
    print("="*60)
    print("1. Probar conexión a MongoDB")
    print("2. Ver todos los productos")
    print("3. Buscar productos por género")
    print("4. Ver productos ordenados por precio")
    print("5. Actualizar precio de producto")
    print("6. Buscar productos con stock bajo")
    print("7. Buscar empleados por cargo")
    print("8. Buscar clientes VIP")
    print("9. Ver ventas por método de pago")
    print("10. Ver estadísticas de productos")
    print("11. Crear nuevo producto (ejemplo)")
    print("12. Eliminar producto (ejemplo)")
    print("0. Salir")
    print("="*60)

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (0-12): ").strip()
        
        if opcion == "0":
            print("👋 Saliendo del menú...")
            break
        
        elif opcion == "1":
            db = conectar_mongodb()
            if db is not None:
                print("✅ Conexión exitosa!")
                print(f"   Base de datos: {db.name}")
                print(f"   Colecciones: {db.list_collection_names()}")
        
        elif opcion == "2":
            print("\n📦 TODOS LOS PRODUCTOS:")
            productos = leer_documentos_generico("Productos", sort_campo="nombre")
            for i, p in enumerate(productos, 1):
                print(f"   {i}. {p.get('nombre', 'N/A')} - ${p.get('precio', 0)} - Stock: {p.get('stock', 0)}")
        
        elif opcion == "3":
            genero = input("Género a buscar (Rock/Pop/Jazz/etc): ").strip()
            if genero:
                productos = buscar_productos_por_genero(genero)
                print(f"\n🎵 Productos de {genero}:")
                for p in productos:
                    print(f"   • {p.get('nombre')} (${p.get('precio')})")
            else:
                print("❌ Debes ingresar un género")
        
        elif opcion == "4":
            orden = input("Orden (asc/desc) [asc]: ").strip() or "asc"
            productos = obtener_productos_ordenados_por_precio(orden)
            print(f"\n💰 Productos ordenados por precio ({orden}):")
            for p in productos:
                print(f"   • ${p.get('precio')} - {p.get('nombre')}")
        
        elif opcion == "5":
            nombre = input("Nombre del producto a actualizar: ").strip()
            if nombre:
                nuevo_precio = float(input("Nuevo precio: "))
                resultado = actualizar_precio_producto(nombre, nuevo_precio)
                print(f"\n{'✅' if resultado['success'] else '❌'} {resultado.get('message', resultado.get('error', ''))}")
            else:
                print("❌ Debes ingresar un nombre")
        
        elif opcion == "6":
            umbral = int(input("Umbral de stock bajo [10]: ").strip() or "10")
            productos = buscar_productos_con_stock_bajo(umbral)
            print(f"\n⚠️  Productos con stock bajo de {umbral}:")
            for p in productos:
                print(f"   • {p.get('nombre')} - Stock: {p.get('stock')}")
        
        elif opcion == "7":
            cargo = input("Cargo a buscar (Vendedor/Gerente/etc): ").strip()
            if cargo:
                empleados = buscar_empleados_por_cargo(cargo)
                print(f"\n👔 Empleados con cargo '{cargo}':")
                for e in empleados:
                    print(f"   • {e.get('identificador')} - ${e.get('sueldo')} - Turno: {e.get('turno')}")
        
        elif opcion == "8":
            clientes = buscar_clientes_vip()
            print("\n⭐ CLIENTES VIP:")
            for c in clientes:
                print(f"   • {c.get('identificador')} - {c.get('email')} - Edad: {c.get('edad')}")
        
        elif opcion == "9":
            metodo = input("Método de pago (Efectivo/Tarjeta/Yape/etc): ").strip()
            if metodo:
                ventas = buscar_ventas_por_metodo_pago(metodo)
                print(f"\n💳 Ventas con método '{metodo}':")
                for v in ventas:
                    print(f"   • ${v.get('total')} - {v.get('folio')}")
        
        elif opcion == "10":
            stats = obtener_estadisticas_productos()
            print("\n📊 ESTADÍSTICAS DE PRODUCTOS:")
            print(f"   Total productos: {stats['total_productos']}")
            print(f"   Precio promedio: ${stats['promedio_precio']:.2f}")
            print(f"   Stock total: {stats['total_stock']}")
            if stats['producto_mas_caro']:
                print(f"   Producto más caro: {stats['producto_mas_caro'].get('nombre')} (${stats['producto_mas_caro'].get('precio')})")
        
        elif opcion == "11":
            print("\n➕ CREAR NUEVO PRODUCTO (ejemplo):")
            nuevo_producto = {
                "nombre": "Vinilo Especial Edición Limitada",
                "genero": "Rock",
                "precio": 89.99,
                "stock": 25,
                "formato": "Vinilo",
                "artista_id": "Artista_RCK"
            }
            resultado = crear_documento_generico("Productos", nuevo_producto)
            print(f"{'✅' if resultado['success'] else '❌'} {resultado.get('message', resultado.get('error', ''))}")
        
        elif opcion == "12":
            print("\n🗑️  ELIMINAR PRODUCTO (ejemplo - buscará 'Test'):")
            filtro = {"nombre": {"$regex": "Test", "$options": "i"}}
            resultado = eliminar_documento_generico("Productos", filtro, confirmar=True)
            print(f"{'✅' if resultado['success'] else '❌'} {resultado.get('message', resultado.get('error', ''))}")
        
        else:
            print("❌ Opción no válida")
        
        input("\nPresiona Enter para continuar...")

#  EJECUCIÓN PRINCIPAL 

if __name__ == "__main__":
    print("="*60)
    print("🔧 MÓDULO CRUD COMPLETO PARA MONGODB ATLAS")
    print("="*60)
    print("Este módulo contiene:")
    print("• Conexión a MongoDB Atlas")
    print("• Operaciones CRUD completas con validaciones")
    print("• Funciones específicas para cada colección (4)")
    print("• Consultas con filtros, sort, limit (cumple rúbrica)")
    print("• Manejo robusto de errores")
    print("• Funciones de estadísticas")
    print("• Menú interactivo de prueba")
    print("="*60)
    
    # Probar conexión automáticamente

    db = conectar_mongodb()
    if db is None:
        print("\n❌ No se pudo conectar a MongoDB. Verifica:")
        print("   • Tu conexión a internet")
        print("   • La URI de conexión")
        print("   • Que el cluster en MongoDB Atlas esté activo")
    else:
        print(f"\n✅ Conectado a: {db.name}")
        print(f"📊 Colecciones disponibles: {db.list_collection_names()}")
        
        # Preguntar si ejecutar menú interactivo
        
        ejecutar = input("\n¿Ejecutar menú interactivo de pruebas? (s/n): ").strip().lower()
        if ejecutar == 's':
            ejecutar_menu()
        else:
            print("\n✅ Módulo importado correctamente")
            print("\n📋 Funciones disponibles:")
            print("   • conectar_mongodb()")
            print("   • crear_documento_generico(coleccion, datos)")
            print("   • leer_documentos_generico(coleccion, filtro, sort_campo, orden, limite, skip)")
            print("   • actualizar_documento_generico(coleccion, filtro, nuevos_datos)")
            print("   • eliminar_documento_generico(coleccion, filtro, confirmar)")
            print("\n🎯 Funciones específicas por colección (4 colecciones):")
            print("   • buscar_productos_por_genero()")
            print("   • buscar_empleados_por_cargo()")
            print("   • buscar_clientes_vip()")
            print("   • buscar_ventas_por_metodo_pago()")
            print("\n📊 Ejecute 'python C_crud_completo.py' nuevamente para el menú interactivo")