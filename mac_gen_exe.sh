pyinstaller --clean --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' ./src/interface.py
cp ./dist/interface ./Yunlin_normal_class_grouping
