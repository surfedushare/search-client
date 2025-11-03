from search_client.constants import Platforms, Entities
from search_client.serializers.products import LearningMaterial, ResearchProduct
from search_client.opensearch.configuration.core import SearchConfiguration


class ProductSearchConfiguration(SearchConfiguration):
    pass


def build_product_search_configuration(platform: Platforms) -> SearchConfiguration:
    filter_fields = {
        "publisher_year_normalized", "authors.name.keyword", "language.keyword", "language", "copyright.keyword",
        "licenses", "publishers.keyword", "technical_type", "technical_types", "publisher_year", "provider"
    }
    if platform in [Platforms.EDUSOURCES, Platforms.MBODATA]:
        serializer = LearningMaterial
        filter_fields |= {
            "study_vocabulary.keyword", "disciplines_normalized.keyword",
            "lom_educational_levels", "consortium.keyword", "material_types", "aggregation_level"
        }
        if platform is Platforms.MBODATA:
            filter_fields |= {"harvest_source", "industries.keyword", "sectors.keyword", "access_rights"}
        search_fields = [
            "texts.nl.titles.text^5", "texts.nl.titles.text.analyzed", "texts.nl.titles.text.folded^5",
            "texts.nl.subtitles.text^5", "texts.nl.subtitles.text.analyzed", "texts.nl.subtitles.text.folded^5",
            "texts.nl.contents.text^3", "texts.nl.contents.text.analyzed", "texts.nl.contents.text.folded^3",
            "texts.nl.descriptions.text^3", "texts.nl.descriptions.text.analyzed", "texts.nl.descriptions.text.folded^3",  # noqa: E501

            "texts.en.titles.text^5", "texts.en.titles.text.analyzed", "texts.en.titles.text.folded^5",
            "texts.en.subtitles.text^5", "texts.en.subtitles.text.analyzed", "texts.en.subtitles.text.folded^5",
            "texts.en.contents.text^3", "texts.en.contents.text.analyzed", "texts.en.contents.text.folded^3",
            "texts.en.descriptions.text^3", "texts.en.descriptions.text.analyzed", "texts.en.descriptions.text.folded^3",  # noqa: E501

            "texts.unk.titles.text^5", "texts.unk.titles.text.analyzed", "texts.unk.titles.text.folded^5",
            "texts.unk.subtitles.text^5", "texts.unk.subtitles.text.analyzed", "texts.unk.subtitles.text.folded^5",
            "texts.unk.contents.text^3", "texts.unk.contents.text.analyzed", "texts.unk.contents.text.folded^3",
            "texts.unk.descriptions.text^3", "texts.unk.descriptions.text.analyzed", "texts.unk.descriptions.text.folded^3",  # noqa: E501

            "keywords^4", "keywords.folded^4",
            "authors.name.folded^2",
            "publishers^2", "publishers.folded^2",

            "consortium.nl^2", "consortium.nl.analyzed^2", "consortium.nl.folded^2",
            "consortium.en^2", "consortium.en.analyzed^2", "consortium.en.folded^2",
            "study_vocabulary.nl^2", "study_vocabulary.nl.analyzed^2", "study_vocabulary.nl.folded^2",
            "study_vocabulary.en^2", "study_vocabulary.en.analyzed^2", "study_vocabulary.en.folded^2",
            "disciplines_normalized.nl^2", "disciplines_normalized.nl.analyzed^2", "disciplines_normalized.nl.folded^2",
            "disciplines_normalized.en^2", "disciplines_normalized.en.analyzed^2", "disciplines_normalized.en.folded^2",
            "industries.nl^2", "industries.nl.analyzed^2", "industries.nl.folded^2",
            "industries.en^2", "industries.en.analyzed^2", "industries.en.folded^2",
            "sectors.nl^2", "sectors.nl.analyzed^2", "sectors.nl.folded^2",
            "sectors.en^2", "sectors.en.analyzed^2", "sectors.en.folded^2",
        ]
    elif platform is Platforms.PUBLINOVA:
        serializer = ResearchProduct
        filter_fields |= {"research_object_type", "research_themes", "has_material"}
        search_fields = [
            "texts.nl.titles.text^2", "texts.nl.titles.text.analyzed^2", "texts.nl.titles.text.folded^2",
            "texts.nl.subtitles.text^2", "texts.nl.subtitles.text.analyzed^2", "texts.nl.subtitles.text.folded^2",
            "texts.nl.contents.text", "texts.nl.contents.text.analyzed", "texts.nl.contents.text.folded",
            "texts.nl.descriptions.text", "texts.nl.descriptions.text.analyzed", "texts.nl.descriptions.text.folded",

            "texts.en.titles.text^2", "texts.en.titles.text.analyzed^2", "texts.en.titles.text.folded^2",
            "texts.en.subtitles.text^2", "texts.en.subtitles.text.analyzed^2", "texts.en.subtitles.text.folded^2",
            "texts.en.contents.text", "texts.en.contents.text.analyzed", "texts.en.contents.text.folded",
            "texts.en.descriptions.text", "texts.en.descriptions.text.analyzed", "texts.en.descriptions.text.folded",

            "texts.unk.titles.text^2", "texts.unk.titles.text.analyzed^2", "texts.unk.titles.text.folded^2",
            "texts.unk.subtitles.text^2", "texts.unk.subtitles.text.analyzed^2", "texts.unk.subtitles.text.folded^2",
            "texts.unk.contents.text", "texts.unk.contents.text.analyzed", "texts.unk.contents.text.folded",
            "texts.unk.descriptions.text", "texts.unk.descriptions.text.analyzed", "texts.unk.descriptions.text.folded",

            "keywords", "keywords.folded",
            "authors.name.folded",
            "parties.name.folded",
            "projects.name.folded",

            "provider.filter_search"
        ]
    else:
        raise ValueError(f"Can't build product search configuration for platform: {platform}")
    return ProductSearchConfiguration(
        platform=platform,
        entities={Entities.PRODUCTS},
        search_fields=search_fields,
        serializers={
            Entities.PRODUCTS: serializer
        },
        filter_fields=filter_fields,
        range_filter_fields={
            "published_at", "modified_at", "metrics.stars.average",
            "publisher_date"  # deprecated, use published_at
        },
        highlights={
            "description": {"texts:description"},
            "text": {"texts:contents"}
        },
        more_like_this_field_references={"texts:titles", "texts:descriptions"},
    )
