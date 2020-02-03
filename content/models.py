from enum import Enum
from django.utils.decorators import classonlymethod
from djangoldp.models import Model
from django.db import models
import random


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


class Tag(Model):
    """tag applied to content to mark it with semantics for content generation"""
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    type = models.CharField(max_length=16, choices=TagType.choices(), default=TagType.Misc)

    def __str__(self):
        return self.name + " (" + self.type + ")"


def list_intersection(list_a, list_b):
    """returns the intersection of two lists"""
    return list(set(list_a) & set(list_b))


def select_random_from(items, tags=None, choices=1, superset_only=False):
    """
    takes a set of items and selects random item which has the correct tags
    @:param items: QuerySet of values to select from
    @:param tags: QuerySet of tags to use in selection. None indicates all Tags should match
    @:param choices: the number of values to select. Note that there may be no values matching
            query, or less than the desired selection
    @:param superset_only: if True, only items which have _all_ of the target tags will be selected
            if False, items which have > 0 matching tags will be selected

    @:return a list containing a random selection according to passed parameters
    """
    if tags is None:
        superset_only = False

    if items is None or len(items) < 1:
        raise ValueError("received empty items set")
    if not hasattr(items[0], 'tags'):
        raise ValueError("received items which do not have tags")

    # build a set of values containing one or more of the target tags
    if tags is not None:
        values = set(v for v in items if len(set(v.tags.all().values_list('tag')) & set(tags.values_list('pk'))) > 0)

        if superset_only:
            values = set(v for v in values if len(set(v.tags.all().values_list('tag')) - set(tags.values_list('pk'))) == 0)
    else:
        values = items

    # ensuring selection possible
    if len(values) == 0:
        return list()
    if len(values) < choices:
        choices = len(values)

    # convert to list to allow indexing (necessary for getting random sample)
    values = list(values)

    if choices > 1:
        return random.sample(values, choices)
    return [random.choice(values)]


# models for different kinds of content
class ContentType(Enum):
    NAME = 'name'


class Content(models.Model):
    @property
    def content_type(self):
        raise NotImplementedError('This is an abstract class!')

    @classonlymethod
    def generate_content_random(self, tags=None, choices=1, superset_only=False):
        """
        Selects random value(s) for the content type
        @:param items: QuerySet of values to select from
        @:param tags: QuerySet of tags to use in selection. None indicates all tags should be used
        @:param choices: the number of values to select. Note that there may be no values matching
                query, or less than the desired selection
        @:param superset_only: if True, only items which have _all_ of the target tags will be selected
                if False, items which have > 0 matching tags will be selected

        @:return a list containing a random selection according to passed parameters
        """
        raise NotImplementedError('This is an abstract class!')


class NameContent(Content):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    @property
    def content_type(self):
        return ContentType.NAME

    @classonlymethod
    def generate_content_random(self, tags=None, choices=1, superset_only=False):
        return select_random_from(NameContent.objects.all(), tags, choices, superset_only)

    def __str__(self):
        return self.name


class ContentTag(Model):
    """A many to many between Tags and Content"""
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='content')

    def __str__(self):
        return str(self.content) + " - " + self.tag.name
