import pandas as pd
import math
from command import Key

class LoadCommand:
    def execute(self, commandData, context):
        context.df_put(commandData[Key.DATA_FRAME_NAME], pd.read_csv(commandData[Key.FILE_NAME]))
        print("Loaded {fileName} into DataFrame {dataFrameName}".format(fileName=commandData[Key.FILE_NAME], dataFrameName=commandData[Key.DATA_FRAME_NAME]))

class SaveCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        fileName = "{dataFrameName}.csv".format(dataFrameName=dataFrameName)
        dataFrame.to_csv(fileName)
        print("Saved CSV File '{fileName}'".format(fileName=fileName))

class CreateColumnCommand:
    def execute(self, commandData, context):
        dataFrame = context.df_get(commandData[Key.DATA_FRAME_NAME])
        columnName = commandData[Key.COLUMN_NAME]
        code = commandData[Key.CODE]
        dataFrame[columnName] = eval(code)
    

class DropColumnsCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        columnNames =  commandData[Key.PARAMETERS]
        context.df_put(dataFrameName, dataFrame.drop(columnNames, axis=1))
        print("Dropped {columnNames} from DataFrame '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnNames=columnNames))

class ShowColumnsCommand:
    def execute(self, commandData, context):
        dataFrame = context.df_get(commandData[Key.DATA_FRAME_NAME])
        print(dataFrame.columns.values)


