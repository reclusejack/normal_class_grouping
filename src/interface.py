from tkinter import *
from tkinter import ttk
import tkinter, tkinter.constants, tkinter.filedialog
from tkinter.font import Font
from group import *
from load_data import *
from write_data import *
import re;

orig_data = [] 
group_data = [] 
rule = [] 
th_tab = 0
by_tab = 1
gl_tab = 2
sp_tab = 3

class NestedPanesDemo(ttk.Frame):

    def convert65536(self, s):
        #Converts a string with out-of-range characters in it into a string with codes in it.
        l=list(s);
        i=0;
        while i<len(l):
            o=ord(l[i]);
            if o>65535:
                l[i]="{"+str(o)+"ū}";
            i+=1;
        return "".join(l);

    def parse65536(self, match):
        #This is a regular expression method used for substitutions in convert65536back()
        text=int(match.group()[1:-2]);
        if text>65535:
            return chr(text);
        else:
            return "ᗍ"+str(text)+"ūᗍ";
    def convert65536back(self, s):
        #Converts a string with codes in it into a string with out-of-range characters in it
        while re.search(r"{\d\d\d\d\d+ū}", s)!=None:
            s=re.sub(r"{\d\d\d\d\d+ū}", self.parse65536, s);
        s=re.sub(r"ᗍ(\d\d\d\d\d+)ūᗍ", r"{\1ū}", s);
        return s;

    def __init__(self, isapp=True, name='class_grouping'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('雲林縣常態編班程式')
        self.isapp = isapp
        self._create_widgets()
         
    def _create_widgets(self):
         
        self._create_group_panel()
         
    def _create_group_panel(self):
        groupPanel = ttk.Frame(self, name='group')
        groupPanel.pack(side=TOP, fill=BOTH, expand=Y)
         
        self._create_wnd_struct(groupPanel)
        self._input_pane()
        self._button_pane()
        self._status_pane()
        self._grouping_status_pane()
         
    def _create_wnd_struct(self, parent):
        outer = ttk.PanedWindow(parent, orient=VERTICAL, name='outer')
         
        top = ttk.PanedWindow(outer, orient=HORIZONTAL, name='top')
        bot = ttk.PanedWindow(outer, orient=HORIZONTAL, name='bot')
        tl = ttk.LabelFrame(top, text='學校資訊', padding=3, name='tleft',width=250, height=140)
        tlm = ttk.LabelFrame(top, text='編班狀態', padding=3, name='tleftmid',width=250, height=140)
        tm = ttk.LabelFrame(top, text='編班資訊', padding=3, name='tmid', width=250, height=140)
        tr = ttk.LabelFrame(top, text='操作', padding=3, name='tright', width=250, height=140)
        top.add(tl)
        top.add(tlm)
        top.add(tm)
        top.add(tr)
        outer.pack(side=LEFT, expand=Y, fill=BOTH)
        outer.add(top)

        outer.pack(side=RIGHT, expand=Y, fill=BOTH)
        outer.add(bot)
        
        bl = ttk.LabelFrame(bot, text='男生名單', padding=3, name='bleft', width=380, height=420)
        bm = ttk.LabelFrame(bot, text='女生名單', padding=3, name='bmid', width=380, height=420)
        br = ttk.LabelFrame(bot, text='導師名單', padding=3, name='bright', width=240, height=420)
        bot.add(bl)
        bot.add(bm)
        bot.add(br)
 
    def _button_pane(self):
        # create and add button
        tright = self.nametowidget('group.outer.top.tright')
        bo = ttk.Button(tright, text='開檔', command=self.askopenfilename)
        bo.pack(expand=0, padx=2, pady=3)
        bo = ttk.Button(tright, text='編班', command=self.group_func)
        bo.pack(expand=0, padx=2, pady=3)
        bo = ttk.Button(tright, text='存檔', command=self.write_func)
        bo.pack(expand=0, padx=2, pady=3)

         
    def _input_pane(self):
        self.separate = IntVar()
        #self.separate.set(0)
        self.total_class = StringVar()
        self.boy_class = StringVar()
        self.girl_class = StringVar()
        self.separate.set(0)
        tmid = self.nametowidget('group.outer.top.tmid')
        rb1 = ttk.Radiobutton(tmid, text='男女合班', variable=self.separate, value=0, command=self.selected)
        rb2 = ttk.Radiobutton(tmid, text='男女分班', variable=self.separate, value=1, command=self.selected)
        rb1.pack()
        rb2.pack()
        leftlabel = ttk.Frame(tmid)
        rightentry = ttk.Frame(tmid)
        leftlabel.pack(side=LEFT) 
        rightentry.pack(side=RIGHT) 
        self.label_total = Label(leftlabel, text= "男女合班總數")
        self.entry_class_number = ttk.Entry(rightentry)
        self.entry_class_number.pack()
        self.label_total.pack()
        self.label_boy = Label(leftlabel, text= "男生班總數")
        self.label_boy.pack()
        self.entry_boy_class_number = ttk.Entry(rightentry)
        self.label_girl = Label(leftlabel, text= "女生班總數")
        self.label_girl.pack()
        self.entry_girl_class_number = ttk.Entry(rightentry)
        self.entry_boy_class_number.pack()
        self.entry_girl_class_number.pack()
        self.entry_class_number.configure(state="normal")
        self.entry_class_number.update()
        self.entry_boy_class_number.configure(state="disabled")
        self.entry_girl_class_number.configure(state="disabled")
        self.entry_boy_class_number.update()
        self.entry_girl_class_number.update()

    def selected(self):
        if self.separate.get()==1:
            self.entry_boy_class_number.configure(state="normal")
            self.entry_girl_class_number.configure(state="normal")
            self.entry_boy_class_number.update()
            self.entry_girl_class_number.update()
            self.entry_class_number.configure(state="disabled")
            self.entry_class_number.update()
            print ("separated")
        else :
            self.entry_class_number.configure(state="normal")
            self.entry_class_number.update()
            self.entry_boy_class_number.configure(state="disabled")
            self.entry_girl_class_number.configure(state="disabled")
            self.entry_boy_class_number.update()
            self.entry_girl_class_number.update()
            print ("merged")

    def _grouping_status_pane(self):
        tlm = self.nametowidget('group.outer.top.tleftmid')
        leftmidlabel = ttk.Frame(tlm)
        leftmidlabel.pack() 
        self.grouping_status = StringVar()
        self.grouping_status.set("請選擇學校")
        self.label_grouping_status = Label(leftmidlabel, textvariable = self.grouping_status, fg = "blue", font="16")
        self.label_grouping_status.pack()

        botl = self.nametowidget('group.outer.bot.bleft')
        boyframe = ttk.Frame(botl)
        boyframe.pack(side=TOP, fill=BOTH, expand=Y)
        self._create_boy_treeview(boyframe)
        botm = self.nametowidget('group.outer.bot.bmid')
        girlframe = ttk.Frame(botm)
        girlframe.pack(side=TOP, fill=BOTH, expand=Y)
        self._create_girl_treeview(girlframe)
        botr = self.nametowidget('group.outer.bot.bright')
        teacherframe = ttk.Frame(botr)
        teacherframe.pack(side=TOP, fill=BOTH, expand=Y)
        self._create_teacher_treeview(teacherframe)

    def _status_pane(self):
        tleft = self.nametowidget('group.outer.top.tleft')
        leftlabel = ttk.Frame(tleft)
        leftlabel.pack() 
        self.label_teacher_string = StringVar()
        self.label_teacher_string.set("導師人數:")
        self.label_st_string = StringVar()
        self.label_st_string.set("學生人數:")
        self.label_boy_string = StringVar()
        self.label_boy_string.set("男生人數:")
        self.label_girl_string = StringVar()
        self.label_girl_string.set("女生人數:")
        self.label_sp_string = StringVar()
        self.label_sp_string.set("特殊生人數:")
        self.label_teacher_number= Label(leftlabel, textvariable = self.label_teacher_string)
        self.label_teacher_number.pack()
        self.label_student_number= Label(leftlabel, textvariable = self.label_st_string)
        self.label_student_number.pack()
        self.label_boy_number= Label(leftlabel, textvariable = self.label_boy_string)
        self.label_boy_number.pack()
        self.label_girl_number= Label(leftlabel, textvariable = self.label_girl_string)
        self.label_girl_number.pack()
        self.label_special_number= Label(leftlabel, textvariable = self.label_sp_string)
        self.label_special_number.pack()

    def _status_school_update(self):
        self.teacher_number = len(orig_data[th_tab]) 
        self.label_teacher_string.set("導師人數:"+str(self.teacher_number))
        self.student_number= len(orig_data[by_tab]) + len(orig_data[gl_tab]) + len(orig_data[sp_tab])
        self.label_st_string.set("學生人數:"+str(self.student_number))
        self.boy_number = len(orig_data[by_tab])
        self.label_boy_string.set("男生人數:"+str(self.boy_number))
        self.girl_number = len(orig_data[gl_tab])
        self.label_girl_string.set("女生人數:"+str(self.girl_number))
        self.special_number = len(orig_data[sp_tab])
        self.label_sp_string.set("特殊生人數:"+str(self.special_number))
             
    def askopenfilename(self):
        self.filename = tkinter.filedialog.askopenfilename()
        print ("open filename : %s" %self.filename)
# clean all data
        del orig_data[:]
        del group_data[:]
        del rule[:]
        for i in self.boy_tree.get_children():
            self.boy_tree.delete(i)
        for i in self.girl_tree.get_children():
            self.girl_tree.delete(i)
        for i in self.teacher_tree.get_children():
            self.teacher_tree.delete(i)
# clean all data
        load_data(self.filename, orig_data, rule)
        tmp = self.filename.replace(".xlsx", "")
        schoolname = re.search(r'.*\d+(.*)$', tmp).group(1)
        self.grouping_status.set("讀取"+ schoolname +"新生資料")
        self._status_school_update()
        self._load_boy_data()
        self._load_girl_data()
        self._load_teacher_data()


    def group_func(self):
        print ("grouping!!")
        if self.separate.get() == 1:
            self.total_class = "0"
            self.boy_class = self.entry_boy_class_number.get()
            self.girl_class = self.entry_girl_class_number.get()
        else :
            self.total_class = self.entry_class_number.get()
            self.boy_class = "0"
            self.girl_class = "0"
        group_data = grouping(orig_data, self.total_class, self.boy_class, self.girl_class, rule)
        self.data = copy.deepcopy(group_data)
        print ("Total class number ", self.total_class)
        print ("boy class number ", self.boy_class)
        print ("girl class number ", self.girl_class)
        self.grouping_status.set("編班結束 請存檔")


    def write_func(self):
        writefile(self.data, self.filename, self.total_class, self.boy_class, self.girl_class)
        print ("writing file!!")
        self.grouping_status.set("存檔結束")
# clean all data
        del orig_data[:]
        del group_data[:]
        del rule[:]
        for i in self.boy_tree.get_children():
            self.boy_tree.delete(i)
        for i in self.girl_tree.get_children():
            self.girl_tree.delete(i)
        for i in self.teacher_tree.get_children():
            self.teacher_tree.delete(i)
        self.label_teacher_string.set("導師人數:")
        self.label_st_string.set("學生人數:")
        self.label_boy_string.set("男生人數:")
        self.label_girl_string.set("女生人數:")
        self.label_sp_string.set("特殊生人數:")
        self.entry_boy_class_number.delete(0, 'end')
        self.entry_girl_class_number.delete(0, 'end')
        self.entry_class_number.delete(0, 'end')

    def _create_boy_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=TOP, fill=BOTH, expand=Y)
         
        # create the tree and scrollbars
        self.studentCols = ('姓名', '序號', '成績','同班','不同班','對應序號')
        self.boy_tree = ttk.Treeview(columns=self.studentCols,
                                 show = 'headings')
         
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.boy_tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.boy_tree.xview)
        self.boy_tree['yscroll'] = ysb.set
        self.boy_tree['xscroll'] = xsb.set
         
        # add boy_tree and scrollbars to frame
        self.boy_tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)
         
        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def _create_girl_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=TOP, fill=BOTH, expand=Y)
         
        # create the tree and scrollbars
        self.studentCols = ('姓名', '序號', '成績','同班','不同班','對應序號')
        self.girl_tree = ttk.Treeview(columns=self.studentCols,
                                 show = 'headings')
         
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.girl_tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.girl_tree.xview)
        self.girl_tree['yscroll'] = ysb.set
        self.girl_tree['xscroll'] = xsb.set
         
        # add girl_tree and scrollbars to frame
        self.girl_tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)
         
        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def _create_teacher_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=TOP, fill=BOTH, expand=Y)
         
        # create the tree and scrollbars
        self.teacherCols = ('姓名', '序號', '性別')       
        self.teacher_tree = ttk.Treeview(columns=self.teacherCols,
                                 show = 'headings')
         
        ysb = ttk.Scrollbar(orient=VERTICAL, command= self.teacher_tree.yview)
        xsb = ttk.Scrollbar(orient=HORIZONTAL, command= self.teacher_tree.xview)
        self.teacher_tree['yscroll'] = ysb.set
        self.teacher_tree['xscroll'] = xsb.set
         
        # add teacher_tree and scrollbars to frame
        self.teacher_tree.grid(in_=f, row=0, column=0, sticky=NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=NS)
        xsb.grid(in_=f, row=1, column=0, sticky=EW)
         
        # set frame resize priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

    def _load_boy_data(self):
      # configure column headings
        for c in self.studentCols:
            self.boy_tree.heading(c, text=c.title(),
                              command=lambda c=c: self._column_sort(c, MCListDemo.SortDir))
            self.boy_tree.column(c, width=Font().measure(c.title()))
             
        # add data to the boy_tree
        for item in orig_data[by_tab]:
            item[1] = self.convert65536(''.join(item[1]))
            self.boy_tree.insert('', 'end', values=(item[1],item[0],item[3],item[5],item[6],item[7]))
            item[1] = self.convert65536back(''.join(item[1]))
             
    def _load_girl_data(self):
      # configure column headings
        for c in self.studentCols:
            self.girl_tree.heading(c, text=c.title(),
                              command=lambda c=c: self._column_sort(c, MCListDemo.SortDir))
            self.girl_tree.column(c, width=Font().measure(c.title()))
             
        # add data to the girl_tree
        for item in orig_data[gl_tab]:
            item[1] = self.convert65536(''.join(item[1]))
            self.girl_tree.insert('', 'end', values=(item[1],item[0],item[3],item[5],item[6],item[7]))
            item[1] = self.convert65536back(''.join(item[1]))

    def _load_teacher_data(self):
      # configure column headings
        for c in self.teacherCols:
            self.teacher_tree.heading(c, text=c.title(),
                              command=lambda c=c: self._column_sort(c, MCListDemo.SortDir))
            self.teacher_tree.column(c, width=Font().measure(c.title()))
             
        # add data to the teacher_tree
        for item in orig_data[th_tab]:
            item[1] = self.convert65536(''.join(item[1]))
            self.teacher_tree.insert('', 'end', values=(item[1],item[0],item[2]))
            item[1] = self.convert65536back(''.join(item[1]))
         
 
if __name__ == '__main__':
    root = Tk()
    root.call('encoding','system','unicode')
    root.minsize(width=1000, height=600)
    root.resizable(width=False, height=False)
    NestedPanesDemo().mainloop()
