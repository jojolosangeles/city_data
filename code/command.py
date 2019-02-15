import re

#
#  These are the values that get extrated from commands
#
class Key:
    DATA_FRAME_NAME="dataFrameName"
    FILE_NAME="fileName"
    COLUMN_NAME="columnName"
    COMMAND="command"
    CODE="code"
    PARAMETERS="params"

class Command:
    # Load a DataFrame
    LOAD = "load"
    # Add a column to a DataFrame
    CREATE_COLUMN = "create"
    # Show the columns in a DataFrame
    SHOW_COLUMNS = "columns"
    # Drop some columns from the DataFrame
    DROP_COLUMNS = "drop"
    # Code doesn't know the intention of the text


    ### These are just tags, there is no associated action
    CAPTURED_BY_REGEX = "captured_by_regex" # used to identify the command, otherwise unused
    UNKNOWN = "unknown" # text does not match any known pattern

    def __init__(self, humanForm, regexForm, command, *args):
        self.humanForm = humanForm
        self.regexForm = regexForm
        self.command = command
        self.keys = args
        self.number_groups_captured = re.compile(regexForm).groups
        self.verify_regex()

    def verify_regex(self):
        number_command_parameters = len(self.keys)

        # is the command clearly identified?
        # for LOAD the command is implicit, so there's no capture
        command_implicit = self.command in [ self.LOAD, self.CREATE_COLUMN ]
        # otherwise, there MUST be a command matched
        # the keys must contain "command", and the number of keys MUST
        # match the number of groups captured into vairalbes
        if command_implicit:
            # we should NOT be matching a COMMAND key, since we already have it
            if Key.COMMAND in self.keys:
                print("*** {humanForm} {regexForm} -- WON'T WORK due to 'command' in keys, overriding previously set command  {command}".format(humanForm=self.humanForm, regexForm=self.regexForm, command=self.command))
            elif self.number_groups_captured != number_command_parameters:
                print("*** {humanForm} {regexForm} -- WON'T WORK, capturing {n} variables, command expects {m}".format(humanForm=self.humanForm, regexForm=self.regexForm, n=self.number_groups_captured, m=number_command_parameters))
        elif Key.COMMAND not in self.keys:
            print("*** {humanForm} {regexForm} -- WON'T WORK, command has not been specified, keys are: {keys}".format(humanForm=self.humanForm, regexForm=self.regexForm, keys=self.keys))

    def matches(self, line):
        self.matchData = re.match(self.regexForm, line)
        return self.matchData

    def asData(self):
        # Key/value data representing the command
        #
        # humanForm -- to find it in code
        # command -- name of the command to execute, can be overridden
        #
        # for each key, fill in one of the following keys:
        #  command -- override the command from above, key to Command implementation (class with execute method)
        #  dataFrameName -- Key.DATA_FRAME_NAME
        #  columnName -- Key.COLUMN_NAME
        #  code -- free form Python code
        #  params -- free form text, alpha-numeric and commas allowed
        #
        result = { "humanForm": self.humanForm, "command": self.command }
        for idx, val in enumerate(self.keys):
            ok = True
            print("idx={idx}, val={val}".format(idx=idx,val=val))
            if val == "command":
                matchValue = self.matchData.group(idx + 1)
                if matchValue != self.CAPTURED_BY_REGEX:
                    result[val] = matchValue
            else:
                ok = False
                print("Number groups captured: {n}, looking for group number {groupNumber}".format(n=self.number_groups_captured,groupNumber=idx + 1))
                print("{humanForm}, GROUPS:".format(humanForm=self.humanForm))
                print("{matchData}".format(matchData=self.matchData))
                for key in self.keys:
                    print("  key={key}".format(key=key))
                for parameter_offset in range(0, self.number_groups_captured):
                    print("  GROUP={captured}".format(captured=self.matchData.group(parameter_offset)))

            if ok:
                result[val] = self.matchData.group(idx + 1)

        print("asData={d}".format(d=result))
        return result


class UnknownCommand:
    def execute(self, commandData, context):
        pass
