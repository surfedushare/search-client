# Tox tries to generate metadata from this __init__.py in the egg_info phase before dependencies become available.
# Therefore imports inside this file may not rely on dependencies.
# To keep backward compatability with versions that expect these imports while also allowing Tox to generate metadata,
# these imports have been wrapped in an unfortunately broad try-except clause.
try:
    from search_client.opensearch.client import SearchClient
    from search_client.constants import DocumentTypes
except ImportError:
    pass
