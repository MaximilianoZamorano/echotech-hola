from persistencia.crear_db import crear_tablas
from presentacion.menu_usuario import menu_privado, solicitar_login

def main():
    try:
        crear_tablas()
    except Exception as error:
        raise SystemExit(f"No fue posible inicializar la base de datos: {error}") from error

    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None
        if opcion == "0":
            return
        print("Sesión cerrada. Ingrese nuevamente.")

if __name__ == "__main__":
    main()

