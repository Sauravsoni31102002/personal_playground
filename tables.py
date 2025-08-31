import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shailesh@123',  
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS me_api;")
cursor.execute("USE me_api;")

# Table creation commands
table_commands = [
    """
    CREATE TABLE IF NOT EXISTS profile (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        email VARCHAR(100),
        education VARCHAR(200)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS skills (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS projects (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(100),
        description TEXT,
        link VARCHAR(200),
        skill_id INT,
        FOREIGN KEY (skill_id) REFERENCES skills(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS work (
        id INT PRIMARY KEY AUTO_INCREMENT,
        company VARCHAR(100),
        position VARCHAR(100),
        start_date DATE,
        end_date DATE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS links (
        id INT PRIMARY KEY AUTO_INCREMENT,
        profile_id INT,
        github VARCHAR(200),
        linkedin VARCHAR(200),
        portfolio VARCHAR(200),
        FOREIGN KEY (profile_id) REFERENCES profile(id)
    );
    """
]

for cmd in table_commands:
    cursor.execute(cmd)

print("All tables created successfully!")

# Sample data insertions
sample_data = [
    """
    INSERT INTO profile (name, email, education) VALUES
    ("Amit Sharma", "amit.sharma@email.com", "BTech Computer Science, XYZ University");
    """,
    """
    INSERT INTO skills (name) VALUES ("Python"), ("SQL"), ("HTML"), ("Flask"), ("MySQL");
    """,
    """
    INSERT INTO projects (title, description, link, skill_id) VALUES
    ("Me-API Playground", "REST API for candidate profile & queries", "https://github.com/amits/me-api", 1),
    ("Portfolio Site", "Personal portfolio website", "https://amit.dev", 3);
    """,
    """
    INSERT INTO work (company, position, start_date, end_date) VALUES
    ("ABC Tech", "Software Engineer", "2022-06-01", "2024-07-31");
    """,
    """
    INSERT INTO links (profile_id, github, linkedin, portfolio) VALUES
    (1, "https://github.com/amits", "https://linkedin.com/in/amitsharma", "https://amit.dev");
    """
]

for insert in sample_data:
    try:
        cursor.execute(insert)
    except mysql.connector.errors.IntegrityError:
        # Ignore duplicate entries if script is run multiple times
        pass

conn.commit()
cursor.close()
conn.close()

print("Sample data inserted successfully!")
