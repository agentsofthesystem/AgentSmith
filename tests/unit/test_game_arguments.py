import os

from application.api.v1.source.games.common.game_argument import GameArgument


class TestGameArgs:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_game_args(self):
        this_arg = GameArgument("--abc", "123", use_equals=True)
        formatted_arg = this_arg._format_string()

        assert formatted_arg == '--abc="123"'

        this_arg = GameArgument("--abc", "'123'", use_equals=False)
        formatted_arg = this_arg._format_string()

        assert formatted_arg == "--abc \"'123'\""
