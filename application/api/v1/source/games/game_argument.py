class GameArgument:
    FORMAT_STR = "{arg} {val}"
    FORMAT_STR_WITH_EQUALS = "{arg}={val}"

    def __init__(self, argument, value, required=True, use_equals=False) -> None:
        self._arg = argument
        self._value = value
        self._required = required
        self._use_equals = use_equals

        self._formatted_arg = ""

    def _format_string(self) -> str:
        if self._use_equals:
            self._formatted_arg = self.FORMAT_STR_WITH_EQUALS.format(
                arg=self._arg, val=self._value
            )
        else:
            self._formatted_arg = self.FORMAT_STR.format(arg=self._arg, val=self._value)

        return self._formatted_arg

    def __str__(self) -> str:
        return self._format_string()
