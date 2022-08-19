from alkemy_data_builder.builder import init_db, load_data
import argparse


def arguments():
    """Esta funcion toma los argumentos de la linea de comandos al correr el main.py

    Returns:
        string: con el argumento
    """
    parser = argparse.ArgumentParser(description="toma los argumentos para la consulta")
    parser.add_argument(
        "-s",
        "--scripts",
        type=str,
        default="load_data",
        help="debe ingresar como argumento el script a ejecutar: init_db, load_data, ambos",
    )
    args = parser.parse_args()
    script_type = args.scripts
    return script_type


if __name__ == "__main__":

    script_type = arguments()

    if script_type == "ambos":
        init_db()
        load_data()
    elif script_type == "init_db":
        init_db()
    else:
        load_data()
