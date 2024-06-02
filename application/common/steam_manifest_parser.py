import os


def read_dir(dir: str):
    steamapps = {}

    for file in os.listdir(dir):
        if file.endswith(".acf"):
            # acf = read_dir(dir)
            acf = read_acf(os.path.join(dir, file))
            # acf = read_acf(dir + file)
            steamapps[acf["appid"]] = acf

    return steamapps


def read_acf(acffile: str) -> dict:
    with open(acffile, "r") as file:
        content = [line.replace("\t\t", "") for line in file]
        content = [line.strip("\t\n") for line in content]

    return parser(content)[0]


def parser(content: str, index=0) -> dict:
    appstate = {}
    i = index

    while i < len(content):
        x = content[i]

        if x == '"AppState"' or x == "{" or x == "}":
            i = i + 1
            continue

        # Due to a new variable called "BetaConfig", blanks cannot be removed completely.
        # Consider the example: ['', 'BetaKey', '', '']
        # Removing all '' elements would leave only 'BetaKey'
        # Thus the older system would work best.

        # TODO: An alternative and cleaner implementation soon.
        line = x.split('"')

        # Peek forward for an opening curly brace
        if content[i + 1] == "{":
            # Pass back to parser and increment index forward
            appstate[line[1]], i = parser(content, i + 1)
            i = i + 1
            # Continue to loop till a closing curly brace is found
            continue

        elif content[i + 1] == "}":
            # Create dict and return
            appstate[line[1]] = line[3]
            return appstate, i

        appstate[line[1]] = line[3]
        i = i + 1

    return appstate, i
