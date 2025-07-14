import yaml

def load_config():
    """
    Load the entire configuration from the config.yaml file.

    :return: The configuration as a dictionary.
    """
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config