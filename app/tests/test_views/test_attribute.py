import json
from unittest import mock
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TransactionTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from app.models import Attribute
from app.models.attribute import AttributeOption
from app.models.course import Course
from app.views.attribute import AttributeViewSet
from rest_framework.parsers import JSONParser
from django.core.exceptions import FieldError

# Create your tests here.


class TestAttribute(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.course = Course.objects.create(name="test")

    def tearDown(self):
        Attribute.objects.all().delete()
        AttributeOption.objects.all().delete()
        Course.objects.all().delete()

    def test_save_attribute_without_options(self):
        data = {
            "name": "name",
            "question": "question",
            "value_type": "String",
            "max_selections": 1,
            "team_set_template": None,
            "course": self.course.pk,
        }

        with self.assertRaises(FieldError) as context:
            AttributeViewSet.save_attribute(AttributeViewSet, get_post_request(data))

        self.assertTrue("Options field is required" in str(context.exception))

    def test_save_attribute_with_non_existent_id_raises_404(self):
        data = {
            "id": 100,
            "name": "name",
            "question": "question",
            "value_type": "String",
            "max_selections": 1,
            "team_set_template": None,
            "course": self.course.pk,
        }

        with self.assertRaises(Http404) as context:
            AttributeViewSet.save_attribute(AttributeViewSet, get_post_request(data))

        self.assertTrue("No Attribute matches the given query" in str(context.exception))

    def test_save_attribute_without_id_creates_new_attribute(self):
        data = {
            "name": "name",
            "question": "question",
            "value_type": "String",
            "max_selections": 1,
            "team_set_template": None,
            "course": self.course.pk,
            "options": [],
        }

        attribute = AttributeViewSet.save_attribute(
            AttributeViewSet, get_post_request(data)
        )

        self.assertEqual(Attribute.objects.count(), 1)

        attribute = get_object_or_404(Attribute, pk=attribute.data.get("id"))
        self.assertEqual(attribute.name, "name")
        self.assertEqual(attribute.question, "question")
        self.assertEqual(attribute.value_type, "String")
        self.assertEqual(attribute.max_selections, 1)
        self.assertEqual(attribute.team_set_template, None)
        self.assertEqual(attribute.course.pk, self.course.pk)
        self.assertEqual(attribute.options.count(), 0)

    def test_save_attribute_with_id_updates_old_attribute(self):
        attribute = Attribute.objects.create(
            name="name1",
            question="question1",
            value_type="String",
            max_selections=1,
            team_set_template=None,
            course=self.course,
        )

        data = {
            "id": attribute.pk,
            "name": "name2",
            "question": "question2",
            "value_type": "Number",
            "max_selections": 2,
            "team_set_template": None,
            "course": self.course.pk,
            "options": [],
        }

        updated_attribute = AttributeViewSet.save_attribute(
            AttributeViewSet, get_post_request(data)
        )

        self.assertEqual(Attribute.objects.count(), 1)

        updated_attribute = get_object_or_404(
            Attribute, pk=updated_attribute.data["id"]
        )
        self.assertEqual(updated_attribute.name, "name2")
        self.assertEqual(updated_attribute.question, "question2")
        self.assertEqual(updated_attribute.value_type, "Number")
        self.assertEqual(updated_attribute.max_selections, 2)
        self.assertEqual(updated_attribute.team_set_template, None)
        self.assertEqual(updated_attribute.course.pk, self.course.pk)
        self.assertEqual(updated_attribute.options.count(), 0)

    @mock.patch("app.models.attribute.Attribute.clear_student_responses")
    def test_save_attribute_with_id_and_different_value_type_clears_attribute_responses(
        self, mock_clear_student_responses
    ):
        attribute = Attribute.objects.create(
            name="name1",
            question="question1",
            value_type="String",
            max_selections=1,
            team_set_template=None,
            course=self.course,
        )

        data = {
            "id": attribute.pk,
            "name": "name1",
            "question": "question1",
            "value_type": "Number",
            "max_selections": 1,
            "team_set_template": None,
            "course": self.course.pk,
            "options": [],
        }

        AttributeViewSet.save_attribute(AttributeViewSet, get_post_request(data))

        mock_clear_student_responses.assert_called_once()

    def test_save_attribute_options_without_id_creates_new_attribute_option(self):
        attribute = Attribute.objects.create(
            name="test",
            question="test",
            value_type="String",
            max_selections=1,
            team_set_template=None,
            course=self.course,
        )

        options = [
            {"value": "value1", "label": "label1"},
            {"value": "value2", "label": "label2"},
        ]

        for option in options:
            AttributeViewSet.save_attribute_option(AttributeViewSet, option, attribute.pk)

        self.assertEqual(AttributeOption.objects.count(), 2)

        attribute_options = AttributeOption.objects.all()
        self.assertEqual(attribute_options[0].value, "value1")
        self.assertEqual(attribute_options[0].label, "label1")
        self.assertEqual(attribute_options[0].attribute.pk, attribute.pk)
        self.assertEqual(attribute_options[1].value, "value2")
        self.assertEqual(attribute_options[1].label, "label2")
        self.assertEqual(attribute_options[1].attribute.pk, attribute.pk)

    def test_save_attribute_options_with_id_updates_old_attribute_option(self):
        attribute = Attribute.objects.create(
            name="test",
            question="test",
            value_type="String",
            max_selections=1,
            team_set_template=None,
            course=self.course,
        )
        attribute_option = AttributeOption.objects.create(
            attribute=attribute, label="label1", value="value1"
        )

        option = {
            "id": attribute_option.pk,
            "value": "value2",
            "label": "label2",
        }

        AttributeViewSet.save_attribute_option(AttributeViewSet, option, attribute.pk)

        self.assertEqual(AttributeOption.objects.count(), 1)

        updated_attribute_option = get_object_or_404(
            AttributeOption, pk=attribute_option.pk
        )
        self.assertEqual(updated_attribute_option.value, "value2")
        self.assertEqual(updated_attribute_option.label, "label2")
        self.assertEqual(updated_attribute_option.attribute.pk, attribute.pk)


    def test_save_attribute_options_with_non_existent_id_raises_404(self):
        attribute = Attribute.objects.create(
            name="test",
            question="test",
            value_type="String",
            max_selections=1,
            team_set_template=None,
            course=self.course,
        )

        option = {
            "id": 100,
            "value": "value2",
            "label": "label2",
        }

        with self.assertRaises(Http404) as context:
            AttributeViewSet.save_attribute_option(AttributeViewSet, option, attribute.pk)

        self.assertTrue("No AttributeOption matches the given query" in str(context.exception))

def get_post_request(data):
    factory = APIRequestFactory()
    factory_request = factory.post(
        "/api/v1/attributes/save_attribute/",
        content_type="application/json",
        data=json.dumps(data),
    )
    request = Request(factory_request, parsers=[JSONParser()])
    return request
