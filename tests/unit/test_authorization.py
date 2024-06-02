from application.common import authorization


class FakeRequest:
    def __init__(self, headers=None):
        self.headers = headers or {}


class FakeToken:
    def __init__(self) -> None:
        self.token_name = "foo"


class FakeSetting:
    def __init__(self) -> None:
        self.setting_value = "bar"


class TestAuthorization:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_verify_bearer_token(self, mocker):
        # Arrange
        fake_headers = {"Authorization": "Bearer 1234"}
        fake_request = FakeRequest(headers=fake_headers)
        fake_token = FakeToken()
        fake_setting = FakeSetting()

        mocker.patch(
            "application.common.authorization._get_token", return_value=fake_token
        )
        mocker.patch(
            "application.common.authorization._get_setting", return_value=fake_setting
        )
        mocker.patch("jwt.decode", return_value={"token_name": "foo"})

        return_code = authorization._verify_bearer_token(fake_request)

        assert return_code == 200
