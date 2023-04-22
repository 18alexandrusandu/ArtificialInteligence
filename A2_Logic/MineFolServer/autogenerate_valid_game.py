
from propety import Propety
import random




def generate_random_bomb(obst,version,n=4,d=8):
    f= open("./games_configurations/bombs"+version,"w+")
    print("thisis my n",n)
    nr_bomb=n
    while nr_bomb>0:
    
        x= int(1+random.random()*d)
        y = int(1 + random.random() * d)
        if (not x==1) or (not y==1) & obst.at(x,y)[0]==0:
            obst.set_state(x,y,1)
            
            f.write(str(x)+" "+str(y)+"\n")
            nr_bomb-=1

def valid_position(i,j,obst,messages):
    if obst.at(i,j)[0]==0 and messages.at(i,j)[0]==0:
        return True
    else:
        return False
def build_valid_positions_list(obst,messages,n=9):
     list_valid=[]
     for i in range(1,n):
         for j in range(1, n):
            if valid_position(i,j,obst,messages):
                list_valid.append((i,j))
     return list_valid


def choice_message_position(obst,messages,n=9):
    index_try=0
    list=build_valid_positions_list(obst,messages,n=9)
    limit_tries = 10 * len(list)
    if len(list)>0:
     i1=int(1+random.random()*(len(list)-2))
     elm=list[i1]
     list.pop(i1)
     return elm
     
    else:
        return None






def build_random_fol_valid_messages(obst,version,nr_messages_to_build=10):
 f= open("./games_configurations/messages"+version,"w+")
 messages=Propety(obst.dim,"messages")
 texts=Propety(obst.dim,"texts")
 print("build ",nr_messages_to_build," messages")
  
 while nr_messages_to_build >0 :
     choice = int(1+random.random() * 18)
     position=choice_message_position(obst,messages,obst.dim)
     if not position ==None:
        if choice == 1:
             #give the location of a mine 
             bombs=[]
             for i in range(1,obst.dim+1):
                for j in range(1,obst.dim+1):
                   if obst.at(i,j)[0]==1:
                      bombs.append((i,j))
             if len(bombs)>0:         
              index=int(random.random()*(len(bombs)-1))
              messages.at(position[0],position[1])[0]=1
              texts.at(position[0],position[1])[0]=1
              f.write(str(position[0])+" "+ str(position[1])+" "
              +"mine("+str(bombs[index][0]) +","+str(bombs[index][1])+")."
               +" mine on location "+"("+str(bombs[index][0]) +","+str(bombs[index][1])+")\n")
              nr_messages_to_build-=1
             continue
        if choice == 2:
                  #give the location of a free position
              no_bombs=[]
              for i in range(1,obst.dim+1):
                for j in range(1,obst.dim+1):
                   if obst.at(i,i)[0]==0:
                      no_bombs.append((i,j))
              if len(no_bombs)>0:       
               index=int(random.random()*(len(no_bombs)-1))
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(str(position[0])+" "+ str(position[1])+" "
               +"-mine("+str(no_bombs[index][0]) +","+str(no_bombs[index][1])+")."
               +"no mine on location "+"("+str(no_bombs[index][0]) +","+str(no_bombs[index][1])+")\n")
               nr_messages_to_build-=1
              continue
        if choice == 3:

            # check for a free main diagonal
            free_d=True
            for i in range(1,obst.dim+1):
              if obst.at(i,i)[0]==1:
                free_d=False
     
            if free_d:
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(str(position[0])+" "+ str(position[0])+" "
               +"-(exists x (x>=1 & mine(x,x)))."
               +  "no mine on the main diagonal "+"\n")
               nr_messages_to_build-=1
               continue
        if choice == 4:
            # check free second diagonal
            free_d=True
            for i in range(1,obst.dim+1):
              if obst.at(i,obst.dim-1-i)[0]==1:
                free_d=False
            if free_d:
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(str(position[0])+" "+ str(position[1])+" "
               +"-(exists x (x>=1 &  mine(x,"+str(obst.dim)+"-x)))."
               +" no mine on the second diagonal "+"\n")
               nr_messages_to_build-=1
               continue
        if choice == 5:
            # check for a free row
            free_lines=[]
            for i in range(1,obst.dim+1):
                free_line=True
                for j in range(1,obst.dim+1):
                    if obst.at(i,j)[0]==1:
                        free_line=False
                if free_line:
                       free_lines.append(i)
            if len(free_lines)>0 :
               index=int(random.random()*(len(free_lines)-1))
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
                str(position[0])+" "+ str(position[1])+" "+
               "-(exists x (x>=1 &  mine("+str(free_lines[index])+",x)))."+
               " no mine on the row "+str(free_lines[index])+"\n")
               nr_messages_to_build-=1
            continue
        if choice == 6:
              #check for free column 
            free_columns=[]
            for i in range(1,obst.dim+1):
                free_column=True
                for j in range(1,obst.dim+1):
                    if obst.at(j,i)[0]==1:
                        free_column=False
                if free_column:
                       free_columns.append(i)
            if len(free_columns)>0 :
               index=int(random.random()*(len(free_columns)-1))
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1  
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "-(exists x (x>=1 & mine(x,"+str(free_columns[index])+")))."+
               " no mine on column "+str(free_columns[index])+"\n")
               nr_messages_to_build-=1
            continue
          
        if choice == 7:
            # check general simetry x,z =z,x 1.
             simetry1=True
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                    if not obst.at(i,j)==obst.at(j,i):
                       simetry1=False
             if simetry1:
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "mine(x,y)->mine(y,x)."+
               "mines are disposed simetric by the main diagonal"+"\n")
               nr_messages_to_build-=1
             continue
            
        if choice == 8:
            # check general simetry x,8-x,  1.
             simetry1=True
             for i in range(1,obst.dim+1):
                for j in range(1,obst.dim+1):
                    if not obst.at(i,j)==obst.at(obst.dim-j,obst.dim-i):
                       simetry1=False
             if simetry1:
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "mine(x,y)->mine(8-y,8-x)."+
               "mines are disposed simetric by the second diagonal"+"\n")
               nr_messages_to_build-=1
             continue
        if choice == 9:
           #check same line positioning
           same_lines=[]
           for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
        
                 same_line=True
                 for k in range(1,obst.dim+1):
                   if i==j or not obst.at(i,k)==obst.at(j,k)  :
                     same_line=False
                 if same_line==True:
                    same_lines.append((i,j))
           if len(same_lines)>0:
               index=int(random.random()*(len(same_lines)-1))
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists x (x>=1 & mine("+str(same_lines[index][0])+",x)->mine("+str(same_lines[index][1])+",x))."+
               "if there is a mine on the line "+str(same_lines[index][0])+" there is a bomb on the line "+str(same_lines[index][1])+"at the same column"+"\n")
               nr_messages_to_build-=1
           continue
        if choice == 10:
              #check same column positioning
           same_columns=[]
           for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
        
                 same_column=True
                 for k in range(1, obst.dim+1):
                   if i==j or not obst.at(k,i)==obst.at(k,j):
                     same_column=False
                 if same_column==True:
                    same_columns.append((i,j))
           if len(same_columns)>0:
               index=int(random.random()*(len(same_columns)-1))
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists x (x>=1 & mine(x,"+str(same_columns[index][0])+")->mine(x,"+str(same_columns[index][1])+"))."+
               "if there is a mine on the column "+str(same_columns[index][0])+" there is a bomb on the column "+str(same_columns[index][1])+" at the same column"+"\n")
               nr_messages_to_build-=1
           continue
           if choice == 11:
            # check general simetry x,z =z,x 1.
             simetrics=[]
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                  simetry1=True
                  for k  in range(1,obst.dim+1):
                    if not obst.at(i,k)==obst.at(k,j):
                       simetry1=False
                  if simetry1:
                    simetrics.append((i,j))
                    
             if len(simetrics)>0:
               index_s=int(random.random()*(len(simetrics)+1))     
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "mine("+str(simetrics[index_s][0])+",y)<->mine(y,"+str(simetrics[index_s][1])+")."+
               "if there are mines on the row"+str(simetrics[index_s][0])+"there are mines on the  column"+ +str(simetrics[index_s][1])+"at the same row as the colum from the first row \n")
               nr_messages_to_build-=1
             continue
             
        if choice == 12:
            # no bomb on a row lower than the bomb with the smallest index
             minim=obst.dim+2
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                        if i<minim:
                           minim=i
             if  not minim<=1:                  
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists y (y<"+str(minim)+"-> -mine(y,x))."
               "No mine has the row smaller than "+str(minim)+"\n")
               nr_messages_to_build-=1
             continue 
        if choice == 13:
            # no bomb on a column lower than the bomb with the smallest index
             minim=obst.dim+2
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                        if j<minim:
                           minim=j
             if  not minim<=1:                   
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists x (x<"+str(minim)+"-> -mine(y,x))."
               "No mine has the column smaller than "+str(minim)+"\n")
               nr_messages_to_build-=1
             continue 
        if choice == 14:
            # no bomb on a row bigger than the bomb with the biggest index
             maxim=-1
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                        if i>maxim:
                           maxim=i
             if  not maxim>=obst.dim:               
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists y (y>"+str(maxim)+"-> -mine(y,x))."
               "No mine has the row bigger than "+str(maxim)+"\n")
               nr_messages_to_build-=1
             continue             
        if choice == 15:
            # no bomb on a column bigger than the bomb with the biggest index
             maxim=-1
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                        if j>maxim:
                           maxim=j
             if  not maxim>=obst.dim:                    
               messages.at(position[0],position[1])[0]=1
               texts.at(position[0],position[1])[0]=1
               f.write(
               str(position[0])+" "+ str(position[1])+" "+
               "exists x (x<"+str(maxim)+"-> -mine(y,x))."
               "No mine has the column smaller than "+str(maxim)+"\n")
               nr_messages_to_build-=1
             continue  
        if choice == 16:
            # share the position of two boms
             chosen_first=False
             chosen_second=False
             i1=[0,0]
             i2=[0,0]
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                         if chosen_first==False:
                           i1[0]=i
                           i1[1]=j
                           chosen_first=True
                         else:
                          if chosen_second==False:
                           i2[0]=i
                           i2[1]=j
                           chosen_second=True
             f.write(
             str(position[0])+" "+ str(position[1])+" "+
             "mine("+str(i1[0])+","+str(i1[1])+")->mine("+str(i2[0])+","+str(i2[1])+")."+
             "if there is one mine on ("+str(i1[0]) +","+str(i1[1]) +") than there is one also on ("+str(i2[0]) +","+str(i2[1]) +")\n")
             nr_messages_to_build-=1
             continue               
        if choice == 17:
            # a bomb on a line
             bombs=[]
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                      bombs.append((i,j))
             bomb= random.choice(bombs)
             f.write(
             str(position[0])+" "+ str(position[1])+" "+
             "existx x (x>=1 & mine("+str(bomb[0])+",x))."+
             "there is at least a mine on line "+str(bomb[0])+"\n")
             nr_messages_to_build-=1
             continue 
        if choice == 18:
            # a bomb on a column
             bombs=[]
             for i in range(1,obst.dim+1):
                for j in range(1, obst.dim+1):
                     if obst.at(i,j)[0]==1:
                      bombs.append((i,j))
             bomb= random.choice(bombs)
             f.write(
             str(position[0])+" "+ str(position[1])+" "+
             "exists x (x>=1 & mine(x,"+str(bomb[1])+"))."+
             "there is at least a mine on column "+str(bomb[1])+"\n")
             nr_messages_to_build-=1
             continue    
     else:
      f.close()
      return messages
 f.close()
 return messages 

import sys
  
n=4
version="_3"
nr_m=10

def process_argv():
 global n,version,nr_m
 for a in sys.argv:
   if a=="-n_b":
       n=int(sys.argv[sys.argv.index(a)+1])
   if a=="-n_m":
       nr_m= int(sys.argv[sys.argv.index(a)+1])
   if a=="-v":
       version=sys.argv[sys.argv.index(a)+1]
  
if __name__ == "__main__":
  obst=Propety(8,"mines")
  process_argv()
  print "here",n
  generate_random_bomb(obst,version,n)
  build_random_fol_valid_messages(obst,version,nr_m)
  
  
  
  
  
  

