import pandas as pd
import numpy as np
import math
import getch
import sys
from command import Key
from commands.altair_types import AltairTypes

class LoadCommand:
    def execute(self, commandData, context):
        context.df_put(commandData[Key.DATA_FRAME_NAME], pd.read_csv(commandData[Key.FILE_NAME]))
        print("Loaded {fileName} into DataFrame '{dataFrameName}'".format(fileName=commandData[Key.FILE_NAME], dataFrameName=commandData[Key.DATA_FRAME_NAME]))

class SaveCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        fileName = context.dataFrameFileNames.df_fileName(dataFrameName)
        dataFrame.to_csv(fileName)
        print("Saved CSV File '{fileName}'".format(fileName=fileName))

class AnalyzeDF:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        for col in dataFrame.columns:
            sample = dataFrame.sample(frac=0.05)
            at = AltairTypes()
            types = at.identify_QONT(sample[col])
            print(types)

class CreateColumnCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        columnName = commandData[Key.COLUMN_NAME]
        code = commandData[Key.CODE]
        code = code.replace(dataFrameName, 'dataFrame')
        dataFrame[columnName] = eval(code)

def yes(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    while True:
        k = getch.getch()
        if k == 'y' or k == 'Y':
            print("YES")
            return True
        elif k == 'n' or k == 'N':
            print("no")
            return False

def selectDropColumns(dataFrame):
    columnNames = dataFrame.columns
    print(columnNames)
    z = dataFrame.iloc[0]
    result = []
    for idx,columnName in enumerate(columnNames):
        prompt = "\"{columnName}\": {value}    ...keep? (y/n) ".format(columnName=columnName,value=z[idx])
        if not yes(prompt):
            result.append(columnName)
    return result 
    
class DropColumnsCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        if Key.PARAMETERS in commandData:
            columnNames =  commandData[Key.PARAMETERS]
        else:
            columnNames = selectDropColumns(dataFrame)
        context.df_put(dataFrameName, dataFrame.drop(columnNames, axis=1))
        print("Dropped {columnNames} from DataFrame '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnNames=columnNames))

class ShowColumnsCommand:
    def execute(self, commandData, context):
        dataFrame = context.df_get(commandData[Key.DATA_FRAME_NAME])
        print(dataFrame.columns.values)

class ShowImageCommand:
    def execute(self, commandData, context):
        n = 1
        if Key.PARAMETERS in commandData:
            n = int(commandData[Key.PARAMETERS][0])
        print(commandData)
        print(n)
        print(commandData[Key.PARAMETERS])
        context.show_image(n)

class FilterCommand:
    MAX_VALUES_WHEN_SPLITTING_VALUE_PER_FILE = 20

    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        if Key.PARAMETERS in commandData:
            columnName = commandData[Key.PARAMETERS][0]
            uniqueValuesForColumn = dataFrame[columnName].unique()
            self.filter(context, dataFrame, dataFrameName, columnName, uniqueValuesForColumn)
        else:
            for columnName in dataFrame.columns:
                uniqueValuesForColumn = dataFrame[columnName].unique()
                numberValues=len(uniqueValuesForColumn)
                if numberValues > self.MAX_VALUES_WHEN_SPLITTING_VALUE_PER_FILE:
                    print("{numberValues} \"{columnName}\" values exceeds file-per-value max {threshhold}".format(
                        columnName=columnName,
                        numberValues=numberValues,
                        threshhold=self.MAX_VALUES_WHEN_SPLITTING_VALUE_PER_FILE
                    ))
                else:
                    prompt = "Save CSV for the {numberValues} values in \"{columnName}\"? (y/n) ".format(
                        numberValues=numberValues,
                        columnName=columnName)
                    if yes(prompt):
                        print("")
                        totalNumberValues = len(dataFrame)
                        valuesToSave = []
                        for value in uniqueValuesForColumn:
                            valueSpecificDataFrame = dataFrame[dataFrame[columnName] == value]
                            numberValues = len(valueSpecificDataFrame)
                            prompt = "{percent}% \"{value}\" ... keep? (y/n) ".format(
                                value=value,
                                percent=(math.floor(numberValues*100/totalNumberValues))
                            )
                            if yes(prompt):
                                valuesToSave.append(value)

                        self.filter(context, dataFrame, dataFrameName, columnName, valuesToSave)

    def filter(self, context, dataFrame, dataFrameName, columnName, uniqueValuesForColumn):
        for uniqueValue in uniqueValuesForColumn:
            if isinstance(uniqueValue, str):
                keyName = context.dataFrameFileNames.df_key_name(dataFrameName, columnName, uniqueValue)
                filtered_data = dataFrame.loc[dataFrame[columnName] == uniqueValue]
                print("Created DataFrame {keyName}, saved CSV".format(keyName=keyName))
                context.df_put(keyName, filtered_data)
                filtered_data.to_csv(context.dataFrameFileNames.df_filter_fileName(dataFrameName, columnName, uniqueValue),index_label='key')
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


