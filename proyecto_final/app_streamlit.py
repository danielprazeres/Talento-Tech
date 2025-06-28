import streamlit as st
import pandas as pd
from inventario import InventarioManager, Producto
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Inventario",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el manejador de inventario
@st.cache_resource
def get_inventario_manager():
    return InventarioManager()

inventario = get_inventario_manager()

# Título principal
st.title("📦 Sistema de Gestión de Inventario")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("📋 Navegación")
pagina = st.sidebar.selectbox(
    "Seleccione una opción:",
    ["🏠 Inicio", "➕ Registrar Producto", "👁️ Ver Productos", 
     "🔍 Buscar Producto", "✏️ Actualizar Producto", 
     "🗑️ Eliminar Producto", "📊 Reportes"]
)

# Función para obtener todos los productos como DataFrame
def get_productos_df():
    productos = inventario.obtener_todos_los_productos()
    if productos:
        data = []
        for p in productos:
            data.append({
                'ID': p.id,
                'Nombre': p.nombre,
                'Descripción': p.descripcion,
                'Cantidad': p.cantidad,
                'Precio': p.precio,
                'Categoría': p.categoria,
                'Valor Total': p.cantidad * p.precio
            })
        return pd.DataFrame(data)
    return pd.DataFrame()

# Página de Inicio
if pagina == "🏠 Inicio":
    st.header("Bienvenido al Sistema de Inventario")
    
    # Métricas generales
    productos = inventario.obtener_todos_los_productos()
    
    if productos:
        col1, col2, col3, col4 = st.columns(4)
        
        total_productos = len(productos)
        total_stock = sum(p.cantidad for p in productos)
        valor_inventario = sum(p.cantidad * p.precio for p in productos)
        productos_sin_stock = len([p for p in productos if p.cantidad == 0])
        
        with col1:
            st.metric("Total Productos", total_productos)
        with col2:
            st.metric("Stock Total", total_stock)
        with col3:
            st.metric("Valor Inventario", f"${valor_inventario:,.2f}")
        with col4:
            st.metric("Sin Stock", productos_sin_stock)
        
        # Gráficos de resumen
        df = get_productos_df()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Productos por Categoría")
            if not df.empty:
                categoria_counts = df['Categoría'].value_counts()
                fig_pie = px.pie(values=categoria_counts.values, 
                               names=categoria_counts.index,
                               title="Distribución por Categorías")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("📈 Top 10 Productos por Valor")
            if not df.empty:
                top_productos = df.nlargest(10, 'Valor Total')
                fig_bar = px.bar(top_productos, 
                               x='Nombre', y='Valor Total',
                               title="Productos con Mayor Valor en Stock")
                fig_bar.update_layout(xaxis={'tickangle': 45})
                st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No hay productos registrados en el inventario. ¡Comience agregando algunos productos!")

# Página Registrar Producto
elif pagina == "➕ Registrar Producto":
    st.header("Registrar Nuevo Producto")
    
    with st.form("registro_producto"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del Producto*", placeholder="Ej: Laptop Dell")
            cantidad = st.number_input("Cantidad*", min_value=0, step=1)
            categoria = st.text_input("Categoría", placeholder="Ej: Electrónicos")
        
        with col2:
            descripcion = st.text_area("Descripción", placeholder="Descripción detallada del producto")
            precio = st.number_input("Precio*", min_value=0.01, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button("🚀 Registrar Producto", type="primary")
        
        if submitted:
            if not nombre:
                st.error("El nombre del producto es obligatorio")
            elif precio <= 0:
                st.error("El precio debe ser mayor a 0")
            else:
                producto = Producto(nombre, descripcion, cantidad, precio, categoria)
                if inventario.registrar_producto(producto):
                    st.success(f"¡Producto '{nombre}' registrado exitosamente!")
                    # Limpiar el cache para refrescar los datos
                    st.cache_resource.clear()
                    st.rerun()
                else:
                    st.error("Error al registrar el producto")

# Página Ver Productos
elif pagina == "👁️ Ver Productos":
    st.header("Lista de Productos")
    
    df = get_productos_df()
    
    if not df.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            categorias = ["Todas"] + list(df['Categoría'].unique())
            categoria_filtro = st.selectbox("Filtrar por Categoría", categorias)
        
        with col2:
            stock_minimo = st.number_input("Stock Mínimo", min_value=0, value=0)
        
        with col3:
            ordenar_por = st.selectbox("Ordenar por", 
                                     ["Nombre", "Cantidad", "Precio", "Valor Total"])
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if categoria_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_filtro]
        
        if stock_minimo > 0:
            df_filtrado = df_filtrado[df_filtrado['Cantidad'] >= stock_minimo]
        
        # Ordenar
        df_filtrado = df_filtrado.sort_values(ordenar_por)
        
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            column_config={
                "Precio": st.column_config.NumberColumn(
                    "Precio",
                    format="$%.2f"
                ),
                "Valor Total": st.column_config.NumberColumn(
                    "Valor Total",
                    format="$%.2f"
                )
            }
        )
        
        st.info(f"Mostrando {len(df_filtrado)} de {len(df)} productos")
    else:
        st.warning("No hay productos registrados")

# Página Buscar Producto
elif pagina == "🔍 Buscar Producto":
    st.header("Buscar Producto")
    
    tipo_busqueda = st.radio(
        "Tipo de búsqueda:",
        ["Por ID", "Por Nombre", "Por Categoría"]
    )
    
    if tipo_busqueda == "Por ID":
        id_buscar = st.number_input("ID del Producto", min_value=1, step=1)
        if st.button("🔍 Buscar", type="primary"):
            producto = inventario.buscar_producto_por_id(id_buscar)
            if producto:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {producto.id}")
                    st.write(f"**Nombre:** {producto.nombre}")
                    st.write(f"**Cantidad:** {producto.cantidad}")
                with col2:
                    st.write(f"**Precio:** ${producto.precio:.2f}")
                    st.write(f"**Categoría:** {producto.categoria}")
                    st.write(f"**Valor Total:** ${producto.cantidad * producto.precio:.2f}")
                st.write(f"**Descripción:** {producto.descripcion}")
            else:
                st.error(f"No se encontró producto con ID {id_buscar}")
    
    elif tipo_busqueda == "Por Nombre":
        nombre_buscar = st.text_input("Nombre del Producto")
        if st.button("🔍 Buscar", type="primary") and nombre_buscar:
            productos = inventario.buscar_productos_por_nombre(nombre_buscar)
            if productos:
                st.success(f"Se encontraron {len(productos)} producto(s)")
                data = []
                for p in productos:
                    data.append({
                        'ID': p.id, 'Nombre': p.nombre, 'Descripción': p.descripcion,
                        'Cantidad': p.cantidad, 'Precio': p.precio, 'Categoría': p.categoria
                    })
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.error(f"No se encontraron productos con nombre '{nombre_buscar}'")
    
    elif tipo_busqueda == "Por Categoría":
        categoria_buscar = st.text_input("Categoría")
        if st.button("🔍 Buscar", type="primary") and categoria_buscar:
            productos = inventario.buscar_productos_por_categoria(categoria_buscar)
            if productos:
                st.success(f"Se encontraron {len(productos)} producto(s)")
                data = []
                for p in productos:
                    data.append({
                        'ID': p.id, 'Nombre': p.nombre, 'Descripción': p.descripcion,
                        'Cantidad': p.cantidad, 'Precio': p.precio, 'Categoría': p.categoria
                    })
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.error(f"No se encontraron productos en la categoría '{categoria_buscar}'")

# Página Actualizar Producto
elif pagina == "✏️ Actualizar Producto":
    st.header("Actualizar Producto")
    
    id_actualizar = st.number_input("ID del Producto a Actualizar", min_value=1, step=1)
    
    if st.button("🔍 Buscar Producto"):
        producto = inventario.buscar_producto_por_id(id_actualizar)
        if producto:
            st.session_state['producto_actualizar'] = producto
        else:
            st.error(f"No se encontró producto con ID {id_actualizar}")
    
    if 'producto_actualizar' in st.session_state:
        producto = st.session_state['producto_actualizar']
        
        st.info(f"Actualizando: {producto.nombre}")
        
        with st.form("actualizar_producto"):
            col1, col2 = st.columns(2)
            
            with col1:
                nuevo_nombre = st.text_input("Nombre", value=producto.nombre)
                nueva_cantidad = st.number_input("Cantidad", value=producto.cantidad, min_value=0, step=1)
                nueva_categoria = st.text_input("Categoría", value=producto.categoria)
            
            with col2:
                nueva_descripcion = st.text_area("Descripción", value=producto.descripcion)
                nuevo_precio = st.number_input("Precio", value=producto.precio, min_value=0.01, step=0.01, format="%.2f")
            
            submitted = st.form_submit_button("✏️ Actualizar Producto", type="primary")
            
            if submitted:
                if inventario.actualizar_producto(
                    id_actualizar, nuevo_nombre, nueva_descripcion, 
                    nueva_cantidad, nuevo_precio, nueva_categoria
                ):
                    st.success("¡Producto actualizado exitosamente!")
                    del st.session_state['producto_actualizar']
                    st.cache_resource.clear()
                    st.rerun()
                else:
                    st.error("Error al actualizar el producto")

# Página Eliminar Producto
elif pagina == "🗑️ Eliminar Producto":
    st.header("Eliminar Producto")
    
    id_eliminar = st.number_input("ID del Producto a Eliminar", min_value=1, step=1)
    
    if st.button("🔍 Buscar Producto"):
        producto = inventario.buscar_producto_por_id(id_eliminar)
        if producto:
            st.session_state['producto_eliminar'] = producto
        else:
            st.error(f"No se encontró producto con ID {id_eliminar}")
    
    if 'producto_eliminar' in st.session_state:
        producto = st.session_state['producto_eliminar']
        
        st.warning("⚠️ Producto a eliminar:")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**ID:** {producto.id}")
            st.write(f"**Nombre:** {producto.nombre}")
            st.write(f"**Cantidad:** {producto.cantidad}")
        with col2:
            st.write(f"**Precio:** ${producto.precio:.2f}")
            st.write(f"**Categoría:** {producto.categoria}")
            st.write(f"**Descripción:** {producto.descripcion}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Confirmar Eliminación", type="primary"):
                if inventario.eliminar_producto(id_eliminar):
                    st.success("¡Producto eliminado exitosamente!")
                    del st.session_state['producto_eliminar']
                    st.cache_resource.clear()
                    st.rerun()
                else:
                    st.error("Error al eliminar el producto")
        
        with col2:
            if st.button("❌ Cancelar"):
                del st.session_state['producto_eliminar']
                st.rerun()

# Página Reportes
elif pagina == "📊 Reportes":
    st.header("Reportes de Inventario")
    
    # Reporte de Stock Bajo
    st.subheader("📉 Reporte de Stock Bajo")
    limite_stock = st.number_input("Límite de Stock", min_value=0, value=5, step=1)
    
    if st.button("📊 Generar Reporte", type="primary"):
        productos_stock_bajo = inventario.generar_reporte_stock_bajo(limite_stock)
        
        if productos_stock_bajo:
            st.error(f"⚠️ {len(productos_stock_bajo)} producto(s) con stock igual o inferior a {limite_stock}")
            
            data = []
            total_valor = 0
            for p in productos_stock_bajo:
                valor = p.cantidad * p.precio
                total_valor += valor
                data.append({
                    'ID': p.id,
                    'Nombre': p.nombre,
                    'Cantidad': p.cantidad,
                    'Precio': p.precio,
                    'Valor': valor,
                    'Categoría': p.categoria
                })
            
            df_stock_bajo = pd.DataFrame(data)
            st.dataframe(
                df_stock_bajo,
                use_container_width=True,
                column_config={
                    "Precio": st.column_config.NumberColumn("Precio", format="$%.2f"),
                    "Valor": st.column_config.NumberColumn("Valor", format="$%.2f")
                }
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Productos Afectados", len(productos_stock_bajo))
            with col2:
                st.metric("Valor Total Afectado", f"${total_valor:.2f}")
            
            # Gráfico de productos con stock bajo
            fig = px.bar(df_stock_bajo, x='Nombre', y='Cantidad',
                        title=f"Productos con Stock ≤ {limite_stock}",
                        color='Cantidad',
                        color_continuous_scale='Reds')
            fig.update_layout(xaxis={'tickangle': 45})
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.success(f"✅ ¡Excelente! No hay productos con stock igual o inferior a {limite_stock}")

# Footer
st.markdown("---")
st.markdown("Sistema de Gestión de Inventario - Proyecto Final Talento Tech") 