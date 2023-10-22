'''
Mount Symbols
    Loads a list of valid symbols for the parser/lexer to use
    for validation.
'''
def mount_symbols():
    with open("./lib/symbols", 'r') as f:
        valid_symbols = []
        for symbol in f:
            valid_symbols += symbol.replace('\n', '')
        return valid_symbols

'''
Mount Reserved
    Loads a list of reserved words for the parser.
'''
def mount_reserved():
    with open("./lib/reserved", 'r') as f:
        valid_words = []
        for symbol in f:
            valid_words.append(symbol.replace('\n', ''))
        return valid_words

'''
Get Input
    Grabs the input file located in the main directory
    called "input.fpp".
'''
def get_input():
    with open("./port.fpp", 'r') as f:
        return f.read()

def main():
    # Initializing vars
    valid_symbols = mount_symbols()
    reserved_words = mount_reserved()
    
    # Tokenize File
    tokenizer = Tokenizer(get_input())

'''
Parameter
    FORMAT -> [ ref ] identifier : type-name
'''
class Parameter:
    TYPE = 'parameter'
    def __init__(self):
        self.identifier = ''
        self.type_name = ''

'''
Port
    FORMAT -> port identifier [ ( param-list ) ] [ -> type-name ]
'''
class Port:
    TYPE = 'port'
    def __init__(self):
        self.identifier = ''
        self.param_list = [] # Type : <Parameter>
        self.type_name = ''

'''
Port Instance Specifier

'''
class PortInstanceSpecifier:
    VALID_INPUT_KIND = ['async', 'guarded', 'sync'] # Requires the input tag to follow it
    VALID_OUTPUT_KIND = ['output']
    
    def __init__(self,general_port_kind='', identifier='', num_ports=-1, 
                 port_instance_type='', queue_full_behavior='',special_port_kind=None,
                 priority=None):
        self.general_port_kind = general_port_kind # <async input, guarded input, sync input, guarded>
        self.identifier = identifier
        self.num_ports = num_ports
        self.port_instance_type = port_instance_type # <qual_ident, serial> qual_ident Fw.Com
        self.queue_full_behavior = queue_full_behavior # <assert, block, drop>
        self.special_port_kind = special_port_kind
        self.priority = priority # Must be convertable to Integer
        self.description = '' # Description from "@" comments

'''
Tokenizer class

'''
class Tokenizer:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.buffer = ''
        self.tokenize()
    
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
            else:
                if self.input[i] == '\n' and i+1 < len(self.input):
                    # If there is something in the buffer save it
                    if not self.isEmpty():
                        self.save_buffer()
                    # Parse until no more newlines or spaces
                    while self.input[i] == '\n' or self.input[i] == ' ':
                        i += 1
                    self.tokens.append("\n")
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
                else:
                    self.buffer += self.input[i]
                    i += 1
        if not self.isEmpty():
            self.save_buffer()
        self.printBuffer()
    
    def parse(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i] == 'port':
                if self.tokens[i-1] == 'input':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-2]))
                elif self.tokens[i-1] == 'output':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-1]))
            i+=1
    
    def printBuffer(self):
        for token in self.tokens:
            print(token)


# Init
if __name__ == "__main__":
    main()
