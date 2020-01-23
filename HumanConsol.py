import ply.lex as lex
import ply.yacc as yacc
import subprocess
import webbrowser
import re
import os
from sys import platform

tokens = (
    'OPERATE',
    'TYPE',
    'OBJECT'
)


def t_OPERATE(t):
    r'((P|p)leas|(C|c)an(y|Y)ou)?((O|o)pen|(C|c)lose|(S|s)top|(K|k)ill|(S|s)tart)'
    if re.search(r'((o|O)pen|(S|s)tart)', t.value) is not None:
        t.value = 0
    else:
        t.value = 3
    return t


def t_TYPE(t):
    r'(P|p)age|(W|w)ebpage|(S|s)ite|(a|A)pp(lication)?|(d|D)oc(ument)?|(F|f)ile|(P|p)rogram'
    if t.value[1] == 'a' or t.value[1] == 'e' or (t.value[1] == 'i' and t.value[2] == 't'):
        t.value = 1
    elif t.value[1] == 'p' or t.value[1] == 'r':
        t.value = 0
    else:
        t.value = 2
    return t


def t_error(t):
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t


t_OBJECT = r'[A-Za-z0-9\./_\-\:\\]+$'
t_ignore = ' \t'
data = 'Open app ls'
lexer = lex.lex()


def p_error(p):
    print("Sysntax error in input!")


def p_command(p):
    'command : OPERATE TYPE OBJECT'
    action = p[1] + p[2]
    # Close page/document
    try:
        if action > 3:
            print('Cannot do that.')
    # Open app
        elif action == 0:
            if platform[0] == 'd':
                subprocess.call(('open', p[3]))
            elif platform[0] == 'w':
                os.startfile(p[3])
            else:
                subprocess.call(('xdg-open', p[3]))
    # open page
        elif action == 1:
            print('Open page ' + p[3])
            webbrowser.open("https://www." + p[3], new=0)
    # open document
        elif action == 2:
        #to do
            if platform[0] == 'd':
                subprocess.call(('open', p[3]))
            elif platform[0] == 'w':
                os.startfile(p[3])
            else:
                subprocess.call(('xdg-open', p[3]))
    # close app
        else:
            print('Close app' + p[3])
            if platform[0] == "w":
                subprocess.Popen("TASKKILL /F /IM " + p[3])
            elif platform[0] == "l":
                output = subprocess.Popen("ps -ef | grep " + p[3])
                pid = re.search(r'\d', output)
                subprocess.Popen("kill -9 " + pid)
    except Exception as e:
        print(e)

parser = yacc.yacc()

while True:
    s = input('What can i do for you?\n')
    if re.search(r'^((B|b)ye|(G|g)oodbey|(e|E)xit)$', s) is not None:
        break
    parser.parse(s)
