MIME_TYPE_TECH_FORMAT = {
    "application/x-yossymemo": "digiboard",
    "application/x-ibooks+zip": "ebook",
    "image/bmp": "image",
    "application/vnd.openxmlformats-officedocument.presentationml.pre": "presentation",
    "application/vnd.openxmlformats-officedocument.presentationml.sli": "presentation",
    "application/vnd.oasis.opendocument.spreadsheet": "spreadsheet",
    "application/postscript": "text",
    "application/vnd.ms-word": "text",
    "application/x-tar": "archive",
    "application/vnd.ms-word.document.macroEnabled.12": "text",
    "application/x-stuffit": "archive",
    "application/x-koan": "audio",
    "application/vnd.koan": "audio",
    "audio/midi": "audio",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template": "text",
    "image/pjpeg": "image",
    "text/rtf": "text",
    "application/Inspire": "digiboard",
    "message/rfc822": "message",
    "video/quicktime": "video",
    "application/x-AS3PE": "digiboard",
    "application/vnd.ms-publisher": "text",
    "application/vnd.google-earth.kmz": "googleearth",
    "image/png": "image",
    "video/x-msvideo": "video",
    "application/ppt": "presentation",
    "application/x-rar-compressed": "archive",
    "application/rtf": "text",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "spreadsheet",
    "video/mpeg": "video",
    "image/x-icon": "image",
    "image/x-ms-bmp": "image",
    "application/x-pdf": "pdf",
    "image/tiff": "image",
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow": "presentation",
    "application/x-java": "app",
    "image/jpg": "image",
    "application/x-Inspire": "digiboard",
    "application/x-smarttech-notebook": "digiboard",
    "application/x-zip-compressed": "digiboard",
    "application/x-ACTIVprimary3": "digiboard",
    "application/vnd.ms-excel": "spreadsheet",
    "text/plain": "text",
    "audio/x-wav": "audio",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "presentation",
    "application/x-mplayer2": "video",
    "image/gif": "image",
    "audio/mpeg": "audio",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "text",
    "video/mp4": "video",
    "application/vnd.ms-powerpoint": "presentation",
    "video/x-ms-wmv": "video",
    "video/x-flv": "video",
    "text/xml": "text",
    "application/msword": "text",
    "application/zip": "archive",
    "video/x-ms-asf": "video",
    "application/pdf": "pdf",
    "text/html": "text",
    "image/jpeg": "image",
    "application/x-Wikiwijs-Arrangement": "wikiwijsarrangement"
}

TECH_FORMAT_MIME_TYPES = dict()
for k, v in MIME_TYPE_TECH_FORMAT.items():
    TECH_FORMAT_MIME_TYPES.setdefault(v, []).append(k)

DISCIPLINE_CUSTOM_THEME = {
    "2adcec22-095d-4937-aed7-48788080460b": "Aarde en milieu",
    "e683a77c-f926-4c00-8e9e-e609cb93fc85": "Onderwijs en Opvoeding",
    "455d527a-bfd0-4460-919e-12e0478a54cf": "Taal en Communicatie",
    "8e080031-93e9-4c07-b4dc-73d5d096a2fe": "Exact en informatica",
    "92161d11-91ce-48e2-b79a-8aa2df8b7022": "Economie en Bedrijf",
    "cba3253b-ca4b-4bd5-bbf5-2cc90d910e57": "Recht en Bestuur",
    "2b363227-8633-4652-ad57-c61f1efc02c8": "Aarde en milieu",
    "652bc6a3-d024-493f-9199-a08340cbb2b3": "Techniek",
    "1f7aa29f-38d8-4dab-91db-3be52669951f": "Taal en Communicatie",
    "94a7654d-c145-4b9c-aab3-7dc478534437": "Techniek",
    "3629ac98-42b8-47db-acb2-e37327042857": "Taal en Communicatie",
    "4df72ecd-3928-4abb-b227-8abd451e4195": "Gedrag en Maatschappij",
    "24850a94-16c6-4b87-8dce-a8b9a6673e5d": "Aarde en milieu",
    "3b12504f-5600-42b7-aaf3-2b9fd011c093": "Gezondheid",
    "7f772375-6e8e-43fe-9b08-d7f3971d8cc9": "Taal en Communicatie",
    "81a1f605-db58-448d-a1dc-da682316c505": "Taal en Communicatie",
    "4ba5583f-b147-42cc-a083-ce5ebfd53746": "Economie en Bedrijf",
    "8cfb914a-ead0-4125-b389-d5d9816afb95": "Techniek",
    "18f53978-1118-4051-a778-b8d7f60ca982": "Taal en Communicatie",
    "d35b903f-1598-4bdd-a2fa-8aba854df762": "Kunst en Cultuur",
    "9f4710e3-f173-404e-b12e-577657a5da04": "Taal en Communicatie",
    "5c98610c-3f7d-4521-b231-d0932b4ca799": "Gezondheid",
    "c001f86a-4f8f-4420-bd78-381c615ecedc": "Aarde en milieu",
    "ef3a0b2e-0843-4e0a-b45b-788be6e1ec8d": "Kunst en Cultuur",
    "596e13b2-5626-4312-8440-50e9bd7b4271": "Taal en Communicatie",
    "3ddfe1f4-c8d8-44c7-92d0-8c3c5d6e51f5": "Onderwijs en Opvoeding",
    "2845473d-ce18-450a-9135-6738abbdc129": "Exact en informatica",
    "aedcfc1c-a676-4f40-8587-4a5f43a354b5": "Taal en Communicatie",
    "8e3e2aab-1e36-4942-b86a-eba155353b23": "Kunst en Cultuur",
    "db5b20c4-4e94-4554-8137-a45acb130ad2": "Aarde en milieu",
    "315566f5-ca2c-4fb2-bf82-263ec13c9b75": "Techniek",
    "788db119-d221-4fc5-8faa-98564a78aff7": "Aarde en milieu",
    "20f264c8-a132-4b43-96dd-c661fd6bace7": "Aarde en milieu",
    "7aa6f577-b02d-484a-90d6-72fc80199f9a": "Kunst en Cultuur",
    "e98be5ad-4bd2-4768-a9eb-7e24026e360c": "Exact en informatica",
    "3401cf6e-82e4-404c-b216-b980ff407159": "Taal en Communicatie",
    "0861c43d-1874-4788-b522-df8be575677f": "Onderwijs en Opvoeding",
    "03d65ce0-2fd7-4f16-91f1-dcdce873dffc": "Recht en Bestuur",
    "86390768-492e-4d9e-8bfe-65648e79522a": "Onderwijs en Opvoeding",
    "b922af97-b3a5-48ac-a01d-32ad5cab5abc": "Recht en Bestuur",
    "dabf3753-248a-495b-b861-bcd36e2b55cb": "Taal en Communicatie",
    "c6c55e80-9fae-440b-b50a-4a1f70432734": "Techniek",
    "10169c87-c77a-4ab7-8c19-c79ba7865bbf": "Gedrag en Maatschappij",
    "4449624e-dfcc-4414-958a-d770a168f637": "Recht en Bestuur",
    "116fbfd6-77d8-4676-8634-8cfd686942c9": "Taal en Communicatie",
    "3aab168a-9b24-4aca-b0f1-4bfb12e7c288": "Exact en informatica",
    "6cfbea61-4877-4518-9b06-9f07146e139d": "Aarde en milieu",
    "e5346879-4051-4ad9-bef8-2078620ef6cf": "Gedrag en Maatschappij",
    "49b28e01-e836-408b-9cf2-2976f85312c7": "Gedrag en Maatschappij",
    "952bf604-cc38-44e3-889a-a9e74a18da8e": "Taal en Communicatie",
    "b3f61346-92c4-4fb5-9207-6a4142b64122": "Taal en Communicatie",
    "b9a2c9ea-48f6-4218-b974-c14e84b00c1a": "Kunst en Cultuur",
    "e605402f-4cc2-46bb-9026-d1d49bde17bf": "Kunst en Cultuur",
    "e6ca634f-c1aa-4d03-9e26-4725a31887f1": "Techniek",
    "9ca10565-ec88-44b7-abc2-582dfdea5abc": "Techniek",
    "4c8a3378-6616-459d-acc4-83ee5a9b91a2": "Kunst en Cultuur",
    "08018424-b218-4de6-b174-df6982e7a72d": "Economie en Bedrijf",
    "693f235a-511f-4f59-9633-6b1abd0e3b6f": "Techniek",
    "7afbb7a6-c29b-425c-9c59-6f79c845f5f0": "Exact en informatica"
}

CUSTOM_THEME_DISCIPLINES = dict()
for k, v in DISCIPLINE_CUSTOM_THEME.items():
    CUSTOM_THEME_DISCIPLINES.setdefault(v, []).append(k)
