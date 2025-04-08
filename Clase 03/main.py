# Solicite al cliente su nombre, apellido, edad y correo electrónico.

# Compruebe que el nombre, el apellido y el correo no estén en blanco, y que la edad sea mayor de 18 años.

# Muestre los datos por la terminal, en el orden que se ingresaron. Si alguno de los datos ingresados no cumple los requisitos, sólo mostrar el texto “ERROR!”.

# Solicitar datos al cliente
nombre = input("Cuál es tu nombre?")
apellido = input("Cuál es tu apellido?")
edad = int(input("Cuál es tu edad?"))
correo = input("Cuál es tu correo?")

# Comprobar que los datos no estén en blanco y que la edad sea mayor de 18 años
if nombre and apellido and correo and edad > 18:
    print("\n====================================")
    print("      TARJETA DE PRESENTACIÓN")
    print("======================================")
    print(f"Nombre: {nombre} {apellido}")
    print(f"Edad: {edad} años")
    print(f"Correo electrónico: {correo}")
    print("==============================")
else:
    print("ERROR!") 