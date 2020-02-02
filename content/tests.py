from rest_framework.test import APITestCase
from content.models import NameContent, Tag, TagType, ContentTag, select_random_from


class GeneratorTestCase(APITestCase):
    def _generate_and_append_tag(self, name, type=TagType.Misc):
        t = Tag(name=name, type=type)
        t.save()
        self.tags.append(t)

    def _generate_name_content(self, name, tags):
        n = NameContent(name=name)
        n.save()
        for tag in tags:
            ct = ContentTag(content=n, tag=tag)
            ct.save()

    def setUpTags(self):
        self.tags = []
        self._generate_and_append_tag('English', TagType.Culture)
        self._generate_and_append_tag('Welsh', TagType.Culture)
        self._generate_and_append_tag('French', TagType.Culture)

        self._generate_name_content('William', [self.tags[0]])
        self._generate_name_content('Daffyd', [self.tags[1]])
        self._generate_name_content('Guillame', [self.tags[2]])
        self._generate_name_content('Calum', [])

    # select_random_from
    # single choice
    def test_select_random_from_single(self):
        self.setUpTags()

        selection = select_random_from(NameContent.objects.all(), Tag.objects.all())
        self.assertEqual(len(selection), 1)
        self.assertTrue(isinstance(selection[0], NameContent))

    # multiple choice
    def test_select_random_from_multiple(self):
        self.setUpTags()

        selection = select_random_from(NameContent.objects.all(), Tag.objects.all(), choices=2)
        self.assertEqual(len(selection), 2)
        self.assertTrue(isinstance(selection[0], NameContent))

    # superset_only
    def test_select_random_from_superset_only(self):
        self.setUpTags()

        # choose two tags that only one NameContent has
        tags = Tag.objects.filter(name='English')

        english_names = NameContent.objects.filter(tags__tag__name='English')
        self.assertEqual(len(english_names), 1)

        selection = select_random_from(NameContent.objects.all(), tags, superset_only=True)
        self.assertEqual(len(selection), 1)
        self.assertTrue(isinstance(selection[0], NameContent))
        self.assertEqual(selection[0].tags.all()[0].tag.name, 'English')

    # no tags possible
    def test_select_random_from_empty_set(self):
        self.setUpTags()

        t = Tag(name='Scottish', type=TagType.Culture)
        t.save()
        tags = Tag.objects.filter(name=t.name)

        selection = select_random_from(NameContent.objects.all(), tags, superset_only=True)
        self.assertEqual(len(selection), 0)
