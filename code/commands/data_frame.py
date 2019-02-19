import pandas as pd
import numpy as np
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
        fileName = context.dataFrameFileNames.df_fileName(dataFrameName)
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

class FilterCommand:
   def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        columnName = commandData[Key.PARAMETERS][0]
        uniqueValuesForColumn = dataFrame[columnName].unique()

        for uniqueValue in uniqueValuesForColumn:
            if isinstance(uniqueValue, str):
                keyName = context.dataFrameFileNames.df_key_name(dataFrameName, columnName, uniqueValue)
                filtered_data = dataFrame.loc[dataFrame[columnName] == uniqueValue]
                print("Created DataFrame {keyName}, saved CSV".format(keyName=keyName))
                context.df_put(keyName, filtered_data)
                filtered_data.to_csv(context.dataFrameFileNames.df_filter_fileName(dataFrameName, columnName, uniqueValue))
            else:
                print("Skipping non-string")

class XrowCommand:
   def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        conditions = commandData[Key.PARAMETERS][0]
        leq,req = conditions.split("=")
        if np.issubdtype(dataFrame[leq].dtype, np.integer):
            dataFrame = dataFrame[dataFrame[leq] != int(req)]
        else:
            dataFrame = dataFrame[dataFrame[leq] != req]
        context.df_put(dataFrameName, dataFrame)
        print("Now {numberRows} rows".format(numberRows=len(dataFrame)))


