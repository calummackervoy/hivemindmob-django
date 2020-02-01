from djangoldp.models import Model
from django.db import models


class TagType(object):
    """Categories of tag, what kind of semantic am I marking?"""
    Misc = 'misc'
    Culture = 'culture'
    Theme = 'theme'

    @classmethod
    def choices(cls):
        return (
            (cls.Culture, 'Culture'),
            (cls.Theme, 'Theme'),
            (cls.Theme, 'Misc'),
        )


class ContentTag(Model):
    """tag applied to content to mark it with semantics for content generation"""
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    type = models.CharField(max_length=16, choices=TagType.choices(), default=TagType.Misc)
