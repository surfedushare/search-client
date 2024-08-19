PERSONS = {
    "brian": {
        "name": "Brian May",
        "email": "brian@queen.com",
        "external_id": "person:1"
    }
}


PROJECTS = {
    "math": {
        "srn": "edurep:project:1",
        "external_id": "project:1",
        "title": "Een wiskundig project",
        "status": "finished",
        "started_at": "1970-01-01",
        "ended_at": "2020-01-01",
        "coordinates": [],
        "goal": "Mission accomplished",
        "description": "Dit is de beschrijving van een project met wiskundig onderzoek",
        "contacts": [PERSONS["brian"]],
        "owners": [PERSONS["brian"]],
        "persons": [PERSONS["brian"]],
        "keywords": ["nerds"],
        "parties": ["Wikiwijs Maken"],
        "products": [
            "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        ],
        "research_themes": [],
        "suggest_phrase": "Een wiskundig project",
        "suggest_completion": ["Een", "wiskundig", "project"],
    }
}


def generate_project(topic="math", title=None, description=None, external_id=None):
    copy = PROJECTS[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
    return copy
