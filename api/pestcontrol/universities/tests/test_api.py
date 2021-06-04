import json
import pytest
import logging
from unittest import TestCase
from django.test import Client
from django.urls import reverse
from api.pestcontrol.universities.models import University

logger = logging.getLogger("UNI_LOGS")


@pytest.mark.django_db
class BasicUniversityAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.unis_url = reverse("universities-list")

    def tearDown(self) -> None:
        pass


class TestGetUniversities(BasicUniversityAPITestCase):
    def test_zero_universities_should_return_empty_list(self) -> None:
        response = self.client.get(self.unis_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_university_exists_should_succeed(self) -> None:
        test_uni = University.objects.create(name="Southampton")
        response = self.client.get(self.unis_url)
        response_content = json.loads(response.content)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), test_uni.name)
        self.assertEqual(response_content.get("status"), test_uni.status)
        self.assertEqual(
            response_content.get("application_link"), test_uni.application_link
        )
        self.assertEqual(response_content.get("notes"), test_uni.notes)
        test_uni.delete()


class TestPostUniversities(BasicUniversityAPITestCase):
    def test_create_university_without_arguments_should_fail(self) -> None:
        res = self.client.post(path=self.unis_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {"name": ["This field is required."]})

    def test_create_existing_university_should_fail(self) -> None:
        University.objects.create(name="Southampton")
        res = self.client.post(path=self.unis_url, data={"name": "Southampton"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.content),
            {"name": ["university with this name already exists."]},
        )

    def test_create_university_with_name_and_default_fields_only(self) -> None:
        res = self.client.post(path=self.unis_url, data={"name": "test uni"})
        response_content = json.loads(res.content)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_content.get("name"), "test uni")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_uni_with_layoffs_status_should_succeed(self) -> None:
        res = self.client.post(
            path=self.unis_url, data={"name": "test uni", "status": "Layoffs"}
        )
        self.assertEqual(res.status_code, 201)
        res_content = json.loads(res.content)
        self.assertEqual(res_content.get("status"), "Layoffs")

    def test_create_uni_with_wrong_status_should_fail(self) -> None:
        res = self.client.post(
            path=self.unis_url, data={"name": "test uni", "status": "VeryWrongIndeed"}
        )
        self.assertEqual(res.status_code, 400)
        res_content = json.loads(res.content)
        self.assertIn("VeryWrongIndeed", str(res.content))
        self.assertIn("is not a valid choice", str(res.content))

    @pytest.mark.xfail
    def test_should_b_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 2)


def raise_big_ole_exception() -> None:
    raise ValueError("I'm a big ol' exception!")


def test_raise_big_ole_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_big_ole_exception()
    assert "I'm a big ol' exception!" == str(e.value)


def test_raise_big_ole_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_big_ole_exception()
    assert "I'm a big ol' exception!" == str(e.value)


def function_that_logs_stuff() -> None:
    try:
        raise ValueError("Exception Thymeeee")
    except ValueError as e:
        logger.warning(f"I'm logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_stuff()
    assert "I'm logging Exception Thymeeee" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("Logging info level")
        assert "Logging info level" in caplog.text
