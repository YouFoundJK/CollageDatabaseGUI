import random
from datetime import datetime

def generate_random_data(n):
    first_names = ['John', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Isabella', 'Lucas', 'Sophia', 'Mason', 'Jane', 'Bob', 'Alice', 'Mike', 'Samantha', 'David', 'Emily', 'Daniel', 'Olivia', 'Sophia', 'William']
    middle_names = ['Elizabeth', 'Michael', 'Grace', 'David', 'Rose', '', '', '']
    last_names = ['Doe','Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Smith', 'Johnson', 'Brown', 'Lee', 'Davis', 'Wilson', 'Taylor', 'Anderson', 'Thomas']
    data = []
    for i in range(n):
        middle = random.choice(middle_names)
        if middle =='':
            name = random.choice(first_names) + " " + random.choice(last_names)
        else:
            name = random.choice(first_names) + " " + middle+" " + random.choice(last_names)
            
        roll_number = random.randint(100, 250)
        dob = datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(2000, 2022)), '%j %Y')
        dob_str = dob.strftime('%m-%d-%Y')
        year_of_admission = random.randint(2020, 2030)
        alumni = random.randint(0, 1)
        data.append([name, str(roll_number), dob_str, str(year_of_admission), '0'])
    return data

n = 400
data = generate_random_data(n)
filename = "student_datatest.csv"
with open(filename, mode='w') as file:
    for row in data:
        file.write(','.join(row) + '\n')