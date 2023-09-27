from application.common.constants import FileModes


class GameArgument:
    FORMAT_STR = "{arg} {val}"
    FORMAT_STR_NO_EQUAL_WITH_QUOTES = '{arg} "{val}"'
    FORMAT_STR_WITH_EQUALS = "{arg}={val}"
    FORMAT_STR_WITH_EQUALS_AND_QUOTES = '{arg}="{val}"'

    def __init__(
        self,
        argument,
        value=None,
        required=False,
        use_equals=False,
        use_quotes=True,
        is_permanent=False,
        file_mode=FileModes.NOT_A_FILE.value,
    ) -> None:
        self._arg = argument
        self._value = value
        self._required = required
        self._is_permanent = is_permanent
        self._file_mode = file_mode
        self._use_equals = use_equals
        self._use_quotes = use_quotes

        self._formatted_arg = ""

    def is_requried(self) -> bool:
        return self._required

    def _format_string(self) -> str:
        """
        Four possibilities / combos
            # use_equals = True, use_quotes = True    # FORMAT_STR_WITH_EQUALS_AND_QUOTES
            # use_equals = True, use_quotes = False   # FORMAT_STR_WITH_EQUALS
            # use_equals = False, use_quotes = True   # FORMAT_STR_NO_EQUAL_WITH_QUOTES
            # use_equals = False, use_quotes = False  # FORMAT_STR
        """
        if self._use_equals and self._use_quotes:
            self._formatted_arg = self.FORMAT_STR_WITH_EQUALS_AND_QUOTES.format(
                arg=self._arg, val=self._value
            )
        elif self._use_equals and not self._use_quotes:
            self._formatted_arg = self.FORMAT_STR_WITH_EQUALS.format(
                arg=self._arg, val=self._value
            )
        elif not self._use_equals and self._use_quotes:
            self._formatted_arg = self.FORMAT_STR_NO_EQUAL_WITH_QUOTES.format(
                arg=self._arg, val=self._value
            )
        else:
            self._formatted_arg = self.FORMAT_STR.format(arg=self._arg, val=self._value)
        return self._formatted_arg

    def __str__(self) -> str:
        return self._format_string()
