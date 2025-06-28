from typing import List, Optional, Dict, Any
from database import DatabaseManager

class Producto:
    """
    Clase que representa un producto del inventario.
    """
    
    def __init__(self, nombre: str, descripcion: str, cantidad: int, precio: float, categoria: str, id: int = None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio
        self.categoria = categoria
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el producto a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'categoria': self.categoria
        }

class InventarioManager:
    """
    Clase para manejar las operaciones del inventario.
    """
    
    def __init__(self):
        """Inicializa el manejador de inventario."""
        self.db = DatabaseManager()
    
    def registrar_producto(self, producto: Producto) -> bool:
        """
        Registra un nuevo producto en el inventario.
        
        Args:
            producto: Objeto Producto a registrar
            
        Returns:
            True si se registró exitosamente, False en caso contrario
        """
        try:
            query = '''
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                VALUES (?, ?, ?, ?, ?)
            '''
            params = (producto.nombre, producto.descripcion, producto.cantidad, 
                     producto.precio, producto.categoria)
            
            self.db.execute_query(query, params)
            print(f"Producto '{producto.nombre}' registrado exitosamente.")
            return True
            
        except Exception as e:
            print(f"Error al registrar producto: {e}")
            return False
    
    def obtener_todos_los_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.
        
        Returns:
            Lista de objetos Producto
        """
        try:
            query = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos"
            resultados = self.db.execute_query(query)
            
            productos = []
            if resultados:
                for fila in resultados:
                    producto = Producto(
                        id=fila[0],
                        nombre=fila[1],
                        descripcion=fila[2],
                        cantidad=fila[3],
                        precio=fila[4],
                        categoria=fila[5]
                    )
                    productos.append(producto)
            
            return productos
            
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
    
    def buscar_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        """
        Busca un producto por su ID.
        
        Args:
            id_producto: ID del producto a buscar
            
        Returns:
            Objeto Producto si se encuentra, None en caso contrario
        """
        try:
            query = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?"
            resultado = self.db.execute_query(query, (id_producto,))
            
            if resultado and len(resultado) > 0:
                fila = resultado[0]
                return Producto(
                    id=fila[0],
                    nombre=fila[1],
                    descripcion=fila[2],
                    cantidad=fila[3],
                    precio=fila[4],
                    categoria=fila[5]
                )
            
            return None
            
        except Exception as e:
            print(f"Error al buscar producto: {e}")
            return None
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos por nombre (búsqueda parcial).
        
        Args:
            nombre: Nombre del producto a buscar
            
        Returns:
            Lista de productos que coinciden
        """
        try:
            query = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?"
            resultado = self.db.execute_query(query, (f"%{nombre}%",))
            
            productos = []
            if resultado:
                for fila in resultado:
                    producto = Producto(
                        id=fila[0],
                        nombre=fila[1],
                        descripcion=fila[2],
                        cantidad=fila[3],
                        precio=fila[4],
                        categoria=fila[5]
                    )
                    productos.append(producto)
            
            return productos
            
        except Exception as e:
            print(f"Error al buscar productos por nombre: {e}")
            return []
    
    def buscar_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """
        Busca productos por categoría.
        
        Args:
            categoria: Categoría del producto a buscar
            
        Returns:
            Lista de productos de la categoría
        """
        try:
            query = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE categoria LIKE ?"
            resultado = self.db.execute_query(query, (f"%{categoria}%",))
            
            productos = []
            if resultado:
                for fila in resultado:
                    producto = Producto(
                        id=fila[0],
                        nombre=fila[1],
                        descripcion=fila[2],
                        cantidad=fila[3],
                        precio=fila[4],
                        categoria=fila[5]
                    )
                    productos.append(producto)
            
            return productos
            
        except Exception as e:
            print(f"Error al buscar productos por categoría: {e}")
            return []
    
    def actualizar_producto(self, id_producto: int, nombre: str = None, descripcion: str = None,
                          cantidad: int = None, precio: float = None, categoria: str = None) -> bool:
        """
        Actualiza los datos de un producto existente.
        
        Args:
            id_producto: ID del producto a actualizar
            nombre: Nuevo nombre (opcional)
            descripcion: Nueva descripción (opcional)
            cantidad: Nueva cantidad (opcional)
            precio: Nuevo precio (opcional)
            categoria: Nueva categoría (opcional)
            
        Returns:
            True si se actualizó exitosamente, False en caso contrario
        """
        try:
            # Verificar si el producto existe
            producto_existente = self.buscar_producto_por_id(id_producto)
            if not producto_existente:
                print(f"No se encontró producto con ID {id_producto}")
                return False
            
            # Construir la consulta dinámicamente
            campos_actualizar = []
            valores = []
            
            if nombre is not None:
                campos_actualizar.append("nombre = ?")
                valores.append(nombre)
            
            if descripcion is not None:
                campos_actualizar.append("descripcion = ?")
                valores.append(descripcion)
            
            if cantidad is not None:
                campos_actualizar.append("cantidad = ?")
                valores.append(cantidad)
            
            if precio is not None:
                campos_actualizar.append("precio = ?")
                valores.append(precio)
            
            if categoria is not None:
                campos_actualizar.append("categoria = ?")
                valores.append(categoria)
            
            if not campos_actualizar:
                print("No se especificaron campos para actualizar")
                return False
            
            valores.append(id_producto)
            query = f"UPDATE productos SET {', '.join(campos_actualizar)} WHERE id = ?"
            
            self.db.execute_query(query, tuple(valores))
            print(f"Producto con ID {id_producto} actualizado exitosamente.")
            return True
            
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """
        Elimina un producto del inventario.
        
        Args:
            id_producto: ID del producto a eliminar
            
        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            # Verificar si el producto existe
            producto_existente = self.buscar_producto_por_id(id_producto)
            if not producto_existente:
                print(f"No se encontró producto con ID {id_producto}")
                return False
            
            query = "DELETE FROM productos WHERE id = ?"
            self.db.execute_query(query, (id_producto,))
            print(f"Producto con ID {id_producto} eliminado exitosamente.")
            return True
            
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
    
    def generar_reporte_stock_bajo(self, limite_stock: int) -> List[Producto]:
        """
        Genera un reporte de productos con stock bajo.
        
        Args:
            limite_stock: Límite de stock para considerar como "bajo"
            
        Returns:
            Lista de productos con stock igual o inferior al límite
        """
        try:
            query = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ?"
            resultado = self.db.execute_query(query, (limite_stock,))
            
            productos_stock_bajo = []
            if resultado:
                for fila in resultado:
                    producto = Producto(
                        id=fila[0],
                        nombre=fila[1],
                        descripcion=fila[2],
                        cantidad=fila[3],
                        precio=fila[4],
                        categoria=fila[5]
                    )
                    productos_stock_bajo.append(producto)
            
            return productos_stock_bajo
            
        except Exception as e:
            print(f"Error al generar reporte de stock bajo: {e}")
            return [] 