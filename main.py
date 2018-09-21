import re
 
class Literal: #CLass Literal, it has attributes name and sign to denote whether the literal is positve or negative in use
   def __init__(self,name, sign = True ):
       self.name = str(name)
       self.sign = sign
 
   def __neg__(self): #returns a new literal with the same name but the opposite sign of its parent literal
       return Literal(self.name, False)
 
   def __str__(self):
       return str(self.name)
 
   def __repr__(self): #returns the string of the literal name,( or the string with a negative sign) each time the instance of the ltieral is called
       if self.sign:
           return '%r' %str(self.__str__())
       else:
           return '%r' %str("-" + self.__str__())
 
def CNFconvert(KB): #This function converts the Kb from a list of sets to a list of list for easire computing
   storage = []
   for i in KB:
       i = list(i)
       for j in i:
           j = str(j)
       storage.append(i)
   return storage
 
def VariableSet(KB): #This function finds all the used literals in the KB, and in order to assist with running the DPLL
   KB = eval((CNFconvert(KB).__str__()))
   storage = []
   for obj in KB:
       for item in obj:
           if item[0] == '-' and item[1:] not in storage:
               storage.append(str(item[1:]))
           elif item not in storage and item[0] != '-':
               storage.append(str(item))
   return storage
 
def Negativeofx(x): #This function is for holding the negative form of the literal, for use in the DPLL algorithm
   check = re.match("-",str(x))
   if(check):
       return str(x[1:])
   else:
       return "-"+str(x)
 
def pickX(literals,varList): #This function picks a literal from the variable set and works with it as a node in the tree
   for x in varList:
       if x not in literals:
           break
   return x
 
def splitFalseLiterals(cnf,x):
   holder = []
   for item in cnf:
       if x in item:
           item.remove(x)
       holder.append(item)
   return holder
 
def splitTrueLiteral(cnf,x):
   holder = []
   for item in cnf:
       if x in item:
           continue
       else:
           holder.append(item)
   return holder
 
def unitResolution(clauses):
   literalholder = {}  #dictionary for holding the literalholder and their bool
   i = 0
   #  This part of the code goes through each and every clause until the all literals in the KB are resolved
   while i < len(clauses): #for each clause
       newClauses = []
       clause = clauses[i]
       # picks a clause to work on
       if(len(clause) == 1):
           literal = str(clause[0])
           pattern = re.match("-",literal)
           # Populates the dictionary
           if(pattern):
               nx = literal[1:]
               literalholder[nx] = False
           else:
               nx = "-"+literal
               literalholder[literal] = True
           # Checks for all other appearances o the literal or its opposite int he KB
           for item in clauses:
               if item != clauses[i]:
                   if(nx in item):
                       item.remove(nx)
                       newClauses.append(item)
           i = 0
           clauses = newClauses
       # no unit clause
       else:
           i += 1
   return literalholder, clauses
 
def dpll(clauses,varList):#recursively performs the dpll algorithm
   literals, cnf = unitResolution(clauses)
   if(cnf == []):
       return literals
   elif([] in cnf):
       return "notsatisfiable"
   else:
       # pick a literal which isn't set yet but has an impact on the Kb, and then work on it recursively
       while True:
           x = pickX(literals,varList)
           x = str(x)
           nx = Negativeofx(x)
 
           ncnf = splitTrueLiteral(cnf,x)
           ncnf = splitFalseLiterals(ncnf,nx)
           if ncnf == cnf:
               varList.remove(x)
           else:
               break
       # does the same dpll recursively, but follows the true path for that variable
       case1 = dpll(ncnf,varList)
       if(case1 != "notsatisfiable"):
           copy = case1.copy()
           copy.update(literals)
           copy.update({x: True})
           return copy
 
       # does the dpll recursively, but follows the false path for that variable
       case1 = dpll(ncnf,varList)
       if not case1:
           copy = case1.copy()
           copy.update(literals)
           copy.update({x: False})
           return copy
       else:
           return "notsatisfiable"
 
def DPLL(KB): #Finally restructures the output to fit the required output by the assignment description
   KB=eval((CNFconvert(KB).__str__()))
   varList = VariableSet(KB)
   result = dpll(KB, varList)
   if result == 'notsatisfiable':
       False
   else:
       for i in varList:
           if i in result and result[i] == True:
               result[i] = 'true'
           elif i in result and result[i] == False:
               result[i] = 'false'
           else:
               result[i] = 'free'
   return [True, result]
 
A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
KB = [{A,B},{A,-C},{-A,B,D}]
print DPLL(KB)
