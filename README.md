FaceReg is a Python-based face recognition attendance system designed to streamline and automate attendance tracking for students and faculty. Using a webcam, the system recognizes known faces, allows new users to register, and notifies administrators upon successful recognition through SMS.

#####
Features-

Real-Time Face Recognition: Identifies and verifies faces in real-time using live video feed from a webcam.
Automated Attendance: Automatically tracks attendance by recognizing pre-registered faces.
New User Registration: Allows students and faculty to register their faces for future recognition.
SMS Notification: Sends a notification via Twilio whenever a known face is recognized.
User-Friendly Interface: Intuitive GUI with separate tabs for students and faculty.
#####

Install the required Python packages:
pip install -r requirements.txt

#####

Set up Twilio:

Sign up for a Twilio account.
Update the account_sid, auth_token, and phone numbers in the source code with your Twilio credentials.
Prepare known faces:

Add known student images to the known_faces/ directory.
Add known faculty images to the faculty_faces/ directory.
Ensure images are named in the format name.jpg, name.png, or name.jpeg.

#####
