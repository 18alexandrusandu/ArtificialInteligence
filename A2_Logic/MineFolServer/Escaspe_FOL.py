from commonsFOL import *


keyx = 0
keyy = 0
doorx = 0
doory = 0

assunptions_ruler = []

import re


def get_keyx():
    return keyx

def get_keyy():
    return keyy

def get_doorx():
    return doorx
def get_doory():
    return doory

def load_key_door(path):

    print("key-door loaded")
    f = open(path)
    line = f.readline()
    result = re.search("(\d+) (\d+) (\d+) (\d+)", line)
    if not result == None:
        global keyy, keyx, doorx, doory
        print("found pattern")
        keyx = result.group(1)
        keyy = result.group(2)
        doorx = result.group(3)
        doory = result.group(4)


def setup_assumptions_escape_fol(n=9):
    add_option1("domain_size," + str(n))
    add_option2("arithmetic")
    add_fact("mine(x,y) | safe(x,y)")

    add_rule("mine(x,y)->-safe(x,y)")
    add_fact("safe(1,1)")


def setup_assumptions_rule_maker(n=9):
    add_rule("exists x exists y (x>=1 & y>=1  &  key(x,y) & visited(x,y) ) <-> key_found ", assunptions_ruler)
    add_rule("exists x (exists y (x>=1 & y>=1  &  visited(x,y) & door(x,y) )) <-> door_found", assunptions_ruler)
    add_rule("door(x,y) & door(z,w) -> x=z & y=w", assunptions_ruler)
    add_rule("key(x,y) & key(z,w) -> x=z & y=w", assunptions_ruler)
    add_rule("exists x exists y (x>=1 & y>=1  & (visited(x,y) & mine(x,y)) )-> lose", assunptions_ruler)
    add_rule("door_found & key_found <-> Win", assunptions_ruler)

    add_fact("key(" + str(keyy) + "," + str(keyx) + ")", assunptions_ruler)
    add_fact("door(" + str(doory) + "," + str(doorx) + ")", assunptions_ruler)
   # add_fact(" -(x="+str(doory)+") | -(y="+str(doorx)+")" +"-> -door(x,y)",assunptions_ruler)
    #add_fact(" -(x=" + str(keyy) + ") | -(y=" + str(keyx) + ")" + "-> -key(x,y)",assunptions_ruler)
    for i in range(1, n):
        for j in range(1, n):
            add_fact("-visited(" + str(i) + "," + str(j) + ")", assunptions_ruler)

    for i in range(1, n):
        for j in range(1, n):
            if obst.at(i, j)[0] == 1:
                add_fact("mine(" + str(i) + "," + str(j) + ")", assunptions_ruler)
            else:
                add_fact("-mine(" + str(i) + "," + str(j) + ")", assunptions_ruler)













def set_key(i, j):
    add_fact("key(" + str(i) + "," + str(j) + ")")


def set_door(i, j):
    add_fact("door(" + str(i) + "," + str(j) + ")")


def reset_page(n=9):
    print("reset")
    remove_assumptions()
    remove_assumptions(assunptions_ruler)
    remove_options()
    remove_goals()
    setup_assumptions_escape_fol(n)
    setup_assumptions_rule_maker(n)
    global visited
    visited = Propety(n, "visited")


def check_win(different_base=None):
    print( "check win")
    set_goal("-Win")
    return not check_usingMace4("EscapeJail", different_base)






