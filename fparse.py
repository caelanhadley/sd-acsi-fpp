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

'''
Tokenizer

'''
def tokenizer(input, reserved_words, valid_symbols):
    tokens = []
    token_buffer = ""
    comment_flag = 0
    newline_flag = 0

    for c in input:
        if c == '#'or c == "@": comment_flag = 1 # note: Consider moving @ comments into a different area so they can be stored
        if comment_flag:
            if c == '\n': comment_flag = 0
            else: continue
        if (c != ' ' and c != '\n'):
            token_buffer += c
        elif (token_buffer != ""):
            tokens.append(token_buffer)
            token_buffer = ''
    return tokens

def parser(tokens):
    index = 0
    while index < len(tokens):
        if tokens[index] == 'port':
            print(f"PORT => {tokens[index - 2]} {tokens[index - 1]} {tokens[index]} {tokens[index + 1]}")
        index += 1



def temp(reserved_words, token_buffer):
    match_buffer = "NONE"
    for word in reserved_words:
        if token_buffer == word:
            match_buffer = word
def main():
    # Initializing vars
    valid_symbols = mount_symbols()
    reserved_words = mount_reserved()
    
    # Tokenize File
    # tokens = tokenizer(get_input(), reserved_words, valid_symbols)
    tokenizer = Tokenizer(get_input())

'''
Parameter
    FORMAT
    [ ref ] identifier : type-name
'''
class Parameter:
    TYPE = 'parameter'
    def __init__(self):
        self.identifier = ''
        self.type_name = ''

'''
Port
    FORMAT
    port identifier [ ( param-list ) ] [ -> type-name ]
'''
class Port:
    def __init__(self):
        self.identifier = ''
        self.param_list = [] # Type : <Parameter>
        self.type_name = ''

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

class Tokenizer:
    def __init__(self, input):
        self.input = input
        self.tokens = []
        self.buffer = ''
        self.tokenize()
    
    # Saves the contents of the buffer
    def save(self):
        print(self.buffer)
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
                self.save()
                i += 1
            else:
                if self.input[i] == '\n' and i+1 < len(self.input):
                    # If there is something in the buffer save it
                    if not self.isEmpty():
                        self.save()
                    # Parse until no more newlines or spaces
                    while self.input[i] == '\n' or self.input[i] == ' ':
                        i += 1
                    self.tokens.append("\n")
                else:
                    self.buffer += self.input[i]
                    i += 1
        if not self.isEmpty():
            self.save()
        self.parse()
    
    def parse(self):
        i = 0
        while i < len(self.tokens):
            if self.tokens[i] == 'port':
                if self.tokens[i-1] == 'input':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-2]))
                elif self.tokens[i-1] == 'output':
                    port = PortInstanceSpecifier(general_port_kind=(self.tokens[i-1]))
            i+=1


# Init
if __name__ == "__main__":
    main()