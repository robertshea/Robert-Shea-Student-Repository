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
        self._majors = defaultdict(Major)
    
    def read_students_file(self, path, fields=3, sep=';', header=True):
        '''Reads the student file to pull out the appropriate information.'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")
        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is ';'
                        if len(separate_line) != fields: #Checks that the length of the seperated line is the same as the amount of indicated fields and raises an error if not
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                            continue
                        else:
                            self._students[separate_line[0]] = Student(separate_line[0], separate_line[1], separate_line[2]) #Each new instance of student is appended to the dict

    def read_instructors_file(self, path, fields=3, sep='|', header=True):
        '''Reads the instructors file to pull out the appropriate information'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")

        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is '|'
                        if len(separate_line) != fields: #Checks that the length of the seperated line is the same as the amount of indicated fields and raises an error if not
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                            continue
                        else:
                            self._instructors[separate_line[0]] = Instructor(separate_line[0], separate_line[1], separate_line[2]) #Each new instance of instructor is appended to the dict

    def read_grades_file(self, path, fields=4, sep='|', header=True):
        '''Reads the grades file to pull out the appropriate information'''
        file_name = path
        try:
            fp = open(file_name, 'r')
        
        except FileNotFoundError:
            raise FileNotFoundError(f"Can't open {file_name}!")
        else:
            with fp:
                    for offset, line in enumerate(fp): #Iterates through all the lines in the file and stores an offset value for each line
                        separate_line = line.rstrip('\n').split(sep) #Separates the line based on the indicated separator. In this case it is '|'
                        if len(separate_line) != fields: 
                            raise ValueError(f'{file_name} in line {offset} has {len(separate_line)} but expected {fields}')
                        elif header is True: #Checks that the first line is a header and does not evaluate it if so
                            header = False
                            continue
                        else:
                            _grades_student = separate_line[0]
                            _course = separate_line[1]
                            _grade = separate_line[2]
                            _grades_instructor = separate_line[3]
                        if _grades_student in self._students:
                            self._students[_grades_student].add_course(_course, _grade)
                        else: 
                            print(f'Found grade for unknown student {_grades_student}')
                        if _grades_instructor in self._instructors:
                            self._instructors[_grades_instructor].num_students(_course)
                        else: 
                            print(f'Found an unknown instructor {_grades_instructor}')
    
    def read_majors_file(self, path, fields=3, sep='\t', header=True):
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
                            continue
                        else:
                            dept, req_or_elect, course = separate_line[0], separate_line[1], separate_line[2]
                            self._majors[dept].add_courses(req_or_elect, course) #Adds the department as a key to the _majors dictionary with keys that are the course and whether it is required or an elective
    
    def courses_remaining(self,student):
        '''This is a function to determine the remaining courses that need to be taken'''
        required_class = self._majors[student._major]._required_courses
        elective_class = self._majors[student._major]._elective_courses
        passing_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'] #Values that will be compared to as a passing grade for a course
        courses_passed = set() 
        
        for course,grade in student._courses.items():
            if grade in passing_grades: #If the student grade in the class is in the list of passing grades, then they passed the course and it is added to a set
                courses_passed.add(course)
        if any(elective_class.intersection(courses_passed)) == True: #If the set that includes the courses passed and the list of courses that are electives have any classes in common, then the student has taken the required amount of electives and the electives remaining is none
            electives_remaining = []
        else: 
            electives_remaining = elective_class
            ''' required_class.difference(courses_passed) will give the difference between the list of courses that are required and the list of required courses that the student has passed.
            The difference is the remaining required courses that the student still has to take'''
        return(courses_passed, required_class.difference(courses_passed), electives_remaining)


    def students_table(self):
        '''This creates a pretty table that is a Student Summary of each students CWID, Name, and their completed courses'''
        print('Student Summary')
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']) #The top field names for the table
        for student in self._students.values(): 
            '''I was not sure how else to do this but I have the information for the students courses_passed, required_remaining, and elective_remaining that are from the repository.
            I made a list of the elements that are in student.pt_row(). Then I sorted and appended each element to the list.'''
            courses_passed, required_remaining, electives_remaining = self.courses_remaining(student)
            lst = student.pt_row()
            lst.append(sorted(courses_passed))
            lst.append(sorted(required_remaining))
            lst.append(sorted(electives_remaining))
            pt.add_row(lst)
        print(pt)
    
    def instructors_table(self):
        '''This creates a pretty table that is an Instructor Summary of each instructors CWID, name, the department they are from, the course they teach, and the number of students in that course'''
        print('Instructor Summary')
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Students']) #The top field names for the table
        for instructor in self._instructors.values(): #This pretty table will create a new row for each professors classes that they teach and the number of students in those classes
            for row in instructor.pt_row():
                pt.add_row(row)
        print(pt)
    
    def majors_table(self):
        '''This creates a pretty table that is a Majors Summary of each department, the departments required courses, and the departments required electives'''
        print('Majors Summary')
        pt = PrettyTable(field_names = ['Dept', 'Required', 'Electives'])
        for major in self._majors.keys():
            pt.add_row([major, sorted(self._majors[major]._required_courses), sorted(self._majors[major]._elective_courses)])
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
        return [self._CWID, self._name, self._major]  #The completed courses in the pretty table are sorted in alphabetical order by course name and numerical order by course number



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

class Major():
    '''This class stores the majors data'''
    def __init__(self):
        self._required_courses = set()
        self._elective_courses = set()
    
    def add_courses(self, req_or_elect, course):
        '''If the "flag" starts with an "R" then it is a required course and if it starts with an "E" then it is an elective and will be stored in the dictionary _majors as such.
        If it is neither then perhaps there is an error, typo, or there is another unspecified "flag".'''
        if req_or_elect.upper() == 'R':
            self._required_courses.add(course)
        elif req_or_elect.upper() == 'E':
            self._elective_courses.add(course)
        else:
            raise ValueError(f'Expected "R" or "E" but instead encountered {req_or_elect} in majors.txt')
    
    def pt_row(self):
        return [Major, self._required_courses, self._elective_courses]

def main():
    Stevens = Repository('Stevens')

    Stevens.read_students_file('HW10_students.txt',fields=3, sep=';', header=True)
    Stevens.read_instructors_file('instructors2.txt',fields=3, sep='|', header=True)
    Stevens.read_grades_file('grades2.txt',fields=4, sep='|', header=True)
    Stevens.read_majors_file('majors.txt',fields=3, sep='\t', header=True)

    Stevens.majors_table()

    Stevens.students_table()

    Stevens.instructors_table()

    Stevens.pt_dict_students()

    Stevens.pt_dict_instructors()

if __name__ == '__main__':

    main()

