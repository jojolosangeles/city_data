import os

class DataFrameFileNames:
    DATA_FRAME_ENVIRONMENT_VARIABLE = "DF_CSV"

    def __init__(self):
        self.basePath = "."
        if self.DATA_FRAME_ENVIRONMENT_VARIABLE in os.environ:
            self.basePath = os.environ[self.DATA_FRAME_ENVIRONMENT_VARIABLE]

    def df_fileName(self, dataFrameName):
        fileName = "{dataFrameName}.csv".format(dataFrameName=dataFrameName)
        return os.path.join(self.basePath, fileName)

    def df_key_name(self, dataFrameName, columnName, value):
        columnName = self.name_normalize(columnName)
        value = self.name_normalize(value)
        return "{dataFrameName}.{columnName}.{value}".format(dataFrameName=dataFrameName, columnName=columnName, value=value)

    def df_filter_fileName(self, dataFrameName, columnName, value):
        keyName = self.df_key_name(dataFrameName, columnName, value)
        fileName = "{keyName}.csv".format(keyName=keyName)
        return os.path.join(self.basePath, fileName)

    def name_normalize(self, name_with_spaces):
        return name_with_spaces.replace(' ', '_')