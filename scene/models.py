from djangoldp.models import Model
from django.db import models
from content.models import Tag, NameContent


class SceneType(Model):
    """Model defines how the scene behaves and guides how to generate it"""
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, default='')
    rarity = models.PositiveIntegerField(default=1, null=False,
                                         help_text='number of instances in every 1000. Set to 0 to make the scene unique')

    def __str__(self):
        return self.name


class SceneTypeTag(Model):
    scene_type = models.ForeignKey(SceneType, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scene_types')


class Scene(Model):
    """A setting during gameplay"""
    name = models.ForeignKey(NameContent, on_delete=models.SET_NULL, related_name='scenes', null=True)
    type = models.ForeignKey(SceneType, on_delete=models.SET_NULL, related_name='scenes', null=True)

    def __str__(self):
        return self.name


class SceneTag(Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scenes')


class Feature(Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, default='')

    @property
    def can_interact(self):
        return False


class FeatureTag(Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='features')


class SceneFeature(Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='instances')
