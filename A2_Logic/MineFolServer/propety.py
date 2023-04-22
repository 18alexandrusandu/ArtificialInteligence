class Propety:
   def __init__(self,dim,name):
    self.myName=name
    self.locations=[]
    self.dim=dim
    for i in range(1,dim+1):
        rowList=[]
        for j in range(1,dim+1):
          rowList.append([0,""])
        self.locations.append(rowList)

   def at(self,i,j):
      return self.locations[i-1][j-1]
   def set(self,i,j,msg):
        self.locations[i-1][j-1][0]=1
        self.locations[i-1][j-1][1] = msg

   def set_state(self, i, j,nr=-1):
       self.locations[i - 1][j - 1][0] =nr
       self.locations[i - 1][j - 1][1] = ""




   def take_prop(self,i,j):
    if not self.locations[i-1][j-1][0]==0:
        return self.locations[i-1][j-1][1]
    else:
        return ""
