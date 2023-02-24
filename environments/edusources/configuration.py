REPOSITORY = "017973353230.dkr.ecr.eu-central-1.amazonaws.com"
REPOSITORY_AWS_PROFILE = "pol-prod"
FARGATE_CLUSTER_NAME = "surfpol"
SEARCH_FIELDS = [
    "title^10", "title.analyzed^10", "title.folded^10",
    "text", "text.analyzed", "text.folded",
    "description", "description.analyzed", "description.folded",
    "keywords", "keywords.folded",
    "authors.name.folded",
    "publishers", "publishers.folded",
    "ideas", "ideas.folded"
]
