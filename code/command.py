import re

#
#  These are the values that get extrated from commands
#
class Key:
    HUMAN_FORM="humanForm"
    COLUMN_1="column_1"
    COLUMN_2="column_2"
    DATA_FRAME_NAME="dataFrameName"
    FILE_NAME="fileName"
    COLUMN_NAME="columnName"
    COMMAND="command"
    CODE="code"
    PARAMETERS="params"


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

    def __init__(self, humanForm, regexForm, key, *args):
        self.humanForm = humanForm
        self.regexForm = regexForm
        self.key = key
        self.keys = args

    def matches(self, line):
        self.matchData = re.match(self.regexForm, line)
        return self.matchData

    def asData(self):
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
