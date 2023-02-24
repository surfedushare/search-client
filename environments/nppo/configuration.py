REPOSITORY = "870512711545.dkr.ecr.eu-central-1.amazonaws.com"
REPOSITORY_AWS_PROFILE = "nppo-prod"
FARGATE_CLUSTER_NAME = "nppo"
SEARCH_FIELDS = [
    "title^2", "title.analyzed^2", "title.folded^2",
    "text", "text.analyzed", "text.folded",
    "description", "description.analyzed", "description.folded",
    "keywords", "keywords.folded",
    "authors.name.folded",
    "parties.name.folded",
    "projects.name.folded",
]
