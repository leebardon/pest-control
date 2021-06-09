import json
from django.core import mail
from unittest.mock import patch

import pytest

def test_send_email_should_succeed(mailoutbox, settings) -> None:
    settings.EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    #send message
    mail.send_mail(
        subject="Hullo",
        message="heyyyyy",
        from_email="sillyemail2000@gmail.com",
        recipient_list=["sillyemail2000@gmail.com"],
        fail_silently=False,
    )
    # test 1 message was sent
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Hullo"

def test_email_without_args_should_return_empty_email(client) -> None:
    with patch (
        "api.pestcontrol.universities.views.send_mail"
    ) as mocked_send_email_function:
        res = client.post(path="/send-email", follow=True)
        print(res)
        # res_content = json.loads(res.content)
        assert res.status_code == 200
        breakpoint()
        # assert res_content["status"] == "success"
        # assert res_content["info"] == "email sent"

        mocked_send_email_function.assert_called_with(
            subject==None,
            message==None,
            from_email="sillyemail2000@gmail.com",
            recipient_list=["sillyemail2000@gmail.com"],
        )

