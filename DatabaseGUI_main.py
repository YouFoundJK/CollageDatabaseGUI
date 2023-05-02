'''
DATABASE MANAGEMENT SYSTEM

Features -
 - Nested Filter with exports
 - Department filter using multithreading
 - Addition/Modification of data won't rewrite old backup.
 - Inheritance used for TeacherDatabaseGUI, StudentMarksGUI
 - cache generated during runtime for ease of multithreading (to be implemented)
 - Modify data requires login: USERNAME AND PASSWORD is Admin implemented using hash
 - Filter search optimised using threading (partially implemented in Department filter)

UPDATES - 
v3.0
	- Improved the result aesthetics (tabular form using carriage return character)
	
Read before use - 
    - USERNAME AND PASSWORD for add/modify is Admin
'''

import os
import shutil 
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

class Database_Manager_GUI:
    def __init__(self, master):
        style = ttk.Style()
        font = Font(family="Helvetica", size=12)
        style.configure("TButton", font=font)

        self.master = master
        self.master.title('Database Manager')
        self.master.geometry('250x200')
        self.button_press = 0
        
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(side="top", fill="both", expand=False)
        self.department_button = ttk.Button(self.button_frame, text='Department', command=self.department_database, width=20)
        self.student_button = ttk.Button(self.button_frame, text='Student Database', command=self.student_database, width=20)
        self.teacher_button = ttk.Button(self.button_frame, text='Staff Database', command=self.teachers_database, width=20)
        self.credit_button = ttk.Button(self.button_frame, text='Credits', command= lambda: CreditsWindowGUI(self.master), width=20)
        self.department_button.pack(side="top", padx=10, pady=10)
        self.student_button.pack(side="top", padx=10, pady=(0,20))
        self.teacher_button.pack(side="top", padx=10, pady=10)
        self.credit_button.pack(side="top", padx=10, pady=10)
        
        self.button_frame_extended = ttk.Frame(self.master)
        self.button_personal_info = self.student_button = ttk.Button(self.button_frame_extended, text='Personal Data', command=self.personal_info, width=20)
        self.button_mark_database = self.student_button = ttk.Button(self.button_frame_extended, text='Student Marks', command=self.mark_data, width=20)
    def department_database(self):
        self.master.withdraw()
        self.button_personal_info.pack_forget()
        self.button_mark_database.pack_forget()
        self.master.geometry('250x200')
        self.button_frame.pack(side="top", fill="both", expand=False)
        self.button_press = 0

        new_window = DepartmentDatabaseGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
    def student_database(self):
        if self.button_press !=1:
            self.button_frame.pack(side="left", fill="both", expand=False)
            self.button_personal_info.pack(side="top", padx=10, pady=(50,0))
            self.button_frame_extended.pack(side="left", fill="y", expand=True)
            self.button_mark_database.pack(side="top", padx=10, pady=10)
            self.master.geometry('400x200')
            self.button_press = 1
    def personal_info(self):
        self.master.withdraw()
        self.button_personal_info.pack_forget()
        self.button_mark_database.pack_forget()
        self.master.geometry('250x200')
        self.button_frame.pack(side="top", fill="both", expand=False)
        self.button_press = 0
        
        new_window = StudentDatabaseGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
    def mark_data(self):
        self.master.withdraw()
        self.button_personal_info.pack_forget()
        self.button_mark_database.pack_forget()
        self.master.geometry('250x200')
        self.button_frame.pack(side="top", fill="both", expand=False)
        self.button_press = 0

        new_window = StudentMarksGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
    def mark_database(self):
        self.master.withdraw()
        self.master.geometry('250x200')
        self.button_frame.pack(side="top", fill="both", expand=False)

        new_window = StudentMarksGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
    def teachers_database(self):
        self.master.withdraw()
        self.master.geometry('250x200')
        self.button_frame.pack(side="top", fill="both", expand=False)
        self.button_personal_info.pack_forget()
        self.button_mark_database.pack_forget()
        self.button_press = 0

        new_window = TeacherDatabaseGUI(self.master)
        new_window.main_window.wait_window()
        self.master.deiconify()
class CreditsWindowGUI:
    def __init__(self, master):
        # self.master = master
        self.master = tk.Toplevel(master)
        self.master.title('Credits')
        self.master.geometry('800x400')
        self.canvas = tk.Canvas(self.master, width=800, height=400)
        self.canvas.pack()
        self.text = f"DATABASE MANAGEMENT SYSTEM\n\n\nAuthor: Jovi K\n\nLast Modified: 30 April 2023\nDatabase project commited as part of Coursework.\n\nFeatures -\n - Nested Filter with exports\n - Department filter using multithreading\n - Inheritance used for TeacherDatabaseGUI, StudentMarksGUI\n - Addition/Modification of data won't rewrite old backup.\n - Filter search optimised using threading (partially implemented in Department filter)\n - cache generated during runtime for ease of multithreading (to be implemented)\n\nUPDATES -\n\n v3.0\n - Improved the result aesthetics (tabular form using carriage return character)\n\n v2.2\n - Optimisation in filter and attribute_checker\n\nv2.1\n - Bug fix\n - aesthetics\n - Credits\n\n v2.0\n - Bug fix and optimisation\n"
        self.text_obj = None
        self.after_id = None
        self.y_pos = 500
        self.roll_credits()

    def roll_credits(self):
        if not self.text_obj:
            self.text_obj = self.canvas.create_text(400, 500, text=self.text, font=("Arial", 15), fill="black", width=800)

        self.canvas.move(self.text_obj, 0, -2)
        self.y_pos -= 2

        if self.y_pos < -100:
            self.y_pos = 500
            self.canvas.delete(self.text_obj)
            self.text_obj = None

        self.after_id = self.master.after(30, self.roll_credits)

class StudentDatabaseGUI:
	def __init__(self, master, inheritance_parameter = 'Student'):
			self.main_window = tk.Toplevel(master)
			# self.main_window = master
			self.user_input = ''
			self.category = 'student'
			self.displayed_member_list = None
			self.export_file_name = f'all_{self.category}_data'
			self.current_backup_status = 1                              # backup not required
			self.button_pressed = tk.IntVar()
			self.filter = member_filter                                 # used for filtering
			self.attrib_checker = member_attribute_checker              # used to check
			self.filter_name = {1:'Name', 2:'Roll No', 3:'Year of birth', 4:'Year of Admission', 5:'Is Alumni'}
			self.inheritance_manager = inheritance_parameter		# 'Student', 'Teacher', 'StudentMarks'
			self.main_window.title("Student Database")
			self.main_window.geometry("1200x652")
			style = ttk.Style()
			font = Font(family="Helvetica", size=12)
			style.configure("TButton", font=font)

			self.button_frame = ttk.Frame(self.main_window)
			self.button_frame.pack(side="top", fill="x", expand=False)
			self.print_button = ttk.Button(self.button_frame, text="Display All Data", command=self.print_data_button)
			self.filter_button = ttk.Button(self.button_frame, text="Search/filter data", command=lambda: self.new_interface('filter'))
			self.export_button = ttk.Button(self.button_frame, text="Export Data", command=self.export_data_button)
			self.admin_login = ttk.Button(self.button_frame, text="Admin Login", command=self.modify_data)

			self.name_button = ttk.Button(self.button_frame, text="Name", command=lambda:self.button_pressed.set(1))
			self.roll_no_button = ttk.Button(self.button_frame, text="Roll No", command=lambda:self.button_pressed.set(2))
			self.dob_button = ttk.Button(self.button_frame, text="Year of Birth", command=lambda:self.button_pressed.set(3))
			self.year_button = ttk.Button(self.button_frame, text="Year of Admission", command=lambda:self.button_pressed.set(4))
			self.alumni_button = ttk.Button(self.button_frame, text="Alumni", command=lambda:self.button_pressed.set(5))

			self.add_button = ttk.Button(self.button_frame, text="Add data", command=lambda:self.button_pressed.set(1))
			self.modify_button = ttk.Button(self.button_frame, text="Modify data", command=lambda:self.button_pressed.set(2))
			self.back_button = ttk.Button(self.button_frame, text="Back", command=self.back)

			if self.inheritance_manager == 'Student':    # Requirement for inheritance
				self.init_packing()
	def init_packing(self):
		# Reading data from latest backup
		file = [filename for filename in os.listdir('./backup') if filename.startswith(f'{self.category}_data')]
		self.members = read_file(f'./backup/{file[-1]}')


		self.print_button.pack(side="left", padx=10, pady=5,)
		self.filter_button.pack(side="left", padx=10, pady=5)
		# self.export_button.pack(side="left", padx=10, pady=5)
		self.admin_login.pack(side="right", padx=10, pady=5)

		# User Input / Entry Widget
		self.entry_frame = ttk.Frame(self.main_window)
		self.entry_frame.pack(side="bottom", fill="x", expand=False)
		self.entry = ttk.Entry(self.entry_frame)
		self.entry.pack(side="left", padx=10, fill="x", expand=True)
		# Enter Button
		self.enter_button = ttk.Button(self.entry_frame, text="Enter", command=self.get_entry)
		self.enter_button.pack(side="left", padx=10, pady=5)
		# main_window.bind("<Tab>", lambda event: self.enter_button.focus_set())

		# Text Area
		self.text_frame = ttk.Frame(self.main_window)
		self.text_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10) # , 
		self.text_widget = tk.Text(self.text_frame, font=("Arial", 14))
		self.text_widget.pack(side="left", fill="both", expand=True)
		# Scroll Bar for text
		scrollbar = ttk.Scrollbar(self.text_frame)
		scrollbar.pack(side='right', fill='y')
		scrollbar.config(command=self.text_widget.yview)
		self.text_widget.config(yscrollcommand=scrollbar.set)

		self.main_window.protocol("WM_DELETE_WINDOW", self.close_window)
		self.main_window.bind("<Return>", lambda event=None: self.enter_button.invoke())
	def get_entry(self):
			self.user_input = self.entry.get()
			self.button_pressed.set(100)
			self.entry.delete(0, tk.END) 
	def print_data_button(self):
			
			self.displayed_member_list = read_file(f"./backup/{self.category}_data.csv")		# Required for exporting data
			self.text_widget.delete('1.0', 'end')
			self.export_button.pack(side="top", padx=10, pady=5)
			self.text_widget.insert(tk.END, f'Here is the list of all {self.category}:\n\n')

			if self.members[1].category == 'student_marks':
				self.text_widget.insert(tk.END, f'Name\t\t\tSemester\tDepartment\t\tCGPA\n'+'-'*150)
			elif self.members[1].category == 'student':
				self.text_widget.insert(tk.END, f'Name\t\t\tDOB\t\tRoll No.\tYr of Admission\t\tAlumni\n'+'-'*150)
			elif self.members[1].category == 'teacher':
				self.text_widget.insert(tk.END, f'Name\t\t\tGender\tDepartment\t\tHOD\tYear of Joining\n'+'-'*150)
			
			self.text_widget.insert(tk.END, '\n'.join(str(member) for member in self.members).join(f'\n\n'))

			self.text_widget.see(tk.END)
	def export_data_button(self):
		self.text_widget.insert(tk.END, "Exporting data...\n")
		write_file(self.displayed_member_list, './export/'+str(self.export_file_name)+'.csv')
		self.text_widget.insert(tk.END, "Export Successful. Check in ./export.\n\n")
		self.text_widget.see(tk.END)
	def back(self):
		# unpack all existing buttons
		self.name_button.pack_forget()
		self.roll_no_button.pack_forget()
		self.dob_button.pack_forget()
		self.year_button.pack_forget()
		if self.inheritance_manager != 'StudentMarks':
			self.alumni_button.pack_forget()
		self.back_button.pack_forget()
		self.add_button.pack_forget()
		self.modify_button.pack_forget()
		self.export_button.pack_forget()

		# Unhide main menu buttons to frame
		self.print_button.pack(side="left", padx=10, pady=5)
		self.filter_button.pack(side="left", padx=10, pady=5)
		# self.export_button.pack(side="left", padx=10, pady=5)
		self.admin_login.pack(side="right", padx=10, pady=5)

		self.text_widget.delete(1.0, tk.END)
		self.button_pressed.set(110)
	def new_interface(self, parameter):
		''' Used for filtering and add/modify data'''

		# Hide all existing buttons
		self.print_button.pack_forget()
		self.export_button.pack_forget()
		self.filter_button.pack_forget()
		self.admin_login.pack_forget()

		self.back_button.pack(side="right", padx=10, pady=5)
		
		self.text_widget.delete('1.0', tk.END)
		bypass = 0
		if parameter == 'filter':
			self.export_file_name = f'filter_{self.category}_'
			self.displayed_member_list = self.members
			parameter = 'filter'
			
		elif parameter == 'admin':
			self.export_file_name = f'modify_{self.category}_'

			self.add_button.pack(side="left", padx=10, pady=5)
			self.modify_button.pack(side="left", padx=10, pady=5)

			self.text_widget.insert(tk.END, "Choose an option: \n")
			self.text_widget.see(tk.END)
			self.main_window.wait_variable(self.button_pressed)

			if self.button_pressed.get() == 1:
					parameter = 'add'
					self.displayed_member_list = [-1,-1,-1,-1,-1]
					if self.inheritance_manager == 'StudentMarks':											
						del self.displayed_member_list[-1]
			elif self.button_pressed.get() == 2:
					parameter = 'narrow down'
					self.displayed_member_list = self.members
			else:
				bypass = 1

		if bypass != 1:
			self.add_button.pack_forget()
			self.modify_button.pack_forget()
			self.name_button.pack(side="left", padx=10, pady=5)
			self.roll_no_button.pack(side="left", padx=10, pady=5)
			self.dob_button.pack(side="left", padx=10, pady=5)
			self.year_button.pack(side="left", padx=10, pady=5)
			if self.inheritance_manager != 'StudentMarks':
				self.alumni_button.pack(side="left", padx=10, pady=5)
			self.export_button.pack(side="top", padx=10, pady=5)
			self.text_widget.insert(tk.END, f"Select attribute to {parameter} ...\n")
			self.text_widget.see(tk.END)
			self.main_window.wait_variable(self.button_pressed)			# intented for filter_no

		# Nested Filter Implementation - handles Adding/Modifying and Filtering Data
		bypass = 0
		
		while True:
			''' 
			Nested Filter execution requires exiting checkpoints implemented in back() and while - break sequences. Otherwise closing the GUI doesn't exit the interpreter.

			'''
			if self.button_pressed.get() == 110:
				# exit code 110 - close button and back button
				break
			elif self.button_pressed.get() == 100:
				self.main_window.wait_variable(self.button_pressed)
			else:																														# intented pipeline
				filter_no = self.button_pressed.get()
				if bypass == 0:
					self.text_widget.insert(tk.END, f"{self.filter_name.get(filter_no)} selected for {parameter}.\n")

				while True:
					if self.button_pressed.get() == 5:
						if bypass == 0:
							self.text_widget.insert(tk.END, "Input y or n and press Enter.\n")
						else:
							self.text_widget.insert(tk.END, "Input 1 or 0 and press Enter.\n")
						self.text_widget.see(tk.END)
					elif self.button_pressed.get() in [1, 2, 3, 4]:
						if bypass == 0:
							self.text_widget.insert(tk.END, f"Input keyword to {parameter} and press Enter.\n")
						else:
							self.text_widget.insert(tk.END, f"Input the new value for {self.filter_name.get(filter_no)} and press Enter.\n")
						self.text_widget.see(tk.END)

					self.main_window.wait_variable(self.button_pressed)					# intented for filter_keyword

					if self.button_pressed.get() == 110:
						break
					elif (self.button_pressed.get() == 100) and (self.user_input):			# intented pipeline
						if bypass == 0:
							if parameter in ['filter', 'narrow down']:
								# export_file_name import is required to trim user_input for 
								#       an allowed file name
								self.displayed_member_list, export_file_name_temp, error_message = self.filter(self.displayed_member_list, filter_no, self.user_input)

								if not error_message: 
									self.text_widget.insert(tk.END, f"Results for data containing names with keyword: '{self.user_input}'\n\n")
									
									if not self.displayed_member_list: 
											self.text_widget.insert(tk.END, 'No match found\n')
											self.displayed_member_list = self.members              # Reset the data pool
											self.text_widget.insert(tk.END, f"Select attribute to {parameter} ...\n")
											self.text_widget.see(tk.END)   
											self.main_window.wait_variable(self.button_pressed)
											break
									else:

										if parameter == 'filter':
											if self.members[1].category == 'student_marks':
												self.text_widget.insert(tk.END, f'Name\t\t\tSemester\tDepartment\t\tCGPA\n'+'-'*150+'\n')
											elif self.members[1].category == 'student':
												self.text_widget.insert(tk.END, f'Name\t\t\tDOB\t\tRoll No.\tYr of Admission\t\tAlumni\n'+'-'*150+'\n')
											elif self.members[1].category == 'teacher':
												self.text_widget.insert(tk.END, f'Name\t\t\tGender\tDepartment\t\tHOD\tYear of Joining\n'+'-'*150+'\n')

											self.text_widget.insert(tk.END, '\n'.join(str(member) for member in self.displayed_member_list)+'\n\n')
									
											self.text_widget.insert(tk.END, f'Select attribute for nested filtering or Export the results.\n')
											self.export_file_name += export_file_name_temp
											self.text_widget.see(tk.END)
											self.main_window.wait_variable(self.button_pressed)
											break

										elif parameter == 'narrow down':
											if self.members[1].category == 'student_marks':
												self.text_widget.insert(tk.END, f'Name\t\t\tSemester\tDepartment\t\tCGPA\n'+'-'*150+'\n')
											elif self.members[1].category == 'student':
												self.text_widget.insert(tk.END, f'Name\t\t\tDOB\t\tRoll No.\tYr of Admission\t\tAlumni\n'+'-'*150+'\n')
											elif self.members[1].category == 'teacher':
												self.text_widget.insert(tk.END, f'Name\t\t\tGender\tDepartment\t\tHOD\tYear of Joining\n'+'-'*150+'\n')

											self.text_widget.insert(tk.END, '\n'.join(str(member) for member in self.displayed_member_list)+'\n\n')
												
											if len(self.displayed_member_list) != 1:
												self.text_widget.insert(tk.END, f'Select attribute for narrowing down on result to modify.\n')
												self.text_widget.see(tk.END)
												while True:
													self.main_window.wait_variable(self.button_pressed)
													if self.button_pressed.get() != 100:
														break
												break

											elif len(self.displayed_member_list) == 1:
												self.text_widget.insert(tk.END, f"Input 'y' to confirm selection to modify\n")
												self.text_widget.see(tk.END)
												self.main_window.wait_variable(self.button_pressed)

												if self.button_pressed.get() == 110:
													break
												elif self.button_pressed.get() == 100 and self.user_input.lower() == 'y':
													self.text_widget.insert(tk.END, f"Select attribute in this data for modification:\n")
													self.text_widget.see(tk.END)
													bypass = 1
													break

												else:
													self.back()
													break

											else:
												print('Error in nested filter - modify - len(self.displayed_member_list)')
												pass

										else:
											print('Error -lets see 2')
											pass

								else:
									self.text_widget.insert(tk.END, f'{error_message}\n\n')
									self.text_widget.insert(tk.END, f"Select attribute to {parameter} ...\n")
									self.text_widget.see(tk.END)
							elif parameter == 'add':
								if self.inheritance_manager == 'StudentMarks':
									button_unpack = [self.name_button, self.roll_no_button, self.dob_button, self.year_button]
								elif self.inheritance_manager == 'Student':
									button_unpack = [self.name_button, self.roll_no_button, self.dob_button, self.year_button, self.alumni_button]
								else:
									button_unpack = [self.name_button, self.roll_no_button, self.dob_button, self.year_button, self.alumni_button]

								new_value = self.user_input
								error_message, new_value = self.attrib_checker(self.inheritance_manager,filter_no, new_value)

								if error_message:
									self.text_widget.insert(tk.END, str(error_message)+'\n')
								else:
									button_unpack[filter_no-1].pack_forget()
									self.displayed_member_list[filter_no-1] = (new_value)
									self.text_widget.insert(tk.END, f'Input successful.\nSelect next attribute\n\n')
								
								if (not -1 in self.displayed_member_list and self.inheritance_manager == 'Student'):
									self.members.append(Student(*self.displayed_member_list))
									self.current_backup_status = 0
									self.back()
									self.text_widget.insert(tk.END, f'New student successfully added.\n\n')
									self.text_widget.see(tk.END)
								elif (not -1 in self.displayed_member_list and self.inheritance_manager == 'StudentMarks'):
									self.members.append(StudentMarks(*self.displayed_member_list))
									self.current_backup_status = 0
									self.back()
									self.text_widget.insert(tk.END, f'New Student Marks successfully added.\n\n')
									self.text_widget.see(tk.END)
								elif (not -1 in self.displayed_member_list and self.inheritance_manager == 'Teacher'):
									self.members.append(Teacher(*self.displayed_member_list))
									self.current_backup_status = 0
									self.back()
									self.text_widget.insert(tk.END, f'New Staff successfully added.\n\n')
									self.text_widget.see(tk.END)
								break
			
							else:
								print('Check - lets see 4')
								pass

						elif bypass == 1 and parameter == 'narrow down':
						# Starting Modification
							new_value = self.user_input
							self.text_widget.insert(tk.END, f"{self.filter_name.get(filter_no)} will be changed to {new_value} in the above data\n")
							self.text_widget.insert(tk.END, 'Enter "y" to confirm changes\n')
							self.text_widget.see(tk.END)
							self.main_window.wait_variable(self.button_pressed)

							if self.button_pressed.get() == 110:
								break
							elif self.button_pressed.get() == 100 and self.user_input.lower() == 'y':
								index = [index for index, member in enumerate(self.members) if member.name == self.displayed_member_list[0].name][0]
								attribute_name = {1:'name', 2:'roll_no', 3:'dob', 4:'year_of_admission', 5:'alumni'}
								error_message, new_value = self.attrib_checker(self.inheritance_manager, filter_no, new_value)

								if not error_message:
										setattr(self.members[index], attribute_name.get(filter_no), new_value)
										self.text_widget.insert(tk.END, 'Value succesfully changed.\nSelect a new attribute to change value or press back.\n\n')
										self.text_widget.see(tk.END)
										self.current_backup_status = 0
										break
								else:
											self.text_widget.insert(tk.END, str(error_message)+'\n')
											self.text_widget.see(tk.END)
							elif self.button_pressed.get() == 100:
								self.text_widget.insert(tk.END, 'Enter the correct value and press enter\n')
								self.main_window.wait_variable(self.button_pressed)
							else:
								print('Check - what to do??')
								break
					else:
						break
	def modify_data(self):
			# self.new_interface('admin')
			self.button_pressed.set(0)
			self.text_widget.delete("1.0", "end")
			
			while self.button_pressed.get() != 110:
				self.text_widget.delete("end-1l", "end")
				self.text_widget.insert(tk.END, "\nEnter Username: ")
				self.text_widget.see(tk.END)
				self.main_window.wait_variable(self.button_pressed)			# Username input
				if self.button_pressed.get() == 100 and self.user_input:
					user = self.user_input
					self.text_widget.insert(tk.END, user +"\nEnter Password: ")
					self.text_widget.see(tk.END)
					self.main_window.wait_variable(self.button_pressed)		# Password input

					if self.button_pressed.get() == 110:
							break
					elif self.button_pressed.get() == 100:
						password = self.user_input
						self.text_widget.insert(tk.END, '*' *len(password) +'\n')

						if 63116079 == hash_string(password) and user == 'Admin' :       # Admin
							self.new_interface('admin')
							break
						else:
							self.text_widget.delete('1.0', tk.END)
							self.text_widget.insert(tk.END, "Wrong Credentials\n\n")
	def close_window(self):         # Safely exit the loop in new_interface
		self.button_pressed.set(110)
		self.main_window.destroy()
		if self.current_backup_status == 0:
			# Changes to reflect in both Student_data.csv and Student_marks.csv
			index = len([filename for filename in os.listdir('./backup') if filename.startswith(f'{self.category}_data')])
			write_file(self.members, f'./backup/{self.category}_data_{index}.csv')
class TeacherDatabaseGUI(StudentDatabaseGUI):       # Inherited from StudentDatabaseGUI
	def __init__(self, master):
		super().__init__(master, 'Teacher')
		
		self.category = 'teacher'
		self.main_window.title("Staff Database")
		
		self.filter_name = {1:'Name', 2:'Gender', 3:'Department', 4:'Year of Joining', 5:'Is HOD'}

		self.name_button = ttk.Button(self.button_frame, text="Name", command=lambda:self.button_pressed.set(1))
		self.roll_no_button = ttk.Button(self.button_frame, text="Gender", command=lambda:self.button_pressed.set(2))
		self.dob_button = ttk.Button(self.button_frame, text="Department", command=lambda:self.button_pressed.set(3))
		self.year_button = ttk.Button(self.button_frame, text="Year of Joining", command=lambda:self.button_pressed.set(4))
		self.alumni_button = ttk.Button(self.button_frame, text="HOD", command=lambda:self.button_pressed.set(5))
		
		self.init_packing()
class StudentMarksGUI(StudentDatabaseGUI):       	# Inherited from StudentDatabaseGUI
	def __init__(self, master):
		super().__init__(master, 'StudentMarks')
		
		self.category = 'student_marks'
		self.main_window.title("Mark Database")
		self.filter_name = {1:'Name', 2:'Semester', 3:'Department', 4:'CGPA'}
		
		self.name_button = ttk.Button(self.button_frame, text="Name", command=lambda:self.button_pressed.set(1))
		self.roll_no_button = ttk.Button(self.button_frame, text="Semester", command=lambda:self.button_pressed.set(2))
		self.dob_button = ttk.Button(self.button_frame, text="Department", command=lambda:self.button_pressed.set(3))
		self.year_button = ttk.Button(self.button_frame, text="CGPA", command=lambda:self.button_pressed.set(4))
		self.alumni_button = ttk.Button(self.button_frame, text="HOD", command=lambda:self.button_pressed.set(5))
		
		self.init_packing()
class DepartmentDatabaseGUI:
	def __init__(self, master):
		self.main_window = tk.Toplevel(master)
		# self.main_window = master

		self.user_input = None
		self.category = 'department' #'Members'
		self.displayed_member_list = None
		self.export_file_name = f'all_{self.category}_data'
		self.button_pressed = tk.IntVar()

		self.main_window.title("Department Database")
		self.main_window.geometry("1200x652")
		style = ttk.Style()
		font = Font(family="Helvetica", size=12)
		style.configure("TButton", font=font)

		self.members = []

		self.button_frame = ttk.Frame(self.main_window)
		self.button_frame.pack(side="top", fill="x", expand=False)

		self.depart_info_button = ttk.Button(self.button_frame, text="Department Information", command=lambda: self.disply_filter_members('display_info'))
		self.filter_button = ttk.Button(self.button_frame, text="Search/filter Members", command=lambda: self.disply_filter_members('filter'))
		self.export_button = ttk.Button(self.button_frame, text="Export Data", command=self.export_data_button)
		self.back_button = ttk.Button(self.button_frame, text="Back", command=self.back)

		self.depart_info_button.pack(side="left", padx=10, pady=5,)
		self.filter_button.pack(side="left", padx=10, pady=5)

		# self.admin_login.pack(side="right", padx=10, pady=5)

		# User Input / Entry Widget
		self.entry_frame = ttk.Frame(self.main_window)
		self.entry_frame.pack(side="bottom", fill="x", expand=False)
		self.entry = ttk.Entry(self.entry_frame)
		self.entry.pack(side="left", padx=10, fill="x", expand=True)
		# Enter Button
		self.enter_button = ttk.Button(self.entry_frame, text="Enter", command=self.get_entry)
		self.enter_button.pack(side="left", padx=10, pady=5)
		# main_window.bind("<Tab>", lambda event: self.enter_button.focus_set())

		# Text Area
		self.text_frame = ttk.Frame(self.main_window)
		self.text_frame.pack(side="top", fill="both", expand=True, pady=10, padx=10) # , 
		self.text_widget = tk.Text(self.text_frame, font=("Arial", 14))
		self.text_widget.pack(side="left", fill="both", expand=True)
		# Scroll Bar for text
		scrollbar = ttk.Scrollbar(self.text_frame)
		scrollbar.pack(side='right', fill='y')
		scrollbar.config(command=self.text_widget.yview)
		self.text_widget.config(yscrollcommand=scrollbar.set)

		self.main_window.protocol("WM_DELETE_WINDOW", self.close_window)
		self.main_window.bind("<Return>", lambda event=None: self.enter_button.invoke())

	def get_entry(self):
		self.user_input = self.entry.get()
		self.button_pressed.set(100)
		self.entry.delete(0, tk.END) 
	def disply_filter_members(self, parameter):
		self.text_widget.delete('1.0', 'end')
		departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology']
		self.button_pressed.set(0)
		self.text_widget.insert(tk.END, f'Lists out all the students and teachers in the department under separate heading.\nInput a department to view the list: ')
		while self.button_pressed.get() != 110:
			self.main_window.wait_variable(self.button_pressed)
			list_department = ''
			if self.button_pressed.get() == 100 and self.user_input:
				self.text_widget.insert(tk.END, str(self.user_input)+'\n')
				filtered_departments = [department for department in departments if self.user_input.lower() in department.lower()]
				if len(filtered_departments) != 0:
					if parameter == 'display_info':
						with open('./backup/department_info.csv', 'r') as file:
							for line in file:
								data = line.strip().split(',')
								if self.user_input.lower() in data[0].lower():
									list_department+=f'\nName: {data[0]}.\nDate of Formation: {data[1]}.\nHistoric Summary: {data[2]}\n\n'
						self.text_widget.insert(tk.END, list_department)
						self.text_widget.insert(tk.END, f'\nInput another department to view details:')	
						self.text_widget.see(tk.END)
					else:
						if len(filtered_departments) != 1:
							self.text_widget.insert(tk.END, f'Multiple departments selected:\n')	
							self.text_widget.insert(tk.END, ', '.join(member for member in filtered_departments))
							self.text_widget.insert(tk.END, f'\n\nInput keyword to select one:')	
							self.text_widget.see(tk.END)

						else:
							self.export_button.pack(side="top", padx=10, pady=5)
							file = [filename for filename in os.listdir('./backup') if filename.startswith(f'student_marks_data')]
							student_list = read_file(f'./backup/{file[-1]}')
							file = [filename for filename in os.listdir('./backup') if filename.startswith(f'teacher_data')]
							teacher_list = read_file(f'./backup/{file[-1]}')
							student_list, teacher_list = worker_filter_department(filtered_departments[0], student_list, teacher_list)
							
							self.text_widget.delete('1.0', 'end')
							self.text_widget.insert(tk.END, f'Students in {filtered_departments[0]}:\n')
							self.text_widget.insert(tk.END, f'Name\t\t\tSemester\tDepartment\t\tCGPA\n'+'-'*150+'\n')
							self.text_widget.insert(tk.END, f'\n'.join(str(member) for member in student_list).join(f'\n\n'))
							self.text_widget.insert(tk.END, '\n')
							self.text_widget.see(tk.END)
							self.text_widget.insert(tk.END, f'Teachers in {filtered_departments[0]}:\n')
							self.text_widget.insert(tk.END, f'Name\t\t\tGender\tDepartment\t\tHOD\tYear of Joining\n'+'-'*150+'\n')
							self.text_widget.insert(tk.END, '\n'.join(str(member) for member in teacher_list).join(f'\n\n'))
							self.text_widget.insert(tk.END, '\n')
							self.text_widget.insert(tk.END, f'Enter new department to filter or export the results.\nFor nested filtering options go to other database.\n')
							self.text_widget.see(tk.END)
							
							self.displayed_member_list = student_list
							self.displayed_member_list.extend(teacher_list)
							self.export_file_name = f'department_filter_{filtered_departments[0]}'

				else:
					self.text_widget.insert(tk.END, f'\nNo department with that keyword found.\nInput a department for filter:')	
					self.text_widget.see(tk.END)
			elif self.button_pressed.get() != 100:
				self.button_pressed.set(110)
	def export_data_button(self):
		self.text_widget.insert(tk.END, "Exporting data...\n")
		write_file(self.displayed_member_list, './export/'+str(self.export_file_name)+'.csv')
		self.text_widget.insert(tk.END, "Export Successful. Check in ./export.\n\n")
		self.text_widget.see(tk.END)
	def back(self):
		# unpack all existing buttons
		self.name_button.pack_forget()
		self.roll_no_button.pack_forget()
		self.dob_button.pack_forget()
		self.year_button.pack_forget()
		self.alumni_button.pack_forget()
		self.back_button.pack_forget()
		self.add_button.pack_forget()
		self.modify_button.pack_forget()
		self.export_button.pack_forget()

		# Unhide main menu buttons to frame
		self.print_button.pack(side="left", padx=10, pady=5)
		self.filter_button.pack(side="left", padx=10, pady=5)
		# self.export_button.pack(side="left", padx=10, pady=5)
		self.admin_login.pack(side="right", padx=10, pady=5)

		self.text_widget.delete(1.0, tk.END)
		self.button_pressed.set(110)
	
	def modify_data(self):
			# self.new_interface('admin')
			self.button_pressed.set(0)
			self.text_widget.delete("1.0", "end")
			
			while self.button_pressed.get() != 110:
				self.text_widget.delete("end-1l", "end")
				self.text_widget.insert(tk.END, "\nEnter Username: ")
				self.text_widget.see(tk.END)
				self.main_window.wait_variable(self.button_pressed)			# Username input
				if self.button_pressed.get() == 100 and self.user_input:
					user = self.user_input
					self.text_widget.insert(tk.END, user +'\n')
					self.text_widget.insert(tk.END, "Enter Password: ")
					self.text_widget.see(tk.END)
					self.main_window.wait_variable(self.button_pressed)		# Password input

					if self.button_pressed.get() == 110:
							break
					elif self.button_pressed.get() == 100:
						password = self.user_input
						self.text_widget.insert(tk.END, '*' *len(password) +'\n')

						if 63116079 == hash_string(password) and user == 'Admin' :       # Admin
							self.new_interface('admin')
							break
						else:
							self.text_widget.delete('1.0', tk.END)
							self.text_widget.insert(tk.END, "Wrong Credentials\n\n")
	def close_window(self):         # Safely exit the loop in new_interface
		self.button_pressed.set(110)
		self.main_window.destroy()

class StudentMarks:
    def __init__(self, *args):
        # student_name, semester, department, marks
        self.category = 'student_marks'
        self.name = args[0]
        self.semester = int(args[1])
        self.department = args[2]
        self.cgpa = args[3]
    def __str__(self):
        return f"{self.name}\t\t\t{self.semester}\t{self.department}\t\t{self.cgpa}"
    def export_data(self):
        #Name,Roll Number,Date of Birth,Year of Admission,Alumni
        return f"{self.name},{self.semester},{self.department},{self.cgpa}"
class Student:
    def __init__(self, *args): 
	# Name,Roll Number,Date of Birth,Year of Admission,Alumni
        self.category = 'student'
        self.name = args[0]
        self.roll_no = int(args[1])
        self.dob = args[2]
        self.year_dob = int(args[2].split('-')[2])
        self.year_of_admission = int(args[3])
        self.alumni = int(args[4])
    def __str__(self):
        return f"{self.name}\t\t\t{self.dob}\t\t{self.roll_no}\t{self.year_of_admission}\t\t{'Yes' if self.alumni == 1 else 'No'}"
    def export_data(self):
        #Name,Roll Number,Date of Birth,Year of Admission,Alumni
        return f"{self.name},{self.roll_no},{self.dob},{self.year_of_admission},{self.alumni}"
class Teacher:
    def __init__(self, *args): 
        #name, gender, department, hod, year_of_joining
        self.category = 'teacher'
        self.name = args[0]
        self.gender = int(args[1])
        self.department = args[2]
        self.hod = int(args[3])
        self.year_of_joining = int(args[4])
    def __str__(self):
        return f"{self.name}\t\t\t{'M' if self.gender == 1 else 'F'}\t{self.department}\t\t{'Yes' if self.hod == 1 else 'No'}\t{self.year_of_joining}"
    def export_data(self):
        return f"{self.name},{self.gender},{self.department},{self.hod},{self.year_of_joining}"

def member_filter(members, attrib_no, attrib_value_inp):
    if members[0].category == 'student':
	# Input members - list of class Student
        error_message = ''
        export_file_name = ''
        filtered_members = members
        attrib_name = {1:'name', 2:'Roll No', 3:'Year of birth', 4:'Year of Admission', 5:'Is Alumni'}.get(attrib_no)

        if attrib_no in [2, 3, 4]:
            try:
                attrib_symbol = attrib_value_inp[0]; attrib_value = int(attrib_value_inp[1:])
            except:
                filtered_members = members
                error_message = 'Check Input - attrib_value_inp Error\nEg: =200'
            else: 

                if attrib_symbol == '>':
                    filtered_members = [student for student in members if (attrib_no == 2 and student.roll_no > attrib_value) or (attrib_no == 3 and student.year_dob > attrib_value) or (attrib_no == 4 and student.year_of_admission > attrib_value)]
                elif attrib_symbol == '<':
                    filtered_members = [student for student in members if (attrib_no == 2 and student.roll_no < attrib_value) or (attrib_no == 3 and student.year_dob < attrib_value) or (attrib_no == 4 and student.year_of_admission < attrib_value)]
                elif attrib_symbol == '=':
                    filtered_members = [student for student in members if (attrib_no == 2 and student.roll_no == attrib_value) or (attrib_no == 3 and student.year_dob == attrib_value) or (attrib_no == 4 and student.year_of_admission == attrib_value)]
                else: 
                    filtered_members = members
                    error_message = 'Check Input: attrib_symbol Error\nEg: =200'

        elif attrib_no == 1:
            attrib_value = attrib_value_inp

            if attrib_value:
                filtered_members = [student for student in members if attrib_value.lower() in student.name.lower()]
            else:
                error_message = 'Check Input: Give a name keyword to filter'
            
        elif attrib_no == 5:
            attrib_value = attrib_value_inp
            if attrib_value.lower() == 'y':
                attrib_value = 1
                filtered_members = [student for student in members if attrib_value == student.alumni]
            elif attrib_value.lower() == 'n':
                attrib_value = 0
                filtered_members = [student for student in members if attrib_value == student.alumni]
            else:
                error_message = 'Check Input: attrib_value_inp Error\nEg: "y" or "n"'

        if not error_message:
            export_file_name = f'{attrib_name}-{attrib_value}_'

        return filtered_members, export_file_name, error_message
    elif members[0].category == 'teacher':
        # Input members - list of class teacher
        error_message = ''
        export_file_name = ''
        filtered_teachers = members
        attrib_name = {1:'Name', 2:'Gender', 3:'Department', 4:'Year of Joining', 5:'HOD'}.get(attrib_no)
        # DONE - 2, 5, 4
        if attrib_no == 4:
            try:
                attrib_symbol = attrib_value_inp[0]; attrib_value = int(attrib_value_inp[1:])
            except:
                filtered_teachers = members
                error_message = 'Check Input - attrib_value_inp Error\nEg: =2007'
            else: 
                filtered_teachers = []
                if attrib_symbol == '>':
                    filtered_teachers = [teacher for teacher in members if teacher.year_of_joining > attrib_value]
                elif attrib_symbol == '<':
                    filtered_teachers = [teacher for teacher in members if teacher.year_of_joining < attrib_value]
                elif attrib_symbol == '=':
                    filtered_teachers = [teacher for teacher in members if teacher.year_of_joining == attrib_value]
                else: 
                    filtered_teachers = members
                    error_message = 'Check Input: attrib_symbol Error\nEg: =2006'

        elif attrib_no in [1, 3]:
            attrib_value = attrib_value_inp

            if attrib_value:
                filtered_teachers = []
                filtered_teachers = [teacher for teacher in members if (attrib_value.lower() in teacher.name.lower() or attrib_value.lower() in teacher.department.lower())]
            else:
                error_message = 'Check Input: Give a name keyword to filter'
                if attrib_no == 3:
                    error_message+="\nValid departments are: 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology'"
            
        elif attrib_no in [2, 5]:
            attrib_value = attrib_value_inp

            if attrib_value.lower() == 'y' or attrib_value.lower() == 'm':
                attrib_value = 1
                filtered_teachers = [teacher for teacher in members if ((attrib_value == teacher.hod and attrib_no == 5 ) or (attrib_value == teacher.gender and attrib_no == 2 ))]
		
            elif attrib_value.lower() == 'n' or attrib_value.lower() == 'f':
                attrib_value = 0
                filtered_teachers = [teacher for teacher in members if ((attrib_value == teacher.hod and attrib_no == 5 ) or (attrib_value == teacher.gender and attrib_no == 2 ))]
            else:
                if attrib_no == 2:
                    error_message = 'Check Input: attrib_value_inp Error\nEg: "m" or "f"'
                else:
                    error_message = 'Check Input: attrib_value_inp Error\nEg: "y" or "n"'

        if not error_message:
            export_file_name = f'{attrib_name}-{attrib_value}_'

        return filtered_teachers, export_file_name, error_message
    elif members[0].category == 'student_marks':
        # Input members - list of class student_mark
        error_message = ''
        export_file_name = ''
        filtered_members = members
        attrib_name = {1:'Name', 2:'Semester', 3:'Department', 4:'CGPA'}.get(attrib_no)
        if attrib_no in [2, 4]:
            try:
                attrib_symbol = attrib_value_inp[0]
                if attrib_no == 2:
                    attrib_value = int(attrib_value_inp[1:])
                else:
                    attrib_value = int(float(attrib_value_inp[1:])*10)
            except:
                filtered_members = members
                if attrib_no == 2:
                    error_message = 'Check Input - attrib_value_inp Error\nEg: >7'
                else:
                    error_message = 'Check Input - attrib_value_inp Error\nEg: <5.6'
            else: 
                if attrib_symbol == '>':
                    filtered_members = [student_mark for student_mark in members if (int(float(student_mark.cgpa)*10) > attrib_value or student_mark.semester > attrib_value)]
                elif attrib_symbol == '<':
                    filtered_members = [student_mark for student_mark in members if (int(float(student_mark.cgpa)*10) < attrib_value or student_mark.semester < attrib_value)]
                elif attrib_symbol == '=':
                    filtered_members = [student_mark for student_mark in members if (int(float(student_mark.cgpa)*10) == attrib_value or student_mark.semester == attrib_value)]
                else: 
                    filtered_members = members
                    error_message = 'Check Input: attrib_symbol Error\nEg: =2006'

        elif attrib_no in [1, 3]:
            attrib_value = attrib_value_inp

            if attrib_value:
                filtered_members = [student_mark for student_mark in members if (attrib_value.lower() in student_mark.name.lower() or attrib_value.lower() in student_mark.department.lower())]
            else:
                error_message = 'Check Input: Give a name keyword to filter'
                if attrib_no == 3:
                    error_message+="\nValid departments are: 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology'"
            
        if not error_message:
            export_file_name = f'{attrib_name}-{attrib_value}_'

        return filtered_members, export_file_name, error_message
def member_attribute_checker(category, filter_no, new_value):
	import re
	department = new_value
	error_message = None
	if category == 'Student':
		if filter_no in [2,4,5]:
			try:
				new_value = int(new_value)   
			except:
				error_message = "InputError: Enter Integer Input."
			else:    
				if filter_no == 2:
					if not isinstance(new_value, int) or len(str(new_value)) != 3:
						error_message = "InputError: The input value is not a 3 digit integer."
				elif filter_no == 4:
					if not isinstance(new_value, int) or len(str(new_value)) != 4:
						error_message = "InputError: The input value is not a 4 digit integer."
				elif filter_no == 5:
					if new_value not in [0, 1]:
						error_message = "InputError: The input value is not either 0 or 1."
		elif filter_no == 3:
			if not re.match(r"^\d{2}-\d{2}-\d{4}$", new_value):
				error_message = "InputError: The input value is not in the format dd-mm-yyyy where i is an integer."
		else:
			error_message = None
		return error_message, new_value
	elif category == 'Teacher':
    # 1:'Name', 2:'Gender', 3:'Department', 4:'Year of Joining', 5:'HOD'
		if filter_no in [2,4,5]:
			try:
				new_value = int(new_value)
			except:
				if filter_no == 2:
					error_message = "InputError: Input 1 for Male or 0 for Female"
				else:
					error_message = "InputError: Input Integer values"
			else:
				if filter_no == 4:
					if not isinstance(new_value, int) or len(str(new_value)) != 4:
						error_message = "InputError: The input value is not a 4 digit integer."
				elif filter_no in [2, 5]:
					if new_value not in [0, 1]:
						error_message = "InputError: The input value either 0 or 1."

		elif filter_no == 3:
			departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology']
			matches = [department for department in departments if new_value.lower() in department.lower()]
			if len(matches) != 1:
				error_message = "InputError: Department not uniquely identifiable\nInput any in: 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology'"
			else:
				department = matches[0]
				error_message = None
		else:
			error_message = None

		return error_message, department
	elif category == 'StudentMarks':
		# 1:'Name', 2:'Semester', 3:'Department', 4:'CGPA'
		if filter_no in [2,4]:
			try:
				if filter_no == 2:
					new_value = int(new_value)
				else:
					new_value = float(new_value)
				
			except:
				if filter_no == 2:
					error_message = "InputError: Input Interger value between 1-10"
				else:
					error_message = "InputError: Input float value between 1-10"
			else:
				if new_value > 10 or new_value < 0:
					error_message = "InputError: The input value between 1 and 10."

		elif filter_no == 3:
			departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology']
			matches = [department for department in departments if new_value.lower() in department.lower()]
			if len(matches) != 1:
				error_message = "InputError: Department not uniquely identifiable\nInput any in: 'Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology'"
			else:
				department = matches[0]
				error_message = None
		else:
			error_message = None
		return error_message, department        

def read_file(filename):
    if 'student_data' in filename:
        Member = Student
    elif 'teacher' in filename:
        Member = Teacher
    elif 'student_marks' in filename:
        Member = StudentMarks
    else:
        print('\nread_file condition not matched\n')
    if Member:
        member_data = []
        with open(filename, mode='r') as file:
            next(file)
            for line in file:
                data = tuple(line.strip().split(','))
                member = Member(*data)
                member_data.append(member)
    return member_data
def write_file(data, filename):
	header = ''
	if 'student_data' in filename:
		header = 'Name, Roll Number, Date of Birth, Year of Admission, Alumni\n'
	elif 'teacher' in filename:
		header = 'Name, Gender, Department, Is HOD, Year of Joining\n'
	elif 'student_marks' in filename:
		header = 'Name, Semester, Department, CGPA\n'
	else:
		print('\nread_file condition in module_database not matched\n')
	with open(filename, 'w') as file:
		file.write(header)
		for member in data:
			file.write(f'{member.export_data()}\n')

def hash_string(string):
    '''
    For Login password hashing
    '''
    hash = 0
    for char in string:
        hash = (hash * 31 + ord(char)) % 2**32
    return hash
def worker_filter_department(department_name, student_list, teacher_list):
    '''
    Filtering for department members using multithreading
    '''
    def worker(members_list, department_name, append_to):
        for member in members_list:
            if member.department.lower() == department_name.lower():
                append_to.append(member)

    filter_teachers = []
    filter_students = []
    threads = [threading.Thread(target=worker, args=(student_list, department_name, filter_students)), 
               threading.Thread(target=worker, args=(teacher_list, department_name, filter_teachers))]
    
    [t.start() for t in threads]
    [t.join() for t in threads]

    return filter_students, filter_teachers
def split_file_by_lines(source_filename, destination_filename, lines_per_file):
    ''' 
    Not implemented yet. To be used for faster filtering using multithreading.
    '''
    with open(source_filename) as file:
        out_file = None
        next(file)
        for i, line in enumerate(file):
            if i % lines_per_file == 0:
                if out_file:
                    out_file.close()
                out_file = open(f"{destination_filename}_{i//lines_per_file}.csv", "w")
            out_file.write(line)
        if out_file:
            out_file.close()

if __name__=='__main__':
    [directory for directory in ['./export', './.cache', './backup'] if not os.path.exists(directory) and os.makedirs(directory, exist_ok=True)]
    file_paths = ['./backup/department_info.csv', './backup/student_data.csv', './backup/student_marks_data.csv', './backup/teacher_data.csv']

    exitcode = 0
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist.")
            exitcode = 1
    if exitcode == 0:
        root = tk.Tk()
        my_gui = Database_Manager_GUI(root)
        root.mainloop()
    shutil.rmtree('./.cache')               # uncomment to delete cache after each use
