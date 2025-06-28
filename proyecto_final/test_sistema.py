#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de prueba para el Sistema de Gestión de Inventario
Demuestra todas las funcionalidades implementadas
"""

from inventario import InventarioManager, Producto
import os

def limpiar_pantalla():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("🧪 SCRIPT DE PRUEBA - SISTEMA DE GESTIÓN DE INVENTARIO")
    print("=" * 60)
    
    # Inicializar el sistema
    inventario = InventarioManager()
    
    print("\n1. 📦 REGISTRANDO PRODUCTOS DE PRUEBA...")
    print("-" * 40)
    
    # Productos de prueba
    productos_prueba = [
        Producto("Laptop Dell Inspiron 15", "Laptop para uso general con 8GB RAM", 5, 750.00, "Electrónicos"),
        Producto("Mouse Logitech MX Master", "Mouse inalámbrico ergonómico", 15, 85.99, "Accesorios"),
        Producto("Teclado Mecánico Corsair", "Teclado gaming RGB con switches azules", 8, 120.50, "Accesorios"),
        Producto("Monitor Samsung 24''", "Monitor Full HD IPS 24 pulgadas", 3, 299.99, "Electrónicos"),
        Producto("Webcam Logitech C920", "Webcam HD 1080p para streaming", 0, 89.99, "Accesorios"),
        Producto("Auriculares Sony WH-1000XM4", "Auriculares inalámbricos con cancelación de ruido", 2, 349.99, "Audio"),
        Producto("Smartphone Samsung Galaxy S21", "Teléfono inteligente Android", 12, 699.99, "Celulares"),
        Producto("Tablet iPad Air", "Tablet Apple con pantalla de 10.9 pulgadas", 6, 599.99, "Electrónicos")
    ]
    
    # Registrar productos
    for producto in productos_prueba:
        if inventario.registrar_producto(producto):
            print(f"✅ Registrado: {producto.nombre}")
        else:
            print(f"❌ Error al registrar: {producto.nombre}")
    
    print(f"\nTotal de productos registrados: {len(productos_prueba)}")
    
    print("\n2. 👁️ VISUALIZANDO TODOS LOS PRODUCTOS...")
    print("-" * 40)
    productos = inventario.obtener_todos_los_productos()
    
    if productos:
        print(f"{'ID':<3} {'NOMBRE':<30} {'CANTIDAD':<8} {'PRECIO':<10} {'CATEGORÍA':<15}")
        print("-" * 75)
        for p in productos:
            print(f"{p.id:<3} {p.nombre[:29]:<30} {p.cantidad:<8} ${p.precio:<9.2f} {p.categoria:<15}")
    
    print("\n3. 🔍 PROBANDO BÚSQUEDAS...")
    print("-" * 40)
    
    # Buscar por ID
    print("🔍 Buscando producto con ID 1:")
    producto = inventario.buscar_producto_por_id(1)
    if producto:
        print(f"   Encontrado: {producto.nombre} - ${producto.precio}")
    
    # Buscar por nombre
    print("\n🔍 Buscando productos con 'Logitech':")
    productos_nombre = inventario.buscar_productos_por_nombre("Logitech")
    for p in productos_nombre:
        print(f"   - {p.nombre} (ID: {p.id})")
    
    # Buscar por categoría
    print("\n🔍 Buscando productos en categoría 'Electrónicos':")
    productos_categoria = inventario.buscar_productos_por_categoria("Electrónicos")
    for p in productos_categoria:
        print(f"   - {p.nombre} (Stock: {p.cantidad})")
    
    print("\n4. ✏️ ACTUALIZANDO PRODUCTO...")
    print("-" * 40)
    
    # Actualizar precio del producto con ID 2
    print("Actualizando precio del Mouse Logitech...")
    if inventario.actualizar_producto(2, precio=79.99):
        producto_actualizado = inventario.buscar_producto_por_id(2)
        print(f"✅ Precio actualizado: ${producto_actualizado.precio}")
    
    # Actualizar stock del producto con ID 4
    print("Actualizando stock del Monitor Samsung...")
    if inventario.actualizar_producto(4, cantidad=10):
        producto_actualizado = inventario.buscar_producto_por_id(4)
        print(f"✅ Stock actualizado: {producto_actualizado.cantidad} unidades")
    
    print("\n5. 📊 GENERANDO REPORTE DE STOCK BAJO...")
    print("-" * 40)
    
    # Reporte con límite de 5 unidades
    limite = 5
    productos_stock_bajo = inventario.generar_reporte_stock_bajo(limite)
    
    print(f"Productos con stock igual o menor a {limite}:")
    if productos_stock_bajo:
        print(f"{'NOMBRE':<30} {'STOCK':<8} {'PRECIO':<10} {'VALOR':<10}")
        print("-" * 65)
        valor_total = 0
        for p in productos_stock_bajo:
            valor = p.cantidad * p.precio
            valor_total += valor
            print(f"{p.nombre[:29]:<30} {p.cantidad:<8} ${p.precio:<9.2f} ${valor:<9.2f}")
        
        print(f"\n📈 Resumen del reporte:")
        print(f"   • Productos afectados: {len(productos_stock_bajo)}")
        print(f"   • Valor total afectado: ${valor_total:.2f}")
        
        # Identificar productos sin stock
        sin_stock = [p for p in productos_stock_bajo if p.cantidad == 0]
        if sin_stock:
            print(f"   ⚠️ Productos SIN STOCK: {len(sin_stock)}")
            for p in sin_stock:
                print(f"      - {p.nombre}")
    else:
        print("✅ ¡Excelente! No hay productos con stock bajo.")
    
    print("\n6. 📈 ESTADÍSTICAS GENERALES...")
    print("-" * 40)
    
    todos_productos = inventario.obtener_todos_los_productos()
    if todos_productos:
        total_productos = len(todos_productos)
        stock_total = sum(p.cantidad for p in todos_productos)
        valor_inventario = sum(p.cantidad * p.precio for p in todos_productos)
        productos_sin_stock = len([p for p in todos_productos if p.cantidad == 0])
        
        # Contar por categorías
        categorias = {}
        for p in todos_productos:
            cat = p.categoria or "Sin categoría"
            categorias[cat] = categorias.get(cat, 0) + 1
        
        print(f"📊 Estadísticas del Inventario:")
        print(f"   • Total de productos: {total_productos}")
        print(f"   • Stock total: {stock_total} unidades")
        print(f"   • Valor del inventario: ${valor_inventario:,.2f}")
        print(f"   • Productos sin stock: {productos_sin_stock}")
        print(f"   • Categorías registradas: {len(categorias)}")
        
        print(f"\n📋 Distribución por categorías:")
        for categoria, cantidad in categorias.items():
            print(f"   - {categoria}: {cantidad} producto(s)")
    
    print("\n7. 🗑️ ELIMINANDO PRODUCTO DE PRUEBA...")
    print("-" * 40)
    
    # Eliminar el último producto agregado
    ultimo_producto = max(todos_productos, key=lambda x: x.id)
    print(f"Eliminando: {ultimo_producto.nombre} (ID: {ultimo_producto.id})")
    
    if inventario.eliminar_producto(ultimo_producto.id):
        print("✅ Producto eliminado exitosamente")
        
        # Verificar que se eliminó
        productos_actualizados = inventario.obtener_todos_los_productos()
        print(f"📊 Productos restantes: {len(productos_actualizados)}")
    
    print("\n" + "=" * 60)
    print("🎉 PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    
    print("\n💡 PRÓXIMOS PASOS:")
    print("1. Ejecutar la interfaz de consola: python main.py")
    print("2. Ejecutar la interfaz web: streamlit run app_streamlit.py")
    print("3. Ejecutar la API: python api.py")
    print("4. Ver documentación de la API: http://localhost:8000/docs")
    
    print("\n🎯 El sistema está listo para usar!")

if __name__ == "__main__":
    main() 