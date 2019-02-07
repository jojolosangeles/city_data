import sys
import pandas as pd

USAGE = """
Usage: python process_csv.py <inputFilePath> <outputFilePath>
"""
if len(sys.argv) != 3:
    print(USAGE)
    sys.exit(0)

inputFilePath = sys.argv[1]
outputFilePath = sys.argv[2]

print("inputFilePath={inputFilePath}\nouptutFilePath={outputFilePath}"
      .format(inputFilePath=inputFilePath, outputFilePath=outputFilePath))

class CsvTransformer:
    def __init__(self, inputFilePath, dataFrameTransformer, outputFilePath):
        self.inputFilePath = inputFilePath
        self.dataFrameTransformer = dataFrameTransformer
        self.outputFilePath = outputFilePath

    def execute(self):
        # load input CSV file
        df = pd.read_csv(self.inputFilePath)

        # transform it to a different CSV file
        transformed_df = self.dataFrameTransformer.transform(df)

        # save the output CSV file
        transformed_df.to_csv(self.outputFilePath)

class DataFrameTransformer:
    def __init__(self):
        pass

    def normalize(self, s):
        try:
            return " ".join(list(map(lambda x: x.capitalize(), s.split())))
        except:
            return s

    #
    #  Transforms one DataFrame into another
    #
    #  1/2019 header is:
    #
    #  -X- DR Number,
    #  -X- Date Reported,
    #      Date Occurred => Date as DateTime
    #                    => Weekday 0-6
    #      Time Occurred,
    #  -X- Area ID,
    #  -X- Area Name => filter rows by value
    #  -X- Reporting District,
    #  -X- Crime Code,
    #  -X- Crime Code Description,
    #  -X- MO Codes,
    #      Victim Age,
    #      Victim Sex,
    #      Victim Descent,
    #  -X- Premise Code,
    #  -X- Premise Description,
    #      Address, => normalized so not ALL CAPITALIZED
    #      Cross Street, => normalized so not ALL CAPITALIZED
    #      Location === (longitude,latitude) => longitude, latitude
    #
    def transform(self, df):
        # add/transform columns: latitude, longitude, Date, Weekday, Address, Cross Street
        df['longitude'] = [eval(x)[1] for x in df['Location']]
        df['latitude'] = [eval(x)[0] for x in df['Location']]
        df['Date'] = pd.to_datetime(df['Date Occurred'])
        df['Weekday'] = [x.weekday() for x in df['Date']]
        df['Year'] = [x.year for x in df['Date']]

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


dataTransformer = DataFrameTransformer()
csvTransformer = CsvTransformer(inputFilePath, dataTransformer, outputFilePath)
csvTransformer.execute()
