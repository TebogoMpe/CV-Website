import os
from dotenv import load_dotenv
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Home Page Route
@app.route('/')
def home():
    return render_template('index.html')

# Personal Information Page Route
@app.route('/personal-info')
def personal_info():
    mydb = get_db_connection()
    if mydb:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT name, email, phone, bio, id FROM Personal_Info")
            personal_info_data = cursor.fetchall()  # Fetch all rows
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('personal_info.html', personal_info=personal_info_data)
        except mysql.connector.Error as err:
            print(f"Error fetching personal info: {err}")
            return render_template('error.html', error_message="Unable to load personal information.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Route to Add New Personal Information
@app.route('/add-personal-info', methods=['GET', 'POST'])
def add_personal_info():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        bio = request.form['bio']

        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Personal_Info (name, email, phone, bio) VALUES (%s, %s, %s, %s)"
                values = (name, email, phone, bio)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                mydb.close()
                return redirect(url_for('personal_info'))
            except mysql.connector.Error as err:
                print(f"Error inserting personal information: {err}")
                return render_template('error.html', error_message="Unable to add personal information.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    
    return render_template('add_personal_info.html')

# Route to Edit Personal Information
@app.route('/edit-personal-info/<int:id>', methods=['GET', 'POST'])
def edit_personal_info(id):
    mydb = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        bio = request.form['bio']

        if mydb:
            try:
                cursor = mydb.cursor()
                sql = """
                    UPDATE Personal_Info
                    SET name=%s, email=%s, phone=%s, bio=%s
                    WHERE id=%s
                """
                values = (name, email, phone, bio, id)
                cursor.execute(sql, values)
                mydb.commit()

                cursor.close()
                mydb.close()

                return redirect(url_for('personal_info'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update personal information.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    else:
        if mydb:
            cursor = mydb.cursor()
            sql = "SELECT name, email, phone, bio FROM Personal_Info WHERE id=%s"
            cursor.execute(sql, (id,))
            personal_info_data = cursor.fetchone()

            cursor.close()
            mydb.close()

            return render_template('edit_personal_info.html', personal_info=personal_info_data)
        else:
            return render_template('error.html', error_message="Database connection failed.")

# Route to Delete Personal Information
@app.route('/delete-personal-info/<int:id>', methods=['GET'])
def delete_personal_info(id):
    mydb = get_db_connection()

    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM Personal_Info WHERE id = %s"
            cursor.execute(sql, (id,))
            mydb.commit()
            cursor.close()
            mydb.close()
            return redirect(url_for('personal_info'))
        except mysql.connector.Error as err:
            print(f"Error deleting personal info: {err}")
            return render_template('error.html', error_message="Unable to delete the personal info.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Education Page Route
@app.route('/education')
def education():
    mydb = get_db_connection()
    if mydb:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT school, achievement, start_year, end_year, description, id FROM Education")
            education_data = cursor.fetchall()  # Fetch all the records
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('education.html', education=education_data)
        except mysql.connector.Error as err:
            print(f"Error fetching education data: {err}")
            return render_template('error.html', error_message="Unable to load education data.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Route to Add New Education
@app.route('/add-education', methods=['GET', 'POST'])
def add_education():
    if request.method == 'POST':
        school = request.form['school']
        achievement = request.form['achievement']
        start_year = request.form['start_year']
        end_year = request.form['end_year']
        description = request.form['description']

        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Education (school, achievement, start_year, end_year, description) VALUES (%s, %s, %s, %s, %s)"
                values = (school, achievement, start_year, end_year, description)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                mydb.close()
                return redirect(url_for('education'))
            except mysql.connector.Error as err:
                print(f"Error inserting education data: {err}")
                return render_template('error.html', error_message="Unable to add education.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    
    return render_template('add_education.html')

# Route to Edit Education
@app.route('/edit-education/<int:id>', methods=['GET', 'POST'])
def edit_education(id):
    mydb = get_db_connection()

    if request.method == 'POST':
        school = request.form['school']
        achievement = request.form['achievement']
        start_year = request.form['start_year']
        end_year = request.form['end_year']
        description = request.form['description']

        if mydb:
            try:
                cursor = mydb.cursor()
                sql = """
                    UPDATE Education
                    SET school=%s, achievement=%s, start_year=%s, end_year=%s, description=%s
                    WHERE id=%s
                """
                values = (school, achievement, start_year, end_year, description, id)
                cursor.execute(sql, values)
                mydb.commit()

                cursor.close()
                mydb.close()

                return redirect(url_for('education'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update education.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    else:
        if mydb:
            cursor = mydb.cursor()
            sql = "SELECT school, achievement, start_year, end_year, description FROM Education WHERE id=%s"
            cursor.execute(sql, (id,))
            education_data = cursor.fetchone()

            cursor.close()
            mydb.close()

            return render_template('edit_education.html', education=education_data)
        else:
            return render_template('error.html', error_message="Database connection failed.")

# Route to Delete Education
@app.route('/delete-education/<int:id>', methods=['GET'])
def delete_education(id):
    mydb = get_db_connection()

    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM Education WHERE id = %s"
            cursor.execute(sql, (id,))
            mydb.commit()
            cursor.close()
            mydb.close()
            return redirect(url_for('education'))
        except mysql.connector.Error as err:
            print(f"Error deleting education: {err}")
            return render_template('error.html', error_message="Unable to delete the education.")
    else:
        return render_template('error.html', error_message="Database connection failed.")


# Work Experience Page Route
@app.route('/work-experience')
def work_experience():
    mydb = get_db_connection()
    if mydb:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT company, position, start_year, end_year, description, id FROM Work_Experience")
            work_experience_data = cursor.fetchall()  # Fetch all the records
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('work_experience.html', work_experience=work_experience_data)
        except mysql.connector.Error as err:
            print(f"Error fetching work experience data: {err}")
            return render_template('error.html', error_message="Unable to load work experience data.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Route to Add New Work Experience
@app.route('/add-work-experience', methods=['GET', 'POST'])
def add_work_experience():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        start_year = request.form['start_year']
        end_year = request.form['end_year']
        description = request.form['description']

        # Connect to the database and insert new entry
        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Work_Experience (company, position, start_year, end_year, description) VALUES (%s, %s, %s, %s, %s)"
                values = (company, position, start_year, end_year, description)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                mydb.close()

                # Redirect back to the Work Experience page after adding the entry
                return redirect(url_for('work_experience'))
            except mysql.connector.Error as err:
                print(f"Error inserting work experience: {err}")
                return render_template('error.html', error_message="Unable to add work experience.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    
    # Render the form to add a new work experience if the request is GET
    return render_template('add_work_experience.html')
    
# Route to Edit Work Experience    
@app.route('/edit-work-experience/<int:id>', methods=['GET', 'POST'])
def edit_work_experience(id):
    mydb = get_db_connection()

    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        start_year = request.form['start_year']
        end_year = request.form['end_year']
        description = request.form['description']

        if mydb:
            try:
                cursor = mydb.cursor()
                sql = """
                    UPDATE Work_Experience
                    SET company=%s, position=%s, start_year=%s, end_year=%s, description=%s
                    WHERE id=%s
                """
                values = (company, position, start_year, end_year, description, id)
                cursor.execute(sql, values)
                mydb.commit()

                cursor.close()
                mydb.close()

                # Redirect to work experience page after successful update
                return redirect(url_for('work_experience'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update work experience.")
        else:
            return render_template('error.html', error_message="Database connection failed.")

    else:
        if mydb:
            cursor = mydb.cursor()
            sql = "SELECT company, position, start_year, end_year, description FROM Work_Experience WHERE id=%s"
            cursor.execute(sql, (id,))
            work_experience_data = cursor.fetchone()

            cursor.close()
            mydb.close()

            return render_template('edit_work_experience.html', work_experience=work_experience_data)
        else:
            return render_template('error.html', error_message="Database connection failed.")

# Route to Delete New Work Experience 
@app.route('/delete-work-experience/<int:id>', methods=['GET'])
def delete_work_experience(id):
    mydb = get_db_connection()

    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM Work_Experience WHERE id = %s"
            cursor.execute(sql, (id,))
            mydb.commit()
            cursor.close()
            mydb.close()
            return redirect(url_for('work_experience'))
        except mysql.connector.Error as err:
            print(f"Error deleting work experience: {err}")
            return render_template('error.html', error_message="Unable to delete the work experience.")
    else:
        return render_template('error.html', error_message="Database connection failed.")



# Skills Page Route
@app.route('/skills')
def skills():
    mydb = get_db_connection()
    if mydb:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT skill_name, category, proficiency_level, id FROM Skills")
            skills_data = cursor.fetchall()  # Fetch all records
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('skills.html', skills=skills_data)
        except mysql.connector.Error as err:
            return render_template('error.html', error_message="Unable to load skills data.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Route to Add New Skill
@app.route('/add-skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        skill_name = request.form['skill_name']
        proficiency_level = request.form['proficiency_level']

        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Skills (skill_name, category, proficiency_level) VALUES (%s,%s, %s)"
                values = (skill_name, category, proficiency_level)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                mydb.close()

                return redirect(url_for('skills'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to add skill.")
        else:
            return render_template('error.html', error_message="Database connection failed.")

    return render_template('add_skill.html')

# Route to Edit Skill
@app.route('/edit-skill/<int:id>', methods=['GET', 'POST'])
def edit_skill(id):
    mydb = get_db_connection()

    if request.method == 'POST':
        skill_name = request.form['skill_name']
        category = request.form['category']
        proficiency_level = request.form['proficiency_level']

        if mydb:
            try:
                cursor = mydb.cursor()
                sql = """
                    UPDATE Skills
                    SET skill_name=%s, category=%s, proficiency_level=%s
                    WHERE id=%s
                """
                values = (skill_name, category, proficiency_level, id)
                cursor.execute(sql, values)
                mydb.commit()

                cursor.close()
                mydb.close()

                return redirect(url_for('skills'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update skill.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    else:
        if mydb:
            cursor = mydb.cursor()
            sql = "SELECT skill_name, category, proficiency_level FROM Skills WHERE id=%s"
            cursor.execute(sql, (id,))
            skill_data = cursor.fetchone()

            cursor.close()
            mydb.close()

            return render_template('edit_skill.html', skill=skill_data)
        else:
            return render_template('error.html', error_message="Database connection failed.")

# Route to Delete Skill
@app.route('/delete-skill/<int:id>', methods=['GET'])
def delete_skill(id):
    mydb = get_db_connection()

    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM Skills WHERE id = %s"
            cursor.execute(sql, (id,))
            mydb.commit()
            cursor.close()
            mydb.close()

            return redirect(url_for('skills'))
        except mysql.connector.Error as err:
            return render_template('error.html', error_message="Unable to delete the skill.")
    else:
        return render_template('error.html', error_message="Database connection failed.")



# Projects Page Route
@app.route('/projects')
def projects():
    mydb = get_db_connection()
    if mydb:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT project_name, description, start_date, end_date, id FROM Projects")
            projects_data = cursor.fetchall()  # Fetch all records
            cursor.close()  # Close the cursor
            mydb.close()    # Close the connection
            return render_template('projects.html', projects=projects_data)
        except mysql.connector.Error as err:
            print(f"Error fetching projects data: {err}")
            return render_template('error.html', error_message="Unable to load projects data.")
    else:
        return render_template('error.html', error_message="Database connection failed.")

# Route to Add New Project
@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        start_year = request.form['start_date']
        end_year = request.form['end_date']

        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Projects (project_name, description, start_date, end_date) VALUES (%s, %s, %s, %s)"
                values = (project_name, description, start_date, end_date)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()
                mydb.close()
                return redirect(url_for('projects'))
            except mysql.connector.Error as err:
                print(f"Error inserting project: {err}")
                return render_template('error.html', error_message="Unable to add project.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    
    return render_template('add_project.html')

# Route to Edit Project
@app.route('/edit-project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    mydb = get_db_connection()

    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if mydb:
            try:
                cursor = mydb.cursor()
                sql = """
                    UPDATE Projects
                    SET project_name=%s, description=%s, start_date=%s, end_date=%s
                    WHERE id=%s
                """
                values = (project_name, description, start_date, end_date, id)
                cursor.execute(sql, values)
                mydb.commit()

                cursor.close()
                mydb.close()

                return redirect(url_for('projects'))
            except mysql.connector.Error as err:
                return render_template('error.html', error_message="Unable to update project.")
        else:
            return render_template('error.html', error_message="Database connection failed.")
    else:
        if mydb:
            cursor = mydb.cursor()
            sql = "SELECT project_name, description, start_date, end_date FROM Projects WHERE id=%s"
            cursor.execute(sql, (id,))
            project_data = cursor.fetchone()

            cursor.close()
            mydb.close()

            return render_template('edit_project.html', project=project_data)
        else:
            return render_template('error.html', error_message="Database connection failed.")

# Route to Delete Project
@app.route('/delete-project/<int:id>', methods=['GET'])
def delete_project(id):
    mydb = get_db_connection()

    if mydb:
        try:
            cursor = mydb.cursor()
            sql = "DELETE FROM Projects WHERE id = %s"
            cursor.execute(sql, (id,))
            mydb.commit()
            cursor.close()
            mydb.close()
            return redirect(url_for('projects'))
        except mysql.connector.Error as err:
            print(f"Error deleting project: {err}")
            return render_template('error.html', error_message="Unable to delete the project.")
    else:
        return render_template('error.html', error_message="Database connection failed.")


# Contact Form Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        mydb = get_db_connection()
        if mydb:
            try:
                cursor = mydb.cursor()
                sql = "INSERT INTO Contact (name, email, message) VALUES (%s, %s, %s)"
                values = (name, email, message)
                cursor.execute(sql, values)
                mydb.commit()
                cursor.close()  # Close the cursor
                mydb.close()    # Close the connection
                return redirect(url_for('home'))
            except mysql.connector.Error as err:
                print(f"Error submitting contact form: {err}")
                return render_template('error.html', error_message="Unable to submit your message. Please try again.")
        else:
            return render_template('error.html', error_message="Database connection failed.")

    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)

