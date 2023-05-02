'''
DATABASE MANAGEMENT SYSTEM

Features -
 - Nested Filter with exports
 - Filter search optimised using threading
 - cache generated during runtime for ease of multithreading
 - Inheritance used for TeacherDatabaseGUI

'''

import os
import shutil                       # to remove .cache with all its sub directories
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import module_database as mod

class StudentDatabaseGUI:
	def __init__(self, master):
			# self.main_window = tk.Toplevel(master)
			self.main_window = master

			self.user_input = ''
			self.category = 'student'
			self.displayed_member_list = None
			self.export_file_name = f'all_{self.category}_data'
			self.current_backup_status = 1                              # backup not required
			self.button_pressed = tk.IntVar()

			# Reading data from latest backup
			file = [filename for filename in os.listdir('./backup') if filename.startswith(f'{self.category}_data')]
			self.members = mod.read_file(f'./backup/{file[-1]}')

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
			self.modify_button = ttk.Button(self.button_frame, text="Admin Login", command=self.modify_data)

			self.print_button.pack(side="left", padx=10, pady=5,)
			self.filter_button.pack(side="left", padx=10, pady=5)
			# self.export_button.pack(side="left", padx=10, pady=5)
			self.modify_button.pack(side="right", padx=10, pady=5)

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
			self.displayed_member_list = mod.read_file(f"./backup/{self.category}_data.csv")
			self.text_widget.delete('1.0', 'end')
			self.export_button.pack(side="top", padx=10, pady=5)
			self.text_widget.insert(tk.END, f'Here is the list of all {self.category}:\n')
			self.text_widget.insert(tk.END, '\n'.join(str(member) for member in self.displayed_member_list).join(f'\n\n'))
			self.text_widget.insert(tk.END, '\n')
			self.text_widget.see(tk.END)
	def export_data_button(self):
			self.text_widget.insert(tk.END, "Exporting data...\n")
			mod.write_file(self.displayed_member_list, './export/'+str(self.export_file_name)+'.csv')
			self.text_widget.insert(tk.END, "Export Successful. Check in ./export.\n\n")
			self.text_widget.see(tk.END)
	def new_interface(self, parameter):
		''' Used for filtering and add/modify data'''
		def back():
			# Destroy all existing buttons
			name_button.destroy()
			roll_no_button.destroy()
			dob_button.destroy()
			year_button.destroy()
			alumni_button.destroy()
			back_button.destroy()
			add_button.destroy()
			modify_button.destroy()
			self.export_button.pack_forget()

			# Unhide main menu buttons to frame
			self.print_button.pack(side="left", padx=10, pady=5)
			self.filter_button.pack(side="left", padx=10, pady=5)
			# self.export_button.pack(side="left", padx=10, pady=5)
			self.modify_button.pack(side="right", padx=10, pady=5)

			self.text_widget.delete(1.0, tk.END)
			self.button_pressed.set(110)

		# Hide all existing buttons
		self.print_button.pack_forget()
		self.export_button.pack_forget()
		self.filter_button.pack_forget()
		self.modify_button.pack_forget()

		name_button = ttk.Button(self.button_frame, text="Name", command=lambda:self.button_pressed.set(1))
		roll_no_button = ttk.Button(self.button_frame, text="Roll No", command=lambda:self.button_pressed.set(2))
		dob_button = ttk.Button(self.button_frame, text="Year of Birth", command=lambda:self.button_pressed.set(3))
		year_button = ttk.Button(self.button_frame, text="Year of Admission", command=lambda:self.button_pressed.set(4))
		alumni_button = ttk.Button(self.button_frame, text="Alumni", command=lambda:self.button_pressed.set(5))

		add_button = ttk.Button(self.button_frame, text="Add data", command=lambda:self.button_pressed.set(1))
		modify_button = ttk.Button(self.button_frame, text="Modify data", command=lambda:self.button_pressed.set(2))
		back_button = ttk.Button(self.button_frame, text="Back", command=back)

		back_button.pack(side="right", padx=10, pady=5)

		bypass = 0
		if parameter == 'filter':
			self.export_file_name = f'filter_{self.category}_'
			self.displayed_member_list = self.members
			parameter = 'filter'
			filter_name = {1:'name', 2:'Roll No', 3:'Year of birth', 4:'Year of Admission', 5:'Is Alumni'}
		elif parameter == 'admin':
			dob_button = ttk.Button(self.button_frame, text="Date of Birth", command=lambda:self.button_pressed.set(3))
			self.export_file_name = f'modify_{self.category}_'

			add_button.pack(side="left", padx=10, pady=5)
			modify_button.pack(side="left", padx=10, pady=5)

			self.text_widget.insert(tk.END, "Choose an option: \n")
			self.text_widget.see(tk.END)
			self.main_window.wait_variable(self.button_pressed)
			filter_name = {1:'name', 2:'Roll No', 3:'Date of birth', 4:'Year of Admission', 5:'Is Alumni'}

			if self.button_pressed.get() == 1:
					parameter = 'add'
					self.displayed_member_list = []
			elif self.button_pressed.get() == 2:
					parameter = 'narrow down'
					self.displayed_member_list = self.members
			else:
				bypass = 1

		if bypass != 1:
			add_button.pack_forget()
			modify_button.pack_forget()
			name_button.pack(side="left", padx=10, pady=5)
			roll_no_button.pack(side="left", padx=10, pady=5)
			dob_button.pack(side="left", padx=10, pady=5)
			year_button.pack(side="left", padx=10, pady=5)
			alumni_button.pack(side="left", padx=10, pady=5)
			self.export_button.pack(side="top", padx=10, pady=5)
			self.text_widget.insert(tk.END, f"Select attribute to {parameter} ...\n")
			self.text_widget.see(tk.END)
			self.main_window.wait_variable(self.button_pressed)			# intented for filter_no

		# Nested Filter Implementation
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
					self.text_widget.insert(tk.END, f"{filter_name.get(filter_no)} selected for {parameter}.\n")

				while True:
					if self.button_pressed.get() == 5:
						if bypass == 0:
							self.text_widget.insert(tk.END, "Is alumni? (y or n) and press Enter.\n")
						else:
							self.text_widget.insert(tk.END, "Is alumni? (1 or 0) and press Enter.\n")
						self.text_widget.see(tk.END)
					elif self.button_pressed.get() in [1, 2, 3, 4]:
						print('Check - bypass = 0 button_pressed in 1-4')
						if bypass == 0:
							self.text_widget.insert(tk.END, f"Input keyword to {parameter} and press Enter.\n")
						else:
							self.text_widget.insert(tk.END, f"Input the new value for {filter_name.get(filter_no)} and press Enter.\n")
						self.text_widget.see(tk.END)

					self.main_window.wait_variable(self.button_pressed)					# intented for filter_keyword

					if self.button_pressed.get() == 110:
						break
					elif (self.button_pressed.get() == 100) and (self.user_input):			# intented pipeline
						if bypass == 0:
							if parameter in ['filter', 'narrow down']:
								# export_file_name import is required to trim user_input for 
								#       an allowed file name
								self.displayed_member_list, export_file_name_temp, error_message = mod.filter_students(self.displayed_member_list, filter_no, self.user_input)

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
												self.text_widget.insert(tk.END, '\n'.join(str(member) for member in self.displayed_member_list)+'\n\n')
										
												self.text_widget.insert(tk.END, f'Select attribute for nested filtering or Export the results.\n')
												self.export_file_name += export_file_name_temp
												self.text_widget.see(tk.END)
												self.main_window.wait_variable(self.button_pressed)
												break

										elif parameter == 'narrow down':
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
												print('Check - confirm when len ==1')
												self.text_widget.insert(tk.END, f"Input 'y' to confirm selection to modify\n")
												self.text_widget.see(tk.END)
												self.main_window.wait_variable(self.button_pressed)

												if self.button_pressed.get() == 110:
													break
												elif self.button_pressed.get() == 100 and self.user_input.lower() == 'y':
													self.text_widget.insert(tk.END, f"Select attribute in this data for modification:\n")
													self.text_widget.see(tk.END)
													bypass = 1
													print('Check - Modify bypass = 1')
													break

												else:
													back()
													print('Check - Why are we here?')
													break

											else:
												print('Error in nested filter - modify - len(self.displayed_member_list)')

										else:
											print('Check -lets see 2')

								else:
									self.text_widget.insert(tk.END, f'{error_message}\n\n')
									self.text_widget.insert(tk.END, f"Select attribute to {parameter} ...\n")
									self.text_widget.see(tk.END)
							elif parameter == 'add':
								print('Check - parameter add')
								button_unpack = [name_button, roll_no_button, dob_button, year_button, alumni_button]
								new_value = self.user_input
								error_message = mod.attribute_checker(filter_no, new_value)

								if error_message:
									self.text_widget.insert(tk.END, str(error_message)+'\n')
								else:
									button_unpack[filter_no-1].pack_forget()
									self.displayed_member_list.append(new_value)
									self.text_widget.insert(tk.END, f'Input successful.\nSelect next attribute\n\n')
								
								if len(self.displayed_member_list) == 5:
									self.members.append(mod.Student(*self.displayed_member_list))
									self.current_backup_status = 0
									back()
									self.text_widget.insert(tk.END, f'New student successfully added.\n\n')
								break
			
							else:
										print('Check - lets see 4')

						elif bypass == 1 and parameter == 'narrow down':
						# Starting Modification
							new_value = self.user_input
							self.text_widget.insert(tk.END, f"{filter_name.get(filter_no)} will be changed to {new_value} in the above data\n")
							self.text_widget.insert(tk.END, 'Enter "y" to confirm changes\n')
							self.text_widget.see(tk.END)
							self.main_window.wait_variable(self.button_pressed)
							print('Check - we are here at bypass == 1 parameter == "narrow down"')

							if self.button_pressed.get() == 110:
								break
							elif self.button_pressed.get() == 100 and self.user_input.lower() == 'y':
								index = [index for index, member in enumerate(self.members) if member.name == self.displayed_member_list[0].name][0]
								attribute_name = {1:'name', 2:'roll_no', 3:'dob', 4:'year_of_admission', 5:'alumni'}
								error_message = mod.student_attrib_check(filter_no, new_value)

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
						print('Check - END of LOOP')
						break

		print('Check - My soul is free')

	def modify_data(self):
			self.new_interface('admin')
			# while True:
					# self.text_widget.insert(tk.END, "Enter Username: ")
					# self.text_widget.see(tk.END)
					# self.main_window.wait_variable(self.button_pressed)
					# if self.button_pressed.get() == 110:
					#         break
					# elif self.button_pressed.get() == 100:
					#     user = self.user_input
					#     self.text_widget.insert(tk.END, user +'\n')
					#     self.text_widget.insert(tk.END, "Enter Password: ")
					#     self.text_widget.see(tk.END)
					#     self.main_window.wait_variable(self.button_pressed)

					#     if self.button_pressed.get() == 110:
					#             break
					#     elif self.button_pressed.get() == 100:
					#         password = self.user_input
					#         self.text_widget.insert(tk.END, '*' *len(password) +'\n')

					#         if 63116079 == mod.hash_string(password) and user == 'Admin' :       # Admin
					#             self.new_interface('admin')
					#             break
					#         else:
					#             self.text_widget.delete('1.0', tk.END)
					#             self.text_widget.insert(tk.END, "Wrong Credentials\n\n")
					
	def close_window(self):         # Safely exit the loop in new_interface
			self.button_pressed.set(110)
			self.main_window.destroy()
			if self.current_backup_status == 0:
					index = len([filename for filename in os.listdir('./backup') if filename.startswith(f'{self.category}_data')])
					mod.write_file(self.members, f'./backup/{self.category}_data_{index}.csv')
					print('Check - backup complete')



if __name__ == '__main__':

	# Checks and makes new directory if necessary along with .temp folder
	[directory for directory in ['./export', './.cache', './backup'] if not os.path.exists(directory) and os.makedirs(directory, exist_ok=True)]

	if os.path.exists('./backup/student_data.csv'):
		source_filename = "./backup/student_data.csv"

		mod.split_file_by_lines(source_filename, './.cache/student_data', 100)

		root = tk.Tk()
		my_gui = StudentDatabaseGUI(root)
		root.bind("<Return>", lambda event=None: my_gui.enter_button.invoke())
		# root.bind("<Tab>", lambda event=None: my_gui.modify_button.focus_set())
		root.mainloop()

		# Reading files with names containing name_string
		dir_path = './.cache'
		name_string = 'zxv'
		files = [filename for filename in os.listdir(dir_path) if filename.startswith(name_string)]
		# print(files)


		# shutil.rmtree('./.cache')               # Deletes cache after use

	else:
		print("Program cannot start - ./backup/student_data.csv not found.")

