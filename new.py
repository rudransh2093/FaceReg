import cv2
import face_recognition
import os
import twilio.rest
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

known_students_folder = "" #add location for the known faces
known_faculty_folder = ""

def load_known_faces(folder):
    known_faces = []
    for file_name in os.listdir(folder):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder, file_name)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_faces.append({"name": file_name.split('.')[0], "encoding": face_encoding})
    return known_faces

known_students = load_known_faces(known_students_folder)
known_faculty = load_known_faces(known_faculty_folder)

def recognize_face(frame, root, timer_start_time, known_faces):
    try:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([f["encoding"] for f in known_faces], face_encoding)

            if True in matches:
                known_person = next(person for person in known_faces if matches[known_faces.index(person)])
                print(f"Recognized: {known_person['name']}")

                client = twilio.rest.Client('', '') #add creds from twilio

                message = client.messages.create(
                    body=f"A known face ({known_person['name']}) was recognized.",
                    from_='', ##
                    to='', ##
                )

                if cv2.getTickCount() - timer_start_time > 3 * cv2.getTickFrequency():
                    video_capture.release()

                    if root.winfo_exists():
                        root.destroy()

                        success_label = Label(main_window, text="Success!", font="Helvetica 16 bold", fg="green")
                        success_label.pack(pady=20)
                return
    except Exception as e:
        print(f"Error during face recognition: {e}")

def register_person(username, folder, frame):
    try:
        image_path = os.path.join(folder, f"{username}.jpg")
        cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        print(f"{username} registered successfully.")
    except Exception as e:
        print(f"Error during registration: {e}")

def start_registration_window(folder):
    registration_window = Toplevel(main_window)
    registration_window.title("Registration")

    label = Label(registration_window, text="Enter your username:", font="Helvetica 12")
    label.pack(pady=10)

    entry = Entry(registration_window, font="Helvetica 12")
    entry.pack(pady=10)

    canvas = Canvas(registration_window, width=400, height=300, bg="white")
    canvas.pack()

    style = ThemedTk(theme="equilux")  

    def video_preview():
        ret, frame = video_capture.read()
        if ret:
            frame = cv2.flip(frame, 1)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(Image.fromarray(image))
            canvas.create_image(0, 0, anchor=NW, image=photo)
            canvas.photo = photo
            registration_window.after(10, video_preview)

    video_preview()

    def capture_image():
        username = entry.get()
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(image))
        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.photo = photo

        save_button = ttk.Button(registration_window, text="Save", command=lambda: save_image(username, folder, frame, registration_window), style="Large.TButton", cursor="hand2")
        save_button.pack(side=LEFT, padx=20)
        retake_button = ttk.Button(registration_window, text="Retake", command=lambda: retake_image(canvas, registration_window), style="Large.TButton", cursor="hand2")
        retake_button.pack(side=RIGHT, padx=20)

    capture_button = ttk.Button(registration_window, text="Capture Image", command=capture_image, style="Large.TButton", cursor="hand2")
    capture_button.pack(pady=10)

def save_image(username, folder, frame, registration_window):
    register_person(username, folder, frame)
    registration_window.destroy()

def retake_image(canvas, registration_window):
    canvas.delete("all")
    registration_window.geometry("400x300")

video_capture = cv2.VideoCapture(0)

def start_main_window(known_faces):
    timer_start_time = cv2.getTickCount()

    while True:
        ret, frame = video_capture.read()

        frame = cv2.flip(frame, 1)

        recognize_face(frame, main_window, timer_start_time, known_faces)

        if not main_window.winfo_exists():
            break

        cv2.imshow('FaceCam', frame)

        key = cv2.waitKey(1)
        if key != -1 and key != 255:
            break

def start_student_registration():
    start_registration_window(known_students_folder)

def start_faculty_registration():
    start_registration_window(known_faculty_folder)

main_window = ThemedTk(theme="equilux") 
main_window.title("Face Recognition System")
main_window.geometry("800x600")

main_window.configure(bg="#8FED8F")  

notebook = ttk.Notebook(main_window)
notebook.pack(fill=BOTH, expand=YES)

student_tab = Frame(notebook, width=800, height=600, bg="#8FED8F") 
notebook.add(student_tab, text="Student")

style = ttk.Style(main_window)
style.configure("Large.TButton", padding=(20, 10), font=("Helvetica", 14), foreground="white", background="#4CAF50", bordercolor="black", anchor="center")

student_image_label = Label(student_tab, text="Student Image Placeholder", font="Helvetica 14 italic", bg="#8FED8F") 
student_image_label.pack(pady=20)

register_student_label = Label(student_tab, text="Click here for Student Registration", font="Helvetica 14 bold", bg="#8FED8F") 
register_student_label.pack(pady=10, padx=20)

register_student_button = ttk.Button(student_tab, text="Register", command=start_student_registration, style="Large.TButton", cursor="hand2")
register_student_button.pack(pady=10)

existing_student_label = Label(student_tab, text="Click here for Existing Student", font="Helvetica 14 bold", bg="#8FED8F") 
existing_student_label.pack(pady=10, padx=20)

existing_student_button = ttk.Button(student_tab, text="Existing", command=lambda: start_main_window(known_students), style="Large.TButton", cursor="hand2")
existing_student_button.pack(pady=10)

faculty_tab = Frame(notebook, width=800, height=600, bg="#8FED8F")
notebook.add(faculty_tab, text="Faculty")

faculty_image_label = Label(faculty_tab, text="Faculty Image Placeholder", font="Helvetica 14 italic", bg="#8FED8F")
faculty_image_label.pack(pady=20)

register_faculty_label = Label(faculty_tab, text="Click here for Faculty Registration", font="Helvetica 14 bold", bg="#8FED8F") 

register_faculty_button = ttk.Button(faculty_tab, text="Register", command=start_faculty_registration, style="Large.TButton", cursor="hand2")
register_faculty_button.pack(pady=10)

existing_faculty_label = Label(faculty_tab, text="Click here for Existing Faculty", font="Helvetica 14 bold", bg="#8FED8F") 

existing_faculty_button = ttk.Button(faculty_tab, text="Existing", command=lambda: start_main_window(known_faculty), style="Large.TButton", cursor="hand2")
existing_faculty_button.pack(pady=10)

header_title_label = Label(main_window, text="ATTENDANCE SYSTEM", font="Helvetica 24 bold", pady=20, bg="#8FED8F") 

main_window.mainloop()

video_capture.release()
cv2.destroyAllWindows()