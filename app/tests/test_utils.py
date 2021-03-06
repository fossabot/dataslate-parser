from app.parsers import killteam, heresy

supported_parsers = {
    'killteam': killteam,
    'heresy': heresy
}


def fetch_and_parse_roster(roster_file, gametype):
    with open(roster_file, "r") as roster_file:
        contents = roster_file.read()
        parser = get_parser_method(gametype)
        parsed_roster = parser.parse_units(contents=contents)
        return parsed_roster


def get_parser_method(gametype):
    parser = None
    try:
        parser = supported_parsers.get(gametype)
    except Exception:
        print('Parser not supported')
    return parser
