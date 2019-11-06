'''Author: Robert Shea
Code Purpose: The purpose of this code is to create a data repository of courses, students and instructors. The system will help students track their required courses, the courses they have successfully completed, their grades,  GPA, etc. '''
from collections import defaultdict
from prettytable import PrettyTable

class Repository():
    '''This class will hold all of the information for a specific university. It holds student, major, and professor. For students this includes classes taken and grades achieved.'''

    def __init__(self, university):
        self._university = university
        self._students = dict()
        self._instructors = dict()
    
    def read_students_file(self, path, fields=3, sep='\t', header=False):
        '''Reads the student file to pull out the appropriate information.'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")
        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is '\t'
                        if len(separate_line) != fields: #Checks that the length of the seperated line is the same as the amount of indicated fields and raises an error if not
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                        else:
                            self._students[separate_line[0]] = Student(separate_line[0], separate_line[1], separate_line[2]) #Each new instance of student is appended to the dict

    def read_instructors_file(self, path, fields=3, sep='\t', header=False):
        '''Reads the instructors file to pull out the appropriate information'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")

        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is '\t'
                        if len(separate_line) != fields: #Checks that the length of the seperated line is the same as the amount of indicated fields and raises an error if not
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                        else:
                            self._instructors[separate_line[0]] = Instructor(separate_line[0], separate_line[1], separate_line[2]) #Each new instance of instructor is appended to the dict

    def read_grades_file(self, path, fields=4, sep='\t', header=False):
        '''Reads the grades file to pull out the appropriate information'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")
        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is '\t'
                        if len(separate_line) == fields: 
                            _grades_student = separate_line[0]
                            _course = separate_line[1]
                            _grade = separate_line[2]
                            _grades_instructor = separate_line[3]
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                        else:
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        if _grades_student in self._students:
                            self._students[_grades_student].add_course(_course, _grade)
                        else: 
                            print(f'Found grade for unknown student {_grades_student}')
                        if _grades_instructor in self._instructors:
                            self._instructors[_grades_instructor].num_students(_course)
                        else: 
                            print(f'Found an unknown instructor {_grades_instructor}')


    def students_table(self):
        '''This creates a pretty table that is a Student Summary of each students CWID, Name, and their completed courses'''
        print('Student Summary')
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Major', 'Completed Courses']) #The top field names for the table
        for student in self._students.values(): 
            pt.add_row(student.pt_row())
        print(pt)
    
    def instructors_table(self):
        '''This creates a pretty table that is an Instructor Summary of each instructors CWID, name, the department they are from, the course they teach, and the number of students in that course'''
        print('Instructor Summary')
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']) #The top field names for the table
        for instructor in self._instructors.values(): #This pretty table will create a new row for each professors classes that they teach and the number of students in those classes
            for row in instructor.pt_row():
                pt.add_row(row)
        print(pt)

    def pt_dict_students(self): #This is a dictionary with keys of the student CWID and values that correspond to the pretty table row for that CWID
        self.pt_dict_stud = dict()
        for key, value in self._students.items(): 
            self.pt_dict_stud[key] = value.pt_row()
        return self.pt_dict_stud
    
    def pt_dict_instructors(self): #This is a dictionary with keys of the instructor CWID and values that correspond to the pretty table row for that CWID
        self.pt_dict_inst = dict()
        for key, value in self._instructors.items():
            tup = tuple(value.pt_row())
            self.pt_dict_inst[key] = tup
        return self.pt_dict_inst

        
class Student():
    '''This class stores all the student data'''
    def __init__(self, CWID, name, major):
        self._CWID = CWID
        self._name = name
        self._major = major
        self._courses = dict() #This dictionary will have a key as the course number and a value as the grade

    def add_course(self, course, grade='N/A'):
        self._courses[course] = grade
    
    def pt_row(self):
        return [self._CWID, self._name, self._major, sorted(self._courses.keys())]  #The completed courses in the pretty table are sorted in alphabetical order by course name and numerical order by course number



class Instructor():
    '''This class stores the professor data'''
    def __init__(self, CWID, name, dept):
        '''This creates the instance of the class Instructor that will record the CWID, name, and dept from the instructors file.
        It will also create a dictionary with the amount of students in each of the courses that they teach'''
        self._CWID = CWID
        self._name = name
        self._dept = dept
        self._courses = defaultdict(int) #This dictionary will have a key as the course number and a value as the number of students in the class
    
    def num_students(self,course):
        self._courses[course] += 1 
    
    def pt_row(self):
        for course, students in self._courses.items():
            yield [self._CWID, self._name, self._dept, course, students]

def main():
    Stevens = Repository('Stevens')

    Stevens.read_students_file('students.txt',fields=3, sep='\t', header=False)
    Stevens.read_instructors_file('instructors.txt',fields=3, sep='\t', header=False)
    Stevens.read_grades_file('grades.txt',fields=4, sep='\t', header=False)

    Stevens.students_table()

    Stevens.instructors_table()

    Stevens.pt_dict_students()

    Stevens.pt_dict_instructors()
if __name__ == '__main__':

    main()

