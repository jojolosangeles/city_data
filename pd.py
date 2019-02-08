import fileinput
import sys
import pandas as pd

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

class SaveCommand:
    def execute(self, context, *args):
        if len(*args) != 1:
            raise ValueError("Expected 1 parameter: <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))

        parameters = args[0]
        dataFrameName = parameters[0]
        fileName = "{dataFrameName}.csv".format(dataFrameName=dataFrameName)
        context.dataFrames[dataFrameName].to_csv(fileName)
        print("Saved {fileName}".format(fileName=fileName))

class ShowColumnsCommand:
    def execute(self, context, *args):
        if len(*args) != 1:
            raise ValueError("Expected 1 parameter: <dataframe name>, got {numargs} parameters".format(numargs=len(*args)))
        dataFrameName = args[0][0]
        dataFrame = context.dataFrames[dataFrameName]
        if dataFrame is not None:
            print(dataFrame.columns.values)

class DropColumnCommand:
    def execute(self, context, *args):
        if len(*args) != 2:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 2 parameters: <dataframe name> <column name>, got {numargs} parameters".format(numargs=len(*args)))
        dataFrameName = args[0][0]
        columnName = args[0][1]
        columnName = columnName.replace('+', ' ')
        print("Dropping '{columnName}' from '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnName=columnName))
        dataFrame = context.dataFrames[dataFrameName]
        context.dataFrames[dataFrameName] = dataFrame.drop([columnName], axis=1)

class CreateColumnCommand:
    def execute(self, context, *args):
        if len(*args) < 3:
            for arg in args:
                print(" {arg}".format(arg=arg))
            raise ValueError("Expected 3 or more parameters: <dataframe name> <column name> <row transformation code>, got {numargs} parameters".format(numargs=len(*args)))
        dataFrameName = args[0][0]
        columnName = args[0][1]
        columnName.replace('+', ' ')
        rowCode = ' '.join(args[0][2:])
        print("{dataFrameName}.{columnName}=".format(dataFrameName=dataFrameName,columnName=columnName))
        dataFrame = context.dataFrames[dataFrameName]
        dataFrame[columnName] = eval(rowCode)
        context.dataFrames[dataFrameName] = dataFrame
        dataFrame = context.dataFrames[dataFrameName]

class Context:
    def __init__(self):
        self.commands = {
            "load": LoadCommand(),
            "save": SaveCommand(),
            "columns": ShowColumnsCommand(),
            "drop": DropColumnCommand(),
            "create": CreateColumnCommand()
        }
        self.dataFrames = {}

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

print("Test: {script}".format(script=sys.argv[0]))
context = Context()

for line in fileinput.input():
    line = line.strip()
    print("> {}".format(line))
    context.process_line(line)

print("Test completed: {script}".format(script=sys.argv[0]))
