import re

#
#  These are the values that get extrated from commands
#
class Key:
    HUMAN_FORM="humanForm"

    COLUMN_1="COL1"
    COLUMN_2="COL2"
    DATA_FRAME_NAME="DF"
    FILE_NAME="FILE"
    COLUMN_NAME="COL"
    COMMAND="COMMAND"
    CODE="CODE"
    PARAMETERS="PARAMS"

class RegexGenerator:
    COLUMN_REGEX = r"([ \w]+)"
    NAME_REGEX = r"(\w+)"
    ANY_TEXT_REGEX = r"([ -~]+)"
    FILE_NAME_REGEX = r"([\w\.\\/]+)"
    SPACE_REGEX = r"\s+"
    DOT_REGEX = r"\."

    def __init__(self):
        self.rmap = {}
        self.rmap[" "] = self.SPACE_REGEX
        self.rmap["."] = self.DOT_REGEX
        self.rmap[Key.DATA_FRAME_NAME] = self.NAME_REGEX
        self.rmap[Key.COLUMN_1] = self.COLUMN_REGEX
        self.rmap[Key.COLUMN_2] = self.COLUMN_REGEX
        self.rmap[Key.COLUMN_NAME] = self.COLUMN_REGEX
        self.rmap[Key.COMMAND] = self.NAME_REGEX
        self.rmap[Key.CODE] = self.ANY_TEXT_REGEX
        self.rmap[Key.PARAMETERS] = self.ANY_TEXT_REGEX
        self.rmap[Key.FILE_NAME] = self.FILE_NAME_REGEX
    
    def getRegex(self, s):
        parameters = []
        for key in self.rmap:
            if s.find(key) >= 0:
                s = s.replace(key, self.rmap[key])
                if len(key) > 1:
                    parameters.append(key)
        return s, parameters


class Command:
    # command keys that map to a specific implementation
    # LoadCommand, SaveCommand
    LOAD = "load"
    SAVE = "save"
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

    ### These are just tags, there is no associated action
    # key is extracted from the text line provided to "matches"
    CAPTURED_BY_REGEX = "captured_by_regex" 
    # UnknownCommand
    UNKNOWN = "unknown" # text does not match any known pattern

    def __init__(self, humanForm):
        self.humanForm = humanForm
        self.regexForm, self.keys = RegexGenerator().getRegex(humanForm)
        if Key.COMMAND in self.keys:
            self.key = Command.CAPTURED_BY_REGEX
        elif Key.COLUMN_NAME in self.keys:
            self.key = Command.CREATE_COLUMN # df.col <= code -- doesn't specify command
        else:
            self.key = Command.LOAD  # df = file -- doesn't specify command     

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
