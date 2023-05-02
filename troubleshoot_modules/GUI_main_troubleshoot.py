import os
import shutil 
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from GUI_popups import StudentDatabaseGUI


class Database_Manager:
    def __init__(self, master):
        style = ttk.Style()
        font = Font(family="Helvetica", size=12)
        style.configure("TButton", font=font)

        self.master = master
        self.master.title('Database Manager')
        self.master.geometry('500x100')
        
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(side="left", fill="y", expand=False)
        self.student_button = ttk.Button(self.button_frame, text='Student Database', command=self.student_database)
        self.teacher_button = ttk.Button(self.button_frame, text='Teachers Database', command=self.teachers_database)
        self.student_button.pack(padx=10, pady=(0,20))
        self.teacher_button.pack()

    def student_database(self):
        def personal_info():
            self.master.withdraw()
            button_personal_info.pack_forget()
            button_mark_database.pack_forget()
            button_frame.pack_forget()

            
            new_window = StudentDatabaseGUI(self.master)
            new_window.main_window.wait_window()
            self.master.deiconify()
        def mark_data():
            self.master.withdraw()
            button_personal_info.pack_forget()
            button_mark_database.pack_forget()
            button_frame.pack_forget()


            new_window = StudentDatabaseGUI(self.master)
            new_window.main_window.wait_window()
            self.master.deiconify()

        button_frame = ttk.Frame(self.master)
        button_frame.pack(side="top", fill="y", expand=True)
        button_personal_info = self.student_button = ttk.Button(button_frame, text='Personal Data', command=personal_info)
        button_mark_database = self.student_button = ttk.Button(button_frame, text='Student Marks', command=mark_data)
        button_personal_info.pack()
        button_mark_database.pack()
    def mark_database(self):
        self.master.withdraw()

        new_window = StudentDatabaseGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
    def teachers_database(self):
        self.master.withdraw()

        new_window = StudentDatabaseGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()

        
[directory for directory in ['./export', './.cache', './backup'] if not os.path.exists(directory) and os.makedirs(directory, exist_ok=True)]

if os.path.exists('./backup/student_data.csv'):
    source_filename = ["./backup/student_data.csv"]
    destination_filename = ['./.cache/student_data']
    # [mod.split_file_by_lines(source_file, destination_file, 100) for source_file in source_filename for destination_file in destination_filename]

    root = tk.Tk()
    my_gui = Database_Manager(root)
    root.mainloop()

    # shutil.rmtree('./.cache')               # uncomment to delete cache after each use

else:
    print("Program cannot start - ./backup/student_data.csv not found.")




## Reading files with names containing name_string
# dir_path = './.cache'
# name_string = 'studen'
# files = [filename for filename in os.listdir(dir_path) if filename.startswith(name_string)]
# print(files)