from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # allow requests from frontend

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',
    'database': 'me_api'
}

def get_db():
    return mysql.connector.connect(**db_config)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/profile', methods=['GET'])
def get_profile():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM profile LIMIT 1")
    profile = cursor.fetchone()
    cursor.close()
    db.close()
    return jsonify(profile)

@app.route('/skills', methods=['GET'])
def get_skills():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM skills")
    skills = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(skills)

@app.route('/projects', methods=['GET'])
def get_projects():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT projects.*, skills.name as skill 
        FROM projects 
        LEFT JOIN skills ON projects.skill_id = skills.id
    """)
    projects = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(projects)

@app.route('/projects/skill/<skillname>', methods=['GET'])
def get_projects_by_skill(skillname):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT projects.*, skills.name as skill
        FROM projects
        LEFT JOIN skills ON projects.skill_id = skills.id
        WHERE skills.name = %s
    """, (skillname,))
    projects = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(projects)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # Basic search: look for query in project/title/description
    cursor.execute("""
        SELECT projects.*, skills.name as skill
        FROM projects
        LEFT JOIN skills ON projects.skill_id = skills.id
        WHERE projects.title LIKE %s OR projects.description LIKE %s
    """, (f"%{query}%", f"%{query}%"))
    projects = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(projects)

# Add update/create routes if needed for update/insert operations

if __name__ == '__main__':
    app.run(debug=True)
