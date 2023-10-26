'''
File: fparse.py
Date: 10/22/2023
Author(s):
    - Caelan Hadley

'''
from lib.types import Number as num
from lib.types import Port as port
from lib.types import Command as cmd

# num.contains(num.F32) -> True
# cmd.hasKind(cmd.KIND_SYNC) -> True

def main():
    # Tokenize File
    tokens = Tokenizer(get_input()).tokenize()
    parser = Parser(tokens)
    component = parser.getComponent()
    component.toString()



'''
----------------------------------------------------------------
Functions
----------------------------------------------------------------
'''

'''
Get Input
    Grabs the input file located in the main directory
    called "input.fpp".

returns: the contents of an input fpp file.
'''
def get_input():
    with open("./input.fpp", 'r') as f:
        return f.read()

# Valid symbols from the specification
def get_symbols():
    return "()*+,-->./:;=[]\{\}"

# Removes symbols from given text
def rmsym(text):
    buf = ''
    for c in text:
        if c in get_symbols():
            continue
        buf += c
    return buf

'''
Throw Warning
    Prints a warning message but does not stop execution.
'''
def throwWarning(message):
    print(f"Warning: {message}")

'''
Throw Exception
    Prints an error message and stops execution.
'''
def throwException(message):
    raise Exception(f"Error: {message}")




'''
----------------------------------------------------------------
Classes
----------------------------------------------------------------
'''

'''
Parameter
    FORMAT -> [ ref ] identifier : type-name
'''
class Parameter:
    typeof = 'parameter'
    def __init__(self):
        self.identifier = ''
        self.type_name = ''

'''
Port Class
    FORMAT -> port identifier [ ( param-list ) ] [ -> type-name ]
'''
class Port:
    typeof = 'port'
    def __init__(self):
        self.identifier = ''
        self.param_list = [] # Type : <Parameter>
        self.type_name = ''

    def toString(self):
        print(f"[{self.typeof}] {self.identifier} {len(self.param_list)}xPort(s) -> <{self.type_name}>")

class Command:
    typeof = 'command'

    def __init__(self, kind=None, identifier=None, param_list=None, opcode=None, priority=None, queue_full_behavior=None):
        self.kind = kind
        self.identifier = identifier
        self.param_list = param_list
        self.opcode = opcode
        self.priority = priority
        self.queue_full_behavior = queue_full_behavior
    
    # Object verificaiton (debating doing this for all objects that need to be verified - Caelan)
    def isValid(self):
        return cmd.hasKind(self.kind)

    def toString(self):
        return f"[{self.typeof}] {self.identifier} <{self.kind}>"

class Event:
    typeof = 'event'
    def __init__(self, identifier=None, param_list=None, severity=None, id=None, format=None, throttle=None):
        self.identifier = identifier
        self.param_list = param_list
        self.severity = severity
        self.id = id
        self.format = format
        self.throttle = throttle

    def toString(self):
        return f"[{self.typeof}] {self.identifier}"

class Telemetry:
    typeof = 'telemetry'
    def __init__(self, identifier=None, type_name=None, id=None, update=None, format=None, low=None, high=None):
        self.identifier = identifier
        self.type_name = type_name
        self.id = id
        self.update = update
        self.format = format
        self.low = low
        self.high = high
    
    def toString(self):
        return f"[{self.typeof}] {self.identifier} <{self.type_name}>"

class PortInstanceSpecifier:
    typeof = 'port_instance_specifier'
    
    def __init__(self,general_port_kind=None, identifier=None, num_ports=None, 
                 port_instance_type=None, queue_full_behavior=None,special_port_kind=None,
                 priority=None, description=None):
        self.general_port_kind = general_port_kind # <async input, guarded input, sync input, guarded>
        self.identifier = identifier
        self.num_ports = num_ports
        self.port_instance_type = port_instance_type # <qual_ident, serial> qual_ident Fw.Com
        self.queue_full_behavior = queue_full_behavior # <assert, block, drop>
        self.special_port_kind = special_port_kind
        self.priority = priority # Must be convertable to Integer
        self.description = description # Description from "@" comments
        
    def toString(self):
        # Return statement depends on the port kind
        if self.general_port_kind == None:
            return f"[port] {self.identifier} <{self.special_port_kind}>"
        return f"[port] {self.identifier} <{self.general_port_kind}>"

class Component:
    def __init__(self, kind=None, identifier=None, ports=[], commands=[], events=[], telemetry=[]):
        self.kind = kind
        self.identifier = identifier
        self.ports = ports
        self.commands = commands
        self.events = events
        self.telemetry = telemetry
    
    # Use this to add ports try not to modify ports directly
    def addPort(self, port):
        if type(port) != PortInstanceSpecifier: throwException()
        self.ports.append(port)
    
    def addCommand(self, command):
        if type(command) != Command: throwException()
        self.commands.append(command)

    def addEvent(self, event):
        if type(event) != Event: throwException()
        self.events.append(event)
    
    def addTelemetry(self, telemetry):
        if type(telemetry) != Telemetry: throwException()
        self.telemetry.append(telemetry)
    
    def toString(self):
        print(f"Component ({self.identifier})")
        for port in self.ports:
            print('- ' + port.toString())
        for command in self.commands:
            print('- ' + command.toString())
        for telemetry in self.telemetry:
            print('- ' + telemetry.toString())
        for event in self.events:
            print('- ' + event.toString())

class Tokenizer:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.buffer = ''

    # Saves the contents of the buffer
    def save_buffer(self):
        self.tokens.append(self.buffer)
        self.clbuf()

    # Clears the buffer
    def clbuf(self):
        self.buffer = ''
    
    # Checks if the buffer is empty returns true if empty
    def isEmpty(self):
        return (True if self.buffer == '' else False)

    def tokenize(self):
        i = 0
        while i < len(self.input):
            # If this is a space save whats in the buffer
            if self.input[i] == ' ' and not self.isEmpty():
                self.save_buffer()
                i += 1
            # If current input is not a space, check for conditions
            else:
                if self.input[i] == '\n' and i+1 < len(self.input):
                    # If there is something in the buffer save it
                    if not self.isEmpty():
                        self.save_buffer()
                    # Parse until no more newlines or spaces
                    while self.input[i] == '\n' or self.input[i] == ' ':
                        i += 1
                    # Append null terminator token to signify end of line to the parser
                    self.tokens.append('\x00')
                # Handles Hashtag Comments
                elif self.input[i] == '#' and i+1 < len(self.input):
                    while self.input[i] != '\n':
                        i += 1
                # Handles Description Comments
                elif self.input[i] == '@' and i+1 < len(self.input):
                    comment_buffer = ''
                    while self.input[i] != '\n':
                        comment_buffer += self.input[i]
                        i += 1
                    self.tokens.append(comment_buffer)
                # If the current input is a word, save it in the buffer
                else:
                    self.buffer += self.input[i]
                    i += 1
        # If something remains in the buffer at EOF then save it.
        if not self.isEmpty():
            self.save_buffer()

        return self.tokens
    
    # Prints all the tokens
    def toStringTokens(self):
        for token in self.tokens:
            print(token)

class Parser:
    def __init__(self, tokens=None):
        if not tokens: throwException("No tokens given to Parser.")
        self.tokens = tokens
        self.component = Component()
        self.parse()

    def parse(self):
        i = 0
        # Carries @ comments
        current_comment = ''

        while i < len(self.tokens):
            # @Comments
            if self.tokens[i][0] == '@':
                current_comment = self.tokens[i]

            # Component
            if self.tokens[i] == 'component':
                self.component.kind = self.tokens[i-1]
                self.component.identifier = self.tokens[i+1]

            # Ports
            if self.tokens[i] == 'port':
                if self.tokens[i-1] == 'input':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-2]),
                                                 identifier=self.tokens[i+1][:-1],
                                                 description=current_comment)
                    current_comment = ''
                    self.component.addPort(port)
                    
                elif self.tokens[i-1] == 'output':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-1]),
                                                 identifier=self.tokens[i+1][:-1],
                                                 description=current_comment)
                    current_comment = ''
                    self.component.addPort(port)
                
                # Special port 'event'
                elif self.tokens[i-1] == 'event':
                    port = PortInstanceSpecifier(special_port_kind=(self.tokens[i-1]),
                                                 identifier=self.tokens[i+1],
                                                 description=current_comment)
                    current_comment = ''
                    self.component.addPort(port)
                    
                # Special port 'telemetry' 
                elif self.tokens[i-1] == 'telemetry':
                    port = PortInstanceSpecifier(special_port_kind=(self.tokens[i-1]),
                                                 identifier=self.tokens[i+1],
                                                 description=current_comment)
                    current_comment = ''
                    self.component.addPort(port)
                    
                # All other special ports 
                else:
                    port = PortInstanceSpecifier(special_port_kind=(
                                                 ' '.join(map(str, self.tokens[i-2:i]))),
                                                 identifier=self.tokens[i+1],
                                                 description=current_comment)
                    current_comment = ''
                    self.component.addPort(port)
                    
            # Commands
            if self.tokens[i] == 'command':
                cmd = Command(kind=self.tokens[i-1], identifier=self.tokens[i+1])
                if cmd.isValid():
                    self.component.addCommand(cmd)

            # Telemetry
            if self.tokens[i] == 'telemetry':
                # Check for special telemetry
                if self.tokens[i+1] != 'port':
                    tlm = Telemetry(identifier=self.tokens[i+1][:-1], type_name=self.tokens[i+2])
                    self.component.addTelemetry(tlm)
            
            # Events
            if self.tokens[i] == 'event':
                # Check for special events
                if self.tokens[i+1] != 'port':
                    event = Event(identifier=rmsym(self.tokens[i+1]))
                    self.component.addEvent(event)

            i += 1

    # Returns the Parser's Component
    def getComponent(self):
        return self.component
    # Prints all the tokens
    def toStringTokens(self):
        for token in self.tokens:
            print(token)

if __name__ == "__main__":
    main()