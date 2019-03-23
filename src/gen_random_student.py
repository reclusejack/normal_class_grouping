import xlsxwriter
import random
import string
import sys
import names
import argparse
from operator import itemgetter

parser = argparse.ArgumentParser(description='please input totoal student count')
parser.add_argument('-n','--number', help='studnet count',required=True)
args = parser.parse_args()
  
## show values ##
print ("Input number: %s" % args.number )

workbook = xlsxwriter.Workbook('106502斗六國中.xlsx')
teacher_sheet = workbook.add_worksheet('導師名冊')
#work_sheet = workbook.add_worksheet('所有學生名冊')
boy_sheet = workbook.add_worksheet('男生名冊')
girl_sheet = workbook.add_worksheet('女生名冊')
special_sheet = workbook.add_worksheet('特殊生名冊')

teacher_list = []
student_list = []
boy_list = []
girl_list = []
special_list = []
row = 0
col = 0
boy = 1
girl = 1
for x in range(1, int(args.number) + 1 ):
        gen_student = []
        ran = random.randint(1, 2) 
        if ran == 1:
                gen_student.append("")
                gen_student.append(names.get_first_name(gender='female')+str(x))
                gen_student.append("女")
                gen_student.append(random.randint(150,300))
                gen_student.append("")
                gen_student.append("")
                gen_student.append("")
                gen_student.append("")
#                print("girl: %d" %girl)        
#                girl = girl + 1
                girl_list.append(gen_student)
        else :
                gen_student.append("")
                gen_student.append(names.get_first_name(gender='male')+str(x))
                gen_student.append("男")
                gen_student.append(random.randint(150,300))
                gen_student.append("")
                gen_student.append("")
                gen_student.append("")
                gen_student.append("")
#                print("boy: %d" %boy)
#                boy = boy + 1
                boy_list.append(gen_student)
#        print("index number %d" %x)
        student_list.append(gen_student)

student_list = sorted(student_list, key = lambda x : int(x[3]), reverse=True)
boy_list = sorted(boy_list, key = lambda x : int(x[3]), reverse=True)
girl_list = sorted(girl_list, key = lambda x : int(x[3]), reverse=True)

#append sequence number base on scores

#serial_number = 1
#for row in range(len(student_list)):
#    student_list[row][0] = serial_number 
#    serial_number += 1

# generate random group/ungroup list
g_serial_number = 1
for row in range(len(girl_list)):
    girl_list[row][0] = "G%d" %g_serial_number 
    g_serial_number += 1

b_serial_number = 1
for row in range(len(boy_list)):
    boy_list[row][0] = "B%d" %b_serial_number 
    b_serial_number += 1

for x in range(1, int(args.number) + 1 ):
        sd = random.randint(1, 10)
        if sd > 8 and x > 1:
            sd_number = random.randint(1, x-1)
            if sd_number == x-1:
                continue
            if (sd == 10):
                if student_list[sd_number][7] != "":
                    continue
                student_list[x-1][5] = "同班"
                student_list[x-1][7] = student_list[sd_number][0]
                student_list[sd_number][5] = "同班"
                student_list[sd_number][7] = student_list[x-1][0]
            else:
                if student_list[sd_number][7] != "":
                    continue
                student_list[x-1][6] = "不同班"
                student_list[x-1][7] = student_list[sd_number][0]
                student_list[sd_number][6] = "不同班"
                student_list[sd_number][7] = student_list[x-1][0]

#generate special list
for x in range(1, random.randint(5, 20)):
        gen_student = []
        ran = random.randint(1, 2) 
        if ran == 1:
                gen_student.append("")
                gen_student.append(names.get_first_name(gender='female')+str(x))
                gen_student.append("女")
                gen_student.append(random.randint(150,300))
                gen_student.append("")
                special_list.append(gen_student)
        else :
                gen_student.append("")
                gen_student.append(names.get_first_name(gender='male')+str(x))
                gen_student.append("男")
                gen_student.append(random.randint(150,300))
                gen_student.append("")
                special_list.append(gen_student)

s_serial_number = 1
for row in range(len(special_list)):
    special_list[row][0] = "S%d" %s_serial_number 
    s_serial_number += 1

#generate teacher list
for x in range(1, int((int(args.number)-(int(args.number)%30))/30) + 4 ):
        gen_teacher = []
        ran = random.randint(1, 2) 
        if ran == 1:
                gen_teacher.append("")
                gen_teacher.append(names.get_first_name(gender='female')+str(x))
                gen_teacher.append("女")
                gen_teacher.append("")
                gen_teacher.append("")
                teacher_list.append(gen_teacher)
        else :
                gen_teacher.append("")
                gen_teacher.append(names.get_first_name(gender='male')+str(x))
                gen_teacher.append("男")
                gen_teacher.append("")
                gen_teacher.append("")
                teacher_list.append(gen_teacher)

t_serial_number = 1
for row in range(len(teacher_list)):
    teacher_list[row][0] = "T%d" %t_serial_number 
    t_serial_number += 1

#teacher title
gen_teacher = []
gen_teacher.append("編號")
gen_teacher.append("姓名")
gen_teacher.append("性別")
gen_teacher.append("編訂班別")
gen_teacher.append("備註")
teacher_list.insert(0, gen_teacher)
gen_title = []
gen_title.append("雲林縣國立斗六國中106學年度新生常態編班導師原始名冊")
teacher_list.insert(0, gen_title)


#student title
#gen_student = []
#gen_student.append("序號")
#gen_student.append("姓名")
#gen_student.append("性別")
#gen_student.append("成績")
#gen_student.append("編訂班別")
#gen_student.append("同班")
#gen_student.append("不同班")
#gen_student.append("同班/不同班 序號")
#gen_student.append("備註")
#student_list.insert(0, gen_student)
boy_list.insert(0, gen_student)
girl_list.insert(0, gen_student)
gen_special_student = []
gen_special_student.append("序號")
gen_special_student.append("姓名")
gen_special_student.append("性別")
gen_special_student.append("成績")
gen_special_student.append("編訂班別")
gen_special_student.append("備註")
special_list.insert(0, gen_special_student)

#gen_title = []
#gen_title.append("雲林縣國立斗六國中106學年度新生常態編班學生原始名冊")
#student_list.insert(0, gen_title)
gen_title = []
gen_title.append("雲林縣國立斗六國中106學年度新生常態編班男生原始名冊")
boy_list.insert(0, gen_title)
gen_title = []
gen_title.append("雲林縣國立斗六國中106學年度新生常態編班女生原始名冊")
girl_list.insert(0, gen_title)
gen_title = []
gen_title.append("雲林縣國立斗六國中106學年度新生常態編班特殊生原始名冊")
special_list.insert(0, gen_title)


merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'left',
    'valign': 'vcenter',
    'fg_color': 'black'})
teacher_sheet.merge_range('A1:E1', 'Merged Range', merge_format)
#work_sheet.merge_range('A1:I1', 'Merged Range', merge_format)
boy_sheet.merge_range('A1:I1', 'Merged Range', merge_format)
girl_sheet.merge_range('A1:I1', 'Merged Range', merge_format)
special_sheet.merge_range('A1:I1', 'Merged Range', merge_format)


#for name in student_list:
#        print("name: %s" %name)

for row, data in enumerate(teacher_list):
        teacher_sheet.write_row(row, col, data)

#for row, data in enumerate(student_list):
#        work_sheet.write_row(row, col, data)

for row, data in enumerate(boy_list):
        boy_sheet.write_row(row, col, data)

for row, data in enumerate(girl_list):
        girl_sheet.write_row(row, col, data)

for row, data in enumerate(special_list):
        special_sheet.write_row(row, col, data)
workbook.close()
