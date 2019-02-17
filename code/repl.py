import sys
import fileinput
from csvfiles.DataFrameFileNames import DataFrameFileNames
from command import Command, Key, UnknownCommand
from commands.data_frame import LoadCommand, SaveCommand, FilterCommand, CreateColumnCommand, ShowColumnsCommand, DropColumnsCommand
from commands.chart import BarGraphCommand, HeatMapCommand

class CommandLineParser:
    def __init__(self):
        self.param_regex_most_to_least_specific = [
            # need to match in this order, from most specific to least specific
            # otherwise, the wrong command is identified
            #
            # DF maps to "dataFrameName" (Key.DATA_FRAME_NAME)
            # COL maps to "columnName" (Key.COLUMN_NAME)
            # COL1, COL2 map to "column_1", "column_2" (Key.COLUMN_1, Key.COLUMN_2)
            # COMMAND maps to the Python class that executes the command
            # CODE free form python code that generates all values for a new DataFrame column
            # PARAMS list of free form text names (with spaces allowed), separated by commas
            #
            Command("DF.COL1.COL2 => COMMAND", "(\w+)\.([ \w]+)\.([ \w]+)\s+=>\s+([ -~]+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COLUMN_1, Key.COLUMN_2, Key.COMMAND),
            Command("DF.COL.COMMAND PARAMS", "(\w+)\.([ \w]+)\.(\w+)\s+([ -~]+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.COMMAND, Key.PARAMETERS),
            Command("DF=FILE", "(\w+)\s*=\s*([\w\.\\\/]+)", Command.LOAD, Key.DATA_FRAME_NAME, Key.FILE_NAME),
            Command("DF.COL<=CODE", "(\w+)\.(\w+)\s*<=\s*([ -~]+)", Command.CREATE_COLUMN, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.CODE),
            Command("DF.COMMAND PARAMS", "(\w+).(\w+)\s+([ -~]+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND, Key.PARAMETERS),
            Command("DF.COMMAND", "(\w+).(\w+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND)
        ]

    def identify_command(self, line):
        line = line.strip()
        for command in self.param_regex_most_to_least_specific:
            if command.matches(line):
                return command.asData()
        return { "command": Command.UNKNOWN }


class Context:
    def __init__(self, dataFrameFileNames):
        self.dataFrames = {}
        self.dataFrameFileNames = dataFrameFileNames

    def df_get(self, dataFrameName):
        return self.dataFrames[dataFrameName]

    def df_slice_names(self, dataFrameName, columnName):
        dataFrame = self.df_get(dataFrameName)
        uniqueValues = dataFrame[columnName].unique()
        return self.dataFrameFileNames.df_slice_names(dataFrameName, columnName, uniqueValues)

    def df_put(self, dataFrameName, dataFrame):
        self.dataFrames[dataFrameName] = dataFrame


class CommandExecutor:
    def __init__(self):
        self.commands = {
            Command.LOAD: LoadCommand(),
            Command.SAVE: SaveCommand(),
            Command.CREATE_COLUMN: CreateColumnCommand(),
            Command.DROP_COLUMNS: DropColumnsCommand(),
            Command.SHOW_COLUMNS: ShowColumnsCommand(),
            Command.FILTER: FilterCommand(),

            # Graph commands
            Command.BAR_GRAPH: BarGraphCommand(),
            Command.HEAT_MAP: HeatMapCommand(),

            # none of the above
            Command.UNKNOWN: UnknownCommand()
        }

    def execute(self, commandData, context):
        self.commands[commandData["command"]].execute(commandData, context)

class Repl:
    def __init__(self, interactive):
        self.context = Context(DataFrameFileNames())
        self.commandLineParser = CommandLineParser()
        self.commandExecutor = CommandExecutor()
        self.interactive = interactive

    def prompt_line(self):
        if self.interactive:
            print(">", end=' ')
            sys.stdout.flush()

    def process_line(self, line):
        commandData = self.commandLineParser.identify_command(line)
        self.commandExecutor.execute(commandData, self.context)

    def print_line(self, line):
        if not self.interactive:
            print("> {}".format(line))

    def run(self, script):
        if not self.interactive:
            print("Test: {script}".format(script=script))
        self.prompt_line()
        for line in fileinput.input():
            line = line.strip()
            self.print_line(line)
            if line == "quit":
                break
            elif len(line) > 0:
                self.process_line(line)
                self.prompt_line()


