import random
from datetime import datetime


def generate_random_data(n):
    data = []
    dept = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Economics', 'Psychology', 'Sociology']
    for i in range(len(n)):
        semester = random.randint(1, 10)
        department = random.choice(dept)
        cgpa = round(random.uniform(4, 9.9), 1)
        data.append([n[i], str(semester), department, str(cgpa)])
    return data


names=[]
with open('./student_data.csv', 'r') as file:
    next(file)
    for line in file:
        temp = line.split(',')[0]
        names.append(temp)

data = generate_random_data(names)
filename = "student_marks.csv"
with open(filename, mode='w') as file:
    for row in data:
        file.write(','.join(row) + '\n')