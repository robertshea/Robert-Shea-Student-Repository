'''Author: Robert Shea
Code Purpose: The purpose of this code is to test different conditions from the HW10_Robert_Shea.py file'''
import unittest
from HW10_Robert_Shea import Repository, Student, Instructor

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

    def test_read_majors_file(self):
        '''Tests for the read_majors_file function'''
        Stevens = Repository('Stevens')
        self.assertEqual(Stevens.read_grades_file('emptyfile.txt'),None) #Testing an empty file
        self.assertRaises(FileNotFoundError, Stevens.read_grades_file, 'nonexistentfile.txt') #Testing a nonexistent file        

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
    
