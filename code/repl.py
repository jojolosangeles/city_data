import sys
import fileinput
from PIL import Image
from csvfiles.DataFrameFileNames import DataFrameFileNames
from command import Command, Key, UnknownCommand
from commands.data_frame import XrowCommand, LoadCommand, UnionCommand, SaveCommand, FilterCommand 
from commands.data_frame import CreateColumnCommand, ShowColumnsCommand, DropColumnsCommand
from commands.data_frame import ShowImageCommand, AnalyzeDF
from commands.chart import BarGraphCommand, HeatMapCommand, StackedLineCommand, GraphCommand
from commands.altair_types import AltairTypes

class CommandLineParser:
    def __init__(self):
        self.param_regex_most_to_least_specific = [
            # need to match in this order, from most specific to least specific
            # otherwise, the wrong command is identified
            Command("DF.COL1.COL2 => COMMAND", Command.CAPTURED_BY_REGEX),
            Command("DF.COL.COMMAND PARAMS", Command.CAPTURED_BY_REGEX),
            Command("DF = DF1.COL1.VAL1 \+ DF2.COL2.VAL2", Command.UNION),
            Command("DF = FILE", Command.LOAD),
            Command("DF.COL <= CODE", Command.CREATE_COLUMN),
            Command("DF.COMMAND PARAMS", Command.CAPTURED_BY_REGEX),
            Command("DF.COMMAND", Command.CAPTURED_BY_REGEX)
        ]

    def identify_command(self, line):
        line = line.strip()
        for command in self.param_regex_most_to_least_specific:
            if command.matches(line):
                return command.asData()
        return { Key.COMMAND: Command.UNKNOWN }


class Context:
    def __init__(self, dataFrameFileNames):
        self.dataFrames = {}
        self.dataFrameColumnMetadata = {}
        self.imageFiles = []
        self.dataFrameFileNames = dataFrameFileNames
        self.altairTypes = AltairTypes()

    def df_get(self, dataFrameName):
        return self.dataFrames[dataFrameName]

    def df_column_metadata(self, dataFrameName, columnName):
        name = "{dataFrameName}.{columnName}".format(dataFrameName=dataFrameName, columnName=columnName)
        dataFrame = self.df_get(dataFrameName)
        sample = dataFrame.sample(frac=0.05)[columnName]
        sample = [str(val) for val in sample]
        basicTypes = self.altairTypes.identify_QONT(sample)
        nunique = dataFrame[columnName].nunique()
        clean99 = []
        boundary = len(sample)/100
        if nunique < 10:
            unique = dataFrame[columnName].unique()
            for val in unique:
                count = len(dataFrame[dataFrame[columnName] == val])
                if count > boundary:
                    clean99.append(val)

        print(name)
        self.dataFrameColumnMetadata[name] = { 
            "types": basicTypes,
            "numberUniqueValues": nunique,
            "clean99": clean99
        }
        print(self.dataFrameColumnMetadata[name])

    def df_slice_names(self, dataFrameName, columnName):
        dataFrame = self.df_get(dataFrameName)
        uniqueValues = dataFrame[columnName].unique()
        return self.dataFrameFileNames.df_slice_names(dataFrameName, columnName, uniqueValues)

    def df_put(self, dataFrameName, dataFrame):
        self.dataFrames[dataFrameName] = dataFrame

    def register_image(self, imageFileName):
        self.imageFiles.append(imageFileName)

    def show_image(self, n):
        if len(self.imageFiles) >= n:
            for _ in range(1, n):
                img = Image.open(self.imageFiles[-n])
                img.show()

class CommandExecutor:
    def __init__(self):
        self.commands = {
            # DataFrame commands
            Command.LOAD: LoadCommand(),
            Command.UNION: UnionCommand(),
            Command.ANALYZE: AnalyzeDF(),
            Command.SAVE: SaveCommand(),
            Command.CREATE_COLUMN: CreateColumnCommand(),
            Command.DROP_COLUMNS: DropColumnsCommand(),
            Command.SHOW_COLUMNS: ShowColumnsCommand(),
            Command.FILTER: FilterCommand(),
            Command.XROW: XrowCommand(),

            # Graph commands
            Command.BAR_GRAPH: BarGraphCommand(),
            Command.HEAT_MAP: HeatMapCommand(),
            Command.STACKED_LINE: StackedLineCommand(),
            Command.GRAPH: GraphCommand(),

            # none of the above
            Command.SHOW_IMAGE: ShowImageCommand(),
            Command.UNKNOWN: UnknownCommand()
        }

    def execute(self, commandData, context):
        self.commands[commandData[Key.COMMAND]].execute(commandData, context)

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


