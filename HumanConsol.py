import ply.lex as lex
import ply.yacc as yacc
import subprocess
import shlex
import webbrowser

tokens = (
    'OPERATE',
    'TYPE',
    'OBJECT'
)

def t_OPERATE(t):
    r'^(O|o)pen|(C|c)lose '
    if t.value[1] == 'p':
        t.value = 0
    else:
        t.value = 3
    return t


def t_TYPE(t):
    r'(P|p)age|(a|A)pp|(d|D)ocument'
    if t.value[1] == 'a':
        t.value = 1
    elif t.value[1] == 'p':
        t.value = 0
    else:
        t.value = 2
    return t

t_OBJECT = r'[A-Za-z0-9\.]+$'
t_ignore = ' \t'
data = 'Open app ls'
lexer = lex.lex()
lexer.input(data)
#
# for tok in lexer:
#     print(tok)


def p_error(p):
    print("Sysntax error in input!")


def p_command(p):
    'command : OPERATE TYPE OBJECT'
    action = p[1] + p[2]
    # Close page/document
    if action > 3:
        print('Cannot do that.')
    # Open app
    elif action == 0:
        arg = shlex.split(p[3])
        p = subprocess.Popen(arg)
        print(p)
    # open page
    elif action == 1:
        print('Open page ' + p[3])
        webbrowser.open("https://www." + p[3], new=0)
    # open document
    elif action == 2:
        #to do
        print('Open document' + p[3])
    # close app
    else:
        print('Close app' + p[3])

parser = yacc.yacc()

while True:
    s = input('What can i do for you?\n')
    if s[0] == 'Bye':
        break
    parser.parse(s)