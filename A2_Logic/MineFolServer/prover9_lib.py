
from __future__  import print_function
import re
import subprocess

options1 =[]
options2 =[]
# this is the default base for assumptions another one can be used
assumptions =[]
goals =[]
lists =[]

builder= lambda  :  print ("no knowledge function given")


def build_file(path ,diferent_base=None):
    f = open(path, "w")

    for option in options1:
        f.write("assign(" + option + ").\n")

    for option in options2:
        f.write("set(" + option + ").\n")

    #
    # f.write("list(distinct).\n")
    # for list in lists:
    #     f.write(list+"." + "\n")
    # f.write("end_of_list.\n")

    f.write("formulas(assumptions).\n")

    if diferent_base==None:
      for assumption in assumptions:
        f.write(assumption + "\n")
    else:
      for assumption in diferent_base:
         f.write(assumption + "\n")



    f.write("end_of_list.\n")

    f.write("formulas(goals).\n")
    for goal in goals:  # add
      f.write(goal + "\n")
    f.write("end_of_list.\n")
    # add goals   f.close()
    f.close()

def build_file2(path ,diferent_base=None):
    f = open(path, "w")

    for option in options1:
        f.write("assign(" + option + ").\n")

    for option in options2:
        f.write("set(" + option + ").\n")

    #
    # f.write("list(distinct).\n")
    # for list in lists:
    #     f.write(list+"." + "\n")
    # f.write("end_of_list.\n")

    f.write("formulas(assumptions).\n")
    if diferent_base==None:
      for assumption in assumptions:
        f.write(assumption + "\n")
    else:
        for assumption in diferent_base:
            f.write(assumption + "\n")
    for goal in goals:
        f.write(goal + "\n")
    f.write("end_of_list.\n")
    # add goals
    f.close()

def load_assumptions(filePath ,diferent_base=None):
    f=open (filePath)
    lines=f.readlines()
    for line in lines:
        add_fact(line,diferent_base)

def set_goal(goal):
    goals[:]=[]
    add_goal(goal)

def set_goals(goals2):
    goals[:]=[]
    for goal in goals2:
        add_goal(goal)



def add_rule(assumption,diferent_base=None):
    assumption=assumption+"."
    if diferent_base==None:
        assumptions.append(assumption)
    else:
        diferent_base.append(assumption)

def add_fact(assumption,diferent_base=None):
    assumption=assumption+"."
    if diferent_base == None:
        assumptions.append(assumption)
    else:
        diferent_base.append(assumption)

def add_goal(goal):
    goal=goal+"."
    goals.append(goal)

def add_option1(option):
    options1.append(option)
def add_option2(option):
    options2.append(option)



def remove_goals():
    goals[:]=[]

def remove_assumptions(diferent_base=None):
    if diferent_base==None:
        assumptions[:]=[]
    else:
        diferent_base[:]=[]



def remove_options():
    options1[:]=[]
    options2[:]=[]


def remove_fact(assumption,different_base=None):
 if different_base==None:
   if assumption+"." in assumptions:
     assumptions.remove(assumption+".")
 else:
   if assumption+"." in different_base:
     different_base.remove(assumption+".")




#used for inference in this project
def check_usingMace4(name="mineFOL",different_base=None,domain=9,build=None):
    print("Name of problem is", name)
    path = "mace4_builder.in"
    patho = "mace4_model.out"
    if not different_base==None:
     path = "mace4_builder_master.in"
     patho = "mace4_model_master.out"
    
    list_cmd = []
    models = []
    nr_models=0
    if not build == None:
        remove_options()
        remove_assumptions(different_base)
        remove_goals()
        build()
    program="mace4"
    list_cmd.append(program)
    list_cmd.append("-m")
    list_cmd.append("3")
    list_cmd.append("-n")
    list_cmd.append(str(domain))
    list_cmd.append("-c")
    list_cmd.append("-f")
    list_cmd.append(path)

    g = open(patho, "w")
    build_file2(path,different_base)
    subprocess.call(list_cmd, stdout=g)
    g.close()
    g = open(patho, "r")
    res = g.read()
    found = False
    if program=="mace4":
      result = re.search(r"\nExiting with (\d+) models.\n", res)
      if result:
        print("somehow result")
        nr_models=int(result.group(1))
        string_start="============================== MODEL ================================="
        string_end="============================== end of model =========================="
        string_antet="interpretation\\((.*?)\\], \\["
        string_model="([^\s].+)+"
        result2=re.findall(string_model,res)

        if result2:
          model1 = []
          start=False
          for r in result2:
            # print(r)
            rs=re.search(string_start,r)
            if rs:
              start=True
            else:
              if start==True:
                  rE = re.search(string_end, r)
                  if rE:
                      start = False
                      print("mod el", model1)
                      models.append(model1)
                      model1 = []
                  else:
                     ra=re.search(string_antet,r)
                     if not ra:
                       string_begin_line="relation\\((.*?), \\[(.*?)\ \]"
                       result3 = re.search(string_begin_line, r)
                       if not result3==None:
                          model1.append((result3.group(1),int(result3.group(2))))
      # print ("model found:", models)
      if nr_models>=1:
          return True
      else:
          return False


#getting all models mace4 can produce not to be used for inference ,switches on prover9 if given goals
def get_models(name,different_base=None,domain=2 , build=None):
    print("Name of problem is", name)
    path = "mace4_builder.in"
    patho = "mace4_model.out"
    if not different_base==None:
     path = "mace4_builder_master.in"
     patho = "mace4_model_master.out"
    
    list_cmd = []
    models=[]
    nr_models=0
    if not build == None:
        remove_options()
        remove_assumptions(different_base )
        remove_goals()
        build()
    program="mace4"
    if len(goals) > 0:
        print("Gaols were given routed on prover9")
        program="prover9"
        list_cmd.append(program)

    else:
        list_cmd.append(program)
        list_cmd.append("-m")
        list_cmd.append("-1")
        list_cmd.append("-n")
        list_cmd.append(str(domain))
        list_cmd.append("-c")

    g = open(patho, "w")
    build_file(path,different_base)
    list_cmd.append("-f")
    list_cmd.append(path)
    subprocess.call(list_cmd, stdout=g)
    g.close()
    g = open(patho, "r")
    res = g.read()
    found = False

    if program=="mace4":
      print("model found:", models)
      result = re.search( '"r " \nExiting with (\d+) models.\n""', res)
      if result:
        print("groups are", result.groups())
        print("group i searched for is:", result.group(1))
        nr_models=int(result.group(1))
        string_start="============================== MODEL ================================="
        string_end="============================== end of model =========================="
        string_antet="interpretation\\((.*?)\\], \\["
        string_model="([^\s].+)+"
        result2=re.findall(string_model,res)

        if result2:
          model1 = []
          start=False
          for r in result2:
            print(r)
            rs=re.search(string_start,r)
            if rs:
              start=True
            else:
              if start==True:
                  rE = re.search(string_end, r)
                  if rE:
                      start = False
                      print("model", model1)
                      models.append(model1)
                      model1 = []
                  else:
                     ra=re.search(string_antet,r)
                     if not ra:
                        string_begin_line="relation\\((.*?), \\[(.*?)\\]"
                        result3 = re.search(string_begin_line, r)
                        if result3:
                          model1.append((result3.group(1),int(result3.group(2))))
                        else:
                           string_begin_line="function\\((.*?), \\[(.*?)\\]"
                           result3 = re.search(string_begin_line, r)
                           if result3:
                            model1.append((result3.group(1),int(result3.group(2))))
                           
      print("model found:", models)

    else:
        found = res.find("\nTHEOREM PROVED\n")
        if found > 0:
            found = True
        else:
            found = False

        return found

    return (nr_models,models)

#used to check using prover9 ,not used at this project
def check_problem(name,different_base=None,build=None):

    print("Name of problem is",name)
    path="prover_provers.in"
    patho="prover_proved.out"
    list_cmd=[]

    if not build==None:
        remove_options()
        remove_assumptions(different_base)
        remove_goals()
        build()

    program = "prover9"
    if len(goals)==0:
     program="mace4"
     list_cmd.append(program)
     list_cmd.append("-m")
     list_cmd.append("-1")
     list_cmd.append("-n")
     list_cmd.append("2")
     list_cmd.append("-c")
    else:
      list_cmd.append(program)
    g=open(patho,"w")

    build_file(path,different_base)
    list_cmd.append("-f")
    list_cmd.append(path)
    subprocess.call(list_cmd,stdout=g)
    g.close()
    g = open(patho, "r")
    res=g.read()
    found=False
    if program == "prover9":
      found=res.find("\nTHEOREM PROVED\n")
      if found>0:
        found=True
      else:
        found=False
    else:

        result=re.search(r"\nExiting with (\d+) models.\n",res)

        if result:
          print("groups are",result.groups())
          print("group i searched for is:",result.group(1))
          found=True
        else:
          found=False
    print(found)
    return found




def exists(domain,rule):
  for dom in domain :
      if rule(dom):
          return True
  return False

def all(domain,rule):
    for dom in domain:
         if not rule(dom):
             return False
    return True



def isTautology(rule,nr_variables ,domain_of_variables=[0,1 ], variables=[]):
       var=False
       for d in domain_of_variables:
            variables.append(d)
            if nr_variables==1:
               if not rule(variables):
                   return  False
               else:
                   return True
            else:
                var=var and isTautology(rule, nr_variables-1,domain_of_variables,variables)
       return var




def isPureLiteral(rules,nr_variables_rules,nr_rules,nr_literal_rules,domain_variables=[ 0,1]):
    return False
  



    
