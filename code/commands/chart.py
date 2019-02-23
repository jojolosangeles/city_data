import altair as alt
import pandas as pd
from command import Key

class GraphCommand:
    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        columns = commandData[Key.PARAMETERS]
        columnMetadata = {}
        for columnName in columns:
            print("AAAA")
            print(columnName)
            columnMetadata[columnName] = context.df_column_metadata(dataFrameName, columnName)
            print("BBBB")
            print(columnMetadata[columnName])
            print("CCCC")


class BarGraphCommand:
     def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]

        if Key.COLUMN_NAME in commandData:
            columnName = commandData[Key.COLUMN_NAME]
            sliceNames = context.df_slice_names(dataFrameName, columnName)
        else:
            columnName = None
            sliceNames = [ dataFrameName ]

        parameters = commandData[Key.PARAMETERS]
        xConfiguration = parameters[0].replace('+', ' ').split('|')
        yConfiguration = parameters[1].replace('+', ' ').split('|')
        for name in sliceNames:
            dataFrame = context.df_get(name)
            print("Making bar chart for DataFrame {name}".format(name=name))
            chart = alt.Chart(dataFrame).mark_bar().encode(
                alt.X(xConfiguration[1], title=xConfiguration[2]),
                alt.Y(yConfiguration[1], title=yConfiguration[2])
            )
            imageFileName = context.dataFrameFileNames.df_image_fileName(name)
            chart.save(imageFileName, scale_factor=2.0)
            context.register_image(imageFileName)
            print("Saved Bar Graph PNG '{imageFileName}'".format(imageFileName=imageFileName))

class StackedLineCommand:
    def fieldName(self, s):
        data = s.split(":")
        if len(data) > 0:
            return data[0]
        else:
            return s

    def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        xDimension = commandData[Key.COLUMN_1]
        yDimension = commandData[Key.COLUMN_2]
        dataFrame = context.df_get(dataFrameName)
        dfCleaned = dataFrame.dropna(subset = [self.fieldName(xDimension), self.fieldName(yDimension)])
        chart = alt.Chart(dfCleaned).mark_area().encode(
            x=xDimension,y="count()",color=yDimension)
        imageFileName = context.dataFrameFileNames.df_stacked_image_fileName(dataFrameName, xDimension, yDimension)
        chart.save(imageFileName)
        context.register_image(imageFileName)
        print("Saved PNG stacked lines: {imageFileName}".format(imageFileName=imageFileName))

class HeatMapCommand:
     def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        xDimension = commandData[Key.COLUMN_1]
        yDimension = commandData[Key.COLUMN_2]
        dataFrame = context.df_get(dataFrameName)
        # X|Year:O|Year Y|count()|Number+of+Accidents

        print("HeatMapCommand({dataFrameName}) {xDimension}, {yDimension}"
            .format(dataFrameName=dataFrameName,xDimension=xDimension,yDimension=yDimension))
        df = dataFrame.groupby([xDimension,yDimension]).count()
        dff = df.reset_index(level=[xDimension,yDimension])
        source = pd.DataFrame({xDimension: dff[xDimension], yDimension: dff[yDimension], 'z': dff[dff.columns[2]]})
        xFormat = "{xDimension}:O".format(xDimension=xDimension)
        yFormat = "{yDimension}:O".format(yDimension=yDimension)
        chart = alt.Chart(source).mark_rect().encode(x=xFormat,y=yFormat,color='z:Q')
        imageFileName = context.dataFrameFileNames.df_heatmap_image_fileName(dataFrameName, xDimension, yDimension)
        chart.save(imageFileName)
        context.register_image(imageFileName)
        print("Saved PNG heatmap: {imageFileName}".format(imageFileName=imageFileName))
