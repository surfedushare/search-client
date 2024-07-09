from dateutil.parser import parse as parse_datetime

from rest_framework import serializers


class PersonSerializer(serializers.Serializer):

    name = serializers.CharField()
    email = serializers.CharField(required=False, allow_null=True)


class OrganisationSerializer(serializers.Serializer):

    name = serializers.CharField()


class ProjectSerializer(serializers.Serializer):

    name = serializers.CharField()


class LabelSerializer(serializers.Serializer):

    label = serializers.CharField()


class BaseSearchResultSerializer(serializers.Serializer):

    srn = serializers.CharField(default=None)
    set = serializers.CharField(default=None)
    external_id = serializers.CharField()
    published_at = serializers.CharField(source="publisher_date", allow_blank=True, allow_null=True)
    modified_at = serializers.SerializerMethodField()
    url = serializers.URLField()
    title = serializers.CharField()
    description = serializers.CharField()
    language = serializers.CharField()
    copyright = serializers.CharField()
    video = serializers.DictField(default=None)
    harvest_source = serializers.CharField()
    previews = serializers.DictField(default=None)
    files = serializers.ListField(child=serializers.DictField())
    authors = serializers.ListField(child=serializers.DictField())
    has_parts = serializers.ListField(child=serializers.CharField())
    is_part_of = serializers.ListField(child=serializers.CharField())
    keywords = serializers.ListField(child=serializers.CharField())

    def get_modified_at(self, obj):
        modified_at = obj.get("modified_at")
        if not modified_at:
            return
        date = parse_datetime(modified_at)
        if not date:
            return
        return date.strftime("%Y-%m-%d")


class SimpleLearningMaterialResultSerializer(BaseSearchResultSerializer):

    score = serializers.FloatField(default=1.0)
    provider = serializers.DictField(default=None, allow_null=True)
    doi = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lom_educational_levels = serializers.ListField(child=serializers.CharField())
    studies = serializers.ListField(child=serializers.CharField())
    disciplines = serializers.ListField(child=serializers.CharField(), default=[],
                                        source="learning_material_disciplines_normalized")
    ideas = serializers.ListField(child=serializers.CharField(), default=[])
    study_vocabulary = serializers.ListField(child=serializers.CharField(), default=[])
    technical_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    material_types = serializers.ListField(child=serializers.CharField(), default=[])
    aggregation_level = serializers.CharField(allow_blank=True, allow_null=True)
    publishers = serializers.ListField(child=serializers.CharField())
    consortium = serializers.CharField(allow_blank=True, allow_null=True)
    subtitle = serializers.CharField(allow_blank=True, allow_null=True)


class LearningMaterialResultSerializer(SimpleLearningMaterialResultSerializer):

    authors = serializers.ListField(child=serializers.CharField())
    lom_educational_levels = serializers.ListField(child=serializers.DictField())
    studies = serializers.ListField(child=serializers.DictField())
    view_count = serializers.IntegerField()
    applaud_count = serializers.IntegerField()
    avg_star_rating = serializers.IntegerField()
    count_star_rating = serializers.IntegerField()


class ResearchProductResultSerializer(BaseSearchResultSerializer):

    provider = serializers.SerializerMethodField()
    doi = serializers.SerializerMethodField()
    type = serializers.CharField(source="technical_type")
    research_object_type = serializers.CharField()
    parties = serializers.ListField(child=serializers.CharField(), source="publishers")
    research_themes = serializers.ListField(child=serializers.CharField())
    projects = serializers.ListField(child=serializers.CharField(), default=[])
    owners = serializers.SerializerMethodField(method_name="list_first_author")
    contacts = serializers.SerializerMethodField(method_name="list_first_author")
    subtitle = serializers.SerializerMethodField()

    def get_provider(self, obj):
        provider = obj["provider"]
        if provider["name"]:
            return provider["name"]
        elif provider["slug"]:
            return provider["slug"]
        elif provider["ror"]:
            return provider["ror"]
        elif provider["external_id"]:
            return provider["external_id"]

    def get_doi(self, obj):
        doi = obj.get("doi", None)
        if not doi:
            return
        return "https://doi.org/" + doi

    def list_first_author(self, obj):
        authors = obj.get("authors", None)
        if not authors:
            return []
        return [authors[0]]

    def get_subtitle(self, obj):
        subtitle = obj.get("subtitle")
        if not subtitle:
            return
        title = obj.get("title", "")
        return subtitle if subtitle not in title else None
