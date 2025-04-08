# Tu tarea es la siguiente:

# Crear una lista con los nombres de los y las clientes que vamos a procesar. Algunos nombres pueden estar en blanco, y debemos detectarlo.

# Recorrer la lista y mostrar el nombre de cada cliente o clienta, junto con su posición en la lista (por ejemplo, Cliente 1, Cliente 2, etc.). 

# Si encuentras a alguien cuyo nombre sea una cadena en blanco, mostrar un mensaje de alerta indicando que ese dato no es válido. 

# Para los nombres válidos, convertir cada uno a formato adecuado usando .capitalize(), de modo que siempre tengan la primera letra en mayúscula y el resto en minúscula.

nombres = []
nombres.append("Juan")
nombres.append("Maria")
nombres.append(" ")
nombres.append("pedro")
nombres.append("Ana")
nombres.append("maria")
nombres.append(" ")

# Recorrer la lista de nombres
for i, nombre in enumerate(nombres):
    if nombre.strip() == "":
        print(f"Cliente {i + 1}: Nombre no válido")
    else:
        nombre_formateado = nombre.strip().capitalize()
        print(f"Cliente {i + 1}: {nombre_formateado}")

