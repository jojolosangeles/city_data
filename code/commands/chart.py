import altair as alt
from command import Key

class BarGraphCommand:
     def execute(self, commandData, context):
        print("BarGraphCommand.execute, commandData=")
        print(commandData)
        print("IS THIS BEING CALLED?")
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        columnName = None
        if Key.COLUMN_NAME in commandData:
            columnName = commandData[Key.COLUMN_NAME]
        dataFrame = context.df_get_slice(dataFrameName, columnName)
        parameters = commandData[Key.PARAMETERS]
        xConfiguration = parameters[0].replace('+', ' ').split('|')
        yConfiguration = parameters[1].replace('+', ' ').split('|')
        print("Making chart")
        chart = alt.Chart(dataFrame).mark_bar().encode(
            alt.X(xConfiguration[1], title=xConfiguration[2]),
            alt.Y(yConfiguration[1], title=yConfiguration[2])
        )
        print("Saving chart")
        imageFileName = context.dataFrameFileNames.df_image_fileName(dataFrameName, columnName)
        print("imageFileName={imageFileName}".format(imageFileName=imageFileName))
        chart.save(imageFileName, scale_factor=2.0)
        print("Saved Bar Graph PNG '{imageFileName}'".format(imageFileName=imageFileName))
