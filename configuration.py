from invoke import Config


def create_configuration(project_location=None) -> Config:
    """
    We're using invoke Config as base for our configuration:
    https://docs.pyinvoke.org/en/stable/concepts/configuration.html#config-hierarchy.

    :return: configuration
    """
    config = Config(lazy=True, project_location=project_location)
    config.load_system()
    config.load_user()
    config.load_project()
    config.load_shell_env()
    config.load_runtime()
    return config
