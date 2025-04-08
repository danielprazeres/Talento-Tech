# Solicita los datos del cliente
apellido = input("Ingrese su apellido: ")
nombre = input("Ingrese su nombre: ")
correo = input("Ingrese su correo electrónico: ")
edad = int(input("Ingrese su edad: "))

# Determinar el rango etario
if edad < 18:
    rango_etario = "Menor de edad"
elif edad < 30:
    rango_etario = "Joven adulto"
elif edad < 60:
    rango_etario = "Adulto"
else:
    rango_etario = "Adulto mayor"

# Registrar los ingresos mensuales
mes = 1
total_ingresos = 0

while mes <= 6:
    try:
        ingreso = float(input(f"Ingrese el ingreso del mes {mes}: "))

        if ingreso < 0:
            print("El valor no es válido. Debe ser un número positivo.")
            continue  # Vuelve a pedir el ingreso del mismo mes

        total_ingresos += ingreso
        mes += 1

    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número.")

# Mostrar los resultados
print("\n==============================")
print("      RESUMEN DEL CLIENTE")
print("==============================")
print(f"Apellido: {apellido}")
print(f"Nombre: {nombre}")
print(f"Correo electrónico: {correo}")
print(f"Rango etario: {rango_etario}")
print("------------------------------")
print(f"Total acumulado en 6 meses: ${total_ingresos:.2f}")
print("==============================")