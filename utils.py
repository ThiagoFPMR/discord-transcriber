import yaml

def load_credential(key):
    """
    Load a specific credential from the credentials.yaml file.
    
    :param key: The key of the credential to load.
    :return: The value of the specified credential.
    """
    with open("credentials.yaml", "r") as file:
        credentials = yaml.safe_load(file)
    return credentials.get(key, None)