import re
import operator

class AltairType:
    def __init__(self, initial, shortName, description, regexList):
        self.initial = initial
        self.shortName = shortName
        self.description = description
        self.regexList = regexList

    def match(self, value):
        value = value.strip()
        result = any(re.match("^" + regex + "$", value) for regex in self.regexList)
        print("Match {value} against {shortName} => {result}".format(value=value,shortName=self.shortName, result=result))
        return result

class DateFormats:
    def __init__(self):
        self.date_formats = []
        self.date_formats.append(r"\d\d/\d\d/\d\d\d\d")
        self.date_formats.append(r"[0-9]{1,4}")

    def formats(self):
        return self.date_formats

class AltairTypes:
    # offsets into identify_QONT tuple result
    QUANTITATIVE = 0
    ORDINAL = 1
    NOMINAL = 2
    TEMPORAL = 3

    # some basic identifier regexes
    REGEX_ALL_DIGITS = f"\d+"
    REGEX_DECIMAL_DIGITS = f"\d+\.\d+"
    REGEX_PRINTABLE_CHARS = r"[ -!]+"
    REGEX_VARIABLE = r"^[a-zA-Z0-9_]+$"

    def __init__(self):
        self.quantitative = AltairType("Q", "quantitative", "real value", [self.REGEX_DECIMAL_DIGITS])
        self.ordinal = AltairType("O", "ordinal", "int value", [self.REGEX_ALL_DIGITS])
        self.nominal = AltairType("N", "nominal", "unordered category", [self.REGEX_PRINTABLE_CHARS])
        self.temporal = AltairType("T", "temporal", "time or date value", DateFormats().formats())
 
        self.variable = AltairType("V", "variable", "variable name in code", [self.REGEX_VARIABLE])

    def identify_QONT(self, values):
        result = (0, 0, 0, 0, 0)
        for value in values:
            result = tuple(map(operator.add, result, 
                ((1 if self.quantitative.match(value) else 0),
                 1 if self.ordinal.match(value) else 0, 
                 1,
                 1 if self.temporal.match(value) else 0,
                 1 if self.variable.match(value) else 0
                )))
        return result

