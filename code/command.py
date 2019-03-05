import re

#
#  These are the values that get extrated from commands
#
class Key:
    HUMAN_FORM="humanForm"

    COLUMN_NAME="COL"
    COLUMN_1="COL1"
    COLUMN_2="COL2"

    VALUE_1="VAL1"
    VALUE_2="VAL2"

    DATA_FRAME_NAME="DF"
    DATA_FRAME_1="DF1"
    DATA_FRAME_2="DF2"
    FILE_NAME="FILE"

    COMMAND="COMMAND"
    CODE="CODE"
    PARAMETERS="PARAMS"

    DOT="."
    SPACE=" "

    NO_KEY=""

class RegexGenerator:
    COLUMN_REGEX = r"([ \w]+)"
    NAME_REGEX = r"([_\w]+)"
    ANY_TEXT_REGEX = r"([ -~]+)"
    FILE_NAME_REGEX = r"([\w\.\\/]+)"
    SPACE_REGEX = r"\s+"
    DOT_REGEX = r"\."
    

    def __init__(self):
        self.rmap = {}
        self.rmap[Key.SPACE] = self.SPACE_REGEX
        self.rmap[Key.DOT] = self.DOT_REGEX
        self.rmap[Key.DATA_FRAME_1] = self.NAME_REGEX
        self.rmap[Key.DATA_FRAME_2] = self.NAME_REGEX
        self.rmap[Key.DATA_FRAME_NAME] = self.NAME_REGEX
        self.rmap[Key.COLUMN_1] = self.COLUMN_REGEX
        self.rmap[Key.COLUMN_2] = self.COLUMN_REGEX
        self.rmap[Key.COLUMN_NAME] = self.COLUMN_REGEX
        self.rmap[Key.VALUE_1] = self.NAME_REGEX
        self.rmap[Key.VALUE_2] = self.NAME_REGEX
        self.rmap[Key.COMMAND] = self.NAME_REGEX
        self.rmap[Key.CODE] = self.ANY_TEXT_REGEX
        self.rmap[Key.PARAMETERS] = self.ANY_TEXT_REGEX
        self.rmap[Key.FILE_NAME] = self.FILE_NAME_REGEX
        self.key_most_specific_to_least = [ 
            Key.DATA_FRAME_1, Key.DATA_FRAME_2, Key.DATA_FRAME_NAME,
            Key.COLUMN_1, Key.COLUMN_2, Key.COLUMN_NAME,
            Key.VALUE_1, Key.VALUE_2,
            Key.COMMAND, Key.CODE, Key.PARAMETERS, Key.FILE_NAME
            ]

    def getRegex(self, s):
        tokens = re.split('[^a-zA-Z0-9]', s)
        s = s.replace(Key.SPACE, self.rmap[Key.SPACE])
        s = s.replace(Key.DOT, self.rmap[Key.DOT])
        # replace most specific to least
        for key in self.key_most_specific_to_least:
            s = s.replace(key, self.rmap[key])
        # parameters have to be in order they are in original pattern
        parameters = []
        for t in tokens:
            if t in self.key_most_specific_to_least:
                parameters.append(t)
        return s, parameters


class Command:
    # command keys that map to a specific implementation
    # LoadCommand, SaveCommand
    LOAD = "load"
    UNION = "union"
    SAVE = "save"
    ANALYZE = "analyze"
    # CreateColumnCommand
    CREATE_COLUMN = "create"
    # ShowColumnsCommand
    SHOW_COLUMNS = "columns"
    # DropColumnsCommand
    DROP_COLUMNS = "drop"
    # FilterCommand
    FILTER = "filter"
    XROW = "xrow"

    # Graph Commands
    BAR_GRAPH = "bar"
    HEAT_MAP = "heatmap"
    STACKED_LINE = "stacked"

    # this one generates a 'reasonable' set based on dimensions selected
    GRAPH = "graph"

    ### These are just tags, there is no associated action
    # key is extracted from the text line provided to "matches"
    CAPTURED_BY_REGEX = "captured_by_regex" 

    # show last image generated
    SHOW_IMAGE = "image"
    # UnknownCommand
    UNKNOWN = "unknown" # text does not match any known pattern

    def __init__(self, humanForm, key):
        self.humanForm = humanForm
        self.regexForm, self.keys = RegexGenerator().getRegex(humanForm)
        self.key = key  

    def matches(self, line):
        self.matchData = re.match(self.regexForm, line)
        return self.matchData

    def asData(self):
        #
        # Key/value data representing the command
        #
        # humanForm -- to find it in code
        # command -- name of the command to execute, can be overridden
        #
        # keys are in order of match, the ones listed below are used when
        # the command is executed:
        #
        #  command -- optional override the command specified above
        #  dataFrameName -- Key.DATA_FRAME_NAME
        #  columnName -- Key.COLUMN_NAME
        #  code -- free form Python code
        #  params -- free form text, alpha-numeric and commas allowed
        #
        result = { Key.HUMAN_FORM: self.humanForm, Key.COMMAND: self.key }
        for idx, val in enumerate(self.keys):
            result[val] = self.matchData.group(idx + 1)
            if val == Key.PARAMETERS:
                result[val] = [x.strip() for x in result[val].split(",")]

        return result


class UnknownCommand:
    def execute(self, commandData, context):
        pass
