import os  # Importing the OS module for operating system dependent functionality
from dotenv import load_dotenv  # Importing dotenv to load environment variables from a .env file
import mysql.connector  # Importing mysql.connector to connect to a MySQL database
from flask import Flask, render_template, request, redirect, url_for  # Importing Flask and necessary functions for web development

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
DB_HOST = os.getenv('DB_HOST')  # Database host
DB_USER = os.getenv('DB_USER')  # Database user
DB_PASSWORD = os.getenv('DB_PASSWORD')  # Database password
DB_NAME = os.getenv('DB_NAME')  # Database name

app = Flask(__name__)  # Creating a Flask application instance

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb  # Return the database connection object
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Print the error if connection fails
        return None  # Return None if the connection fails

# Home Page Route
@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

# Personal Information Page Route
@app.route('/personal-info')
def personal_info():
    """Render the personal information page with data from the database."""
    mydb = get_db_connection()  # Get database connection
    if mydb:
        try:
            cursor = mydb.cursor()  # Create a cursor object to interact with the database
            cursor.execute("SELECT name, email, phone, bio, id FROM personal_info")
            personal_info_data = cursor.fetchall()  # Fetch all rows from the query
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('personal_info.html', personal_info=personal_info_data)  # Render template with data
        except mysql.connector.Error as err:
            print(f"Error fetching personal info: {err}")  # Print error if query fails
            return render_template('error.html', error_message="Unable to load personal information.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Add New Personal Information
@app.route('/add-personal-info', methods=['GET', 'POST'])
def add_personal_info():
    """Handle adding new personal information."""
    if request.method == 'POST':  # Check if the request method is POST
        name = request.form['name']  # Get name from form data
        email = request.form['email']  # Get email from form data
        phone = request.form['phone']  # Get phone from form data
        bio = request.form['bio']  # Get bio from form data

        mydb = get_db_connection()  # Get database connection
        if mydb:
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO personal_info (name, email, phone, bio) VALUES (%s, %s, %s, %s)"  # SQL query to insert data
                values = (name, email, phone, bio)  # Values to insert
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                return redirect(url_for('personal_info'))  # Redirect to the personal info page
            except mysql.connector.Error as err:
                print(f"Error inserting personal information: {err}")  # Print error if insertion fails
                return render_template('error.html', error_message="Unable to add personal information.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails
    
    return render_template('add_personal_info.html')  # Render the form for adding personal info

# Route to Edit Personal Information
@app.route('/edit-personal-info/<int:id>', methods=['GET', 'POST'])
def edit_personal_info(id):
    """Handle editing existing personal information."""
    mydb = get_db_connection()  # Get database connection

    if request.method == 'POST':  # Check if the request method is POST
        name = request.form['name']  # Get name from form data
        email = request.form['email']  # Get email from form data
        phone = request.form['phone']  # Get phone from form data
        bio = request.form['bio']  # Get bio from form data

        if mydb:
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = """
                    UPDATE personal_info
                    SET name=%s, email=%s, phone=%s, bio=%s
                    WHERE id=%s
                """  # SQL query to update data
                values = (name, email, phone, bio, id)  # Values to update
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database

                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection

                return redirect(url_for('personal_info'))  # Redirect to the personal info page
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update personal information.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template
    else:
        if mydb:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "SELECT name, email, phone, bio FROM personal_info WHERE id=%s"  # SQL query to fetch specific personal info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            personal_info_data = cursor.fetchone()  # Fetch the single record

            cursor.close()  # Close the cursor
            mydb.close()  # Close the connection

            return render_template('edit_personal_info.html', personal_info=personal_info_data)  # Render edit form with data
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template

# Route to Delete Personal Information
@app.route('/delete-personal-info/<int:id>', methods=['GET'])
def delete_personal_info(id):
    """Handle deleting personal information."""
    mydb = get_db_connection()  # Get database connection

    if mydb:
        try:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "DELETE FROM personal_info WHERE id = %s"  # SQL query to delete personal info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            mydb.commit()  # Commit the changes to the database
            cursor.close()  # Close the cursor
            mydb.close()  # Close the connection
            return redirect(url_for('personal_info'))  # Redirect to the personal info page
        except mysql.connector.Error as err:
            print(f"Error deleting personal info: {err}")  # Print error if deletion fails
            return render_template('error.html', error_message="Unable to delete the personal info.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template

# Education Page Route
@app.route('/education')
def education():
    """Render the education page with data from the database."""
    mydb = get_db_connection()  # Get database connection
    if mydb:
        try:
            cursor = mydb.cursor()  # Create a cursor object
            cursor.execute("SELECT school, achievement, start_year, end_year, id FROM education")  # SQL query to fetch education data
            education_data = cursor.fetchall()  # Fetch all the records
            cursor.close()  # Close the cursor
            mydb.close()  # Close the connection
            return render_template('education.html', education=education_data)  # Render template with education data
        except mysql.connector.Error as err:
            print(f"Error fetching education data: {err}")  # Print error if query fails
            return render_template('error.html', error_message="Unable to load education data.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template

# Route to Add New Education
@app.route('/add-education', methods=['GET', 'POST'])
def add_education():
    """Handle adding new education information."""
    if request.method == 'POST':  # Check if the request method is POST
        school = request.form['school']  # Get school name from form data
        achievement = request.form['achievement']  # Get achievement from form data
        start_year = request.form['start_year']  # Get start year from form data
        end_year = request.form['end_year']  # Get end year from form data

        mydb = get_db_connection()  # Get database connection
        if mydb:
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO education (school, achievement, start_year, end_year) VALUES (%s, %s, %s, %s)"  # SQL query to insert data
                values = (school, achievement, start_year, end_year)  # Values to insert
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                return redirect(url_for('education'))  # Redirect to the education page
            except mysql.connector.Error as err:
                print(f"Error inserting education information: {err}")  # Print error if insertion fails
                return render_template('error.html', error_message="Unable to add education information.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template
    
    return render_template('add_education.html')  # Render the form for adding education info

# Route to Edit Education Information
@app.route('/edit-education/<int:id>', methods=['GET', 'POST'])
def edit_education(id):
    """Handle editing existing education information."""
    mydb = get_db_connection()  # Get database connection

    if request.method == 'POST':  # Check if the request method is POST
        school = request.form['school']  # Get school name from form data
        achievement = request.form['achievement']  # Get achievement from form data
        start_year = request.form['start_year']  # Get start year from form data
        end_year = request.form['end_year']  # Get end year from form data

        if mydb:
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = """
                    UPDATE education
                    SET school=%s, achievement=%s, start_year=%s, end_year=%s
                    WHERE id=%s
                """  # SQL query to update data
                values = (school, achievement, start_year, end_year, id)  # Values to update
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database

                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection

                return redirect(url_for('education'))  # Redirect to the education page
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update education information.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template
    else:
        if mydb:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "SELECT school, achievement, start_year, end_year FROM education WHERE id=%s"  # SQL query to fetch specific education info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            education_data = cursor.fetchone()  # Fetch the single record

            cursor.close()  # Close the cursor
            mydb.close()  # Close the connection

            return render_template('edit_education.html', education=education_data)  # Render edit form with data
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template

# Route to Delete Education Information
@app.route('/delete-education/<int:id>', methods=['GET'])
def delete_education(id):
    """Handle deleting education information."""
    mydb = get_db_connection()  # Get database connection

    if mydb:
        try:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "DELETE FROM education WHERE id = %s"  # SQL query to delete education info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            mydb.commit()  # Commit the changes to the database
            cursor.close()  # Close the cursor
            mydb.close()  # Close the connection
            return redirect(url_for('education'))  # Redirect to the education page
        except mysql.connector.Error as err:
            print(f"Error deleting education info: {err}")  # Print error if deletion fails
            return render_template('error.html', error_message="Unable to delete the education info.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Work Experience Page Route
@app.route('/work-experience')
def work_experience():
    """Fetch and display all work experience records from the database."""
    mydb = get_db_connection()  # Establish database connection
    if mydb:
        try:
            cursor = mydb.cursor()  # Create a cursor object for executing queries
            cursor.execute("SELECT company, position, start_year, end_year, description, id FROM work_experience")
            work_experience_data = cursor.fetchall()  # Fetch all records from the work_experience table
            cursor.close()  # Close the cursor
            mydb.close()    # Close the database connection
            return render_template('work_experience.html', work_experience=work_experience_data)  # Render the work experience page with fetched data
        except mysql.connector.Error as err:
            print(f"Error fetching work experience data: {err}")  # Log any database errors
            return render_template('error.html', error_message="Unable to load work experience data.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Add New Work Experience
@app.route('/add-work-experience', methods=['GET', 'POST'])
def add_work_experience():
    """Handle adding new work experience records."""
    if request.method == 'POST':  # Check if the form has been submitted
        company = request.form['company']  # Get company name from form data
        position = request.form['position']  # Get position from form data
        start_year = request.form['start_year']  # Get start year from form data
        end_year = request.form['end_year']  # Get end year from form data
        description = request.form['description']  # Get description from form data

        # Connect to the database and insert new work experience entry
        mydb = get_db_connection()  # Establish database connection
        if mydb:
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO work_experience (company, position, start_year, end_year, description) VALUES (%s, %s, %s, %s, %s)"
                values = (company, position, start_year, end_year, description)  # Define values to be inserted
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection

                # Redirect back to the Work Experience page after adding the entry
                return redirect(url_for('work_experience'))  # Redirect to work experience page
            except mysql.connector.Error as err:
                print(f"Error inserting work experience: {err}")  # Log any database errors
                return render_template('error.html', error_message="Unable to add work experience.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails
    
    # Render the form to add a new work experience if the request method is GET
    return render_template('add_work_experience.html')  # Show form for adding work experience

# Route to Edit Work Experience    
@app.route('/edit-work-experience/<int:id>', methods=['GET', 'POST'])
def edit_work_experience(id):
    """Handle editing existing work experience records."""
    mydb = get_db_connection()  # Establish database connection

    if request.method == 'POST':  # Check if the form has been submitted
        company = request.form['company']  # Get updated company name from form data
        position = request.form['position']  # Get updated position from form data
        start_year = request.form['start_year']  # Get updated start year from form data
        end_year = request.form['end_year']  # Get updated end year from form data
        description = request.form['description']  # Get updated description from form data

        if mydb:  # Check if database connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = """
                    UPDATE work_experience
                    SET company=%s, position=%s, start_year=%s, end_year=%s, description=%s
                    WHERE id=%s
                """  # SQL query to update work experience data
                values = (company, position, start_year, end_year, description, id)  # Define updated values
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database

                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection

                # Redirect to work experience page after successful update
                return redirect(url_for('work_experience'))  # Redirect to work experience page
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update work experience.")  # Render error template if update fails
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

    else:
        if mydb:  # Check if database connection was successful
            cursor = mydb.cursor()  # Create a cursor object
            sql = "SELECT company, position, start_year, end_year, description FROM work_experience WHERE id=%s"  # SQL query to fetch specific work experience info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            work_experience_data = cursor.fetchone()  # Fetch the single record

            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection

            return render_template('edit_work_experience.html', work_experience=work_experience_data)  # Render edit form with fetched data
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Delete Work Experience 
@app.route('/delete-work-experience/<int:id>', methods=['GET'])
def delete_work_experience(id):
    """Handle deleting work experience records."""
    mydb = get_db_connection()  # Establish database connection

    if mydb:  # Check if database connection was successful
        try:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "DELETE FROM work_experience WHERE id = %s"  # SQL query to delete work experience entry
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            mydb.commit()  # Commit the changes to the database
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            return redirect(url_for('work_experience'))  # Redirect to work experience page
        except mysql.connector.Error as err:
            print(f"Error deleting work experience: {err}")  # Log any database errors
            return render_template('error.html', error_message="Unable to delete the work experience.")  # Render error template if deletion fails
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Skills Page Route
@app.route('/skills')
def skills():
    """Fetch and display all skills records from the database."""
    mydb = get_db_connection()  # Establish database connection
    if mydb:  # Check if database connection was successful
        try:
            cursor = mydb.cursor()  # Create a cursor object
            cursor.execute("SELECT skill_name, category, proficiency_level, id FROM skills")  # SQL query to fetch skills data
            skills_data = cursor.fetchall()  # Fetch all records from the skills table
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            return render_template('skills.html', skills=skills_data)  # Render the skills page with fetched data
        except mysql.connector.Error as err:
            return render_template('error.html', error_message="Unable to load skills data.")  # Render error template if fetching fails
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Add New Skill
@app.route('/add-skill', methods=['GET', 'POST'])
def add_skill():
    """Handle adding new skill records."""
    if request.method == 'POST':  # Check if the form has been submitted
        skill_name = request.form['skill_name']  # Get skill name from form data
        category = request.form['category']  # Get category from form data
        proficiency_level = request.form['proficiency_level']  # Get proficiency level from form data

        mydb = get_db_connection()  # Establish database connection
        if mydb:  # Check if database connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO skills (skill_name, category, proficiency_level) VALUES (%s, %s, %s)"  # SQL query to insert new skill
                values = (skill_name, category, proficiency_level)  # Define values to be inserted
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection

                return redirect(url_for('skills'))  # Redirect to skills page
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to add skill.")  # Render error template if insertion fails
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

    return render_template('add_skill.html')  # Show form for adding skill if the request method is GET

# Route to Edit Skill
@app.route('/edit-skill/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    """Handle editing existing skill records."""
    mydb = get_db_connection()  # Establish database connection

    if request.method == 'POST':  # Check if the form has been submitted
        skill_name = request.form['skill_name']  # Get updated skill name from form data
        category = request.form['category']  # Get updated category from form data
        proficiency_level = request.form['proficiency_level']  # Get updated proficiency level from form data

        if mydb:  # Check if database connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = """
                    UPDATE skills
                    SET skill_name=%s, category=%s, proficiency_level=%s
                    WHERE id=%s
                """  # SQL query to update skill data
                values = (skill_name, category, proficiency_level, id)  # Define updated values
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database

                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection

                return redirect(url_for('skills'))  # Redirect to skills page
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update skill.")  # Render error template if update fails
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails
    else:
        if mydb:  # Check if database connection was successful
            cursor = mydb.cursor()  # Create a cursor object
            sql = "SELECT skill_name, category, proficiency_level FROM skills WHERE id=%s"  # SQL query to fetch specific skill info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            skill_data = cursor.fetchone()  # Fetch the single record

            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection

            return render_template('edit_skill.html', skill=skill_data)  # Render edit form with fetched data
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Delete Skill
@app.route('/delete-skill/<int:id>', methods=['GET'])
def delete_skill(id):
    """Handle deleting skill records."""
    mydb = get_db_connection()  # Establish database connection

    if mydb:  # Check if database connection was successful
        try:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "DELETE FROM skills WHERE id = %s"  # SQL query to delete skill entry
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            mydb.commit()  # Commit the changes to the database
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection

            return redirect(url_for('skills'))  # Redirect to skills page
        except mysql.connector.Error as err:
            return render_template('error.html', error_message="Unable to delete the skill.")  # Render error template if deletion fails
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Projects Page Route
@app.route('/projects')
def projects():
    """Fetch and display all project records from the database."""
    mydb = get_db_connection()  # Establish database connection
    if mydb:  # Check if connection was successful
        try:
            cursor = mydb.cursor()  # Create a cursor object for executing queries
            cursor.execute("SELECT project_name, description, start_date, end_date, id FROM projects")
            projects_data = cursor.fetchall()  # Fetch all records from the projects table
            cursor.close()  # Close the cursor
            mydb.close()    # Close the database connection
            return render_template('projects.html', projects=projects_data)  # Render the projects page with fetched data
        except mysql.connector.Error as err:
            print(f"Error fetching projects data: {err}")  # Log any database errors
            return render_template('error.html', error_message="Unable to load projects data.")  # Render error template
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Add New Project
@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    """Handle adding new project records."""
    if request.method == 'POST':  # Check if the form has been submitted
        project_name = request.form['project_name']  # Get project name from form data
        description = request.form['description']  # Get description from form data
        start_date = request.form['start_date']  # Get start date from form data
        end_date = request.form['end_date']  # Get end date from form data

        mydb = get_db_connection()  # Establish database connection
        if mydb:  # Check if connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO projects (project_name, description, start_date, end_date) VALUES (%s, %s, %s, %s)"  # SQL query to insert new project
                values = (project_name, description, start_date, end_date)  # Define values to be inserted
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection
                return redirect(url_for('projects'))  # Redirect to projects page after adding the project
            except mysql.connector.Error as err:
                print(f"Error inserting project: {err}")  # Log any database errors
                return render_template('error.html', error_message="Unable to add project.")  # Render error template
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails
    
    return render_template('add_project.html')  # Render form to add new project if the request method is GET

# Route to Edit Project
@app.route('/edit-project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Handle editing existing project records."""
    mydb = get_db_connection()  # Establish database connection

    if request.method == 'POST':  # Check if the form has been submitted
        project_name = request.form['project_name']  # Get updated project name from form data
        description = request.form['description']  # Get updated description from form data
        start_date = request.form['start_date']  # Get updated start date from form data
        end_date = request.form['end_date']  # Get updated end date from form data

        if mydb:  # Check if connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = """
                    UPDATE projects
                    SET project_name=%s, description=%s, start_date=%s, end_date=%s
                    WHERE id=%s
                """  # SQL query to update project data
                values = (project_name, description, start_date, end_date, id)  # Define updated values
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database

                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection

                return redirect(url_for('projects'))  # Redirect to projects page after successful update
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update project.")  # Render error template if update fails
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails
    else:
        if mydb:  # Check if connection was successful
            cursor = mydb.cursor()  # Create a cursor object
            sql = "SELECT project_name, description, start_date, end_date FROM projects WHERE id=%s"  # SQL query to fetch specific project info
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            project_data = cursor.fetchone()  # Fetch the single record

            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection

            return render_template('edit_project.html', project=project_data)  # Render edit form with fetched data
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Route to Delete Project
@app.route('/delete-project/<int:id>', methods=['GET'])
def delete_project(id):
    """Handle deleting project records."""
    mydb = get_db_connection()  # Establish database connection

    if mydb:  # Check if connection was successful
        try:
            cursor = mydb.cursor()  # Create a cursor object
            sql = "DELETE FROM projects WHERE id = %s"  # SQL query to delete project entry
            cursor.execute(sql, (id,))  # Execute the SQL query with ID as parameter
            mydb.commit()  # Commit the changes to the database
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            return redirect(url_for('projects'))  # Redirect to projects page after deletion
        except mysql.connector.Error as err:
            print(f"Error deleting project: {err}")  # Log any database errors
            return render_template('error.html', error_message="Unable to delete the project.")  # Render error template if deletion fails
    else:
        return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

# Contact Form Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle the contact form submission."""
    if request.method == 'POST':  # Check if the form has been submitted
        name = request.form['name']  # Get name from form data
        email = request.form['email']  # Get email from form data
        message = request.form['message']  # Get message from form data

        mydb = get_db_connection()  # Establish database connection
        if mydb:  # Check if connection was successful
            try:
                cursor = mydb.cursor()  # Create a cursor object
                sql = "INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)"  # SQL query to insert new contact message
                values = (name, email, message)  # Define values to be inserted
                cursor.execute(sql, values)  # Execute the SQL query
                mydb.commit()  # Commit the changes to the database
                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection
                return redirect(url_for('home'))  # Redirect to home page after successful submission
            except mysql.connector.Error as err:
                print(f"Error submitting contact form: {err}")  # Log any database errors
                return render_template('error.html', error_message="Unable to submit your message. Please try again.")  # Render error template if submission fails
        else:
            return render_template('error.html', error_message="Database connection failed.")  # Render error template if connection fails

    return render_template('contact.html')  # Render the contact form if the request method is GET

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask application in debug mode
