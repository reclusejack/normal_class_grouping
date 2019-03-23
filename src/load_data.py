from openpyxl import load_workbook
import copy, re

def load_data(school_filename, all_data, rule):
    """load_data from excel file.

    :param school_filename: file name 
    :param all_data: teacher/student information from file
    :param rule: same/diff notation table from excel file
    """
    wb = load_workbook(school_filename, read_only=True)
    ws_teacher = wb['導師名冊'] # ws is now an IterableWorksheet
    ws_boy = wb['男生名冊'] # ws is now an IterableWorksheet
    ws_girl = wb['女生名冊'] # ws is now an IterableWorksheet
    ws_special = wb['特殊生名冊'] # ws is now an IterableWorksheet
   
    teacher_list = []
    boy_list = []
    girl_list = []
    special_list = []
    same_list = []
    diff_list = []
    name_ = '姓名'
    same_ = '同班'
    diff_ = '不同班' 

    skip_row = 1 # skip first row
    for row in ws_teacher.rows:
        teacher_template = []
        #read each cell from xlsx
        for cell in row:
            if cell.value == name_:
                skip_row = 1
                continue
            if skip_row == 0:
                if (cell.value == None):
                    teacher_template.append(" ")
                else:
                    teacher_template.append(cell.value)
        if skip_row == 0:
            teacher_list.append(teacher_template)
        if skip_row == 1:
            skip_row = 0
    all_data.append(teacher_list) 

    skip_row = 1 # skip first row
    tag_same_or_diff = 0
    for row in ws_boy.rows:
        boy_template = []
        sd_template = []
        #read each cell from xlsx
        for cell in row:
            if cell.value == name_:
                skip_row = 1
                continue
            if skip_row == 0:
                if (cell.value == None):
                    boy_template.append(" ")
                else:
                    boy_template.append(cell.value)
            if cell.value == same_:
                tag_same_or_diff = 1
            if cell.value == diff_:
                tag_same_or_diff = 2
        if skip_row == 0:
            boy_list.append(boy_template)
            if tag_same_or_diff == 1:
                same_list.append(copy.deepcopy(boy_template))
                tag_same_or_diff = 0
            if tag_same_or_diff == 2:
                diff_list.append(copy.deepcopy(boy_template))
                tag_same_or_diff = 0
        if skip_row == 1:
            skip_row = 0
            tag_same_or_diff = 0

    all_data.append(boy_list) 
    
    skip_row = 1 # skip first row
    tag_same_or_diff = 0
    for row in ws_girl.rows:
        girl_template = []
        #read each cell from xlsx

        for cell in row:
            if cell.value == name_:
                skip_row = 1
                continue
            if skip_row == 0:
                if (cell.value == None):
                    girl_template.append(" ")
                else:
                    girl_template.append(cell.value)
            if cell.value == same_:
                tag_same_or_diff = 1
            if cell.value == diff_:
                tag_same_or_diff = 2

        if skip_row == 0:
            girl_list.append(girl_template)
            if tag_same_or_diff == 1:
                same_list.append(copy.deepcopy(girl_template))
                tag_same_or_diff = 0
            if tag_same_or_diff == 2:
                diff_list.append(copy.deepcopy(girl_template))
                tag_same_or_diff = 0
        if skip_row == 1:
            skip_row = 0
            tag_same_or_diff = 0
        #print(girl_template, sep='\n')

    #print (diff_list, sep='\n')
    all_data.append(girl_list) 
    
    skip_row = 1 #skip first row
    for row in ws_special.rows:
        special_template = []
        #read each cell from xlsx
        for cell in row:
            if cell.value == name_:
                skip_row = 1
                continue
            if skip_row == 0:
                if (cell.value == None):
                    special_template.append(" ")
                else:
                    special_template.append(cell.value)
        if skip_row == 0:
            special_list.append(special_template)
        if skip_row == 1:
            skip_row = 0
    all_data.append(special_list) 

    #print (diff_list, sep='\n')

    #remove unused column
    for row in same_list :
        del row[1]
        del row[1]
        del row[1]
        del row[1]
        del row[1]
        del row[1]
        row[2] = ' '
#       row[0] , row[1] = row[1], row [0]

    #remove unused column
    for row in diff_list :
        del row[1]
        del row[1]
        del row[1]
        del row[2]
        del row[2]
        row[3] = ' '
#       row[0] , row[2] = row[2], row [0]

    rule.append(copy.deepcopy(same_list)) 
    rule.append(copy.deepcopy(diff_list))
    print (rule, sep='\n')

