import altair as alt
from command import Key

class BarGraphCommand:
     def execute(self, commandData, context):
        dataFrameName = commandData[Key.DATA_FRAME_NAME]
        dataFrame = context.df_get(dataFrameName)
        parameters = commandData[Key.PARAMETERS]
        xConfiguration = parameters[0].replace('+', ' ').split('|')
        yConfiguration = parameters[1].replace('+', ' ').split('|')

        chart = alt.Chart(dataFrame).mark_bar().encode(
            alt.X(xConfiguration[1], title=xConfiguration[2]),
            alt.Y(yConfiguration[1], title=yConfiguration[2])
        )
        imageFileName = "{dataFrameName}.png".format(dataFrameName=dataFrameName)
        chart.save(imageFileName, scale_factor=2.0)
        print("Saved Bar Graph PNG '{imageFileName}'".format(imageFileName=imageFileName))
