# coding=utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from commonsFOL import *

assunptions_ruler=[]






def setup_assumptions_mine_fol(n=9):
    add_option1("domain_size,"+str(n))
    add_option2("arithmetic")
    add_fact("mine(x,y) | safe(x,y)")
    add_rule("mine(x,y)->-safe(x,y)")
    add_rule("-safe(x,y)->mine(x,y)")
    
    add_fact("safe(1,1)")


def setup_assumptions_rule_maker(n=9):
    add_rule(" exists x  exists y  (x>=1  & y>=1 & -visited(x,y) & -mine(x,y))  ->-Win",assunptions_ruler)
    add_rule(" exists x exists y (x>=1 & y>=1  & (visited(x,y) & mine(x,y)) ) -> lose",assunptions_ruler)
    for i in range(1, n):
        for j in range(1, n):
          if  (not (i==1) ) or  (not (j==1)):
            add_fact("-visited(" + str(i) + "," + str(j) + ")",assunptions_ruler)
          else:
            add_fact("visited(" + str(i) + "," + str(j) + ")",assunptions_ruler)

    for i in range(1,n):
        for j in range(1, n):
            if obst.at(i,j)[0]==1:
                add_fact("mine(" + str(i) + "," + str(j) + ")",assunptions_ruler)
            else:
                add_fact("-mine(" + str(i) + "," + str(j) + ")",assunptions_ruler)



def reset_page(n=9):
    print("reset")
    remove_assumptions()
    remove_assumptions(assunptions_ruler)
    remove_options()
    remove_goals()
    setup_assumptions_mine_fol(n)
    setup_assumptions_rule_maker(n)
    global visited
    visited=Propety(n, "visited")







