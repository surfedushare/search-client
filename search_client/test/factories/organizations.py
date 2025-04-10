ORGANIZATIONS = {
    "research": {
        "srn": "sharekit:nppo:b843a11b-0194-4f29-8c69-e753552b4d7f",
        "set": "sharekit:nppo",
        "provider": "sharekit",
        "external_id": "b843a11b-0194-4f29-8c69-e753552b4d7f",
        "name": "Nieuw samenwerkingsaanvraag 2",
        "description": "Het vervolg op Nieuw Samenwerkingsaanvraag",
        "members": [],
        "parents": [],
        "ror": None,
        "secretary": None,
        "state": "active",
        "type": "consortium"
    }
}


def generate_organization(person_type="research"):
    copy = ORGANIZATIONS[person_type].copy()
    return copy
