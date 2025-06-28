from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from inventario import InventarioManager, Producto

# Crear instancia de FastAPI
app = FastAPI(
    title="API Sistema de Inventario",
    description="API REST para gestionar productos en el inventario",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar manejador de inventario
inventario = InventarioManager()

# Modelos Pydantic
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""
    cantidad: int
    precio: float
    categoria: Optional[str] = ""

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None

class ProductoResponse(ProductoBase):
    id: int
    
    class Config:
        from_attributes = True

# Endpoints
@app.get("/", summary="Página de inicio")
async def root():
    return {
        "mensaje": "API Sistema de Gestión de Inventario",
        "version": "1.0.0",
        "documentacion": "/docs"
    }

@app.post("/productos/", response_model=ProductoResponse, summary="Registrar nuevo producto")
async def crear_producto(producto: ProductoCreate):
    """Registra un nuevo producto en el inventario"""
    try:
        nuevo_producto = Producto(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            cantidad=producto.cantidad,
            precio=producto.precio,
            categoria=producto.categoria
        )
        
        if inventario.registrar_producto(nuevo_producto):
            # Obtener el producto recién creado para devolver con ID
            productos = inventario.obtener_todos_los_productos()
            producto_creado = max(productos, key=lambda x: x.id)
            return producto_creado.to_dict()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al registrar el producto"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

@app.get("/productos/", response_model=List[ProductoResponse], summary="Obtener todos los productos")
async def obtener_productos():
    """Obtiene la lista completa de productos"""
    try:
        productos = inventario.obtener_todos_los_productos()
        return [producto.to_dict() for producto in productos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}"
        )

@app.get("/productos/{producto_id}", response_model=ProductoResponse, summary="Buscar producto por ID")
async def obtener_producto(producto_id: int):
    """Busca un producto específico por su ID"""
    try:
        producto = inventario.buscar_producto_por_id(producto_id)
        if producto:
            return producto.to_dict()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar producto: {str(e)}"
        )

@app.get("/productos/buscar/nombre/{nombre}", response_model=List[ProductoResponse], summary="Buscar por nombre")
async def buscar_por_nombre(nombre: str):
    """Busca productos por nombre (búsqueda parcial)"""
    try:
        productos = inventario.buscar_productos_por_nombre(nombre)
        return [producto.to_dict() for producto in productos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar productos: {str(e)}"
        )

@app.get("/productos/categoria/{categoria}", response_model=List[ProductoResponse], summary="Buscar por categoría")
async def buscar_por_categoria(categoria: str):
    """Busca productos por categoría"""
    try:
        productos = inventario.buscar_productos_por_categoria(categoria)
        return [producto.to_dict() for producto in productos]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar productos: {str(e)}"
        )

@app.put("/productos/{producto_id}", response_model=ProductoResponse, summary="Actualizar producto")
async def actualizar_producto(producto_id: int, producto_update: ProductoUpdate):
    """Actualiza los datos de un producto existente"""
    try:
        # Verificar si el producto existe
        producto_existente = inventario.buscar_producto_por_id(producto_id)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        
        # Actualizar solo los campos proporcionados
        success = inventario.actualizar_producto(
            producto_id,
            nombre=producto_update.nombre,
            descripcion=producto_update.descripcion,
            cantidad=producto_update.cantidad,
            precio=producto_update.precio,
            categoria=producto_update.categoria
        )
        
        if success:
            # Devolver el producto actualizado
            producto_actualizado = inventario.buscar_producto_por_id(producto_id)
            return producto_actualizado.to_dict()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al actualizar el producto"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}"
        )

@app.delete("/productos/{producto_id}", summary="Eliminar producto")
async def eliminar_producto(producto_id: int):
    """Elimina un producto del inventario"""
    try:
        success = inventario.eliminar_producto(producto_id)
        if success:
            return {"mensaje": f"Producto {producto_id} eliminado exitosamente"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}"
        )

@app.get("/reportes/stock-bajo/{limite}", response_model=List[ProductoResponse], summary="Reporte stock bajo")
async def reporte_stock_bajo(limite: int):
    """Genera reporte de productos con stock igual o inferior al límite"""
    try:
        if limite < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El límite de stock no puede ser negativo"
            )
        
        productos = inventario.generar_reporte_stock_bajo(limite)
        return [producto.to_dict() for producto in productos]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar reporte: {str(e)}"
        )

@app.get("/estadisticas", summary="Estadísticas del inventario")
async def obtener_estadisticas():
    """Obtiene estadísticas generales del inventario"""
    try:
        productos = inventario.obtener_todos_los_productos()
        
        if not productos:
            return {
                "total_productos": 0,
                "stock_total": 0,
                "valor_inventario": 0.0,
                "productos_sin_stock": 0,
                "categorias": []
            }
        
        total_productos = len(productos)
        stock_total = sum(p.cantidad for p in productos)
        valor_inventario = sum(p.cantidad * p.precio for p in productos)
        productos_sin_stock = len([p for p in productos if p.cantidad == 0])
        
        # Contar productos por categoría
        categorias = {}
        for producto in productos:
            cat = producto.categoria or "Sin categoría"
            categorias[cat] = categorias.get(cat, 0) + 1
        
        return {
            "total_productos": total_productos,
            "stock_total": stock_total,
            "valor_inventario": round(valor_inventario, 2),
            "productos_sin_stock": productos_sin_stock,
            "categorias": categorias
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 