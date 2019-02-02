import pandas as pd

class CsvConfiguration:
    def __init__(self, inputFilePath, dataFrameTransformation, outputFilePath):
        self.inputFilePath = inputFilePath
        self.dataFrameTransformation = dataFrameTransformation
        self.outputFilePath = outputFilePath

    def execute(self):
        # load input CSV file
        df = pd.read_csv(self.inputFilePath, parse_dates=['Date'])
        df.set_index(df["Date"], inplace=True)

        # transform it to a different CSV file
        transformed_df = self.dataFrameTransformation.transform(df)

        # save the output CSV file
        transformed_df.to_csv(self.outputFilePath)

class DataFrameTransformation:
    def __init__(self):
        pass

    def normalize(s):
        try:
            return " ".join(list(map(lambda x: x.capitalize(), s.split())))
        except:
            return s

    #
    #  Transforms one DataFrame into another
    3
    def transform(self, df):
        # add/transform columns: latitude, longitude, Date, Weekday, Address, Cross Street
        df['longitude'] = [eval(x)[1] for x in df['Location']]
        df['latitude'] = [eval(x)[0] for x in df['Location']]
        df['Date'] = pd.to_datetime(df['Date Occurred'])
        df['Weekday'] = [x.weekday() for x in df['Date']]

        # filter rows
        AREA_NAME_FILTER = "Northeast"
        filteredRows = df.loc[df['Area Name'] == AREA_NAME_FILTER]

        # drop columns we don't care about
        newdf = filteredRows.drop(
            ['DR Number', 'Date Reported', 'Area ID', 'Area Name', 'Reporting District', 'Crime Code',
             'Crime Code Description', 'MO Codes', 'Premise Code', 'Premise Description', 'Location'], axis=1)

        newdf['Address'] = [self.normalize(s) for s in newdf['Address']]
        newdf['Cross Street'] = [self.normalize(s) for s in newdf['Cross Street']]
        return newdf

