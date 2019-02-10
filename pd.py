import fileinput
import math
import numbers
import sys
import altair as alt
import pandas as pd

def name_normalize(s):
    return s.replace(' ', '_')

class UnknownCommand:
    def execute(*args):
        print("*** Unknown Command ***")
        for arg in args:
            print(" {arg}".format(arg=arg))

class LoadCommand:
    def execute(self, context, *args):
        if len(*args) != 3:
            raise ValueError("Expected 3 parameters: <file name> as <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        fileName = parameters[0]
        dataFrameName = parameters[2]
        context.dataFrames[dataFrameName] = pd.read_csv(fileName)
        print("Loaded {fileName} into DataFrame {dataFrameName}".format(fileName=fileName, dataFrameName=dataFrameName))

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

class ShowColumnsCommand:
    def execute(self, context, *args):
        if len(*args) != 1:
            raise ValueError("Expected 1 parameter: <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))
        dataFrameName = args[0][0]
        dataFrame = context.dataFrames[dataFrameName]
        if dataFrame is not None:
            print(dataFrame.columns.values)
        else:
            print("DataFrame not found")

class DropColumnCommand:
    def execute(self, context, *args):
        if len(*args) < 2:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 2 parameters: <dataframe name> <column name>, got {numargs} parameters".format(numargs=len(*args)))
        parameters = args[0]
        dataFrameName = parameters[0]
        columns = ' '.join(parameters[1:])
        columnNames =  [col.strip() for col in columns.split(",")]
        print("Dropping {columnNames} from DataFrame '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnNames=columnNames))
        dataFrame = context.dataFrames[dataFrameName]
        context.dataFrames[dataFrameName] = dataFrame.drop(columnNames, axis=1)
        print("Columns dropped")

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
        # dataFrame = context.get_data_frame(dataFrameName)
        # chart = alt.Chart(dataFrame).mark_bar().encode(
        #     alt.X(xConfiguration[1], title=xConfiguration[2]),
        #     alt.Y(yConfiguration[1], title=yConfiguration[2])
        # )
        # imageFileName = "{dataFrameName}.png".format(dataFrameName=dataFrameName)
        # chart.save(imageFileName, scale_factor=2.0)
        # print("Saved {imageFileName}".format(imageFileName=imageFileName))

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

class DoCommand:
    def execute(self, context, *args):
        print("Execute DoCommand")
        if len(*args) < 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 parameters: <command for list> <variableName> <codeBlock>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        command = parameters[0]
        variableName = parameters[1]
        codeBlock = ' '.join(parameters[2:])
        print("{command}({variableName}) => {codeBlock}".format(command=command, variableName=variableName, codeBlock=codeBlock))
        dataFrame = context.byDataFrame
        if command == "filter":
            for category in context.categories:
                print("filter => {category}".format(category=category))
                eval("{variableName} = '{category}'".format(variableName=variableName,category=category))
                new_data_frame = eval(codeBlock)
                print(new_data_frame)

# BarGraphCommand(sample20) ['X', 'Year:0', 'Year'], ['Y', 'count()', 'Number of Accidents']

# chart = alt.Chart(source).mark_bar().encode(
#     alt.X('Year:O', title='Year'),
#     alt.Y('count()', title='Number of Accidents')
# )
class Context:
    def __init__(self):
        self.commands = {
            "load": LoadCommand(),
            "save": SaveCommand(),
            "columns": ShowColumnsCommand(),
            "drop": DropColumnCommand(),
            "create": CreateColumnCommand(),
            "bar": BarGraphCommand(),
            "mbar": MultiBarGraphCommand(),
            "filter": FilterByCommand(),
            "do": DoCommand(),
            "show": ShowCommand(),
            "unique": UniqueCommand()
        }
        self.dataFrames = {}
        self.uniqueValuesForColumn = {}

    def get_data_frame(self, dataFrameName):
        return self.dataFrames[dataFrameName]

    def put_data_frame(self, dataFrameName, dataFrame):
        self.dataFrames[dataFrameName] = dataFrame

    def register_unique_values_for_column(self, columnName, uniqueValuesForColumn):
        self.uniqueValuesForColumn[columnName] = uniqueValuesForColumn

    def get_unique_values_for_column(self, columnName):
        print("REMEMBER UNIQUE VALUES FOR {columnName}".format(columnName=columnName))
        return self.uniqueValuesForColumn[columnName]

    def process_line(self, line):
        data = line.split()
        cmd = data[0].lower()
        args = data[1:]
        command = self.commands.get(cmd, UnknownCommand())
        try:
            command.execute(self, args)
        except ValueError as ve:
            print("*** ERROR: {message} ***".format(message=ve))
        #command = commands[data[0].lowercase9)]

script="interactive"
interactive = True
if len(sys.argv) > 1:
    script = sys.argv[1]
    interactive = False

print("Test: {script}".format(script=script))

context = Context()

def prompt_line():
    if interactive:
        print(">", end=' ')
        sys.stdout.flush()

def print_line(line):
    if not interactive:
        print("> {}".format(line))

prompt_line()
for line in fileinput.input():
    line = line.strip()
    print_line(line)
    if line == "quit":
        break
    elif len(line) > 0:
        context.process_line(line)
    prompt_line()

print("Test completed: {script}".format(script=script))
