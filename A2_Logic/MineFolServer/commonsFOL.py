
from prover9_lib import add_option1, remove_fact
from prover9_lib import add_option2
from prover9_lib import add_fact
from prover9_lib import add_rule
from prover9_lib import check_problem
from prover9_lib import get_models
from prover9_lib import add_goal
from prover9_lib import builder
from prover9_lib import set_goal
from prover9_lib import set_goals
from prover9_lib import load_assumptions
from prover9_lib import check_usingMace4
from propety import Propety
from prover9_lib import remove_assumptions
from prover9_lib import remove_goals
from prover9_lib import remove_options
from util import *
from time import *
import re




def load_messages(filePath,prop,prop2):

    for i in range(1,prop.dim+1):
     for j in range(1,prop.dim+1):
        prop.at(i,j)[0]=0
        prop.at(i,j)[1]=""
        prop2.at(i,j)[0]=0
        prop2.at(i,j)[1]=""
    f=open(filePath)
    lines=f.readlines()
    form="(\d+) (\d+) (.+)\.(.+)"
    for line in lines:
     result= re.search(form,line)
     print("result:",result.group(1)," ; ",result.group(2)," ; ",result.group(3),";",result.group(4))
     prop2.set(int(result.group(1)),int(result.group(2)),result.group(4))
     prop.set(int(result.group(1)),int(result.group(2)),result.group(3))
    print(prop.myName + " loaded")

def load_obstacles(filePath,obst):

    for i in range(1,obst.dim+1):
     for j in range(1,obst.dim+1):
        obst.at(i,j)[0]=0
        obst.at(i,j)[1]=""
     
    f=open(filePath)
    lines=f.readlines()
    form="(\d+) (\d+)"
    for line in lines:
     result= re.search(form,line)
     obst.set(int(result.group(1)),int(result.group(2)),"")
    print(obst.myName + " loaded")

def check_safe(x,y,name="mine_fol"):
    set_goal("safe("+str(x)+","+str(y)+")")
    return check_usingMace4(name)

def check_prop(x,y,different_base=None,prop_name="mine",name="mine_fol"):
    set_goal(prop_name+"(" + str(x) + "," + str(y) + ")")
    return check_usingMace4(name,different_base=None)

def set_obst(i,j,obst_name="mine",different_base=None):
    add_fact(obst_name+"("+str(i)+","+str(j)+")",different_base)
    
    
def set_safe(i,j,different_base=None):
    add_fact("safe("+str(i)+","+str(j)+")",different_base)    
    
    

def grab_message(i,j,msgs,text,different_base=None):
    if msgs.at(i,j)[0]==1:
       print ("I can add  message")
       add_fact(msgs.at(i,j)[1],different_base)
       print(text.at(i,j)[1])

text = Propety(8, "message")
msgs = Propety(8, "message")
obst = Propety(8, "mine")
visited = Propety(8, "visited")





def build_dict_from_messages():
   dict=[]
   for i in range(1,msgs.dim+1):
       for j in range(1, msgs.dim+1):
           if msgs.at(i,j)[0]==1:
            dict.append({"x":j,"y":i,"msg":msgs.at(i,j)[1]})
   return dict

def build_dict_from_texts():
    dict = []
    for i in range(1, text.dim + 1):
        for j in range(1, text.dim + 1):
            if text.at(i, j)[0] == 1:
                dict.append({"x": j, "y": i, "text": text.at(i, j)[1]})
    return dict
def build_dict_from_obst():
    dict = []
    for i in range(1, obst.dim + 1):
        for j in range(1, obst.dim + 1):
            if obst.at(i, j)[0] == 1:
                dict.append({"x": j, "y": i})
    return dict

def set_visited_fol(i,j,different_base=None):
    remove_fact("-visited("+str(i)+","+str(j)+")",different_base)
    add_fact("visited("+str(i)+","+str(j)+")",different_base)

def check_win(different_base=None):
    print("check win")
    set_goal("Win")
    return check_usingMace4("mineFOL",different_base)


def check_lose(different_base=None):
    print("check lost")
    set_goal("-lose")
    return  not check_usingMace4("mineFOL",different_base)













