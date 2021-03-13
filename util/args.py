from typing import List


def read_string(args: List[str], allow_spaces = False) -> (str, List[str]):
    """
    Reads a string from the args
    :param args: Args, starting where you want to search for the string
    :param allow_spaces Whether or not to allow spaces without quotes
    :return: String (None if none can be read), args at end of string
    """

    if len(args) == 0:
        return None, args

    string = args[0]
    idx = 0

    # String start
    if string[0] == '"':
        # "foo -> foo
        string = string[1:]

        # We search starting from next arg, so we need a next arg
        if len(args) == 1:
            return None, args

        # Search for rest of string
        for string2 in args[1:]:
            should_break = False

            if string2[-1] == '"':
                should_break = True
                string2 = string2[:-1]

            string = string + " " + string2

            idx = idx + 1

            if should_break:
                return string, args[idx:]

    # If we reach this part of the code we have an unterminated string
    if idx > 0:
        return None, args

    # Else go onto other checks
    if allow_spaces:
        return ' '.join(args), []

    # Still just args[0]
    return string, args[1:]
