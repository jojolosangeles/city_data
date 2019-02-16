import pytest
from repl import Repl
from repl import CommandLineParser
from command import Command, Key

def test_constructor():
    r = Repl(True)
    assert r.interactive == True

def test_constructor2():
    r = Repl(False)
    assert r.interactive == False

# 
#  Verify the forms we are using match correctly
#
#   A. Command("DF.COL.COMMAND PARAMS", "(\w+)\s*=\s*([\w\.\\\/]+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.COMMAND, Key.PARAMETERS)
#   A. Command("DF=FILE", "(\w+)\s*=\s*([\w\.\\\/]+)", Command.LOAD, Key.DATA_FRAME_NAME, Key.FILE_NAME),
#   B. Command("DF.COL<=CODE", "(\w+\.\w+)\s*<=\s*([ -~]+)", Command.CREATE_COLUMN, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.CODE),
#   C. Command("DF.COMMAND PARAMS", "(\w+).(\w+)\s+(\w[\w\s,]*)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND, Key.PARAMETERS),
#   D. Command("DF.COMMAND", "(\w+).(\w+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND)

@pytest.fixture
def clp():
    return CommandLineParser()

def test_A0(clp):
    command  = clp.identify_command("all_areas.Area Name.bar X|Year:O|Year, Y|count()|Number of Accidents")
    assert command[Key.COMMAND] == "bar"
    assert command[Key.DATA_FRAME_NAME] == "all_areas"
    assert command[Key.COLUMN_NAME] == "Area Name"
    assert len(command[Key.PARAMETERS]) == 2
    assert command[Key.PARAMETERS][0] == "X|Year:O|Year"
    assert command[Key.PARAMETERS][1] == "Y|count()|Number of Accidents"

def test_A1(clp):
    command = clp.identify_command("anyname = path_to_file")
    assert command[Key.COMMAND] == Command.LOAD

def test_A2(clp):
    command = clp.identify_command("anyname = C:\\blah\\blah")
    assert command[Key.COMMAND] == Command.LOAD
   
def test_A3(clp):
    command = clp.identify_command("anyname = /unix/like/path")
    assert command[Key.COMMAND] == Command.LOAD

def test_B1(clp):
    command = clp.identify_command("df.col <= [ random code ,=*/.() ]")
    assert command[Key.COMMAND] == Command.CREATE_COLUMN
    assert command[Key.DATA_FRAME_NAME] == "df"
    assert command[Key.COLUMN_NAME] == "col"
    assert command[Key.CODE] == "[ random code ,=*/.() ]"

def test_C1(clp):
    command = clp.identify_command("some_df.some_command   a,  bb,   param|with|(special)   ")
    assert command[Key.COMMAND] == "some_command"
    assert command[Key.DATA_FRAME_NAME] == "some_df"
    assert len(command[Key.PARAMETERS]) == 3
    assert command[Key.PARAMETERS][0] == "a"
    assert command[Key.PARAMETERS][1] == "bb"
    assert command[Key.PARAMETERS][2] == "param|with|(special)"


def test_D1(clp):
    command = clp.identify_command("  some_df.some_command      ")
    assert command[Key.COMMAND] == "some_command"
    assert command[Key.DATA_FRAME_NAME] == "some_df"