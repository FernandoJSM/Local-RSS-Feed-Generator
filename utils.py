import os


def get_data_filepath(filename):
    """
        Retorna o caminho de um arquivo na pasta "data" do projeto
    Args:
        filename (str): Nome do arquivo
    Returns:
        data_path (str): Caminho da pasta "data" do projeto
    """
    package_folder = os.path.dirname(__file__)
    data_path = os.path.join(package_folder, "data", filename)

    return data_path
