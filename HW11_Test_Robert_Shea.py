'''Author: Robert Shea
Code Purpose: The purpose of this code is to test different conditions from the HW10_Robert_Shea.py file'''
import unittest
import os
from HW11_Robert_Shea import Repository, Student, Instructor

class TestModuleGeneratorFile(unittest.TestCase):

    def test_read_students_file(self):
        '''Tests for the read_students_file function'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        self.assertEqual(Stevens.read_students_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_students_file, 'nonexistentfile.txt') #Testing a nonexistent file

    def test_read_instructors_file(self):
        '''Tests for the read_instructors_file function'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        self.assertEqual(Stevens.read_instructors_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_instructors_file, 'nonexistentfile.txt') #Testing a nonexistent file
        

    def test_read_grades_file(self):
        '''Tests for the read_grades_file function'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        self.assertEqual(Stevens.read_grades_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_grades_file, 'nonexistentfile.txt') #Testing a nonexistent file

    def test_read_majors_file(self):
        '''Tests for the read_majors_file function'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        self.assertEqual(Stevens.read_grades_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_grades_file, 'nonexistentfile.txt') #Testing a nonexistent file     

    """def test_ptable_info(self):
        '''Tests that the pretty table information is correct. The first test that I tried is not working properly.'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        students_dict = dict()
        instructors_dict = dict()
        majors_dict = dict()
        for cwid, student in Stevens._students.items():
            students_dict[cwid] = student.pt_test()
        for cwid, instructor in Stevens._instructors.items():
            instructors_dict[cwid] = instructor.pt_test()
        for major, req_and_elect in Stevens._majors.items():
            majors_dict[major] = req_and_elect.pt_row()
        self.assertEqual(students_dict, {'10103': ['10103', 'Jobs, S', 'SFEN', {'SSW 810': 'A-', 'CS 501': 'B'}],
                                        '10115': ['10115', 'Bezos, J', 'SFEN', {'SSW 810': 'A', 'CS 546': 'F'}],
                                        '10183': ['10183', 'Musk, E', 'SFEN', {'SSW 555': 'A', 'SSW 810': 'A'}],
                                        '11714': ['11714', 'Gates, B', 'CS', {'SSW 810': 'B-', 'CS 546': 'A', 'CS 570': 'A-'}]})"""

    def test_instructor_db(self):
        '''Tests that the data from retrieved from the database matches the expected rows'''
        directory = os.getcwd()
        Stevens = Repository(directory)
        self.assertEqual(Stevens._instructor_database_query, [('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                                                                ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                                                                ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                                                                ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                                                                ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                                                                ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1)])


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    
