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

    def df_slice_key(self, dataFrameName, columnName):
        if columnName:
            return "{dataFrameName}.{columnName}".format(dataFrameName=dataFrameName, columnName=self.name_normalize(columnName))
        else:
            return dataFrameName

    def df_slice_names(self, dataFrameName, columnName, columnValues):
        sliceKey = self.df_slice_key(dataFrameName, columnName)
        result = []
        for val in columnValues:
            if isinstance(val, str):
                result.append("{sliceKey}.{valueKey}".format(sliceKey=sliceKey,valueKey=self.name_normalize(val)))
        return result

    def df_heatmap_image_fileName(self, dataFrameName, xDimension, yDimension):
        keyName = self.df_key_name(dataFrameName, xDimension, yDimension)
        imageFileName = "{keyName}.heatmap.png".format(keyName=keyName)
        return os.path.join(self.basePath, imageFileName)

    def df_image_fileName(self, sliceKey):
        fileName = "{slicekey}.png".format(slicekey=sliceKey)
        return os.path.join(self.basePath, fileName)

    def df_filter_fileName(self, dataFrameName, columnName, value):
        keyName = self.df_key_name(dataFrameName, columnName, value)
        fileName = "{keyName}.csv".format(keyName=keyName)
        return os.path.join(self.basePath, fileName)

    def name_normalize(self, name_with_spaces):
        return name_with_spaces.replace(' ', '_')