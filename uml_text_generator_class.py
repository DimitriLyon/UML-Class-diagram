import re
import os
path = os.path.dirname(os.path.abspath(__file__))

for files in os.listdir(path):
    if os.path.isfile(os.path.join(path, files)) and files[-3:] != ".py":
            name = files
            java_file = open(name,"r")
            
            class_name = []
            method_signatures = []
            attributes = []
            class_name_string = ''
            depth = 0
            
            for i in java_file:
                line_data = re.sub("\t","",i)
                split_line = line_data.split(" ")
                if "class" in split_line:
                    abstract_class = "abstract" in split_line
                    if abstract_class:
                        class_name.append("abstract")
                        class_name_string = split_line[3]
                        class_name.append(split_line[3])
                    else:
                        class_name_string = split_line[2]
                        class_name.append(split_line[2])
                    
                    if "extends" in split_line:
                        class_name.append("extends")
                        if abstract_class:
                            class_name.append(split_line[5])
                        else:
                            class_name.append(split_line[4])
                
                    
                elif depth == 1 and ("public" in split_line or "private" in split_line or "protected" in split_line):
                    #this block can be used by the method line or the attribute line
                    #Handle static methods and attributes.
                    static = False
                    final = False
                    if "static" in split_line:
                        static = True
                        split_line.remove("static")
                    if "final" in split_line:
                        final = True
                        split_line.remove("final")
                    
                    
                    
                    to_insert = ""
                    if "public" in split_line:
                        to_insert = to_insert + "+"
                    elif "private" in split_line:
                        to_insert = to_insert + "-"
                    else:
                        to_insert = to_insert + "#"
                    if not ("=" in i) and (re.search("\(.*\)",line_data) is not None):
                        #method
                        param_split = line_data.replace(")","(").split("(")
                        param_list = param_split[1].split(",")
                        #loop to get rid of space after commas in parameters of functions
                        for k in range(len(param_list)):
                            param_list[k] = re.sub("^ ","",param_list[k])
                        
                        if re.search(class_name_string, line_data) is not None:
                            #constructor
                            to_insert = to_insert + class_name_string + "("
                            
                            for j in param_list:
                                if j == "":
                                    continue
                                split_param = j.split(" ")
                                to_insert += split_param[1] + ": " + split_param[0]
                                if j != param_list[-1]:
                                    to_insert += ", "
                            
                            to_insert += ")"
                        else:
                            #regular method
                            to_insert += split_line[2].split("(")[0]
                            to_insert += "("
                            
                            if param_list[0] != "":
                                for k in param_list:
                                    split_param = k.split(" ")
                                    to_insert += split_param[1] + ": " + split_param[0]
                                    if k != param_list[-1]:
                                        to_insert += ", "
                            
                            to_insert += "): " + split_line[1]
                        if static:
                            to_insert += "  _static_"
                        if final:
                            to_insert += "  _final_"
                        method_signatures.append(to_insert)
                    else:
                        split_line[-1] = split_line[-1].replace(";\n","")
                        to_insert += split_line[2] + ": " + split_line[1]
                        if static:
                            to_insert += "  _static_"
                        if final:
                            to_insert += "  _final_"
                        attributes.append(to_insert)
                
                
                depth += len(re.findall("{",i))
                depth -= len(re.findall("}",i))
            print("-------------------------------------------------------------------")
            for i in class_name:
                print(i)
            print("-------------------------------------------------------------------")
            for i in attributes:
                print(i)
            print("-------------------------------------------------------------------")
            for i in method_signatures:
                print(i)
            print("--------------------------------------------------------------------------------------")