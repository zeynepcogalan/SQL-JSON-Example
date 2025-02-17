# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Zeynep Çoğalan 2021510078 -- Esma Beydili 2020510018
import csv
import json

# We read the csv file, split it with ";", and put it into the data
def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            data.append(row)
    return data

# calls other functions, checking the first word of the input
def inp(choiceInp, tempData): # for select or delete or insert operations
    
    if choiceInp[0]=="SELECT":# does not change tempdata as it only prints to the screen
        select(choiceInp,tempData)
        return tempData
        
    elif choiceInp[0]=="DELETE":# deletes the requested information if the input is in the correct form
        tempData=delete(choiceInp,tempData)
        return tempData
        
    elif choiceInp[0]==('INSERT'): # inserts the requested information if the input is in the correct form
        tempData = insert(choiceInp,tempData)
        return tempData
        
        
    else:
        print("Error(1)! You entered an incorrect entry, please enter it in the correct form.")
        print(choiceInp[0])# prints the error to the screen
        return tempData
        
############################################################################################    
# k =key, k+1= condition operator , k+2= value for choiceInp
# Checking sorted_data values. If the entry matches what is requested, it is thrown into the list.
def infoOplist(choiceInp, sorted_data, k):# Puts the information to be deleted or selected into the "sel" list
         sel=[]
         if choiceInp[k+1]=="=":
            sel = [element for element in sorted_data if element[choiceInp[k]] == choiceInp[k+2]]
            return sel
         elif choiceInp[k+1]=="!=":
            sel = [element for element in sorted_data if element[choiceInp[k]] != choiceInp[k+2]]
            return sel
         elif choiceInp[k+1]=="<":
            sel = [element for element in sorted_data if  int(element[choiceInp[k]]) < int(choiceInp[k+2])]
            return sel
         elif choiceInp[k+1]==">":
            sel = [element for element in sorted_data if  int(element[choiceInp[k]]) > int(choiceInp[k+2])]
            return sel
         elif choiceInp[k+1]==">=" or choiceInp[k+1]=="!<":# same meaning
            sel = [element for element in sorted_data if int(element[choiceInp[k]]) >= int(choiceInp[k+2])  ]
            return sel
         elif choiceInp[k+1]=="<=" or choiceInp[k+1]=="!>":# same meaning
            sel = [element for element in sorted_data if  int(element[choiceInp[k]]) <= int(choiceInp[k+2])  ]
            return sel
         else:
           print("Error(2)! Wrong condition operators")
           
###############################################################################
def infoDel(choiceInp, sorted_data):#input length must be 7 or 11
    if len(choiceInp)==11 and choiceInp[7]=='AND' :# if input length is correct and "and" is used
        k=4 # index of the key in the input
        tempData= sorted_data
        sel=[]
        
        # Creates a list from tempData that meets the first condition, 
        # then lists those that meet the second condition from the list that meets the first condition.
        for x in range(2):# for first and second conditions of "and"
                k = k+(x*4)
                if choiceInp[k]=="id" or choiceInp[k]=="grade":# for integer key
                  sel=infoOplist(choiceInp, tempData,k)
                  tempData = [element for element in tempData if element not in sel]
                  
                #for String key and value
                elif (choiceInp[k]=="name" or choiceInp[k]=="lastname" or choiceInp[k]=="email") and (choiceInp[5]=="=" or choiceInp[5]=="!=") :
                  if choiceInp[k+2].startswith("\"") and choiceInp[k+2].endswith("\"") :# imperative form of string value
                    choiceInp[k+2]= choiceInp[k+2][1:]
                    choiceInp[k+2]= choiceInp[k+2][:len(choiceInp[k+2])-1]
                    sel=infoOplist(choiceInp, tempData,k)
                    tempData = [element for element in tempData if element not in sel]
                    
                  else:
                    print("Error(3)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
                else:
                  print("Error(4)! Your key name may be wrong or your key and your condition operator may not match.")
                tempData=sel #list of data to be deleted
        # in the last case, it puts data in sorted_data that is in sorted_data but not in tempData. And returns sorted_data
        sorted_data = [element for element in sorted_data if element not in tempData]
        return sorted_data
    elif len(choiceInp)==11 and choiceInp[7]=='OR' :# if input length is correct and "or" is used
        k=4
        # Before the sorted_ data, we delete the data that meets the 1st condition, 
        # then we delete the data that meets the 2nd condition.
        for x in range(2):#"for first and second conditions of "or"
                k = k+(x*4)
                if choiceInp[k]=="id" or choiceInp[k]=="grade":# for integer key
                  sel=infoOplist(choiceInp, sorted_data,k)
                  sorted_data = [element for element in sorted_data if element not in sel]# sorted_data-(sorted_data& sel)
                  #for String key and value
                elif (choiceInp[k]=="name" or choiceInp[k]=="lastname" or choiceInp[k]=="email") and (choiceInp[5]=="=" or choiceInp[5]=="!=") :
                  if choiceInp[k+2].startswith("\"") and choiceInp[k+2].endswith("\"") : # imperative form of string value
                    choiceInp[k+2]= choiceInp[k+2][1:]#
                    choiceInp[k+2]= choiceInp[k+2][:len(choiceInp[k+2])-1]
                    sel=infoOplist(choiceInp, sorted_data,k)
                    sorted_data = [element for element in sorted_data if element not in sel]# sorted_data-(sorted_data& sel)
                    
                  else:
                    print("Error(5)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
                else:
                  print("Error(6)! Your key name may be wrong or your key and your condition operator may not match.")
        return sorted_data
                
    elif len(choiceInp)==7:#len7
        if choiceInp[4]=="id" or choiceInp[4]=="grade":# for integer key
            sel=infoOplist(choiceInp, sorted_data,4)
            sorted_data = [element for element in sorted_data if element not in sel]
            return sorted_data
        #for String key and value       
        elif (choiceInp[4]=="name" or choiceInp[4]=="lastname" or choiceInp[4]=="email") and (choiceInp[5]=="=" or choiceInp[5]=="!=") :
           if choiceInp[6].startswith("\"") and choiceInp[6].endswith("\"") : # imperative form of string value
               choiceInp[6]= choiceInp[6][1:]#
               choiceInp[6]= choiceInp[6][:len(choiceInp[6])-1]
               sel=infoOplist(choiceInp, sorted_data,4)
               sorted_data = [element for element in sorted_data if element not in sel]# sorted_data-(sorted_data& sel)
               return sorted_data
           else:
               print("Error(7)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
        else:
            print("Error(8)! Your key name may be wrong or your key and your condition operator may not match.")
    else:
            print("Error(9)! Wrong query. Your input length may be wrong")
        
###############################################################################

def infoSel(choiceInp, sorted_data): #input length must be 15 or 11
    if len(choiceInp)==15 and choiceInp[8]=='AND' :# if input length is correct and "and" is used
        k=5
        tempData= sorted_data
        sel=[]
        temp=[]
        
        # Creates a list from tempData that meets the first condition, 
        # then lists those that meet the second condition from the list that meets the first condition.
        for x in range(2):# for first and second conditions of "and"
                k = k+(x*4)
                if choiceInp[k]=="id" or choiceInp[k]=="grade":# for integer key
                  sel=infoOplist(choiceInp, tempData,k)
                  tempData = [element for element in tempData if element not in sel]
                 
                  # for string key and value
                elif (choiceInp[k]=="name" or choiceInp[k]=="lastname" or choiceInp[k]=="email") and (choiceInp[k+1]=="=" or choiceInp[k+1]=="!=") :
                  if choiceInp[k+2].startswith("\"") and choiceInp[k+2].endswith("\"") : # imperative form of string value
                    choiceInp[k+2]= choiceInp[k+2][1:]#
                    choiceInp[k+2]= choiceInp[k+2][:len(choiceInp[k+2])-1]
                    sel=infoOplist(choiceInp, tempData,k)
                    tempData = [element for element in tempData if element not in sel]
                    
                  else:
                    print("Error(10)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
                else:
                  print("Error(11)! Your key name may be wrong or your key and your condition operator may not match.")
                tempData=sel
        return tempData #list of data to print
    
    elif len(choiceInp)==15 and choiceInp[8]=='OR' :#if input length is correct and "or" is used
        k=5
        #We keep the data providing the 1st condition of Or in a temp list.
        # then we combine it with the list with the data that satisfies the 2nd condition
        for x in range(2):
                k = k+(x*4)
                if choiceInp[k]=="id" or choiceInp[k]=="grade":# for integer key
                  temp=infoOplist(choiceInp, sorted_data,k)
                  if x == 0:
                      sel=temp
                  else:
                      sel.extend(temp) # we throw all the elements of the temp list into the sel list
                 #for string key and values 
                elif (choiceInp[k]=="name" or choiceInp[k]=="lastname" or choiceInp[k]=="email") and (choiceInp[k+1]=="=" or choiceInp[k+1]=="!=") :
                  if choiceInp[k+2].startswith("\"") and choiceInp[k+2].endswith("\"") :# imperative form of string value
                    choiceInp[k+2]= choiceInp[k+2][1:]
                    choiceInp[k+2]= choiceInp[k+2][:len(choiceInp[k+2])-1]
                    temp=infoOplist(choiceInp, sorted_data,k)
                    if x == 0:
                        sel=temp
                    else:
                        sel.extend(temp) # we throw all the elements of the temp list into the sel list
                        
                  else:
                    print("Error(12)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
                else:
                  print("Error(13)! Your key name may be wrong or your key and your condition operator may not match.")
        return sel
                
    else:#len11
        if choiceInp[5]=="id" or choiceInp[5]=="grade":# for integer key
            sel=infoOplist(choiceInp, sorted_data,5)
            return sel
        #for string key and values
        elif (choiceInp[5]=="name" or choiceInp[5]=="lastname" or choiceInp[5]=="email") and (choiceInp[6]=="=" or choiceInp[6]=="!=") :
           if choiceInp[7].startswith("\"") and choiceInp[7].endswith("\"") : # imperative form of string value
               choiceInp[7]= choiceInp[7][1:]#
               choiceInp[7]= choiceInp[7][:len(choiceInp[7])-1]
               sel=infoOplist(choiceInp, sorted_data,5)
               return sel
           else:
               print("Error(14)! The form of the string value in your input is incorrect, you should write the value in quotation marks.")
        else:
            print("Error(15)! Your key name may be wrong or your key and your condition operator may not match.")
    
###############################################################################
def select(choiceInp,sorted_data):
    sel = []
    if (len(choiceInp)== 15 and choiceInp[2]=='FROM'and choiceInp[3] == "STUDENTS" and choiceInp[4] == "WHERE" and choiceInp[12] == "ORDER" 
        and choiceInp[13] == "BY" and (choiceInp[14] == "ASC"or choiceInp[14] == "DSC") and 
        (choiceInp[8] == "AND" or choiceInp[8] == "OR")):# if the input is the correct length and form
        
        line = choiceInp[1].split(",")# column names to be printed are thrown into the list
        if len(line) <= 5:# max 5
             sel=infoSel(choiceInp, sorted_data)# requested data is assigned to this list
             if choiceInp[14] == "ASC":
                 sel = sorted(sel, key=lambda row: int(row['id']))
             else:
                 sel = sorted(sel, key=lambda row: int(row['id']), reverse=True)#for DSC
             columnName_data = [element for element in line if element not in sorted_data[0]]
                 # We print the selected columns of the requested data
             if len(columnName_data) == 0:
                for dic in sel:
                  for data in line:
                     print(dic[data],end=" ")
                  print("\n")  
                  
             else:
                print("Error(23)! column name entered incorrectly.")
           
        else:
            print("Error(16)! You cannot write more than 5 column names.")
    
    elif (len(choiceInp) == 11 and choiceInp[2]=='FROM' and choiceInp[3] == "STUDENTS" and choiceInp[4] == "WHERE" and choiceInp[8] == "ORDER"
    and choiceInp[9] == "BY" and (choiceInp[10] == "ASC" or choiceInp[10] == "DSC")):# if the input is the correct length and form
        line = choiceInp[1].split(",") # column names to be printed are thrown into the list
        if len(line) <= 5:
             sel=infoSel(choiceInp, sorted_data)# requested data is assigned to this list
             if choiceInp[10] == "ASC":
                 sel = sorted(sel, key=lambda row: int(row['id']))
             else:
                 sel = sorted(sel, key=lambda row: int(row['id']), reverse=True)# for DSC
                 columnName_data = [element for element in line if element not in sorted_data[0]]
                 # We print the selected columns of the requested data
             if len(columnName_data) == 0:
                for dic in sel:
                  for data in line:
                     print(dic[data],end=" ")
                  print("\n")  
                  
             else:
                print("Error(24)! column name entered incorrectly.")
             
        else:
            print("Error(17)! You cannot write more than 5 column names.")
    
    else:
        print("Error(18)! Wrong query . Your input length may be wrong")
    

###############################################################################  
def delete(choiceInp,sorted_data):
    if len(choiceInp)>=4 and choiceInp[1]=='FROM' and choiceInp[2]=='STUDENT'and choiceInp[3]=='WHERE':# if the input is the correct length and form
         sorted_data=infoDel(choiceInp, sorted_data) #Returns the list from which the data requested to be deleted has been deleted
         return sorted_data
    else:
         print("Error(19)! Wrong query. Your input length may be wrong")
        
###############################################################################
def insert(choiceInp,sorted_data):
    if len(choiceInp)==4 and choiceInp[1]=='INTO' and choiceInp[2]=='STUDENT':# if the input is the correct length and form 
            data = choiceInp[3].split("(")
            if data[0]=='VALUES':
                data[1]=data[1].strip(")")
                info = data[1].split(",")#The data to be written to json is thrown into the list
                if(len(info)==len(sorted_data[0])):#number of columns must be the same
                    new_entry = {'id': info[0], 'name': info[1], 'lastname': info[2], 'email': info[3], 'grade': info[4]}
                    sorted_data.append(new_entry)
                    sorted_data = sorted(sorted_data, key=lambda row: int(row['id']))
                    return sorted_data
                else:
                    print("Error(20! number of columns must be the 5")
            else:
                print("Error(21)! Wrong query ")
    else:
        print("Error(22)! Wrong query  Your input length may be wrong.")
###############################################################################
# writes the list in the parameter to the json file.
def write_Jason(sorted_data):
    with open('students.json', 'w') as json_file:
        json.dump(sorted_data, json_file, indent = 4, ensure_ascii=False)
###############################################################################
def main():
    #Here we read the csv file and assign it to the csv data list. After sorting by id number, we assign it to the sorted data.
    csv_filename = 'students.csv'
    csv_data = read_csv(csv_filename)
    sorted_data = sorted(csv_data, key=lambda row: int(row['id']))
    
    #We expect the user to enter select or delete or insert or "y" input in the correct form.
    #works unless the user inputs y
    # when user enters the y input, it writes the final state to the json file
    while (True):
        choiceInp=[]
        choice= input("Enter input or press y to exit: ")
        if(choice.lower() != "y"):
            choiceInp= choice.split(" ")# split the input and put it in the list
            sorted_data = inp(choiceInp, sorted_data)# for select or delete or insert operations
        else:
            write_Jason(sorted_data) 
            break
   
###############################################################################     
main()      # code starts working from here
        
























