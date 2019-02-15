import fileinput
import math
import numbers
import sys
import re
import altair as alt
import pandas as pd


def name_normalize(s):
    return s.replace(' ', '_')




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

