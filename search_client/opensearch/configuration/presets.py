from copy import deepcopy

from search_client.constants import Platforms, Entities
from search_client.opensearch.configuration import (
    SearchConfiguration,
    build_multilingual_indices_search_configuration,
    build_product_search_configuration,
    ProjectSearchConfiguration,
)
from search_client.serializers import Project


_EDUSOURCES_PRESETS = {
    "products:multilingual-indices": build_multilingual_indices_search_configuration(Platforms.EDUSOURCES),
    "products:default": build_product_search_configuration(Platforms.EDUSOURCES),
}


_PUBLINOVA_PRESETS = {
    "products:multilingual-indices": build_multilingual_indices_search_configuration(Platforms.PUBLINOVA),
    "products:default": build_product_search_configuration(Platforms.PUBLINOVA),
    "projects:default": ProjectSearchConfiguration(
        platform=Platforms.PUBLINOVA,
        entities={Entities.PROJECTS},
        search_fields=["title", "description"],
        serializers={
            Entities.PROJECTS: Project
        }
    )
}


_PRESETS = {
    Platforms.EDUSOURCES: _EDUSOURCES_PRESETS,
    Platforms.PUBLINOVA: _PUBLINOVA_PRESETS
}


def build_presets_search_configuration(platform: Platforms, presets: list[str], default: str) -> SearchConfiguration:
    platform_presets = _PRESETS[platform]
    presets = iter(presets) if presets else iter([default])
    main_preset_key = next(presets)
    configuration = deepcopy(platform_presets[main_preset_key])
    for preset_key in presets:
        preset_configuration = platform_presets[preset_key]
        if not preset_configuration.allow_multi_entity_results:
            return preset_configuration
        configuration.merge(preset_configuration)
    return configuration


def is_valid_preset_search_configuration(platform: Platforms, preset: str) -> str:
    if ":" not in preset:
        preset += ":default"
    platform_presets = _PRESETS[platform]
    if preset not in platform_presets:
        raise ValueError(f"Preset {preset} is not available for {platform.value}.")
    return preset


def get_preset_search_configuration(platform: Platforms, preset: str) -> SearchConfiguration:
    platform_presets = _PRESETS[platform]
    preset = is_valid_preset_search_configuration(platform, preset)
    return deepcopy(platform_presets[preset])
