import pytest
from command import Command, Key, RegexGenerator

@pytest.fixture
def rxp():
    return RegexGenerator()

def test_Command_1():
    command = Command("DF.COL1.COL2 => COMMAND")
    regex = r"(\w+)\.([ \w]+)\.([ \w]+)\s+=>\s+(\w+)"
    assert regex == command.regexForm
    assert len(command.keys) == 4
    assert command.keys[0] == Key.DATA_FRAME_NAME
    assert command.keys[1] == Key.COLUMN_1
    assert command.keys[2] == Key.COLUMN_2
    assert command.keys[3] == Key.COMMAND

def test_Command_2():
    command = Command("DF.COL.COMMAND PARAMS")
    regex = r"(\w+)\.([ \w]+)\.(\w+)\s+([ -~]+)"
    assert regex == command.regexForm
    assert len(command.keys) == 4
    assert command.keys[0] == Key.DATA_FRAME_NAME
    assert command.keys[1] == Key.COLUMN_NAME
    assert command.keys[2] == Key.COMMAND
    assert command.keys[3] == Key.PARAMETERS


            # Command("DF = FILE", "(\w+)\s*=\s*([\w\.\\\/]+)", Command.LOAD, Key.DATA_FRAME_NAME, Key.FILE_NAME),
            # Command("DF.COL <= CODE", "(\w+)\.(\w+)\s*<=\s*([ -~]+)", Command.CREATE_COLUMN, Key.DATA_FRAME_NAME, Key.COLUMN_NAME, Key.CODE),
            # Command("DF.COMMAND PARAMS", "(\w+).(\w+)\s+([ -~]+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND, Key.PARAMETERS),
            # Command("DF.COMMAND", "(\w+).(\w+)", Command.CAPTURED_BY_REGEX, Key.DATA_FRAME_NAME, Key.COMMAND)

def test_map1(rxp):
    regex, params = rxp.getRegex("DF.COL1.COL2 => COMMAND")
    assert regex == r"(\w+)\.([ \w]+)\.([ \w]+)\s+=>\s+(\w+)"
    assert len(params) == 4
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.COLUMN_1
    assert params[2] == Key.COLUMN_2
    assert params[3] == Key.COMMAND

def test_map2(rxp):
    regex, params = rxp.getRegex("DF.COL.COMMAND PARAMS")
    assert regex == r"(\w+)\.([ \w]+)\.(\w+)\s+([ -~]+)"
    assert len(params) == 4
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.COLUMN_NAME
    assert params[2] == Key.COMMAND
    assert params[3] == Key.PARAMETERS

def test_map3(rxp):
    regex, params = rxp.getRegex("DF = FILE")
    assert regex == r"(\w+)\s+=\s+([\w\.\\/]+)"
    assert len(params) == 2
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.FILE_NAME

def test_map4(rxp):
    regex, params = rxp.getRegex("DF.COL <= CODE")
    assert regex == r"(\w+)\.([ \w]+)\s+<=\s+([ -~]+)"
    assert len(params) == 3
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.COLUMN_NAME
    assert params[2] == Key.CODE

def test_map5(rxp):
    regex, params = rxp.getRegex("DF.COMMAND PARAMS")
    assert regex == r"(\w+)\.(\w+)\s+([ -~]+)"
    assert len(params) == 3
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.COMMAND
    assert params[2] == Key.PARAMETERS

def test_map6(rxp):
    regex, params = rxp.getRegex("DF.COMMAND")
    assert regex == r"(\w+)\.(\w+)"
    assert len(params) == 2
    assert params[0] == Key.DATA_FRAME_NAME
    assert params[1] == Key.COMMAND

