import math
from collections import defaultdict
from collections import Counter
import re
import csv

def fire_percentage_over_forty():
    input_file= open('pokemonTrain.csv','r')
    pokemon_output = open('pokemon1.txt','w')
    reader = csv.reader(input_file)                           #reader object to read through file
    fire_cards_above_forty = 0
    total_fire_cards = 0
    next(reader)                                                            #skip first line which includes headers
    
    for row in reader:                                                      #for each row
        
        try:                                                                #for each instance that is not an empty line
            if re.match('fire',row[4].strip()):                            #if target word found in 4th index of the row             
                total_fire_cards = total_fire_cards +1                      #add to total fire cards
                if float(row[2])>=40:                                       #check level in row at specified index 
                    fire_cards_above_forty = fire_cards_above_forty +1      #add to total number of fire cards >= 40
                else:
                    continue
            else:
                continue
        except:                                                             #for instance of empty line 
            continue                                                        #go to next itteration of loop (next line in this context)
            
    #pokemon_output = open('pokemon1.txt','w')                               #opens file in write mode ('w')
    pokemon_output.write('Percentage of fire type Pokemons at or above level 40 = ' + str(round(fire_cards_above_forty/total_fire_cards*100)))                                                                                     #write to output file
    pokemon_output.close()                                                  #close file very important
    input_file.close()
    
def fill_in_NaN():
    with open('pokemonResult.csv','w',newline='') as writefile:
        writer = csv.writer(writefile)
        with open('pokemonTrain.csv','r') as readfile:

            reader = csv.reader(readfile)
            row = next(reader)
            writer.writerow(row)
            weaknessdic = {}
            counter_type = {}
            newdic={}
            data= []
            threshold = float(40)
            listgreater_atk=[]
            listsmaller_atk=[]
            listgreater_def=[]
            listsmaller_def=[]
            listgreater_hp=[]
            listsmaller_hp=[]
            #column,index
            #level,[2]
            #atk,[6]
            #def,[7]
            #hp,[8]

            for row in reader: #for every row
                pweakness = str(row[5].strip()) #weakness variable holder
                ptype = row[4].strip()  #type in variable holder
                threshold = 40.0
                plevel = (row[2].strip())
                patk = (row[6].strip())
                pdef = (row[7].strip())
                php = (row[8].strip())

                if float(plevel) > threshold: #if level > 40
                    if not re.match('[Nn][Aa][Nn]',patk) :
                        listgreater_atk.append(float(patk))
                    if not re.match('[Nn][Aa][Nn]',pdef):
                        listgreater_def.append(float(pdef))
                    if not re.match('[Nn][Aa][Nn]',php):
                        listgreater_hp.append(float(php))
                else:
                    if not re.match('[Nn][Aa][Nn]',patk):
                        listsmaller_atk.append(float(patk))
                    if not re.match('[Nn][Aa][Nn]',pdef):
                        listsmaller_def.append(float(pdef))
                    if not re.match('[Nn][Aa][Nn]',php):
                        listsmaller_hp.append(float(php))

                if not re.match('[Nn][Aa][Nn]',ptype):  #if type is not NAN

                    if pweakness not in weaknessdic: #(insert reg exp..)if the weakeness is not in the dictionary of weaknesses
                        weaknessdic[pweakness] = [ptype] #then add the weakness mapped to a list. with type in list
                    else: 
                        weaknessdic[pweakness].append(ptype) #or else append it to already created list

                else: #if type is NaN
                    continue #skip to next line


            for eachweakness in weaknessdic: #FOR EACH key in dic (weakness)
                counter_type[eachweakness]=Counter(weaknessdic[eachweakness]) #put counter on every value and save it in counter_type dic


            for key,value in counter_type.items(): #for each item in counter_type dic
                if len(value) ==1: #if only 1 value for that key
                    list_of_type=list(value) #create a list of that value (to get rid of counter type)
                    newdic[key]=list_of_type[0] #put that key and value in newdic

                else: #if length of list contains more than one type
                    dic_of_types_to_count= dict((value)) #create dictionary which has all the multiple values of key   
                    types_in_list = [x for x in dic_of_types_to_count.keys()] #create list of all the the different types
                    typescount_in_list = [x for x in dic_of_types_to_count.values()] #create list of all the number of occurances for each type
                    if typescount_in_list[0]!=typescount_in_list[1]: #if first and second number of counts are not the same
                        newdic[key]=types_in_list[0] #add the first (most occured) type into newdic which will be mapped to key (weakeness)
                    else: #if first and second number are the same...that means there are multiple types with the same number of occurances

                        firstval=typescount_in_list[0] #first value of the list that stores counts which is already ordered

                        newtypeslis = [k for k in dic_of_types_to_count.keys() if dic_of_types_to_count[k]==firstval] #new list with only those highest values


                        newtypeslis.sort() #sort the types in alphabetical order
                        newdic[key]=newtypeslis[0] #add first type to dic with key 
                        
            #atk,def,hp greater and smaller than level 40 avgs
            atkgreateravg = sum(listgreater_atk)/len(listgreater_atk)
            atksmalleravg= sum(listsmaller_atk)/len(listsmaller_atk)
            defgreateravg= sum(listgreater_def)/len(listgreater_def)
            defsmalleravg= sum(listsmaller_def)/len(listsmaller_def)
            hpgreateravg= sum(listgreater_hp)/len(listgreater_hp)
            hpsmalleravg= sum(listsmaller_hp)/len(listsmaller_hp)

            readfile.seek(0) #send reader object back to begining of file
            next(reader) #skip header line

            #need to print type in column index 4 if it is nan
            #need to print atk,def,hp in correct column with corresponding avg in index 6,7, or 8
            for rowfinal in reader: #read each row
                level_final=rowfinal[2].strip()               #each variable set to final value name just for readability
                type_final=rowfinal[4].strip()
                weakness_final=rowfinal[5].strip()
                atk_final=rowfinal[6].strip()
                def_final=rowfinal[7].strip()
                hp_final=rowfinal[8].strip()
                data = rowfinal.copy()
                if re.match('[Na][Aa][Nn]',type_final): #if type is  NAN
                    data[4]= str(newdic.get(weakness_final)) #get the type and assign it to index is list
                    
                    #checks for level: if above thresh(40)
                if float(level_final) > threshold: 
                    #if atk,def,or hp is NaN fill with greateravg
                    if re.match('[Na][Aa][Nn]',atk_final):
                        data[6]=str(round(atkgreateravg,1))
                    
                    if re.match('[Na][Aa][Nn]',def_final):
                        data[7]=str(round(defgreateravg,1))
                        
                    if re.match('[Na][Aa][Nn]',hp_final):
                        data[8]=str(round(hpgreateravg,1))
                        
                else: #if not greater than 40
                    
                    if re.match('[Na][Aa][Nn]',atk_final):
                        data[6]=str(round(atksmalleravg,1))
                        
                    if re.match('[Na][Aa][Nn]',def_final):
                        data[7]=str(round(defsmalleravg,1))
                        
                    if re.match('[Na][Aa][Nn]',hp_final):
                        data[8]=str(round(hpsmalleravg,1))

                writer.writerow((data)) #write row
            writefile.close()
            
            
def type_to_pers(): #mapping type to all personalities that cardtype has. alphabetically ordered (both keys and values)
    #Create a dictionary that maps pokemon types to their personalities. This dictionary would map a string to a list of strings
    with open('pokemonResult.csv','r') as input_file:
        with open('pokemon4.txt','w') as output_file:
            reader = csv.reader(input_file) #reader object

            headerline=next(reader)  #dont need variable, code just to skip header
            dic = {}
            for row in reader:
                ptype = row[4]
                pers = row[3]

                try: #if elements already in for that type
                    dic[ptype].append(pers) 
                except: #if elements not already created for that type
                    dic[ptype]=[pers]
                    
            keyslist = list(sorted(dic.keys()))  #newlist of sorted keys
            output_file.write('Pokemon type to personality mapping:\n')
            for x in keyslist: #itterate through sorted keys
                output_file.write('\t') #tab
                output_file.write(x) #key: output
                output_file.write(': ')
                
                y = list(sorted(set(dic.get(x)))) #list of values in the key[x]
                
                output_file.write(', '.join(y)) #join each element in values of specified key with a commma
                output_file.write('\n') #newline
            output_file.close()

def avg_hp():
    with open('pokemonResult.csv','r') as inputfile:
        with open('pokemon5.txt','w',newline='') as outfile:
            reader = csv.reader(inputfile)
            next(reader) #skip headers
            avghplist = []   #list of all hp if stage is 3

            for row in reader:
                stage = float(row[9].strip())
                hp = row[8].strip()

                if stage == 3: #if stage is 3
                    avghplist.append(float(hp)) #append hp to list of all hp's
                else: #if not 3 continue to next itteration
                    continue

            avghp = round(sum(avghplist)/len(avghplist))
            outfile.write('Average hit point for Pokemons of stage 3.0 = ') 
            outfile.write(str(avghp)) 
            outfile.close()
def main():
    fire_percentage_over_forty() #1
    fill_in_NaN() #2 and 3
    type_to_pers() #4
    avg_hp() #5


if __name__ == "__main__":
    main()