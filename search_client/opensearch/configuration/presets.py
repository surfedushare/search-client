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
        filter_fields={"project_status"},
        search_fields=["title", "description", "keywords", "keywords.folded", "goal"],
        distance_feature_field=None,
        serializers={
            Entities.PROJECTS: Project
        }
    )
}


_MBODATA_PRESETS = {
    "products:multilingual-indices": build_product_search_configuration(Platforms.MBODATA),
    "products:default": build_product_search_configuration(Platforms.MBODATA),
}


_PRESETS = {
    Platforms.EDUSOURCES: _EDUSOURCES_PRESETS,
    Platforms.PUBLINOVA: _PUBLINOVA_PRESETS,
    Platforms.MBODATA: _MBODATA_PRESETS
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


def get_all_preset_keys() -> list[str]:
    entities = set()
    presets = set()
    for platform_presets in _PRESETS.values():
        for preset in platform_presets:
            entity, subtype = preset.split(":")
            entities.add(entity)
            presets.add(preset)
    all_preset_keys = list(entities) + list(presets)
    all_preset_keys.sort()
    return all_preset_keys


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
