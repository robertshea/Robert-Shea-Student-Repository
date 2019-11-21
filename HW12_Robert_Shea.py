'''Author: Robert Shea
Code Purpose: The purpose of this code is to build a web page to display a summary of each Instructor with his/her CWID, Name, Department, Course, and the number of students in the course.
This will be done with Flask and acquiring data dynamically from a database.'''

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/instructor_summary')

def instructor_summary():
    '''This function will query the database for specific data and return the result of the query to Flask for web presentation'''
    sqlite_db_file = 'HW11_DB_Robert_Shea.db'

    query = 'select i.CWID, i.Name, i.Dept, g.Course, count(*) as Students from Instructors i join Grades g on i.CWID = g.InstructorCWID group by i.CWID, i.Name, i.Dept, g.Course'
    try: #Checks if the database file can be opened to extract information and raises an error if it can not
        database = sqlite3.connect(sqlite_db_file)
    except sqlite3.OperationalError:
        print(f'There was an error in opening the database at {sqlite_db_file}!')
    

    '''The query results are converted into a list of dictionaries to pass to the template'''
    data = [{'CWID': cwid, 'Name': name, 'Dept': dept, 'Course': course, 'Students': count} for cwid, name, dept, course, count in database.execute(query)]

    database.close() #closes the connection to the database
    
    '''This combines the templates and the parameter values to create an HTML document'''
    return render_template('instructor_summary.html', 
                            title='Stevens Repository', 
                            table_title='Courses and Student Counts for each Instructor', 
                            instructors=data)

app.run(debug=True)