import pytest
from commands.altair_types import AltairTypes

at = AltairTypes()

@pytest.fixture
def date_occurred_sample():
    return [ "11/04/2010", "08/10/2010", "06/09/2010", "04/06/2010",
    "   05/23/2010", "    09/02/2010", "     10/27/2010", "      09/30/2010", "   11/19/2010",
    "      02/21/2010", "    09/01/2010", "    03/11/2010", "       03/23/2010", 
    "      06/28/2010", "     04/17/2010", "     03/17/2010", "     07/25/2010",
    "      10/27/2010", "      02/03/2010", "     12/15/2010", "      06/17/2010"]

@pytest.fixture
def time_occurred_sample():
    return [
        "1345", "1900", "1925", "1445", "1805", "1520", "1910", "540", "1440", "300", 
        "1530", "1840", "1400", "210", "1130", "1600", "600", "1020", "1520"
    ]

@pytest.fixture
def ambiguous_sample():
    return [
        # 11 numbers
        "123124111", "7", "4372888892","123124111", "77778", "43","1", "7000", "437","123124", "9",
        # 7 times (or numbers) ... simple test n < 2400, so 6 of above are "time-like-numbers"
        "1345", "1900", "1925", "1445", "1805", "1520", "1910",
        # 5 dates
        "08/28/1959", "      10/27/2010", "      02/03/2010", "     12/15/2010", "      06/17/2010",
        # 3 names
        "Bob", "George", "Bill",
        # 2 decimal
        "1.3", "7.432"
    ]

@pytest.fixture
def name_sample():
    return ['Central', '77th Street', 'Pacific', 'Topanga', 'Southwest',
       'Foothill', 'Newton', 'Hollywood', 'N Hollywood', 'Northeast',
       'Hollenbeck', 'West LA', 'Southeast', 'Devonshire', 'Mission',
       'Harbor', 'Wilshire', 'Rampart', 'Olympic', 'West Valley',
       'Van Nuys']

@pytest.fixture
def age_data():
    return ["35.0", "72.0", "56.0", "45.0", "50.0", "20.0", "29.0", "20.0", "42.0",
"53.0", "51.0", "29.0", "55.0", "54.0", "30.0", "27.0", "62.0",
"25.0", "56.0", "40.0"]

@pytest.fixture
def altairTypeDetector():
    return AltairTypes()

def test_ambiguous_sample(altairTypeDetector, ambiguous_sample):
    types = altairTypeDetector.identify_QONT(ambiguous_sample)

    nTimeLikeNumbers = 6
    nTimes = 7
    nNumbers = 11 + 7

    nDates = 5
    nNames = len(ambiguous_sample)
    nDecimal = 2
    assert types[AltairTypes.QUANTITATIVE] == nDecimal
    assert types[AltairTypes.ORDINAL] == nNumbers
    assert types[AltairTypes.NOMINAL] == nNames
    assert types[AltairTypes.TEMPORAL] == nDates + nTimes + nTimeLikeNumbers

def test_date_occurred_sample(altairTypeDetector, date_occurred_sample):
    types = altairTypeDetector.identify_QONT(date_occurred_sample)
    n = len(date_occurred_sample)
    assert len(types) == 5
    assert types[AltairTypes.QUANTITATIVE] == 0
    assert types[AltairTypes.ORDINAL] == 0
    assert types[AltairTypes.NOMINAL] == n
    assert types[AltairTypes.TEMPORAL] == n

def test_time_occurred_sample(altairTypeDetector, time_occurred_sample):
    types = altairTypeDetector.identify_QONT(time_occurred_sample)
    n = len(time_occurred_sample)
    assert len(types) == 5
    assert types[AltairTypes.QUANTITATIVE] == 0
    assert types[AltairTypes.ORDINAL] == n
    assert types[AltairTypes.NOMINAL] == n
    assert types[AltairTypes.TEMPORAL] == n

def test_name_sample(altairTypeDetector, name_sample):
    types = altairTypeDetector.identify_QONT(name_sample)
    n = len(name_sample)
    assert len(types) == 5
    assert types[AltairTypes.QUANTITATIVE] == 0
    assert types[AltairTypes.ORDINAL] == 0
    assert types[AltairTypes.NOMINAL] == n
    assert types[AltairTypes.TEMPORAL] == 0

def test_age_data(altairTypeDetector, age_data):
    types = altairTypeDetector.identify_QONT(age_data)
    n = len(age_data)
    assert len(types) == 5
    assert types[AltairTypes.QUANTITATIVE] == n
    assert types[AltairTypes.ORDINAL] == 0
    assert types[AltairTypes.NOMINAL] == n
    assert types[AltairTypes.TEMPORAL] == 0