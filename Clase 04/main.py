# Formatee correctamente los textos ingresados en “apellido” y “nombre”, convirtiendo la primera letra de cada palabra a mayúsculas y el resto en minúsculas.

# Asegurarse que el correo electrónico no tenga espacios y contenga solo una “@”.

# Que clasifique por rango etario basándose en su edad (“Niño/a” para los menores de 15 años, “Adolescente” de 15 a 18 y “Adulto/a” para los mayores de 18 años.)

nombre = input("Ingrese su nombre: ")
apellido = input("Ingrese su apellido: ")
correo = input("Ingrese su correo electrónico: ")
edad = int(input("Ingrese su edad: "))

# Formatear nombre y apellido
nombre = nombre.strip().title()
apellido = apellido.strip().title()

# Validar correo electrónico
if "@" not in correo or " " in correo:
    print("El correo electrónico no es válido.")
else:
    # Clasificar por rango etario
    if edad < 15:
        rango_etario = "Niño/a"
    elif 15 <= edad <= 18:
        rango_etario = "Adolescente"
    else:
        rango_etario = "Adulto/a"

    # Mostrar resultados
    print(f"Nombre: {nombre}")
    print(f"Apellido: {apellido}")
    print(f"Correo electrónico: {correo}")
    print(f"Edad: {edad}")
    print(f"Rango etario: {rango_etario}")