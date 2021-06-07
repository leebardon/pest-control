import json
import pytest
import logging
from django.urls import reverse
from api.pestcontrol.universities.models import University

logger = logging.getLogger("UNI_LOGS")
unis_url = reverse("universities-list")
pytestmark = (
    pytest.mark.django_db
)  # (sets global @pytest.mark.django_db decorator for all functions in file)


###############################
###  TEST GET UNIVERSITIES  ###
###############################


def test_zero_universities_should_return_empty_list(client) -> None:
    response = client.get(unis_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_university_exists_should_succeed(client) -> None:
    test_uni = University.objects.create(name="Southampton")
    response = client.get(unis_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_uni.name
    assert response_content.get("status") == test_uni.status
    assert response_content.get("application_link") == test_uni.application_link
    assert response_content.get("notes") == test_uni.notes
    test_uni.delete()


###############################
###  TEST POST UNIVERSITIES ###
###############################


def test_create_university_without_arguments_should_fail(client) -> None:
    res = client.post(path=unis_url)
    assert res.status_code == 400
    assert json.loads(res.content) == {"name": ["This field is required."]}


def test_create_existing_university_should_fail(client) -> None:
    University.objects.create(name="Southampton")
    res = client.post(path=unis_url, data={"name": "Southampton"})
    assert res.status_code == 400
    assert json.loads(res.content) == {
        "name": ["university with this name already exists."]
    }


def test_create_university_with_name_and_default_fields_only(client) -> None:
    res = client.post(path=unis_url, data={"name": "test uni"})
    response_content = json.loads(res.content)
    assert res.status_code == 201
    assert response_content.get("name") == "test uni"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_uni_with_layoffs_status_should_succeed(client) -> None:
    res = client.post(path=unis_url, data={"name": "test uni", "status": "Layoffs"})
    assert res.status_code == 201
    res_content = json.loads(res.content)
    assert res_content.get("status") == "Layoffs"


def test_create_uni_with_wrong_status_should_fail(client) -> None:
    res = client.post(
        path=unis_url, data={"name": "test uni", "status": "VeryWrongIndeed"}
    )
    assert res.status_code == 400
    res_content = json.loads(res.content)
    assert "VeryWrongIndeed" in str(res.content)
    assert "is not a valid choice" in str(res.content)


@pytest.mark.xfail
def test_should_b_ok_if_fails() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


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
