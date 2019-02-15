import pandas as pd
from command import Key

class LoadCommand:
    def execute(self, commandData, context):
        print("LoadCommand, commandData={commandData}".format(commandData=commandData))
        context.put_data_frame(commandData[Key.DATA_FRAME_NAME], pd.read_csv(commandData[Key.FILE_NAME]))
        print("Loaded {fileName} into DataFrame {dataFrameName}".format(fileName=commandData[Key.FILE_NAME], dataFrameName=commandData[Key.DATA_FRAME_NAME]))

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
        
class DropColumnsCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.get_data_frame(dataFrameName)
        columnNames =  [col.strip() for col in commandData["params"].split(",")]
        print("Dropping {columnNames} from DataFrame '{dataFrameName}'".format(
        dataFrameName=dataFrameName, columnNames=columnNames))
        context.put_data_frame(dataFrameName, dataFrame.drop(columnNames, axis=1))
        print("Columns dropped")

class ShowColumnsCommand:
    def execute(self, commandData, context):
        dataFrame = context.get_data_frame(commandData[Key.DATA_FRAME_NAME])
        print(dataFrame.columns.values)


