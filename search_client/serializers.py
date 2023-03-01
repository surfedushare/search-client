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

    external_id = serializers.CharField()
    doi = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    url = serializers.URLField()
    title = serializers.CharField()
    description = serializers.CharField()
    language = serializers.CharField()
    copyright = serializers.CharField()
    video = serializers.DictField()
    harvest_source = serializers.CharField()


class LearningMaterialResultSerializer(BaseSearchResultSerializer):

    files = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )
    published_at = serializers.CharField(source="publisher_date", allow_blank=True, allow_null=True)
    lom_educational_levels = serializers.ListField(child=serializers.DictField())
    studies = serializers.ListField(child=serializers.DictField())
    disciplines = serializers.ListField(child=serializers.CharField(), default=[],
                                        source="learning_material_disciplines_normalized")
    ideas = serializers.ListField(child=serializers.CharField())
    technical_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    keywords = serializers.ListField(child=serializers.CharField())
    publishers = serializers.ListField(child=serializers.CharField())
    authors = serializers.ListField(child=serializers.CharField())
    has_parts = serializers.ListField(child=serializers.CharField())
    is_part_of = serializers.ListField(child=serializers.CharField())
    consortium = serializers.CharField(allow_blank=True, allow_null=True)

    previews = serializers.DictField(default=None)

    view_count = serializers.IntegerField()
    applaud_count = serializers.IntegerField()
    avg_star_rating = serializers.IntegerField()
    count_star_rating = serializers.IntegerField()


class RelationSerializer(serializers.Serializer):

    authors = PersonSerializer(many=True)
    keywords = LabelSerializer(many=True)
    parties = OrganisationSerializer(many=True)
    themes = LabelSerializer(many=True)
    projects = ProjectSerializer(many=True)
    children = serializers.ListField(child=serializers.CharField())
    parents = serializers.ListField(child=serializers.CharField())


class ResearchProductResultSerializer(BaseSearchResultSerializer):

    type = serializers.CharField(source="technical_type")
    published_at = serializers.CharField(source="publisher_date", allow_blank=True, allow_null=True)
    research_object_type = serializers.CharField()
    extension = serializers.DictField()
    relations = RelationSerializer()
