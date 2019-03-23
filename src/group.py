import argparse
import copy 
import random
import re

th_tab = 0
by_tab = 1
gl_tab = 2
sp_tab = 3
same_tab = 0
diff_tab = 1

def check_rule(number_id, class_number, rule):
    """check_rule: verify if there is a same or diff candidate in this class
                   return 1 pass the check
                   return 0 reassign another class number

    :param number_id: student id 
    :param class_number: random assign class number
    :param rule: same/diff class notation
    """
    pass_same = 1
    pass_diff = 1

    # check same list
    for row in rule[same_tab]:
        if row[0] == number_id:
            if row[2] != class_number and row[2] !=" ":
                pass_same = 0
#                print ("AA same class %d" %class_number)
#                print ("AA rule %d" %row[2])
                break
        if row[1] == number_id:
            if row[2] != class_number and row[2] !=" ":
                pass_same = 0
#                print ("BB same class %d" %class_number)
#                print ("BB rule %d" %row[2])
                break
    if pass_same == 0:
        print ("check same failed")
        return 0

    # check diff list
    for row in rule[diff_tab]:
        if row[0] == number_id:
            if row[3] == class_number :
                pass_diff = 0
                break
        if row[2] == number_id:
            if row[1] == class_number :
                pass_diff = 0
                break
   
    if pass_diff == 0:
#        print ("check diff failed")
        return 0
    else :
        return 1

def update_class_number(number_id, class_number, data, rule):
    """update_class_number : write class number into data structure

    :param number_id: student id 
    :param class_number: random class number
    :param data: all school data structure
    :param rule: same/diff notation
    """

    # update rule table
    for row in rule[same_tab]:
        if row[0] == number_id:
            row[2] = class_number 
        if row[1] == number_id:
            row[2] = class_number 
    for row in rule[diff_tab]:
        if row[0] == number_id:
            row[1] = class_number 
        if row[2] == number_id:
            row[3] = class_number
    

    # update student table
#    for row in data[st_tab]:
#        if row[0] == number_id:
#            row[4] = class_number
#            print("\n\n\n\n")
#            print(row, sep='\r')
#            print("\n\n\n\n")
    for row in data[by_tab]:
        if row[0] == number_id:
            row[4] = class_number
    for row in data[gl_tab]:
        if row[0] == number_id:
            row[4] = class_number
    return data, rule

def get_same_class_number(number_id, rule):
    """get_same_class_number return the 

    :param number_id: input class number
    :param rule: same/diff notation
    """
    for row in rule[same_tab]:
        if row[0] == number_id or row[1] == number_id:
            if row[2] !=" ":
                #print("%d" %int(row[2]))
                return int(row[2])
    return int(0)

# return suitable position
def change_position(input_data, total_data, class_num, curr):
    """change_position change the student group sequence to minimize 
                       the random effort

    :param input_data: student id 
    :param total_data: girl/boy student list
    :param class_num: boy/girl class count
    :param curr: current running group
    """

    num_a = int(list(re.findall('\d+', input_data[0]))[0])

    # different class, switch to head of group
    if (input_data[6] != " "):
        group_a = int((num_a - 1) /int(class_num))
        # search next normal student
        for x in range (0, int(class_num)):
            if curr == int(group_a * class_num + x) :
                return curr
            if total_data[group_a * class_num + x][7] == " ":
                return (group_a * class_num + x);
        return curr 


    # same class, switch suitable group
    else :
        num_b = int(list(re.findall('\d+', input_data[7]))[0])
    
        group_a = int((num_a - 1) /int(class_num))
        group_b = int((num_b - 1) /int(class_num))

        if input_data[7][0] != input_data[0][0]:
            # search next normal student
            for x in range (0, int(class_num)):
                if curr == int(group_a * class_num + x) :
                    return curr
                if total_data[group_a * class_num + x][7] == " ":
                    return (group_a * class_num + x)
            return curr
        elif group_a != group_b :
            # search next normal student
            for x in range (0, int(class_num)):
                if curr == int(group_a * class_num + x) :
                    return curr
                if total_data[group_a * class_num + x][7][0] != input_data[0][0]:
                    return (group_a * class_num + x)
                if total_data[group_a * class_num + x][5] == " ":
                    return (group_a * class_num + x)
        elif num_b < num_a:
            # search next normal student
            for x in range (0, int(class_num)):
                if curr == int(group_a * class_num + x) :
                    return curr
                if total_data[group_a * class_num + x][7][0] != input_data[0][0]:
                    return (group_a * class_num + x)
                if total_data[group_a * class_num + x][5] == " ":
                    return (group_a * class_num + x)
        else:
            if group_a == len(total_data)/class_num: # last group 
               for x in range (0, int(class_num)):
                   if total_data[(group_a - 1) * class_num + x][7] == " ":
                       print ("return %d" %((group_a - 1) * class_num + x))
                       return ((group_a - 1) * class_num + x)
            else : 
               for x in range (0, int(class_num)):
                   if total_data[(group_a + 1) * class_num + x][7] == " ":
                       print ("return %d" %((group_a + 1) * class_num + x))
                       return ((group_a + 1) * class_num + x)

            return curr

def manage_list(input_data, class_boy, class_girl):
    """manage_list reorder the boy/girl sequence to make the random task works.

    :param input_data: all school data
    :param class_boy: class count of boy
    :param class_girl: class count of girls
    """
    for x in range (1, int(class_boy) + 1):
        curr = 0   
        for row_data in input_data[by_tab]:
            if row_data[7]!= " ":
                target = change_position(row_data, input_data[by_tab], class_boy, curr)
                input_data[by_tab][curr] , input_data[by_tab][target] = input_data[by_tab][target] , input_data[by_tab][curr] 
#                print("\n")
#                print ("from :%d" %curr)
#                print(input_data[by_tab][curr], sep='\n')
#                print ("to :%d" %target)
#                print(input_data[by_tab][target],sep='\n')
#                print("\n")
            curr = curr + 1
    
    for x in range (1, int(class_girl) + 1):
        curr = 0   
        for row_data in input_data[gl_tab]:
            if row_data[7]!= " ": 
                target = change_position(row_data, input_data[gl_tab], class_girl, curr)
                input_data[gl_tab][curr] , input_data[gl_tab][target] = input_data[gl_tab][target] , input_data[gl_tab][curr] 
#                print("\n")
#                print ("from :%d" %curr)
#                print(input_data[gl_tab][curr], sep='\n')
#                print ("to :%d" %target)
#                print(input_data[gl_tab][target],sep='\n')
#                print("\n")
            curr = curr + 1

#show manage_result
#    for row_data in input_data[by_tab]:
#        print(row_data, sep='\r')
#    
#    for row_data in input_data[gl_tab]:
#        print(row_data, sep='\r')
#
    return input_data
        



def group_boy(data, rule, class_number):
    """group_boy: random assign class for each boy 
                    and keep the rule

    :param data: all school information.
    :param rule: same/diff notiation.
    :param class_number: girl class count.
    """
    golden = []
    current_group = []
    possible_group = []
  
    for x in range(1, int(class_number) + 1):
        golden.append(x)
        current_group.append(x)

    # random each boy
    for row_boy in data[by_tab] :
        # get all possible group
        possible = copy.deepcopy(current_group)
        assign = get_same_class_number(row_boy[0],rule) 
        while len(possible) > 0 :
#            print(possible, sep='\n')
#            print(row_boy, sep='\n')
            if (assign != 0) :
                if int(assign) in possible:
                    None
                else :
                    print("someone use %d" %assign)
                    break
                ran = current_group.index(int(assign))
                print ("assign %d" %current_group[ran])
            else :
                ran = random.randint(0, len(current_group)-1)

            if (check_rule(row_boy[0],current_group[ran],rule) == 1):
                data, rule = update_class_number(row_boy[0], current_group[ran], data, rule)
                current_group.remove(current_group[ran])
                break
            else:
                if (current_group[ran] in possible):
                    possible.remove(current_group[ran])

        if len(current_group) == 0:
            current_group = golden[:]
        if row_boy[4] == " ": 
            print("random failed")
            print(row_boy, sep='\n')
            return 1, data, rule
    #print(data[by_tab], sep='\n')
    return 0, data, rule

def group_girl(data, rule, class_number):
    """group_girl : random assign class for each girl
                    and keep the rule

    :param data: all school information.
    :param rule: same/diff notiation.
    :param class_number: girl class count.
    """
    golden = []
    current_group = []
    possible_group = []
    
    for x in range(1, int(class_number) + 1):
        golden.append(x)
        current_group.append(x)
    
    
    # random each girl
    for row_girl in data[gl_tab] :
        # get all possible group
        possible = copy.deepcopy(current_group)
        assign = get_same_class_number(row_girl[0],rule) 
        while len(possible) > 0 :
#            print(possible, sep='\n')
#            print(row_girl, sep='\n')
            if (assign != 0) :
                if int(assign) in possible:
                    None
                else :
                    print("someone use %d" %assign)
                    break
                ran = current_group.index(int(assign))
                print ("assign %d" %current_group[ran])
            else :
                ran = random.randint(0, len(current_group)-1) 

            if (check_rule(row_girl[0],current_group[ran],rule) == 1):
                data, rule = update_class_number(row_girl[0], current_group[ran], data, rule)
                current_group.remove(current_group[ran])
                break
            else:
                if (current_group[ran] in possible):
                    possible.remove(current_group[ran])

        if len(current_group) == 0:
            current_group = golden[:]

        if row_girl[4]==" ":  
            print("random failed")
            print(row_girl, sep='\n')
            return 1, data, rule
        
    return 0, data, rule
#
def grouping (o_data, input_all, input_boy, input_girl, rule):
    """grouping : run boy/girl random funcion and keep the rule

    :param o_data: all student data
    :param input_all: total class count
    :param input_boy: boy class count
    :param input_girl: girl class count
    :param rule: same/diff class notation
    """
    segregated = 0
    class_all = 0
    class_boy = 0
    class_girl = 0
    pass_number = 0
    reset_all = 1
    target_data = o_data[:]
    target_rule = [] 

    # set the class number of boys and girls
    if  input_all == "0":
        segregated = 1
        class_boy = int(input_boy) 
        class_girl = int(input_girl) 
        class_all = class_boy + class_girl
    else :
        segregated = 0
        class_all = int(input_all)
        class_boy = class_all
        class_girl = class_all

    #update student list
    o_data = manage_list(o_data, class_boy, class_girl) 

    #make sure each stuednet pass the rule    
    while reset_all >= 1:
        print ("reset!!\n")
        target_data = copy.deepcopy(o_data)
        target_rule = copy.deepcopy(rule) 
#Start boy grouping
        if (class_boy != 0 ):
            reset_all, target_data, target_rule = group_boy(target_data, target_rule, class_boy)
            print ("reset_all boy %d!!\n" %reset_all)
            if reset_all >=1:
                continue

#Start girl grouping
        if (class_girl != 0 ):
            reset_all, target_data, target_rule = group_girl(target_data, target_rule, class_girl)
            print ("reset_all girl %d!!\n" %reset_all)
            if reset_all >=1:
                continue

#sort boy student list
    curr = 0
    if (class_boy != 0 ):
        for row in target_data[by_tab]:
            num_a = int(list(re.findall('\d+', row[0]))[0]) - 1
            if num_a != curr :
                target_data[by_tab][curr],  target_data[by_tab][num_a] = target_data[by_tab][num_a], target_data[by_tab][curr] 
            curr = curr + 1
   
#sort girl student list
    curr = 0
    if (class_girl != 0 ):
        for row in target_data[gl_tab]:
            num_a = int(list(re.findall('\d+', row[0]))[0]) - 1
            if num_a != curr :
                target_data[gl_tab][curr],  target_data[gl_tab][num_a] = target_data[gl_tab][num_a], target_data[gl_tab][curr] 
            curr = curr + 1
    
    o_data = copy.deepcopy(target_data)
    rule = copy.deepcopy(target_rule)
    print("group complete!!")
    return o_data
