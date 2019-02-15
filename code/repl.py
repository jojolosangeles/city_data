

from command import Command, Key, UnknownCommand
from commands.data_frame import LoadCommand, SaveCommand, ShowColumnsCommand, DropColumnsCommand

class CommandLineParser:
    def __init__(self):
        self.param_regex_most_to_least_specific = [
            # need to match in this order, from most specific to least specific
            # otherwise, the wrong command is identified
            #
            # DF maps to "dataFrameName" (Key.DATA_FRAME_NAME)
            # COL maps to "columnName" (Key.COLUMN_NAME)
            # COMMAND maps to the Python class that executes the command
            # CODE free form python code that generates all values for a new DataFrame column
            # PARAMS list of free form text names (with spaces allowed), separated by commas
            #
            Command("DF=FILE", "(\w+)\s*=\s*([\w\.\\\/]+)", Command.LOAD, Key.DATA_FRAME_NAME, Key.FILE_NAME),
            Command("DF.COL<=CODE", "(\w+)\.(\w+)\s*<=\s*([ -~]+)", Command.CREATE_COLUMN, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.CODE),
            Command("DF.COMMAND PARAMS", "(\w+).(\w+)\s+(\w[\w\s,]*)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND, Key.PARAMETERS),
            Command("DF.COMMAND", "(\w+).(\w+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND)
        ]

    def identify_command(self, line):
        line = line.strip()
        for command in self.param_regex_most_to_least_specific:
            if command.matches(line):
                return(command.asData())
        return { "command": Command.UNKNOWN }


class Context:
    def __init__(self):
        self.dataFrames = {}

    def get_data_frame(self, dataFrameName):
        return self.dataFrames[dataFrameName]

    def put_data_frame(self, dataFrameName, dataFrame):
        self.dataFrames[dataFrameName] = dataFrame

class CommandExecutor:
    def __init__(self):
        self.commands = {
            Command.LOAD: LoadCommand(),
            Command.DROP_COLUMNS: DropColumnsCommand(),
            Command.SHOW_COLUMNS: ShowColumnsCommand(),
            Command.UNKNOWN: UnknownCommand()
        }

    def execute(self, commandData, context):
        print("execute {commandData}".format(commandData=commandData))
        print("commandData['command']={c}".format(c=commandData["command"]))
        self.commands[commandData["command"]].execute(commandData, context)

class Repl:
    def __init__(self, interactive):
        self.context = Context()
        self.commandLineParser = CommandLineParser()
        self.commandExecutor = CommandExecutor()
        self.interactive = interactive

    def prompt_line(self):
        if self.interactive:
            print(">", end=' ')
            sys.stdout.flush()

    def process_line(self, line):
        print(line)
        commandData = self.commandLineParser.parse(line)
        print(commandData)
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


