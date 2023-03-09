from enum import Enum


class DocumentTypes(Enum):
    LEARNING_MATERIAL = "learning_material"
    RESEARCH_PRODUCT = "research_product"


SEARCH_FIELDS = {
    DocumentTypes.LEARNING_MATERIAL: [
        "title^2", "title.analyzed^2", "title.folded^2",
        "text", "text.analyzed", "text.folded",
        "description", "description.analyzed", "description.folded",
        "keywords", "keywords.folded",
        "authors.name.folded",
        "publishers", "publishers.folded",
        "ideas", "ideas.folded"
    ],
    DocumentTypes.RESEARCH_PRODUCT: [
        "title^2", "title.analyzed^2", "title.folded^2",
        "text", "text.analyzed", "text.folded",
        "description", "description.analyzed", "description.folded",
        "keywords", "keywords.folded",
        "authors.name.folded",
        "parties.name.folded",
        "projects.name.folded",
    ]
}


LANGUAGES = ["nl", "en", "unk"]


EDUREP_LEGACY_ID_PREFIXES = {
    "edurep_delen:": "WikiwijsDelen:urn:uuid:"
}
