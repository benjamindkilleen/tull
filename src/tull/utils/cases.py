from stringcase import camelcase, capitalcase, spinalcase


def classcase(string: str) -> str:
    return capitalcase(camelcase(string))


def filenamecase(string: str) -> str:
    return spinalcase(camelcase(string))
