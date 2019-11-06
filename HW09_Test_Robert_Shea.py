'''Author: Robert Shea
Code Purpose: The purpose of this code is to test different conditions from the HW09_Robert_Shea.py file'''
import unittest
from HW09_Robert_Shea import Repository, Student, Instructor

class TestModuleGeneratorFile(unittest.TestCase):
    def test_read_students_file(self):
        '''Tests for the read_students_file function'''
        Stevens = Repository('Stevens')
        self.assertEqual(Stevens.read_students_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_students_file, 'nonexistentfile.txt') #Testing a nonexistent file

    def test_read_instructors_file(self):
        '''Tests for the read_instructors_file function'''
        Stevens = Repository('Stevens')
        self.assertEqual(Stevens.read_instructors_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_instructors_file, 'nonexistentfile.txt') #Testing a nonexistent file
        

    def test_read_grades_file(self):
        '''Tests for the read_grades_file function'''
        Stevens = Repository('Stevens')
        self.assertEqual(Stevens.read_grades_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_grades_file, 'nonexistentfile.txt') #Testing a nonexistent file

    def test_pt_dict_students(self): #This test gives this error "IndentationError: unindent does not match any outer indentation level" and I am not sure how to solve it
        '''This tests that the pretty table values are correctly outputted for each student'''
        Stevens = Repository('Stevens')
        Stevens.read_students_file('students.txt',fields=3, sep='\t', header=False)
        Stevens.read_instructors_file('instructors.txt',fields=3, sep='\t', header=False)
        Stevens.read_grades_file('grades.txt',fields=4, sep='\t', header=False)
        Stevens.pt_dict_students()
        self.assertEqual(Stevens.pt_dict_stud['10103'], ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']])

    def test_pt_dict_instructors(self):
        '''This tests that the pretty table values are correctly outputted for each instrutor and their corresponding classes and number of students in that class'''
        Stevens = Repository('Stevens')
        Stevens.read_students_file('students.txt',fields=3, sep='\t', header=False)
        Stevens.read_instructors_file('instructors.txt',fields=3, sep='\t', header=False)
        Stevens.read_grades_file('grades.txt',fields=4, sep='\t', header=False)
        Stevens.pt_dict_instructors()
        self.assertEqual(Stevens.pt_dict_inst['98765'], (['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4], ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3]))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    
