import yaml


def load_config():
    """
    Load the entire configuration from the config.yaml file.

    :return: The configuration as a dictionary.
    """
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


def load_credential():
    """
    Load a specific credential from the config.yaml file.

    :param key: The key of the credential to load.
    :return: The value of the specified credential.
    """
    config = load_config()
    return config["discord"]["bot_token"]
