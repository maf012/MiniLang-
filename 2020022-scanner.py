import re

class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

class Scanner:
    def __init__(self, filename):
        self.filename = filename
        self.keywords = {'if', 'else', 'print', 'true', 'false'}
        self.operators = {'+', '-', '*', '/', '=', '==', '!='}
        self.tokens = []

    def scan(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines):
                line = line.strip()
                position = 0
                while position < len(line):
                    if line[position].isspace():
                        position += 1
                    elif line[position] == '/':
                        if position + 1 < len(line) and line[position + 1] == '/':
                            break  # ignore the rest of the line as a comment
                        else:
                            self.report_error(line_num + 1, position + 1, "Invalid character '/'")
                            position += 1
                    elif line[position].isalpha():
                        identifier = ''
                        while position < len(line) and (line[position].isalnum() or line[position] == '_'):
                            identifier += line[position]
                            position += 1
                        if identifier in self.keywords:
                            self.tokens.append(Token(identifier.upper(), identifier))
                        else:
                            self.tokens.append(Token('IDENTIFIER', identifier))
                    elif line[position].isdigit():
                        number = ''
                        while position < len(line) and line[position].isdigit():
                            number += line[position]
                            position += 1
                        self.tokens.append(Token('INTEGER', number))
                    elif line[position] in self.operators:
                        operator = line[position]
                        self.tokens.append(Token('OPERATOR', operator))
                        position += 1
                    else:
                        self.report_error(line_num + 1, position + 1, "Invalid character '{}'".format(line[position]))
                        position += 1
        return self.tokens

    def report_error(self, line_num, column_num, message):
        print("Error at line {}, column {}: {}".format(line_num, column_num, message))


if __name__ == '__main__':
    scanner = Scanner('sample.minilang')
    tokens = scanner.scan()
    for token in tokens:
        print(token.type, token.lexeme)