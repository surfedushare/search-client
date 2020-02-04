"""
This module contains implementation of models for communities app.
"""
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models as django_models
from django.utils import timezone
from django_enumfield import enum

from surf.apps.core.models import UUIDModel

from surf.apps.materials.models import Collection
from surf.apps.locale.models import Locale, LocaleHTML
from surf.statusenums import PublishStatus


class CommunityDetail(django_models.Model):
    title = django_models.CharField(max_length=255)
    description = django_models.TextField(max_length=16384, null=True, blank=True)
    website_url = django_models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Community(UUIDModel):
    """
    Implementation of Community model. Communities are related to
    SURFconext Teams.
    """
    publish_status = enum.EnumField(PublishStatus, default=PublishStatus.DRAFT)

    name = django_models.CharField(max_length=255, blank=True)
    deleted_at = django_models.DateTimeField(null=True)

    members = django_models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Team',
        blank=True,
    )

    logo = django_models.ImageField(
        upload_to='communities',
        blank=True,
        null=True,
        help_text="The proportion of the image should be 230x136")

    featured_image = django_models.ImageField(
        upload_to='communities',
        blank=True,
        null=True,
        help_text="The proportion of the image should be 388x227")

    website_url = django_models.URLField(blank=True, null=True)

    # list of community collections
    collections = django_models.ManyToManyField(Collection,
                                                blank=True,
                                                related_name="communities")

    # identifier of SURFconext Team
    external_id = django_models.CharField(max_length=255,
                                          verbose_name="SurfConext group id",
                                          null=True, blank=True)

    language_detail = django_models.ManyToManyField(CommunityDetail, verbose_name="Language specific details",
                                                    blank=True, through='CommunityLanguageDetail')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Communities'

    def restore(self):
        self.deleted_at = None
        self.save()

    def delete(self, using=None, keep_parents=False):
        if not self.deleted_at:
            self.deleted_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.name

    def clean(self):
        # Check whether the entered external_id is a valid URN.
        # regex taken from the O'Reilly Regular Expressions Cookbook, 2nd Edition
        # https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s06.html
        if self.external_id:
            regex = r"^urn:[a-z0-9][a-z0-9-]{0,31}:[a-z0-9()+,\-.:=@;$_!*'%/?#]+$"
            if not re.match(regex, self.external_id):
                raise ValidationError("SURFconext group id isn't a valid URN. Check "
                                      "https://en.wikipedia.org/wiki/Uniform_Resource_Name for examples of valid URNs.")


class CommunityLanguageDetail(django_models.Model):
    detail = django_models.ForeignKey(CommunityDetail, on_delete=django_models.CASCADE)
    community = django_models.ForeignKey(Community, on_delete=django_models.CASCADE)
    language_code = django_models.CharField(max_length=2)

    def clean(self):
        # force consistency
        self.language_code = self.language_code.upper()

    class Meta:
        verbose_name = 'Community Detail Translation'
        constraints = [
            django_models.UniqueConstraint(fields=['language_code', 'community'], name='unique materials in collection')
        ]


class Team(django_models.Model):
    community = django_models.ForeignKey(Community, on_delete=django_models.CASCADE)
    user = django_models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=django_models.CASCADE)
    team_id = django_models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Member'

    def clean(self):
        if not self.community.external_id:
            raise ValidationError("Community SURFconext group id isn't set, can't add users to this community.")
        self.team_id = self.community.external_id
