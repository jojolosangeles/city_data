import fileinput
import math
import numbers
import sys
import re
import altair as alt
import pandas as pd

class Key:
    DATA_FRAME_NAME="dataFrameName"
    FILE_NAME="fileName"
    COLUMN_NAME="columnName"
    COMMAND="command"
    CODE="code"
    PARAMETERS="params"

def name_normalize(s):
    return s.replace(' ', '_')

class UnknownCommand:
    def execute(self, commandData, context):
        pass

class LoadCommand:
    def execute(self, commandData, context):
        print("LoadCommand, commandData={commandData}".format(commandData=commandData))
        context.put_data_frame(commandData[Key.DATA_FRAME_NAME], pd.read_csv(commandData[Key.FILE_NAME]))
        print("Loaded {fileName} into DataFrame {dataFrameName}".format(fileName=commandData[Key.FILE_NAME], dataFrameName=commandData[Key.DATA_FRAME_NAME]))

class ShowColumnsCommand:
    def execute(self, commandData, context):
        dataFrame = context.get_data_frame(commandData[Key.DATA_FRAME_NAME])
        print(dataFrame.columns.values)

class DropColumnsCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.get_data_frame(dataFrameName)
        columnNames =  [col.strip() for col in commandData["params"].split(",")]
        print("Dropping {columnNames} from DataFrame '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnNames=columnNames))
        context.put_data_frame(dataFrameName, dataFrame.drop(columnNames, axis=1))
        print("Columns dropped")

class SaveCommand:
    def execute(self, context, *args):
        if len(*args) != 1:
            raise ValueError("Expected 1 parameter: <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        dataFrameName = parameters[0]
        self.saveDataFrame(context, dataFrameName)

    def saveDataFrame(self, context, dataFrameName):
        fileName = "{dataFrameName}.csv".format(dataFrameName=dataFrameName)
        context.dataFrames[dataFrameName].to_csv(fileName)
        print("Saved CSV File '{fileName}'".format(fileName=fileName))

class ShowCommand:
    def execute(self, context, *args):
        if len(*args) != 1:
            raise ValueError("Expected 1 parameter: <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        dataFrameName = parameters[0]
        self.showDataFrame(context, dataFrameName)

    def showDataFrame(self, context, dataFrameName):
        dataFrame = context.get_data_frame(dataFrameName)
        print(dataFrame)


class CreateColumnCommand:
    def execute(self, context, *args):
        if len(*args) < 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 or more parameters: <dataframe name> <column name> <row transformation code>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        columnName = parameters[1]
        columnName.replace('+', ' ')
        rowCode = ' '.join(parameters[2:])
        print("{dataFrameName}.{columnName}=".format(dataFrameName=dataFrameName,columnName=columnName))
        dataFrame = context.dataFrames[dataFrameName]
        dataFrame[columnName] = eval(rowCode)
        context.dataFrames[dataFrameName] = dataFrame
        dataFrame = context.dataFrames[dataFrameName]

class BarGraphCommand:
    def execute(self, context, *args):
        if len(*args) != 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 parameters: <dataframe name> <X column configuration> <Y column configuration>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        xConfiguration = parameters[1].replace('+', ' ').split('|')
        yConfiguration = parameters[2].replace('+', ' ').split('|')
        dataFrame = context.get_data_frame(dataFrameName)
        self.draw_bar_graph(dataFrameName, dataFrame, xConfiguration, yConfiguration)

    def draw_bar_graph(self, dataFrameName, dataFrame, xConfiguration, yConfiguration):
        print("BarGraphCommand({dataFrameName}) {xConfiguration}, {yConfiguration}"
            .format(dataFrameName=dataFrameName,xConfiguration=xConfiguration,yConfiguration=yConfiguration))

        chart = alt.Chart(dataFrame).mark_bar().encode(
            alt.X(xConfiguration[1], title=xConfiguration[2]),
            alt.Y(yConfiguration[1], title=yConfiguration[2])
        )
        imageFileName = "{dataFrameName}.png".format(dataFrameName=dataFrameName)
        chart.save(imageFileName, scale_factor=2.0)
        print("Saved Bar Graph PNG '{imageFileName}'".format(imageFileName=imageFileName))

class LineCommand:
    def execute(self, context, *args):
        if len(*args) != 4:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 parameters: <dataframe name> <X dimension> <Y dimension> <Color dimension>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        xDimension = parameters[1].replace('+', ' ')
        yDimension = parameters[2].replace('+', ' ')
        colorDimension = parameters[3].replace('+', ' ')
        self.draw_line(dataFrameName, xDimension, yDimension, colorDimension)

    def draw_line(self, dataFrameName, xDimension, yDimension, colorDimension):
        print("LineCommand({dataFrameName}) {xDimension}, {yDimension} {colorDimension}"
            .format(dataFrameName=dataFrameName,xDimension=xDimension,yDimension=yDimension,colorDimension=colorDimension))
        dataFrame = context.get_data_frame(dataFrameName)
        chart = alt.Chart(dataFrame).mark_line().encode(
            alt.X('count()', title=xDimension),
            alt.Y(yDimension, title=yDimension),
            color=colorDimension
        )
        imageFileName = "{dataFrameName}_line.png".format(dataFrameName=dataFrameName)
        chart.save(imageFileName, scale_factor=2.0)
        print("Saved ll_distance PNG '{imageFileName}'".format(imageFileName=imageFileName))

class MultiBarGraphCommand:
    def execute(self, context, *args):
        if len(*args) < 4:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 4 parameters: <dataframe name> <group by column name> <X column configuration> <Y column configuration>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        lastParameterOffset = len(parameters) - 1
        columnDescriminator = parameters[1:(lastParameterOffset-1)]
        columnName = " ".join(columnDescriminator)
        print("Column Descriminator = '{columnName}'".format(columnName=columnName))
        xConfiguration = parameters[lastParameterOffset-1].replace('+', ' ').split('|')
        yConfiguration = parameters[lastParameterOffset].replace('+', ' ').split('|')
        print("BarGraphCommand({dataFrameName}) {xConfiguration}, {yConfiguration}"
            .format(dataFrameName=dataFrameName,xConfiguration=xConfiguration,yConfiguration=yConfiguration))

        uniqueValuesForColumn = context.get_unique_values_for_column(columnName)
        normalized_column_name = name_normalize(columnName)
        print("Unique Values For Column = {uniqueValuesForColumn}".format(uniqueValuesForColumn=uniqueValuesForColumn))
        barGraph = BarGraphCommand()
        for value in uniqueValuesForColumn:
            if isinstance(value, str):
                normalized_value = name_normalize(value)
                dataFrameKey = "{dataFrameName}.{normalized_column_name}.{normalized_value}".format(dataFrameName=dataFrameName,normalized_column_name=normalized_column_name,normalized_value=normalized_value)
                dataFrame = context.get_data_frame(dataFrameKey)
                print("Bar graph for {dataFrameKey}".format(dataFrameKey=dataFrameKey))
                barGraph.draw_bar_graph(normalized_value, dataFrame, xConfiguration, yConfiguration)

class HeatMapCommand:
    def execute(self, context, *args):
        if len(*args) != 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 4 parameters: <dataframe name> <x config> <y config>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        xDimension = parameters[1].replace('+', ' ')
        yDimension = parameters[2].replace('+', ' ')
        dataFrame = context.get_data_frame(dataFrameName)
        # X|Year:O|Year Y|count()|Number+of+Accidents
        self.draw_heat_map(dataFrameName, dataFrame, xDimension, yDimension)

    def draw_heat_map(self, dataFrameName, dataFrame, xDimension, yDimension):
        print("HeatMapCommand({dataFrameName}) {xDimension}, {yDimension}"
            .format(dataFrameName=dataFrameName,xDimension=xDimension,yDimension=yDimension))
        df = dataFrame.groupby([xDimension,yDimension]).count()
        dff = df.reset_index(level=[xDimension,yDimension])
        source = pd.DataFrame({xDimension: dff[xDimension], yDimension: dff[yDimension], 'z': dff[dff.columns[2]]})
        xFormat = "{xDimension}:O".format(xDimension=xDimension)
        yFormat = "{yDimension}:O".format(yDimension=yDimension)
        chart = alt.Chart(source).mark_rect().encode(x=xFormat,y=yFormat,color='z:Q')
        imageFileName = "{dataFrameName}.{xDimension}.{yDimension}.heatmap.png".format(dataFrameName=dataFrameName,xDimension=name_normalize(xDimension),yDimension=name_normalize(yDimension))
        chart.save(imageFileName)
        print("Saved PNG heatmap: {imageFileName}".format(imageFileName=imageFileName))


class UniqueCommand:
    def execute(self, context, *args):
        if len(*args) < 2:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 2 parameters: <dataframe name> <column name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        dataFrameName = parameters[0]
        columnName = ' '.join(parameters[1:])
        normalized_column_name = name_normalize(columnName)
        dataFrame = context.get_data_frame(dataFrameName)
        print("{dataFrameName}.{columnName} unique values".format(dataFrameName=dataFrameName,columnName=columnName))
        uniqueValuesForColumn = dataFrame[columnName].unique()
        for uniqueValue in uniqueValuesForColumn:
            if isinstance(uniqueValue, str) or isinstance(uniqueValue, numbers.Number):
                print(uniqueValue, end=" ")
        print("")


class FilterByCommand:
    def execute(self, context, *args):
        if len(*args) < 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 parameters: <dataframe name> by <column name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        dataFrameName = parameters[0]
        columnName = ' '.join(parameters[2:])
        normalized_column_name = name_normalize(columnName)
        dataFrame = context.get_data_frame(dataFrameName)
        uniqueValuesForColumn = dataFrame[columnName].unique()
        context.register_unique_values_for_column(columnName, uniqueValuesForColumn)
        saveDataFrameCommand = SaveCommand()
        for uniqueValue in uniqueValuesForColumn:
            if isinstance(uniqueValue, str):
                normalized_value = name_normalize(uniqueValue)
                keyName = "{dataFrameName}.{normalized_column_name}.{normalized_value}".format(dataFrameName=dataFrameName, normalized_column_name=normalized_column_name,normalized_value=normalized_value)
                filtered_data = dataFrame.loc[dataFrame[columnName] == uniqueValue]
                print("Created DataFrame {keyName}".format(keyName=keyName))
                context.put_data_frame(keyName, filtered_data)
                saveDataFrameCommand.saveDataFrame(context, keyName)
            else:
                print("Skipping non-string")

class Command:
    # Load a DataFrame
    LOAD = "load"
    # Add a column to a DataFrame
    CREATE_COLUMN = "create"
    # Show the columns in a DataFrame
    SHOW_COLUMNS = "columns"
    # Drop some columns from the DataFrame
    DROP_COLUMNS = "drop"
    # Code doesn't know the intention of the text


    ### These are just tags, there is no associated action
    CAPTURED_BY_REGEX = "captured_by_regex" # used to identify the command, otherwise unused
    UNKNOWN = "unknown" # text does not match any known pattern

    def __init__(self, humanForm, regexForm, command, *args):
        self.humanForm = humanForm
        self.regexForm = regexForm
        self.command = command
        self.keys = args
        self.number_groups_captured = re.compile(regexForm).groups
        self.verify_regex()

    def verify_regex(self):
        number_command_parameters = len(self.keys)

        # is the command clearly identified?
        # for LOAD the command is implicit, so there's no capture
        command_implicit = self.command in [ self.LOAD, self.CREATE_COLUMN ]
        # otherwise, there MUST be a command matched
        # the keys must contain "command", and the number of keys MUST
        # match the number of groups captured into vairalbes
        if command_implicit:
            # we should NOT be matching a COMMAND key, since we already have it
            if Key.COMMAND in self.keys:
                print("*** {humanForm} {regexForm} -- WON'T WORK due to 'command' in keys, overriding previously set command  {command}".format(humanForm=self.humanForm, regexForm=self.regexForm, command=self.command))
            elif self.number_groups_captured != number_command_parameters:
                print("*** {humanForm} {regexForm} -- WON'T WORK, capturing {n} variables, command expects {m}".format(humanForm=self.humanForm, regexForm=self.regexForm, n=self.number_groups_captured, m=number_command_parameters))
        elif Key.COMMAND not in self.keys:
            print("*** {humanForm} {regexForm} -- WON'T WORK, command has not been specified, keys are: {keys}".format(humanForm=self.humanForm, regexForm=self.regexForm, keys=self.keys))

    def matches(self, line):
        self.matchData = re.match(self.regexForm, line)
        return self.matchData

    def asData(self):
        # Key/value data representing the command
        #
        # humanForm -- to find it in code
        # command -- name of the command to execute, can be overridden
        #
        # for each key, fill in one of the following keys:
        #  command -- override the command from above
        #  dataFrameName -- Key.DATA_FRAME_NAME
        #  columnName -- Key.COLUMN_NAME
        #  code
        #  params
        result = { "humanForm": self.humanForm, "command": self.command }
        for idx, val in enumerate(self.keys):
            ok = True
            print("idx={idx}, val={val}".format(idx=idx,val=val))
            if val == "command":
                matchValue = self.matchData.group(idx + 1)
                if matchValue != self.CAPTURED_BY_REGEX:
                    result[val] = matchValue
            else:
                ok = False
                print("Number groups captured: {n}, looking for group number {groupNumber}".format(n=self.number_groups_captured,groupNumber=idx + 1))
                print("{humanForm}, GROUPS:".format(humanForm=self.humanForm))
                print("{matchData}".format(matchData=self.matchData))
                for key in self.keys:
                    print("  key={key}".format(key=key))
                for parameter_offset in range(0, self.number_groups_captured):
                    print("  GROUP={captured}".format(captured=self.matchData.group(parameter_offset)))

            if ok:
                result[val] = self.matchData.group(idx + 1)

        print("asData={d}".format(d=result))
        return result



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
            Command("DF=FILE", "\s*(\w+)\s*=\s*([\w\.\\\/]+)\s*", Command.LOAD, Key.DATA_FRAME_NAME, Key.FILE_NAME),
            Command("DF.COL<=CODE", "\s*(\w+\.\w+)\s*<=\s*([ -~]+)+\s*", Command.CREATE_COLUMN, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.CODE),
            Command("DF.COMMAND PARAMS", "\s*(\w+).(\w+)\s+(\w[\w\s,]*)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND, Key.PARAMETERS),
            Command("DF.COMMAND", "\s*(\w+).(\w+)\s*", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND)
        ]

    def parse(self, line):
        for command in self.param_regex_most_to_least_specific:
            if command.matches(line):
                print("IT's a MATCH with {format}".format(format=command.humanForm))
                return(command.asData())
            else:
                print("did not match: {format}".format(format=command.humanForm))
        print("ALL MATCHES FAILED !!!")
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

interactive = len(sys.argv) == 1
script = None if len(sys.argv) == 1 else sys.argv[1]
repl = Repl(interactive)
repl.run(script)
