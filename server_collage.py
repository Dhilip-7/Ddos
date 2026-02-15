from flask import Flask, render_template_string, jsonify, send_file
import time
import os

app = Flask(__name__)

# --- DATABASE CONFIG ---
# --- DATABASE CONFIG ---
# Update the extensions from ".jpg" to ".jpeg"
students_db = {
    1: {"name": "Venkat Naidu", "dept": "Maths", "roll": "2026-MAT-01", "bio": "Gold Medalist in Calculus.", "status": "Fail", "img": "1.jpeg"},
    2: {"name": "Surya", "dept": "DLCO, OPPS", "roll": "2026-CS-02", "bio": "Representative of the coding club.", "status": "Fail", "img": "2.jpeg"},
    3: {"name": "Hemanth", "dept": "All Subjects", "roll": "2026-GEN-03", "bio": "Excellent all-rounder performance.", "status": "Pass", "img": "3.jpeg"},
    4: {"name": "Sneha", "dept": "Mechanical", "roll": "2026-MECH-04", "bio": "Published research on Thermodynamics.", "status": "Pass", "img": "4.jpeg"},
    5: {"name": "Madhur", "dept": "Civil", "roll": "2026-CIV-05", "bio": "Designed the new campus bridge.", "status": "Pass", "img": "5.jpeg"}
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>College Toppers List 2026</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; text-align: center; }
        .container { width: 85%; max-width: 800px; margin: 50px auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 15px; border-bottom: 1px solid #eee; text-align: left; }
        th { background-color: #3498db; color: white; }
        tr:hover { background-color: #f9f9f9; cursor: pointer; }
        .clickable-name { color: #2980b9; font-weight: bold; text-decoration: underline; cursor: pointer; }
        
        /* POPUP MODAL */
        .modal { display: none; position: fixed; z-index: 1; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.4); }
        .modal-content { background-color: #fefefe; margin: 10% auto; padding: 20px; border: 1px solid #888; width: 350px; border-radius: 10px; text-align: center; }
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        
        /* IMAGE STYLES */
        .student-photo { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 5px solid #3498db; margin-bottom: 15px; display: none; }
        .loading-spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 30px; height: 30px; animation: spin 2s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 College Results 2026 🏆</h1>
        <p>Click on a name to see the student's ID Photo.</p>
        <table>
            <tr><th>Rank</th><th>Student Name</th><th>Department</th><th>Status</th></tr>
            {% for id, student in students.items() %}
            <tr>
                <td>{{ id }}</td>
                <td><span class="clickable-name" onclick="openModal({{ id }})">{{ student.name }}</span></td>
                <td>{{ student.dept }}</td>
                <td style="color: {{ 'green' if student.status == 'Pass' else 'red' }}"><b>{{ student.status }}</b></td>
            </tr>
            {% endfor %}
        </table>
        <small>Server ID: Localhost-Edu-Node-V3 (Media Enabled)</small>
    </div>

    <div id="myModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <div id="loader" class="loading-spinner"></div>
            
            <img id="modal-img" class="student-photo" src="" onload="this.style.display='inline-block'; document.getElementById('loader').style.display='none';">
            
            <div id="modal-text" style="display:none">
                <h2 id="s-name"></h2>
                <p>Roll: <span id="s-roll"></span></p>
                <p><i>"<span id="s-bio"></span>"</i></p>
            </div>
        </div>
    </div>

    <script>
        function openModal(id) {
            document.getElementById('myModal').style.display = "block";
            // Reset modal state
            document.getElementById('loader').style.display = "block";
            document.getElementById('modal-img').style.display = "none";
            document.getElementById('modal-text').style.display = "none";
            document.getElementById('modal-img').src = ""; // Clear old image

            // 1. Fetch Text Data (Takes 2s)
            fetch('/get_student_details/' + id)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('s-name').innerText = data.name;
                    document.getElementById('s-roll').innerText = data.roll;
                    document.getElementById('s-bio').innerText = data.bio;
                    document.getElementById('modal-text').style.display = "block";
                    
                    // 2. Load Image (Takes another 1.5s)
                    // The 'onload' event in the <img> tag handles the spinner hiding
                    document.getElementById('modal-img').src = "/get_photo/" + data.img;
                });
        }
        function closeModal() { document.getElementById('myModal').style.display = "none"; }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, students=students_db)

@app.route('/get_student_details/<int:id>')
def get_student_details(id):
    # Simulate DB latency
    time.sleep(1.0) 
    return jsonify(students_db.get(id))

@app.route('/get_photo/<filename>')
def get_photo(filename):
    # Simulate Media Server Latency (Heavy I/O)
    time.sleep(1.5)
    
    # Securely serve the file from the student_photos folder
    file_path = os.path.join("student_photos", filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/jpeg')
    else:
        return "Image not found", 404

if __name__ == '__main__':
    print("🎓 Starting Media Server on http://127.0.0.1:5000")
    # Single threaded to ensure it crashes easily
    app.run(host='localhost', port=5000, threaded=False)
