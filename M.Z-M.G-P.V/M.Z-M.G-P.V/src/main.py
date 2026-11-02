from persistencia.crear_db import crear_tablas
from presentacion.menu_usuario import menu_privado, solicitar_login

def main():
    try:
        crear_tablas()
    except Exception as error:
        raise SystemExit(f"No fue posible inicializar la base de datos: {error}") from error

    while True:
        print("\n===== INICIO ECOTECH =====")
        print("1. Iniciar sesión")
        print("0. Cerrar programa")
        accion = input("Seleccione una opción: ").strip()
        if accion == "0":
            print("Cerrando programa. ¡Hasta luego!")
            return
        if accion != "1":
            print("Opción no válida.")
            continue

        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para volver al inicio: ").strip() == "0":
                continue
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None
        if opcion == "0":
            print("Sesión cerrada. Ingrese nuevamente.")
            continue
        if opcion == "9":
            return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    main()
