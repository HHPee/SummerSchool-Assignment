'''
NAME:HARIHARAN P
ROLL NO: EE20B042
EE2703 ASSIGNMENT 2 SPICE
'''
#CREATING CLASS FOR EACH COMPONENT AND STORING IT'S DETAILS
class resister:
    def __init__(self,n1,n2,name,value):
        self.n1=n1
        self.n2=n2
        self.name=name
        self.value=value

class inductor:
    def __init__(self,n1,n2,name,value) :
        self.n1=n1
        self.n2=n2
        self.name=name
        self.value=value

class capacitor:
    def __init__(self,n1,n2,name,value):
        self.n1=n1
        self.n2=n2
        self.name=name
        self.value=value

class voltage_source:
    def __init__(self,n1,n2,name,value,current=0):
        self.n1=n1
        self.n2=n2
        self.name=name
        self.value=value
        self.current=current #THIS IS THE INDEX OF THE ROW/COLUMN OF CURRENT THROUGH THIS COLTAGE OURCE IN M MATRIX
class AC_voltage_source:
    def __init__(self,n1,n2,name,type,amp,phase,value,current=0):
        self.n1=n1
        self.n2=n2
        self.name=name
        self.type=type
        self.amp=amp
        self.phase=phase
        self.value=value
        self.current=current #THIS IS THE INDEX OF THE ROW/COLUMN OF CURRENT THROUGH THIS COLTAGE OURCE IN M MATRIX
class current_source:
    def __init__(self,n1,n2,name,value) :
        self.n1=n2
        self.n2=n1
        self.name=name
        self.value=value 
class AC_current_source:
    def __init__(self,n1,n2,name,type,amp,phase,value):
        self.n1=n2
        self.n2=n1
        self.name=name
        self.type=type
        self.amp=amp
        self.phase=phase
        self.value=value

class current_controlled:
    def __init__(self,n1,n2,name,voltagesource,value) :
        self.n1=n1
        self.n2=n2
        self.name=name
        self.voltagesource=voltagesource
        self.value=value

class voltage_controlled:
    def __init__(self,n1,n2,name,volsource_n1,volsource_n2,value) :
        self.n1=n1
        self.n2=n2
        self.name=name
        self.volsource_n1=volsource_n1
        self.volsource_n2=volsource_n2
        self.value=value        
import sys
import math as math
from sys import argv, exit
import numpy as np 
# To improvise editablity
STARTING_CIR = ".circuit"
ENDING_CIR = ".end"
AC_CIR=".ac"   
    # checking number of command line arguments
if len(sys.argv)!=2 :
        sys.exit("Invalid number of inputs! Pass the netlist file as the command line argument.")
else:
        try:
            actual_circuit_details = sys.argv[1]

            # checking if given netlist file is of correct type
            if (not actual_circuit_details.endswith(".netlist"))  :
                print("incorrect file type! please give .netlist file only")
            else:
                with open (actual_circuit_details, "r") as f:
                    SPICE_Lines = []
                    for line in f.readlines():
                        SPICE_Lines.append(line.split('#')[0].split('\n')[0])
                    for line in SPICE_Lines:  
                        AC_CIR == line[:len(AC_CIR)]
                        identifier3 = SPICE_Lines.index(line)    
                    try:
                        # finding the location of the identifiers
                        identifier1 = SPICE_Lines.index(STARTING_CIR)
                        identifier2 = SPICE_Lines.index(ENDING_CIR)
                        
                        SPICELines_Actual = SPICE_Lines[identifier1+1:identifier2]
                        
                    except ValueError:
                        print("The Netlist given does not follow to the given format! Make sure to have .circuit and .end lines in the file.")
        except FileNotFoundError:
            print("Given file does not exist! Make sure you have entered the name of the netlist file correctly.")



components_details=[] #THE LIST THAT STORES THE OBJECTS OF EACH COMPONENT
k_nodes_con_vs=0 # COUNTER TO COUNT CURRENTS THROUGH VOLTAGE SOURCE AND CONTROLLING CURRENT 
ac_checker=0 # CHECKER TO KNOW IF THE SOURCE IS AC OR DC
try:
    for lines in SPICELines_Actual: # FOR LOOP TO COLLECT EACH LINE AND CREATE AN OBJECT FOR COMPONENT
        if(len(lines.split()))==4:
            comp_name,n1,n2,value=lines.split()
            if n1!='GND':
                n1=n1[-1]
            if n2!= 'GND':
                n2=n2[-1]
            if  comp_name[0]=='R':
               component=resister(n1,n2,comp_name,value)
            elif  comp_name[0]=='L':
               component=inductor(n1,n2,comp_name,value)
            elif  comp_name[0]=='C':
               component=capacitor(n1,n2,comp_name,value)
            elif  comp_name[0]=='I':
               component=current_source(n1,n2,comp_name,value)
            elif  comp_name[0]=='V':
               component=voltage_source(n1,n2,comp_name,value)
               k_nodes_con_vs=k_nodes_con_vs+1  
        if(len(lines.split())) ==5 and lines.split()[3]!="dc": 
            comp_name,n1,n2,voltagesource,value=lines.split()
            if n1!='GND':
                n1=n1[-1]
            if n2!= 'GND':
                n2=n2[-1]
            component=current_controlled(n1,n2,comp_name,voltagesource,value)
            if comp_name[0] == 'H':
                k_nodes_con_vs=k_nodes_con_vs+1
                 
        if(len(lines.split())) ==5 and lines.split()[3]=="dc":
            comp_name,n1,n2,type,value=lines.split()
            if n1!='GND':
                n1=n1[-1]
            if n2!= 'GND':
                n2=n2[-1]
            if comp_name[0]=='V':    
                component=voltage_source(n1,n2,comp_name,value)    
                k_nodes_con_vs=k_nodes_con_vs+1
            elif comp_name[0]=='I':
                component=current_source(n1,n2,comp_name,value)
        if((len(lines.split())) ==6 and lines.split()[3]!="ac"): 
            comp_name,n1,n2,volsource_n1,volsource_n2,value=lines.split()
            if n1!='GND':
                n1=n1[-1]
            if n2!= 'GND':
                n2=n2[-1]
            if volsource_n1!='GND':
                volsource_n1=volsource_n1[-1]
            if volsource_n2!='GND':
                volsource_n2=volsource_n2[-1]    
            component=voltage_controlled(n1,n2,comp_name,volsource_n1,volsource_n2,value)
            if comp_name[0]=='E':
                k_nodes_con_vs=k_nodes_con_vs+1
            
                
        if((len(lines.split())) ==6 and lines.split()[3]=="ac"):
            comp_name,n1,n2,type,amp,phase=lines.split()
            if n1!='GND':
                n1=n1[-1]
            if n2!= 'GND':
                n2=n2[-1]
            value=0
            if comp_name[0]=='V':
                component=AC_voltage_source(n1,n2,comp_name,type,amp,phase,value)
                ac_amplitude=float(component.amp)/2
                ac_phase=float(component.phase)
                ac_voltage= ac_amplitude*complex(math.cos(ac_phase),math.sin(ac_phase))
                component.value=ac_voltage
                k_nodes_con_vs=1+k_nodes_con_vs
                ac_checker=1
            else:
                component=AC_current_source(n1,n2,comp_name,type,amp,phase,value)
                ac_amplitude=float(component.amp)/2
                ac_phase=float(component.phase)
                ac_current= ac_amplitude*complex(math.cos(ac_phase),math.sin(ac_phase))
                component.value=ac_current
                ac_checker=1
            
        elif (component.value.isdigit()==1):       #INCASE VALUE ISN'T FLOAT NUMBER, CONVERTING IT INTO FLOAT NUMERAL
            component.value=float(component.value)
        else:
            temp2=component.value.split('e')       #INCASE VALUE ISN'T REAL NUMBER, CONVERTING IT INTO NUMERAL
            component.value=(float(temp2[0]))*(10**int(temp2[1]))
        components_details.append(component)
except:
     print("enter the properly written netlist file")
     exit()

if ac_checker ==1:          #INCASE THE NETLIST HAD AC SOURCE, THEN EXTRACT IT'S FREQUENCY
    SPICElinewithAC= SPICE_Lines[identifier3]
    _,name,acvalue=SPICElinewithAC.split()
    AC_freq=2*3.1415926*(float(acvalue))
gnd_checker=0
all_nodes=dict()            #CREATING A DICTIONARY TO COUNT AND STORE THE DISTINCT NODES
for component in components_details:
    
    if component.n1 == "GND": 
        gnd_checker=1
        all_nodes['n0']=0
    else:
        temp3='n'+component.n1
        all_nodes[temp3] =component.n1   

    
    if component.n2 == "GND": 
        gnd_checker=1
        all_nodes['n0']=0
    else:
        temp4='n'+component.n2
        all_nodes[temp4] =component.n2

no_of_nodes=len(all_nodes)
if gnd_checker==1:
# Creating the M and b matrices for solving the equations.
    M = np.zeros(((no_of_nodes+k_nodes_con_vs-1),(no_of_nodes+k_nodes_con_vs-1)),dtype="complex_")
    b = np.zeros(((no_of_nodes+k_nodes_con_vs-1),1),dtype="complex_")
    cur_val=0
else:
    print("Your netlist file doesn't have any gnd voltage. Make sure to have any one node as gnd")
    exit()
#fill the matrices M and b considerating if it is an AC or a DC source.
for component in components_details:
    if ac_checker ==1:
        if component.name[0] == 'C':
            component.value=-1/(float(component.value)*AC_freq)
            component.value=complex(0,component.value)
        if component.name[0]=='L':
            component.value =1*(float(component.value)*AC_freq)
            component.value=complex(0,component.value)         
  # if it is a R or L or C ,the matrix M is filled as shown.                
    if (component.name[0] == 'R' or 'C' or 'L') and (component.name[0] != 'I') and (component.name[0] != 'V') and (component.name[0] != 'E') and (component.name[0] != 'G') and (component.name[0] != 'F') and (component.name[0] != 'H')  :
    
        if component.n2 == 'GND':
            M[int(component.n1)-1][int(component.n1)-1] += 1/component.value

        elif component.n1 == 'GND':
            M[int(component.n2)-1][int(component.n2)-1] += 1/component.value
					
        else:	
            M[int(component.n1)-1][int(component.n1)-1] += 1/component.value
            M[int(component.n2)-1][int(component.n2)-1] += 1/component.value
            M[int(component.n1)-1][int(component.n2)-1] += -1/component.value
            M[int(component.n2)-1][int(component.n1)-1] += -1/component.value
        
# If it is a current source, the matrix b is filled as shown.
    if component.name[0] == 'I':
        if component.n2 == 'GND':
            b[int(component.n1)-1][0] += component.value

        elif component.n1 == 'GND':
            b[int(component.n2)-1][0] += -component.value

        else:
            b[int(component.n1)-1][0] += component.value
            b[int(component.n2)-1][0] += -component.value
        
# If it is a voltage source, the matrices M and b are filled as shown.
    elif component.name[0]=='V':
        
        if component.n2 == 'GND':
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[no_of_nodes-1+cur_val][int(component.n1)-1] += 1
            b[no_of_nodes-1+cur_val][0] += component.value
            component.current=no_of_nodes-1+cur_val
            cur_val = cur_val+1			
        elif component.n1 == 'GND':
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[no_of_nodes-1+cur_val][int(component.n2)-1] += -1
            b[no_of_nodes-1+cur_val][0] += component.value
            component.current=no_of_nodes-1+cur_val
            cur_val= cur_val+1			
        else:	
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[no_of_nodes-1+cur_val][int(component.n1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.n2)-1] += -1
            b[no_of_nodes-1+cur_val][0] += component.value
            component.current=no_of_nodes-1+cur_val
            cur_val = cur_val+1 
# If it is a voltage controlled voltage source, the matrices M is filled as shown.        
    if component.name[0]=='E':
        if component.n2 == 'GND' and component.volsource_n1== 'GND':
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[no_of_nodes-1+cur_val][int(component.n1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.volsource_n2)-1] += component.value
            cur_val = cur_val+1	
        elif component.n2 == 'GND' and component.volsource_n2== 'GND':
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[no_of_nodes-1+cur_val][int(component.n1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.volsource_n1)-1] += -1*component.value
            cur_val = cur_val+1    		
        elif component.n1 == 'GND' and component.volsource_n1 == 'GND':
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[no_of_nodes-1+cur_val][int(component.n2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.volsource_n2)-1] += component.value
            cur_val= cur_val+1
            	
        elif component.n1 == 'GND' and component.volsource_n2 == 'GND':
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[no_of_nodes-1+cur_val][int(component.n2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.volsource_n1)-1] += -1*component.value
            cur_val= cur_val+1		
        else:	
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[no_of_nodes-1+cur_val][int(component.n1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.n2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.volsource_n1)-1] += -1*component.value
            M[no_of_nodes-1+cur_val][int(component.volsource_n2)-1] += component.value
            cur_val = cur_val+1
# If it is a voltage controlled current source, the matrices M is filled as shown.
    if component.name[0]=='G':
        if component.n2 == 'GND' and component.volsource_n1 == 'GND':
            M[int(component.n1-1)][int(component.volsource_n2)-1] += -1*component.value
        if component.n2 == 'GND' and component.volsource_n2 == 'GND':
            M[int(component.n1-1)][int(component.volsource_n1)-1] += component.value   		
        elif component.n1 == 'GND' and component.volsource_n1 == 'GND':
            M[int(component.n2)-1][int(component.volsource_n2)-1] += component.value
        elif component.n1 == 'GND' and component.volsource_n2 == 'GND':
            M[int(component.n2)-1][int(component.volsource_n1)-1] += -1*component.value  			
        else:	
            M[int(component.n1-1)][int(component.volsource_n1)-1] += component.value
            M[int(component.n1-1)][int(component.volsource_n2)-1] += -1*component.value
            M[int(component.n2)-1][int(component.volsource_n2)-1] += component.value
            M[int(component.n2)-1][int(component.volsource_n1)-1] += -1*component.value
 # If it is a current controlled current source, the matrices M is filled as shown.          
    if component.name[0]=='F':
        node1=0
        node2=0
        currentnode=0
        for temp in components_details:
            if temp.comp_name==component.voltagesource:
                 node1=temp.n1 
                 node2=temp.n2
                 currentnode=temp.current
        if component.n2 == 'GND' and node1== 'GND':
            M[int(component.n1)-1][currentnode] += component.value
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node2)-1] += -1
            
        elif component.n2 == 'GND' and node2== 'GND':
            M[int(component.n1)-1][currentnode] += component.value
            M[int(node1)-1][currentnode] += 1
            M[currentnode][int(node1)-1] += 1
            		
        elif component.n1 == 'GND' and node1=='GND':
            M[int(component.n2)-1][currentnode] += -1*component.value
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node2)-1] += -1
            
        elif component.n1 == 'GND' and node2=='GND':
            M[int(component.n2)-1][currentnode] += -1*component.value
            M[int(node1)-1][currentnode] += 1
            M[currentnode][int(node1)-1] += 1
               		
        else:	
            M[int(component.n1)-1][currentnode] += component.value
            M[int(component.n2)-1][currentnode] += -1*component.value
            M[int(node1)-1][currentnode] += 1
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node1)-1] += 1
            M[currentnode][int(node2)-1] += -1
 # If it is a current controlled voltage source, the matrices M is filled as shown.           
    if component.name[0]=='H':
        node1=0
        node2=0
        currentnode=0
        for temp in components_details:
            if temp.comp_name==component.voltagesource:
                 node1=temp.n1 
                 node2=temp.n2
                 currentnode=temp.current
        if component.n2 == 'GND' and node1== 'GND':
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.n1)-1]+=1
            M[no_of_nodes-1+cur_val][currentnode]+=-1*component.value
            cur_val = cur_val+1
        elif component.n2 == 'GND' and node2== 'GND':
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[int(node1)-1][currentnode] += 1
            M[currentnode][int(node1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.n1)-1]+=1
            M[no_of_nodes-1+cur_val][currentnode]+=-1*component.value
            cur_val = cur_val+1		
        elif component.n1 == 'GND' and node1=='GND':
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.n2)-1]+=1
            M[no_of_nodes-1+cur_val][currentnode]+=-1*component.value
            cur_val = cur_val+1
        elif component.n1 == 'GND' and node2=='GND':
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[int(node1)-1][currentnode] += 1
            M[currentnode][int(node1)-1] += 1
            M[no_of_nodes-1+cur_val][int(component.n2)-1]+=1
            M[no_of_nodes-1+cur_val][currentnode]+=-1*component.value
            cur_val = cur_val+1    		
        else:	
            M[int(component.n1)-1][no_of_nodes-1+cur_val] += 1
            M[int(component.n2)-1][no_of_nodes-1+cur_val] += -1
            M[int(node1)-1][currentnode] += 1
            M[int(node2)-1][currentnode] += -1
            M[currentnode][int(node1)-1] += 1
            M[currentnode][int(node2)-1] += -1
            M[no_of_nodes-1+cur_val][int(component.n1)-1]+=1
            M[no_of_nodes-1+cur_val][int(component.n2)-1]+=1
            M[no_of_nodes-1+cur_val][currentnode]+=-1*component.value
            cur_val = cur_val+1        
# The circuit equations are solved using the linalg.solve() function .  
try:
    V = np.linalg.solve(M,b)
    print(V,"\n")
    for i in range(no_of_nodes-1):
        print("V",i+1,"=",V[i],"\n")
    for j in range(k_nodes_con_vs):
	    print("I",j+1,"=",V[j+no_of_nodes-1],"\n")  
except:
    print("you either have only voltage sources in the loop or only current sources connected to a node ")
        