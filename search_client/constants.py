from enum import Enum


class DocumentTypes(Enum):
    LEARNING_MATERIAL = "learning_material"
    RESEARCH_PRODUCT = "research_product"


SEARCH_FIELDS = {
    DocumentTypes.LEARNING_MATERIAL: [
        "title^5", "title.analyzed", "title.folded^5",
        "text^3", "text.analyzed", "text.folded^3",
        "description^3", "description.analyzed", "description.folded^3",
        "keywords^4", "keywords.folded^4",
        "authors.name.folded^2",
        "publishers^2", "publishers.folded^2",
        "consortium^2", "consortium.folded^2",
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
    "edurep_delen:": "WikiwijsDelen:urn:uuid:",
    "surf:oai:surfsharekit.nl:": "",
    "surfsharekit:oai:surfsharekit.nl:": "",
    "oer_han:oai:surfsharekit.nl:": "",
}
