class Department:
    def __init__(self, name, foundation_year):
        self.name = name
        self.foundation_year = foundation_year
        self.member_list = []
    def add_member(self, member):
        self.member_list.append(member)

class StudentMarks:
    def __init__(self, student_name, semester, department, marks):
        self.student_name = student_name
        self.semester = semester
        self.subject = department
        self.marks = marks

class Student:
    def __init__(self,*args): # Name,Roll Number,Date of Birth,Year of Admission,Alumni
        self.name = args[0]
        self.roll_no = int(args[1])
        self.dob = args[2]
        self.year_dob = int(args[2].split('-')[2])
        self.year_of_admission = int(args[3])
        self.alumni = int(args[4])
    def __str__(self):
        return f"Name: {self.name} Date of Birth: {self.dob} Roll Number: {self.roll_no} Year of Admission: {self.year_of_admission} Alumni: {'True' if self.alumni == 1 else 'False'}"
    def export_data(self):
        return f"{self.name},{self.roll_no},{self.dob},{self.year_of_admission},{self.alumni}"

class Teacher:
    def __init__(self, name, gender, department, year_of_joining, subject):
        self.name = name
        self.gender = gender
        self.department = department
        self.year_of_joining = year_of_joining
        self.subject = subject
    def __str__(self):
        return f"Name: {self.name} Gender: {self.gender} Department: {self.department} Date of Joining: {self.year_of_joining} Subject: {self.subject}"
    def export_data(self):
        return f"{self.name},{self.gender},{self.department},{self.year_of_joining},{self.subject}"

def filter_students(students, attrib_no, attrib_value_inp):
    # Input Students - list of class Student
    error_message = ''
    export_file_name = ''
    filtered_students = students
    attrib_name = {1:'name', 2:'Roll No', 3:'Year of birth', 4:'Year of Admission', 5:'Is Alumni'}.get(attrib_no)

    if attrib_no in [2, 3, 4]:
        try:
            attrib_symbol = attrib_value_inp[0]; attrib_value = int(attrib_value_inp[1:])
        except:
            filtered_students = students
            error_message = 'Check Input - attrib_value_inp Error\nEg: =200'
        else: 

            if attrib_symbol == '>':
                filtered_students = [student for student in students if (attrib_no == 2 and student.roll_no > attrib_value) or (attrib_no == 3 and student.year_dob > attrib_value) or (attrib_no == 4 and student.year_of_admission > attrib_value)]
            elif attrib_symbol == '<':
                filtered_students = [student for student in students if (attrib_no == 2 and student.roll_no < attrib_value) or (attrib_no == 3 and student.year_dob < attrib_value) or (attrib_no == 4 and student.year_of_admission < attrib_value)]
            elif attrib_symbol == '=':
                filtered_students = [student for student in students if (attrib_no == 2 and student.roll_no == attrib_value) or (attrib_no == 3 and student.year_dob == attrib_value) or (attrib_no == 4 and student.year_of_admission == attrib_value)]
            else: 
                filtered_students = students
                error_message = 'Check Input: attrib_symbol Error\nEg: =200'

    elif attrib_no == 1:
        attrib_value = attrib_value_inp

        if attrib_value:
            filtered_students = [student for student in students if attrib_value.lower() in student.name.lower()]
        else:
            error_message = 'Check Input: Give a name keyword to filter'
        
    elif attrib_no == 5:
        attrib_value = attrib_value_inp

        # print(attrib_value)
        if attrib_value.lower() == 'y':
            attrib_value = 1
            filtered_students = [student for student in students if attrib_value == student.alumni]
        elif attrib_value.lower() == 'n':
            attrib_value = 0
            filtered_students = [student for student in students if attrib_value == student.alumni]
        else:
            error_message = 'Check Input: attrib_value_inp Error\nEg: "y" or "n"'

    if not error_message:
        export_file_name = f'{attrib_name}-{attrib_value}_'

    return filtered_students, export_file_name, error_message

def student_attrib_check(filter_no, new_value):
    error_message = ''
    #Name,Roll Number,Date of Birth,Year of Admission,Alumni
    
    return error_message

def attribute_checker(filter_no, new_value):
    import re
    if filter_no in [2,4,5]:
        new_value = int(new_value)       
    if filter_no == 2:
        if not isinstance(new_value, int) or len(str(new_value)) != 3:
            print(not isinstance(new_value, int), len(str(new_value)))
            return "Error: The input value is not a 3 digit integer."
    elif filter_no == 3:
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", new_value):
            return "Error: The input value is not in the format ii-ii-iiii where i is an integer."
    elif filter_no == 4:
        if not isinstance(new_value, int) or len(str(new_value)) != 4:
            return "Error: The input value is not a 4 digit integer."
    elif filter_no == 5:
        if new_value not in [0, 1]:
            return "Error: The input value is not either 0 or 1."
    # else:
    #     return "Error: Invalid filter number."
    return None


def read_file(filename):
    with open(filename, mode='r') as file:
        member_data =[]
        next(file)
        if 'student' in filename:
            for line in file:
                data = tuple(line.strip().split(','))
                member = Student(*data)
                member_data.append(member)
        else:
            print('\nread_file condition in module_database not matched\n')
    return member_data
def write_file(data, filename):
    with open(filename, 'w') as file:
        file.write('Name, Roll Number, Date of Birth, Year of Admission, Alumni\n')
        for member in data:
            file.write(f'{member.export_data()}\n')

def split_file_by_lines(source_filename, destination_filename, lines_per_file):
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
    # print('split complete')


def hash_string(string):
    hash = 0
    for char in string:
        hash = (hash * 31 + ord(char)) % 2**32
    return hash


if __name__ == '__main__':
    print(hash_string('Admin'))