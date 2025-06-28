#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Gestión de Inventario
Aplicación de consola para gestionar productos en una base de datos SQLite.
"""

import os
import sys
from typing import Optional

try:
    from colorama import Fore, Back, Style, init
    # Inicializar colorama para Windows
    init(autoreset=True)
    COLORAMA_DISPONIBLE = True
except ImportError:
    COLORAMA_DISPONIBLE = False
    # Si colorama no está disponible, definir colores vacíos
    class MockColor:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    
    class MockStyle:
        BRIGHT = RESET_ALL = ""
    
    Fore = Back = MockColor()
    Style = MockStyle()

from inventario import InventarioManager, Producto

class InterfazConsola:
    """
    Clase para manejar la interfaz de usuario en consola.
    """
    
    def __init__(self):
        """Inicializa la interfaz de consola."""
        self.inventario = InventarioManager()
        self.titulo = "SISTEMA DE GESTIÓN DE INVENTARIO"
    
    def limpiar_pantalla(self) -> None:
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_titulo(self) -> None:
        """Muestra el título principal de la aplicación."""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("=" * 60)
        print(f"{self.titulo:^60}")
        print("=" * 60)
        print(f"{Style.RESET_ALL}")
    
    def mostrar_menu_principal(self) -> None:
        """Muestra el menú principal de opciones."""
        print(f"\n{Fore.WHITE}{Style.BRIGHT}MENÚ PRINCIPAL{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}┌────────────────────────────────────────────────┐")
        print(f"│  1. Registrar nuevo producto                   │")
        print(f"│  2. Visualizar todos los productos             │")
        print(f"│  3. Buscar producto                            │")
        print(f"│  4. Actualizar producto                        │")
        print(f"│  5. Eliminar producto                          │")
        print(f"│  6. Generar reporte de stock bajo             │")
        print(f"│  7. Salir                                      │")
        print(f"└────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    def obtener_opcion(self) -> int:
        """
        Obtiene y valida la opción seleccionada por el usuario.
        
        Returns:
            Opción válida seleccionada por el usuario
        """
        while True:
            try:
                opcion = input(f"\n{Fore.GREEN}Seleccione una opción (1-7): {Style.RESET_ALL}")
                opcion_num = int(opcion)
                if 1 <= opcion_num <= 7:
                    return opcion_num
                else:
                    print(f"{Fore.RED}Error: Ingrese un número entre 1 y 7.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Error: Ingrese un número válido.{Style.RESET_ALL}")
    
    def registrar_producto(self) -> None:
        """Interfaz para registrar un nuevo producto."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}REGISTRAR NUEVO PRODUCTO{Style.RESET_ALL}")
        print("-" * 40)
        
        try:
            nombre = input(f"{Fore.WHITE}Nombre del producto: {Style.RESET_ALL}").strip()
            if not nombre:
                print(f"{Fore.RED}Error: El nombre no puede estar vacío.{Style.RESET_ALL}")
                return
            
            descripcion = input(f"{Fore.WHITE}Descripción: {Style.RESET_ALL}").strip()
            
            while True:
                try:
                    cantidad = int(input(f"{Fore.WHITE}Cantidad: {Style.RESET_ALL}"))
                    if cantidad < 0:
                        print(f"{Fore.RED}Error: La cantidad no puede ser negativa.{Style.RESET_ALL}")
                        continue
                    break
                except ValueError:
                    print(f"{Fore.RED}Error: Ingrese un número válido para la cantidad.{Style.RESET_ALL}")
            
            while True:
                try:
                    precio = float(input(f"{Fore.WHITE}Precio: ${Style.RESET_ALL}"))
                    if precio <= 0:
                        print(f"{Fore.RED}Error: El precio debe ser mayor a 0.{Style.RESET_ALL}")
                        continue
                    break
                except ValueError:
                    print(f"{Fore.RED}Error: Ingrese un precio válido.{Style.RESET_ALL}")
            
            categoria = input(f"{Fore.WHITE}Categoría: {Style.RESET_ALL}").strip()
            
            # Crear y registrar el producto
            producto = Producto(nombre, descripcion, cantidad, precio, categoria)
            if self.inventario.registrar_producto(producto):
                print(f"{Fore.GREEN}¡Producto registrado exitosamente!{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
    
    def visualizar_productos(self) -> None:
        """Interfaz para visualizar todos los productos."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}LISTA DE PRODUCTOS{Style.RESET_ALL}")
        print("-" * 40)
        
        productos = self.inventario.obtener_todos_los_productos()
        
        if not productos:
            print(f"{Fore.YELLOW}No hay productos registrados en el inventario.{Style.RESET_ALL}")
            return
        
        # Mostrar encabezados
        print(f"{Fore.WHITE}{Style.BRIGHT}")
        print(f"{'ID':<5} {'NOMBRE':<20} {'DESCRIPCIÓN':<25} {'CANT':<6} {'PRECIO':<10} {'CATEGORÍA':<15}")
        print("-" * 90)
        print(f"{Style.RESET_ALL}")
        
        # Mostrar productos
        for producto in productos:
            descripcion_corta = producto.descripcion[:22] + "..." if len(producto.descripcion) > 25 else producto.descripcion
            print(f"{Fore.CYAN}{producto.id:<5} {Fore.WHITE}{producto.nombre:<20} "
                  f"{producto.descripcion[:22]:<25} {Fore.YELLOW}{producto.cantidad:<6} "
                  f"{Fore.GREEN}${producto.precio:<9.2f} {Fore.MAGENTA}{producto.categoria:<15}{Style.RESET_ALL}")
        
        print(f"\n{Fore.BLUE}Total de productos: {len(productos)}{Style.RESET_ALL}")
    
    def buscar_producto(self) -> None:
        """Interfaz para buscar productos."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}BUSCAR PRODUCTO{Style.RESET_ALL}")
        print("-" * 40)
        
        print(f"{Fore.WHITE}Opciones de búsqueda:")
        print(f"1. Buscar por ID")
        print(f"2. Buscar por nombre")
        print(f"3. Buscar por categoría{Style.RESET_ALL}")
        
        while True:
            try:
                opcion = int(input(f"\n{Fore.GREEN}Seleccione tipo de búsqueda (1-3): {Style.RESET_ALL}"))
                if 1 <= opcion <= 3:
                    break
                else:
                    print(f"{Fore.RED}Error: Seleccione una opción válida (1-3).{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Error: Ingrese un número válido.{Style.RESET_ALL}")
        
        if opcion == 1:
            self._buscar_por_id()
        elif opcion == 2:
            self._buscar_por_nombre()
        elif opcion == 3:
            self._buscar_por_categoria()
    
    def _buscar_por_id(self) -> None:
        """Busca un producto por ID."""
        try:
            id_producto = int(input(f"{Fore.WHITE}Ingrese el ID del producto: {Style.RESET_ALL}"))
            producto = self.inventario.buscar_producto_por_id(id_producto)
            
            if producto:
                self._mostrar_producto_detallado(producto)
            else:
                print(f"{Fore.RED}No se encontró producto con ID {id_producto}.{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un ID válido.{Style.RESET_ALL}")
    
    def _buscar_por_nombre(self) -> None:
        """Busca productos por nombre."""
        nombre = input(f"{Fore.WHITE}Ingrese el nombre del producto: {Style.RESET_ALL}").strip()
        if not nombre:
            print(f"{Fore.RED}Error: El nombre no puede estar vacío.{Style.RESET_ALL}")
            return
        
        productos = self.inventario.buscar_productos_por_nombre(nombre)
        
        if productos:
            print(f"\n{Fore.GREEN}Se encontraron {len(productos)} producto(s):{Style.RESET_ALL}")
            self._mostrar_lista_productos(productos)
        else:
            print(f"{Fore.RED}No se encontraron productos con nombre '{nombre}'.{Style.RESET_ALL}")
    
    def _buscar_por_categoria(self) -> None:
        """Busca productos por categoría."""
        categoria = input(f"{Fore.WHITE}Ingrese la categoría: {Style.RESET_ALL}").strip()
        if not categoria:
            print(f"{Fore.RED}Error: La categoría no puede estar vacía.{Style.RESET_ALL}")
            return
        
        productos = self.inventario.buscar_productos_por_categoria(categoria)
        
        if productos:
            print(f"\n{Fore.GREEN}Se encontraron {len(productos)} producto(s) en la categoría '{categoria}':{Style.RESET_ALL}")
            self._mostrar_lista_productos(productos)
        else:
            print(f"{Fore.RED}No se encontraron productos en la categoría '{categoria}'.{Style.RESET_ALL}")
    
    def _mostrar_producto_detallado(self, producto: Producto) -> None:
        """Muestra los detalles completos de un producto."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}DETALLES DEL PRODUCTO{Style.RESET_ALL}")
        print("-" * 40)
        print(f"{Fore.WHITE}ID:          {Fore.CYAN}{producto.id}")
        print(f"{Fore.WHITE}Nombre:      {Fore.YELLOW}{producto.nombre}")
        print(f"{Fore.WHITE}Descripción: {Fore.WHITE}{producto.descripcion}")
        print(f"{Fore.WHITE}Cantidad:    {Fore.MAGENTA}{producto.cantidad}")
        print(f"{Fore.WHITE}Precio:      {Fore.GREEN}${producto.precio:.2f}")
        print(f"{Fore.WHITE}Categoría:   {Fore.BLUE}{producto.categoria}{Style.RESET_ALL}")
    
    def _mostrar_lista_productos(self, productos: list) -> None:
        """Muestra una lista resumida de productos."""
        print(f"{Fore.WHITE}{Style.BRIGHT}")
        print(f"{'ID':<5} {'NOMBRE':<20} {'CANTIDAD':<10} {'PRECIO':<10} {'CATEGORÍA':<15}")
        print("-" * 65)
        print(f"{Style.RESET_ALL}")
        
        for producto in productos:
            print(f"{Fore.CYAN}{producto.id:<5} {Fore.WHITE}{producto.nombre:<20} "
                  f"{Fore.YELLOW}{producto.cantidad:<10} {Fore.GREEN}${producto.precio:<9.2f} "
                  f"{Fore.MAGENTA}{producto.categoria:<15}{Style.RESET_ALL}")
    
    def actualizar_producto(self) -> None:
        """Interfaz para actualizar un producto existente."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}ACTUALIZAR PRODUCTO{Style.RESET_ALL}")
        print("-" * 40)
        
        try:
            id_producto = int(input(f"{Fore.WHITE}Ingrese el ID del producto a actualizar: {Style.RESET_ALL}"))
            
            # Verificar si el producto existe
            producto_existente = self.inventario.buscar_producto_por_id(id_producto)
            if not producto_existente:
                print(f"{Fore.RED}No se encontró producto con ID {id_producto}.{Style.RESET_ALL}")
                return
            
            # Mostrar datos actuales
            print(f"\n{Fore.YELLOW}Datos actuales del producto:{Style.RESET_ALL}")
            self._mostrar_producto_detallado(producto_existente)
            
            print(f"\n{Fore.WHITE}Ingrese los nuevos valores (presione Enter para mantener el valor actual):{Style.RESET_ALL}")
            
            # Obtener nuevos valores
            nombre = input(f"Nuevo nombre [{producto_existente.nombre}]: ").strip()
            nombre = nombre if nombre else None
            
            descripcion = input(f"Nueva descripción [{producto_existente.descripcion}]: ").strip()
            descripcion = descripcion if descripcion else None
            
            cantidad_str = input(f"Nueva cantidad [{producto_existente.cantidad}]: ").strip()
            cantidad = None
            if cantidad_str:
                try:
                    cantidad = int(cantidad_str)
                    if cantidad < 0:
                        print(f"{Fore.RED}Error: La cantidad no puede ser negativa.{Style.RESET_ALL}")
                        return
                except ValueError:
                    print(f"{Fore.RED}Error: Ingrese un número válido para la cantidad.{Style.RESET_ALL}")
                    return
            
            precio_str = input(f"Nuevo precio [{producto_existente.precio}]: ").strip()
            precio = None
            if precio_str:
                try:
                    precio = float(precio_str)
                    if precio <= 0:
                        print(f"{Fore.RED}Error: El precio debe ser mayor a 0.{Style.RESET_ALL}")
                        return
                except ValueError:
                    print(f"{Fore.RED}Error: Ingrese un precio válido.{Style.RESET_ALL}")
                    return
            
            categoria = input(f"Nueva categoría [{producto_existente.categoria}]: ").strip()
            categoria = categoria if categoria else None
            
            # Actualizar producto
            if self.inventario.actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
                print(f"{Fore.GREEN}¡Producto actualizado exitosamente!{Style.RESET_ALL}")
            
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un ID válido.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
    
    def eliminar_producto(self) -> None:
        """Interfaz para eliminar un producto."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}ELIMINAR PRODUCTO{Style.RESET_ALL}")
        print("-" * 40)
        
        try:
            id_producto = int(input(f"{Fore.WHITE}Ingrese el ID del producto a eliminar: {Style.RESET_ALL}"))
            
            # Verificar si el producto existe y mostrarlo
            producto_existente = self.inventario.buscar_producto_por_id(id_producto)
            if not producto_existente:
                print(f"{Fore.RED}No se encontró producto con ID {id_producto}.{Style.RESET_ALL}")
                return
            
            # Mostrar detalles del producto a eliminar
            print(f"\n{Fore.YELLOW}Producto a eliminar:{Style.RESET_ALL}")
            self._mostrar_producto_detallado(producto_existente)
            
            # Confirmar eliminación
            confirmacion = input(f"\n{Fore.RED}¿Está seguro que desea eliminar este producto? (s/N): {Style.RESET_ALL}")
            
            if confirmacion.lower() in ['s', 'si', 'sí']:
                if self.inventario.eliminar_producto(id_producto):
                    print(f"{Fore.GREEN}¡Producto eliminado exitosamente!{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Eliminación cancelada.{Style.RESET_ALL}")
            
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un ID válido.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
    
    def generar_reporte_stock_bajo(self) -> None:
        """Interfaz para generar reporte de productos con stock bajo."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}REPORTE DE STOCK BAJO{Style.RESET_ALL}")
        print("-" * 40)
        
        try:
            limite = int(input(f"{Fore.WHITE}Ingrese el límite de stock: {Style.RESET_ALL}"))
            
            if limite < 0:
                print(f"{Fore.RED}Error: El límite no puede ser negativo.{Style.RESET_ALL}")
                return
            
            productos_stock_bajo = self.inventario.generar_reporte_stock_bajo(limite)
            
            if productos_stock_bajo:
                print(f"\n{Fore.RED}{Style.BRIGHT}PRODUCTOS CON STOCK IGUAL O INFERIOR A {limite}:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{Style.BRIGHT}")
                print(f"{'ID':<5} {'NOMBRE':<20} {'CANTIDAD':<10} {'PRECIO':<10} {'CATEGORÍA':<15}")
                print("-" * 65)
                print(f"{Style.RESET_ALL}")
                
                total_valor = 0
                for producto in productos_stock_bajo:
                    valor_stock = producto.cantidad * producto.precio
                    total_valor += valor_stock
                    
                    # Colorear según nivel crítico
                    if producto.cantidad == 0:
                        color_cantidad = Fore.RED + Style.BRIGHT
                    elif producto.cantidad <= limite // 2:
                        color_cantidad = Fore.RED
                    else:
                        color_cantidad = Fore.YELLOW
                    
                    print(f"{Fore.CYAN}{producto.id:<5} {Fore.WHITE}{producto.nombre:<20} "
                          f"{color_cantidad}{producto.cantidad:<10} {Fore.GREEN}${producto.precio:<9.2f} "
                          f"{Fore.MAGENTA}{producto.categoria:<15}{Style.RESET_ALL}")
                
                print(f"\n{Fore.WHITE}Resumen del reporte:")
                print(f"- Productos con stock bajo: {Fore.RED}{len(productos_stock_bajo)}")
                print(f"{Fore.WHITE}- Valor total del stock bajo: {Fore.GREEN}${total_valor:.2f}{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.GREEN}¡Excelente! No hay productos con stock igual o inferior a {limite}.{Style.RESET_ALL}")
                
        except ValueError:
            print(f"{Fore.RED}Error: Ingrese un número válido.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operación cancelada.{Style.RESET_ALL}")
    
    def pausar(self) -> None:
        """Pausa la ejecución esperando una tecla."""
        input(f"\n{Fore.CYAN}Presione Enter para continuar...{Style.RESET_ALL}")
    
    def ejecutar(self) -> None:
        """Ejecuta el bucle principal de la aplicación."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                self.mostrar_menu_principal()
                
                opcion = self.obtener_opcion()
                
                if opcion == 1:
                    self.registrar_producto()
                elif opcion == 2:
                    self.visualizar_productos()
                elif opcion == 3:
                    self.buscar_producto()
                elif opcion == 4:
                    self.actualizar_producto()
                elif opcion == 5:
                    self.eliminar_producto()
                elif opcion == 6:
                    self.generar_reporte_stock_bajo()
                elif opcion == 7:
                    print(f"\n{Fore.CYAN}¡Gracias por usar el Sistema de Gestión de Inventario!{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}¡Hasta luego!{Style.RESET_ALL}")
                    break
                
                if opcion != 7:
                    self.pausar()
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Salida forzada. ¡Hasta luego!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}Error inesperado: {e}{Style.RESET_ALL}")
                self.pausar()

def main():
    """Función principal de la aplicación."""
    print(f"{Fore.CYAN}Iniciando Sistema de Gestión de Inventario...{Style.RESET_ALL}")
    
    # Verificar si colorama está disponible
    if not COLORAMA_DISPONIBLE:
        print("Nota: Para una mejor experiencia visual, instale colorama: pip install colorama")
    
    try:
        interfaz = InterfazConsola()
        interfaz.ejecutar()
    except Exception as e:
        print(f"Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 