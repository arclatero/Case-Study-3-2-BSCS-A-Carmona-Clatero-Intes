import json
from abc import ABC, abstractmethod



# Abstract Base Class for Person

class Person(ABC):
    x="\nHello to E-Learning Platform"
    y="Welcome to digital school"
    def __init__(self, id, name, email):
        self.__id = id
        self.name = name
        self.email = email

    @abstractmethod
    def get_role(self):
        pass
    def get_id(self):
        return self.__id

# Subclasses for Person
class Student(Person):
    def __init__(self, id, name, email, courses=[]):
        super().__init__(id, name, email)
        self._courses = courses

    def enroll(self, course_id):
        if course_id not in self._courses:
            self._courses.append(course_id)

    def get_role(self):
        return "Student"

   
   
    def view_assignments(student):
        print("\n--- View Assignments ---")

        # Load all courses
        courses = DataManager.load_data("course.json")
        
        # Get the list of enrolled courses for the student
        enrolled_course_ids = student.get("enrolled_courses", [])
        if not enrolled_course_ids:
            print("You are not enrolled in any courses.")
            return

        assignments_found = False

        # Loop through enrolled courses to find assignments
        for course in courses:
            if course["id"] in enrolled_course_ids:
                print(f"\nCourse: {course['title']}")
                
                for subject in course.get("subjects", []):
                    if "assignments" in subject and subject["assignments"]:
                        assignments_found = True
                        print(f"  Subject: {subject['title']}")
                        for idx, assignment in enumerate(subject["assignments"], 1):
                            print(f"    {idx}. {assignment['title']}")
                            print(f"       Description: {assignment['description']}")
                            print(f"       Due Date: {assignment['due_date']}")
                    else:
                        print(f"  Subject: {subject['title']}")
                        print("    No assignments in this subject.")
        



    #dsgggggggggggggggggggggggggggggggggggggggg
    def submit_assignment(student):
        print("\n--- Submit Assignment ---")

        # Access the student's enrolled courses
        enrolled_courses = student.get("enrolled_courses", [])

        if not enrolled_courses:
            print("You are not enrolled in any courses.")
            return

        # Fetch full course details if `enrolled_courses` contains IDs
        all_courses = DataManager.load_data("course.json")
        enrolled_courses = [
            course for course in all_courses if course["id"] in enrolled_courses
        ]

        print("Enrolled Courses:")
        for idx, course in enumerate(enrolled_courses, start=1):
            print(f"{idx}. {course['title']}")

        # Choose a course
        course_choice = input("\nEnter the number of the course to submit assignment: ")
        if course_choice.isdigit() and 1 <= int(course_choice) <= len(enrolled_courses):
            selected_course = enrolled_courses[int(course_choice) - 1]

            # Get subjects for the selected course
            subjects = selected_course.get("subjects", [])
            print("\nSubjects available for the course:")
            for idx, subject in enumerate(subjects, start=1):
                print(f"{idx}. {subject['title']}")

            subject_choice = input("\nEnter the number of the subject to submit assignment: ")
            if subject_choice.isdigit() and 1 <= int(subject_choice) <= len(subjects):
                selected_subject = subjects[int(subject_choice) - 1]
                assignments = selected_subject.get("assignments", [])

                if assignments:
                    print("\nAvailable Assignments:")
                    for idx, assignment in enumerate(assignments, start=1):
                        print(f"{idx}. {assignment['title']} (Due: {assignment['due_date']})")

                    assignment_choice = input("\nChoose an assignment to submit: ")
                    if assignment_choice.isdigit() and 1 <= int(assignment_choice) <= len(assignments):
                        selected_assignment = assignments[int(assignment_choice) - 1]

                        answer = input("\nEnter your answer for the assignment: ")

                        # Save the submission
                        submissions = DataManager.load_data("submitted_assignments.json")
                        submission_data = {
                            "student_id": student["id"],
                            "student_name": student["name"],
                            "course_id": selected_course["id"],
                            "subject_id": selected_subject["id"],
                            "assignment_title": selected_assignment["title"],
                            "answer": answer,
                            "grade": None
                        }
                        submissions.append(submission_data)
                        DataManager.save_data("submitted_assignments.json", submissions)

                        print("\nYour assignment has been submitted successfully!")
                    else:
                        print("\nInvalid assignment choice. Please try again.")
                else:
                    print("No assignments available for this subject.")
            else:
                print("\nInvalid subject choice. Please try again.")
        else:
            print("\nInvalid course choice. Please try again.")



class Instructor(Person):
    def __init__(self, id, name, email, courses=[]):
        super().__init__(id, name, email)
        self._courses = courses

    def assign_course(self, course_id):
        if course_id not in self._courses:
            self._courses.append(course_id)

    def get_role(self):
        return "Instructor"
   
    def assign_assignment(instructor):
        print("\n--- Assign Assignment ---")
        
        # Load all courses
        courses = DataManager.load_data("course.json")
        
        # Find subjects assigned to this instructor
        assigned_subjects = []
        for course in courses:
            for subject in course.get("subjects", []):
                if subject["instructor_id"] == instructor["id"]:
                    assigned_subjects.append(subject)
        
        if not assigned_subjects:
            print("No subjects assigned to you.")
            return
        
        # Display assigned subjects
        print("\n--- Your Assigned Subjects ---")
        for idx, subject in enumerate(assigned_subjects, 1):
            print(f"{idx}. {subject['title']} (ID: {subject['id']}) - {subject['days']} - {subject['units']} Hours")
        
        # Select a subject
        try:
            choice = int(input("\nSelect a subject to assign an assignment (enter number): ")) - 1
            if choice < 0 or choice >= len(assigned_subjects):
                print("Invalid choice.")
                return
        except ValueError:
            print("Invalid input.")
            return
        
        selected_subject = assigned_subjects[choice]
        
        # Gather assignment details
        assignment_title = input("Enter assignment title: ")
        assignment_description = input("Enter assignment description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        
        # Add the assignment to the selected subject
        if "assignments" not in selected_subject:
            selected_subject["assignments"] = []
        
        selected_subject["assignments"].append({
            "title": assignment_title,
            "description": assignment_description,
            "due_date": due_date,
        })
        
        # Save updated course data
        DataManager.save_data("course.json", courses)
        
        print(f"\nAssignment '{assignment_title}' assigned to subject '{selected_subject['title']}'.")

    def view_submitted_assignments(instructor):
        print("\n--- View Submitted Assignments ---")

        # Load submitted assignments
        submissions = DataManager.load_data("submitted_assignments.json")
        if not submissions:
            print("No assignments submitted yet.")
            return

        # Filter assignments for the instructor
        instructor_courses = PlatformAdmin.get_courses_for_instructor(instructor["id"])
        instructor_subject_ids = [
            subject["id"]
            for course in instructor_courses
            for subject in course.get("subjects", [])
            if subject["instructor_id"] == instructor["id"]
        ]

        filtered_submissions = [
            submission
            for submission in submissions
            if submission["subject_id"] in instructor_subject_ids
        ]

        if not filtered_submissions:
            print("No assignments submitted for your subjects.")
            return

        # Display submissions
        for idx, submission in enumerate(filtered_submissions, start=1):
            print(f"\nSubmission {idx}:")
            print(f"Student Name: {submission['student_name']}")
            print(f"Assignment Title: {submission.get('assignment_title', 'N/A')}")
            print(f"Answer: {submission['answer']}")
            print(f"Grade: {'Not graded yet' if submission['grade'] is None else submission['grade']}")

        # Grade assignments
        choice = input("\nEnter the number of the submission to grade (or press Enter to exit): ")
        if choice.isdigit() and 1 <= int(choice) <= len(filtered_submissions):
            selected_submission = filtered_submissions[int(choice) - 1]
            grade = input("Enter grade for this submission: ")

            # Update grade
            for submission in submissions:
                if (
                    submission["student_id"] == selected_submission["student_id"]
                    and submission["subject_id"] == selected_submission["subject_id"]
                    and submission.get("assignment_title") == selected_submission.get("assignment_title")  # Match the assignment title
                ):
                    submission["grade"] = grade
                    break

            DataManager.save_data("submitted_assignments.json", submissions)
            print("\nGrade assigned successfully!")

    
# Course Class
class Course:
    def __init__(self, id, title, instructor_id, schedule):
        self.id = id
        self.title = title
        self.instructor_id = instructor_id
        self.schedule = schedule
    def add_course():
      print("\n--- Add Course ---")
      courses = DataManager.load_data("course.json")
      
      course_id = len(courses) + 1
      title = input("Enter course title: ")

      new_course = {
          "id": course_id,
          "title": title,
          "subjects": []  # Subjects still associated with the course
      }

      # Adding Subjects
      while True:
          add_subject = input("\nDo you want to add a subject to this course? (yes/no): ").strip().lower()
          if add_subject == "yes":
              subject_id = len(new_course["subjects"]) + 1
              subject_title = input("Enter subject title: ")

              # Ask for day, units, and instructor details
              days = input("Enter the days for the subject (e.g., Mon, Wed): ")
              units = input("Enter the number of hours(1:00pm-3:oopm): ")
              instructors = DataManager.load_data("instructor.json")
              
              print("\nList of Instructors:")
              for idx, instructor in enumerate(instructors, start=1):
                  print(f"{idx}. {instructor['name']}")

              instructor_choice = input("Select an instructor by number: ")
              if instructor_choice.isdigit() and 1 <= int(instructor_choice) <= len(instructors):
                  instructor_id = instructors[int(instructor_choice) - 1]["id"]
              else:
                  print("\nInvalid choice. Skipping this subject.\n")
                  continue

              new_subject = {
                  "id": subject_id,
                  "title": subject_title,
                  "instructor_id": instructor_id,
                  "days": days,
                  "units": units
              }
              new_course["subjects"].append(new_subject)
              print(f"\nSubject '{subject_title}' added to the course.\n")
          elif add_subject == "no":
              break
          else:
              print("\nInvalid choice. Please answer 'yes' or 'no'.\n")

      courses.append(new_course)
      DataManager.save_data("course.json", courses)
      print(f"\nCourse '{title}' with subjects added successfully.\n")

# Enrollment Class
class Enrollment:
    def __init__(self):
        self.enrollments = []

    def add_enrollment(self, student_id, course_id):
        self.enrollments.append({"student_id": student_id, "course_id": course_id})
    @staticmethod
    def process_enrollment_requests():
        """Processes enrollment requests and updates student data."""
        enroll_requests = DataManager.load_data("enroll_requests.json")
        students = DataManager.load_data("student.json")

        if not enroll_requests:
            print("No enrollment requests to process.\n")
            return

        print("\n--- Enrollment Requests ---")
        for idx, request in enumerate(enroll_requests, start=1):
            print(f"{idx}. Student: {request['student_name']} | Course: {request['course_title']}")

        choice = input("\nEnter the number of the request to approve (or 'q' to quit): ")
        if choice.isdigit() and 1 <= int(choice) <= len(enroll_requests):
            selected_request = enroll_requests[int(choice) - 1]

            # Find the student
            student = next((s for s in students if s["id"] == selected_request["student_id"]), None)

            if student:
                # Add the course ID to the student's enrolled courses
                if "enrolled_courses" not in student:
                    student["enrolled_courses"] = []
                if selected_request["course_id"] not in student["enrolled_courses"]:
                    student["enrolled_courses"].append(selected_request["course_id"])

                # Save updated student data
                DataManager.save_data("student.json", students)

                # Remove the processed request
                enroll_requests.remove(selected_request)
                DataManager.save_data("enroll_requests.json", enroll_requests)

                print(f"Enrollment for student '{student['name']}' approved.\n")
            else:
                print("Error: Student not found.\n")
        elif choice.lower() == 'q':
            print("Exiting enrollment processing.\n")
        else:
            print("Invalid choice.\n")

# Assignment Class
class Assignment:
    def __init__(self, id, title, course_id, description):
        self.id = id
        self.title = title
        self.course_id = course_id
        self.description = description
    
    def view_assignment_score(student):
        print("\n--- View Assignment Score ---")

        # Load submitted assignments
        submissions = DataManager.load_data("submitted_assignments.json")
        courses = DataManager.load_data("course.json")  # Load course details for lookups

        # Filter submissions for the current student
        student_submissions = [
            submission for submission in submissions if submission["student_id"] == student["id"]
        ]

        if not student_submissions:
            print("You have not submitted any assignments yet.")
            return

        graded_found = False
        for idx, submission in enumerate(student_submissions, start=1):
            # Fetch course and subject info
            course = next((c for c in courses if c["id"] == submission["course_id"]), None)
            subject = next(
                (s for c in courses for s in c.get("subjects", []) if s["id"] == submission["subject_id"]),
                None
            )

            if course and subject:
                grade_display = "Not graded yet" if submission["grade"] is None else submission["grade"]
                print(f"\nAssignment {idx}:")
                print(f"  Course: {course['title']}")
                print(f"  Subject: {subject['title']}")
                print(f"  Assignment Title: {submission.get('assignment_title', 'N/A')}")
                print(f"  Grade: {grade_display}")
                
                if submission["grade"] is not None:
                    graded_found = True

        if not graded_found:
            print("\nNo assignments have been graded yet.")
class Attendance:
    def mark_attendance(student):
        """Allows students to mark attendance for a specific subject in a course."""
        print("\n--- Mark Attendance ---")
        
        # Load courses and filter for enrolled ones
        courses = DataManager.load_data("course.json")
        enrolled_courses = [c for c in courses if c["id"] in student.get("enrolled_courses", [])]

        if not enrolled_courses:
            print("You are not enrolled in any courses.\n")
            return

        # Display enrolled courses
        print("Enrolled Courses:")
        for idx, course in enumerate(enrolled_courses, start=1):
            print(f"{idx}. {course['title']}")

        # Choose a course
        course_choice = input("\nEnter the number of the course to mark attendance: ")
        if not course_choice.isdigit() or not (1 <= int(course_choice) <= len(enrolled_courses)):
            print("Invalid choice. Please try again.")
            return

        selected_course = enrolled_courses[int(course_choice) - 1]

        # Display subjects in the selected course
        print(f"\nSubjects in {selected_course['title']}:")
        for idx, subject in enumerate(selected_course["subjects"], start=1):
            print(f"{idx}. {subject['title']}")

        subject_choice = input("\nEnter the number of the subject to mark attendance: ")
        if not subject_choice.isdigit() or not (1 <= int(subject_choice) <= len(selected_course["subjects"])):
            print("Invalid choice. Please try again.")
            return

        selected_subject = selected_course["subjects"][int(subject_choice) - 1]
        student_name = input("Enter your name: ")
        date = input("Enter the date (YYYY-MM-DD): ")

        # Choose status
        print("1. Present\n2. Absent")
        status_choice = input("Enter your attendance status: ")
        status = "Present" if status_choice == "1" else "Absent"

        # Save attendance record
        attendance_data = DataManager.load_data("attendance.json")
        new_attendance = {
            "student_id": student["id"],
            "student_name": student_name,
            "course_id": selected_course["id"],
            "course_title": selected_course["title"],
            "subject_id": selected_subject["id"],
            "subject_title": selected_subject["title"],
            "date": date,
            "status": status
        }
        attendance_data.append(new_attendance)
        DataManager.save_data("attendance.json", attendance_data)

        print(f"\nAttendance marked as '{status}' for {selected_subject['title']} on {date}.\n")

    def view_attendance(instructor):
        """Allows instructors to view attendance records for their assigned subjects."""
        print("\n--- View Attendance ---")

        # Load courses for the instructor
        instructor_courses = PlatformAdmin.get_courses_for_instructor(instructor["id"])
        if not instructor_courses:
            print("You are not teaching any courses.\n")
            return

        # Display courses
        print("Your Courses:")
        for idx, course in enumerate(instructor_courses, start=1):
            print(f"{idx}. {course['title']}")

        # Choose a course
        course_choice = input("\nEnter the number of the course to view attendance: ")
        if not course_choice.isdigit() or not (1 <= int(course_choice) <= len(instructor_courses)):
            print("Invalid choice. Please try again.")
            return

        selected_course = instructor_courses[int(course_choice) - 1]

        # Display subjects in the selected course
        print(f"\nSubjects in {selected_course['title']}:")
        for idx, subject in enumerate(selected_course["subjects"], start=1):
            print(f"{idx}. {subject['title']}")

        subject_choice = input("\nEnter the number of the subject to view attendance: ")
        if not subject_choice.isdigit() or not (1 <= int(subject_choice) <= len(selected_course["subjects"])):
            print("Invalid choice. Please try again.")
            return

        selected_subject = selected_course["subjects"][int(subject_choice) - 1]

        # Load and filter attendance data
        attendance_data = DataManager.load_data("attendance.json")
        subject_attendance = [
            a for a in attendance_data
            if a.get("subject_id") == selected_subject["id"] and a.get("course_id") == selected_course["id"]
        ]

        if not subject_attendance:
            print(f"No attendance records found for {selected_subject['title']} in {selected_course['title']}.\n")
            return

        # Display attendance records
        print(f"\nAttendance Records for {selected_subject['title']} in {selected_course['title']}:")
        for record in subject_attendance:
            print(f"- Date: {record['date']} | Student: {record['student_name']} | Status: {record['status']}")

    
# Grade Class
class Grade:
    def __init__(self, assignment_id, student_id, grade):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.grade = grade

    
    def assign_final_grades(instructor):
        print("\n--- Assign Final Grade for Each Subject ---")
        courses = DataManager.load_data("course.json")
        students = DataManager.load_data("student.json")

        # Collect subjects assigned to the instructor
        assigned_subjects = []
        for course in courses:
            for subject in course.get("subjects", []):
                if subject.get("instructor_id") == instructor["id"]:
                    assigned_subjects.append((course["title"], subject))
        
        if not assigned_subjects:
            print("No subjects assigned to you.\n")
            return
        
        for course_title, subject in assigned_subjects:
            print(f"\nCourse: {course_title}")
            print(f"  Subject ID: {subject['id']}, Title: {subject['title']}")
            
            enrolled_students = []
            for student in students:
                if course["id"] in student.get("enrolled_courses", []):
                    enrolled_students.append(student)
            
            if not enrolled_students:
                print("    No students enrolled in this subject.\n")
                continue

            for student in enrolled_students:
                print(f"    - {student['name']} (ID: {student['id']})")
                grade = input(f"Enter final grade for {student['name']} in {subject['title']}: ")
                # Save grades in student JSON
                student.setdefault("grades", {}).setdefault(str(subject["id"]), grade)
        
        DataManager.save_data("student.json", students)
        print("Final grades assigned successfully.\n")



    def view_final_grade(student):
        print("\n--- View Final Grades ---")
        
        # Load student JSON data
        students = DataManager.load_data("student.json")
        courses = DataManager.load_data("course.json")

        # Find the logged-in student's data
        student_data = next((s for s in students if s["id"] == student["id"]), None)
        
        if not student_data:
            print("No data found for the student.\n")
            return

        # Check if the student has grades
        grades = student_data.get("grades", {})
        
        if not grades:
            print("No final grades available for your subjects.\n")
            return

        # Display grades for each enrolled subject
        for course in courses:
            if course["id"] in student_data.get("enrolled_courses", []):
                print(f"\nCourse: {course['title']}")
                for subject in course.get("subjects", []):
                    subject_id = str(subject["id"])
                    if subject_id in grades:
                        print(f"  Subject: {subject['title']}")
                        print(f"    Final Grade: {grades[subject_id]}")
                    else:
                        print(f"  Subject: {subject['title']}")
                        print("    Final Grade: Not yet assigned.")
        print()



    
# Schedule Class
class Schedule:
    def __init__(self, course_id, day, time):
        self.course_id = course_id
        self.day = day
        self.time = time
    def view_enrolled_courses(student):
        """Displays detailed information about the courses a student is enrolled in, excluding assignments."""
        print("\n--- View Enrolled Courses ---")
        
        # Check if the student is enrolled in any courses
        if "enrolled_courses" in student and student["enrolled_courses"]:
            courses = DataManager.load_data("course.json")
            
            # Filter courses based on enrolled IDs
            enrolled_courses = [c for c in courses if c["id"] in student["enrolled_courses"]]
            
            if enrolled_courses:
                for idx, course in enumerate(enrolled_courses, start=1):
                    print(f"\n{idx}. Course Title: {course['title']}")
                    print(f"   Course ID: {course['id']}")

                    # Check and display subjects
                    if "subjects" in course and course["subjects"]:
                        print("   Subjects:")
                        for subject_idx, subject in enumerate(course["subjects"], start=1):
                            print(f"      {subject_idx}. Subject Title: {subject['title']}")
                            print(f"         Subject ID: {subject['id']}")
                            print(f"         Instructor ID: {subject['instructor_id']}")
                            print(f"         Days: {subject['days']}")
                            print(f"         Hours: {subject['units']}")
                    else:
                        print("   No subjects available.")
            else:
                print("You are not enrolled in any courses.")
        else:
            print("You are not enrolled in any courses.")
# Utility: JSON Data Management Class
class DataManager:
    @staticmethod
    def load_data(file_name):
        try:
            with open(file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_data(file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
# Platform Admin Class
class PlatformAdmin:
    def __init__(self, id, name):
        self.id = id
        self.name = name
#dsgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
    def get_subjects(course_id):
        courses = DataManager.load_data("course.json")
        for course in courses:
            if course["id"] == course_id:
                return course.get("subjects", [])
        return []
    def get_courses_for_instructor(instructor_id):
        courses = DataManager.load_data("course.json")
        return [
            course
            for course in courses
            if any(
                subject["instructor_id"] == instructor_id
                for subject in course.get("subjects", [])
            )
        ]
    
    

    def drop_student():
        print("\n--- Drop Student ---")
        students = DataManager.load_data("student.json")
        courses = DataManager.load_data("course.json")

        # Filter students who are enrolled in courses
        enrolled_students = [
            {
                "student_id": student["id"],
                "student_name": student["name"],
                "enrolled_courses": student.get("enrolled_courses", [])
            }
            for student in students if "enrolled_courses" in student and student["enrolled_courses"]
        ]

        if not enrolled_students:
            print("No students are currently enrolled in any course.\n")
            return

        # Display enrolled students and their courses
        print("\nList of Enrolled Students:")
        for idx, student in enumerate(enrolled_students, start=1):
            enrolled_courses = [
                next(course["title"] for course in courses if course["id"] == course_id)
                for course_id in student["enrolled_courses"]
            ]
            enrolled_courses_str = ", ".join(enrolled_courses)
            print(f"{idx}. {student['student_name']} (Enrolled in: {enrolled_courses_str})")

        # Select student to drop
        choice = input("\nEnter the number of the student to drop: ")
        if choice.isdigit() and 1 <= int(choice) <= len(enrolled_students):
            selected_student = enrolled_students[int(choice) - 1]

            # Display courses for confirmation
            print(f"\nStudent: {selected_student['student_name']}")
            for idx, course_id in enumerate(selected_student["enrolled_courses"], start=1):
                course_name = next(course["title"] for course in courses if course["id"] == course_id)
                print(f"{idx}. {course_name}")

            course_choice = input("\nEnter the number of the course to drop the student from: ")
            if course_choice.isdigit() and 1 <= int(course_choice) <= len(selected_student["enrolled_courses"]):
                # Remove the course from the student's enrolled courses
                course_id_to_drop = selected_student["enrolled_courses"].pop(int(course_choice) - 1)
                course_name = next(course["title"] for course in courses if course["id"] == course_id_to_drop)

                # Update the student in the data
                student_to_update = next(s for s in students if s["id"] == selected_student["student_id"])
                student_to_update["enrolled_courses"] = selected_student["enrolled_courses"]

                # Save updated data
                DataManager.save_data("student.json", students)

                print(f"\nStudent {selected_student['student_name']} dropped from {course_name}.\n")
            else:
                print("\nInvalid course selection. Returning to menu.\n")
        else:
            print("\nInvalid choice. Please try again.\n")

    def add_instructor():
        print("\n--- Add Instructor ---")
        instructors = DataManager.load_data("instructor.json")

        name = input("Enter the instructor's name: ")
        email = input("Enter the instructor's email: ")
        password = input("Enter the instructor's password: ")

        if any(instructor["email"] == email for instructor in instructors):
            print("Instructor with this email already exists.")
            return

        instructor_id = len(instructors) + 1
        new_instructor = {
            "id": instructor_id,
            "name": name,
            "email": email,
            "password":password

        }
        instructors.append(new_instructor)
        DataManager.save_data("instructor.json", instructors)

        print(f"Instructor {name} added successfully.\n")
    def delete_instructor():
        print("\n--- Delete Instructor ---")
        instructors = DataManager.load_data("instructor.json")

        if not instructors:
            print("No instructors found.")
            return

        print("\nList of Instructors:")
        for idx, instructor in enumerate(instructors, start=1):
            print(f"{idx}. {instructor['name']} (Email: {instructor['email']})")

        choice = input("\nEnter the number of the instructor to delete: ")
        if choice.isdigit() and 1 <= int(choice) <= len(instructors):
            removed_instructor = instructors.pop(int(choice) - 1)
            print(f"\nInstructor {removed_instructor['name']} deleted successfully.\n")
            DataManager.save_data("instructor.json", instructors)
        else:
            print("\nInvalid choice. Please try again.\n")
    def add_course():
        print("\n--- Add Course ---")
        courses = DataManager.load_data("course.json")
        instructors = DataManager.load_data("instructor.json")

        course_id = len(courses) + 1
        title = input("Enter course title: ")

        print("\nList of Instructors:")
        for idx, instructor in enumerate(instructors, start=1):
            print(f"{idx}. {instructor['name']}")

        instructor_choice = input("Select the instructor by number: ")
        if instructor_choice.isdigit() and 1 <= int(instructor_choice) <= len(instructors):
            instructor_id = instructors[int(instructor_choice) - 1]["id"]
        else:
            print("\nInvalid choice. Please try again.\n")
            return

        days = input("Enter the days for the course (e.g., Mon, Tue): ")
        units = input("Enter the number of hours (e.g. 1:00pm-3:00pm): ")

        new_course = {
            "id": course_id,
            "title": title,
            "instructor_id": instructor_id,
            "days": days,
            "units": units
        }
        courses.append(new_course)
        DataManager.save_data("course.json", courses)

        print(f"\nCourse '{title}' added successfully.\n")
    def delete_course():
        print("\n--- Delete Course ---")
        courses = DataManager.load_data("course.json")

        if not courses:
            print("No courses found.")
            return

        print("\nList of Courses:")
        for idx, course in enumerate(courses, start=1):
            print(f"{idx}. {course['title']} (ID: {course['id']})")

        choice = input("\nEnter the number of the course to delete: ")
        if choice.isdigit() and 1 <= int(choice) <= len(courses):
            removed_course = courses.pop(int(choice) - 1)
            print(f"\nCourse '{removed_course['title']}' deleted successfully.\n")
            DataManager.save_data("course.json", courses)
        else:
            print("\nInvalid choice. Please try again.\n")
    def enroll_in_course(student):
      print("\n--- Enroll in a Course ---")
      courses = DataManager.load_data("course.json")
      enroll_requests = DataManager.load_data("enroll_requests.json")

      if not courses:
          print("No courses available for enrollment.\n")
          return

      print("\nAvailable Courses:")
      for idx, course in enumerate(courses, start=1):
          title = course.get("title", "Unknown Title")
          print(f"{idx}. {title}")

      choice = input("\nEnter the number of the course to enroll in: ")
      if choice.isdigit() and 1 <= int(choice) <= len(courses):
          selected_course = courses[int(choice) - 1]

          # Check if the student has already requested or enrolled in the course
          if any(req["student_id"] == student["id"] and req["course_id"] == selected_course["id"] for req in enroll_requests):
              print("You have already requested enrollment in this course.\n")
              return

          # Add enrollment request
          new_request = {
              "id": len(enroll_requests) + 1,
              "student_id": student["id"],
              "student_name": student["name"],
              "course_id": selected_course["id"],
              "course_title": selected_course.get("title", "Unknown Title")
          }
          enroll_requests.append(new_request)
          DataManager.save_data("enroll_requests.json", enroll_requests)

          print(f"Enrollment request submitted for course '{selected_course.get('title', 'Unknown Title')}'.\n")
      else:
          print("\nInvalid choice. Please try again.\n")


    
    


    def add_subject_to_course():
        print("\n--- Add Subject to Course ---")
        courses = DataManager.load_data("course.json")
        instructors = DataManager.load_data("instructor.json")

        if not courses:
            print("No courses available. Please add a course first.")
            return

        print("\nList of Courses:")
        for idx, course in enumerate(courses, start=1):
            print(f"{idx}. {course['title']} (ID: {course['id']})")

        course_choice = input("\nEnter the number of the course to add a subject: ")
        if course_choice.isdigit() and 1 <= int(course_choice) <= len(courses):
            selected_course = courses[int(course_choice) - 1]

            subject_id = len(selected_course.get("subjects", [])) + 1
            subject_title = input("Enter subject title: ")
            days = input("Enter the days for the subject (e.g., Mon, Wed): ")
            units = input("Enter the number of hours (e.g., 1:00pm-3:00pm): ")

            if not instructors:
                print("No instructors available. Please add an instructor first.")
                return

            print("\nList of Instructors:")
            for idx, instructor in enumerate(instructors, start=1):
                print(f"{idx}. {instructor['name']} (ID: {instructor['id']})")

            instructor_choice = input("Select an instructor by number: ")
            if instructor_choice.isdigit() and 1 <= int(instructor_choice) <= len(instructors):
                instructor_id = instructors[int(instructor_choice) - 1]["id"]
            else:
                print("\nInvalid choice. Returning to the main menu.\n")
                return

            new_subject = {
                "id": subject_id,
                "title": subject_title,
                "instructor_id": instructor_id,
                "days": days,
                "units": units
            }

            # Add subject to the selected course
            if "subjects" not in selected_course:
                selected_course["subjects"] = []
            selected_course["subjects"].append(new_subject)

            # Save updated course data
            DataManager.save_data("course.json", courses)
            print(f"\nSubject '{subject_title}' added successfully to course '{selected_course['title']}'.\n")
        else:
            print("\nInvalid choice. Returning to the main menu.\n")
    
    
    def view_assigned_courses_and_subjects(instructor):
        """Displays courses and subjects assigned to the instructor along with enrolled students."""
        print("\n--- Assigned Courses and Subjects ---")
        courses = DataManager.load_data("course.json")
        students = DataManager.load_data("student.json")
        
        assigned_courses = [course for course in courses if any(
            subject.get("instructor_id") == instructor["id"] for subject in course.get("subjects", [])
        )]

        if not assigned_courses:
            print("No courses or subjects assigned to you.\n")
            return

        for course in assigned_courses:
            print(f"\nCourse: {course['title']}")
            for subject in course.get("subjects", []):
                if subject.get("instructor_id") == instructor["id"]:
                    print(f"  Subject ID: {subject['id']}")
                    print(f"  Title: {subject['title']}")
                    print(f"  Days: {subject['days']}")
                    print(f"  Hours: {subject['units']}")
                    
                    # Find students enrolled in this course
                    enrolled_students = [
                        student for student in students if course["id"] in student.get("enrolled_courses", [])
                    ]

                    print("  Enrolled Students:")
                    if not enrolled_students:
                        print("    No students enrolled in this course")
                    else:
                        for student in enrolled_students:
                            print(f"    - {student['name']} (ID: {student['id']})")
    
        

# Login and Signup Management
class Login:
    @staticmethod
    def signup(user_type):
        
        file_name = f"{user_type}.json"
        users = DataManager.load_data(file_name)

        print(f"\n--- {user_type.capitalize()} Sign-Up ---")
        name = input("Enter your full name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        # Check if email already exists
        for user in users:
            if user["email"] == email:
                print(f"Error: A {user_type} with this email already exists.")
                return

        # Add the new user
        user_id = len(users) + 1
        user_data = {
            "id": user_id,
            "name": name,
            "email": email,
            "password": password
        }
        users.append(user_data)
        DataManager.save_data(file_name, users)

        print(f"\n{user_type.capitalize()} account created successfully!\n")

    @staticmethod
    def login(user_type):
      file_name = f"{user_type}.json"
      users = DataManager.load_data(file_name)

      print(f"\n--- {user_type.capitalize()} Login ---")
      email = input("Enter your email: ")
      password = input("Enter your password: ")

      for user in users:
          if user["email"] == email and user["password"] == password:
              print(f"\nWelcome, {user['name']}!")
              if user_type == "admin":
                  Info.admin_dashboard()
              elif user_type == "student":
                  Info.student_dashboard(user)  # Pass the student object
              elif user_type == "instructor":
                  Info.instructor_dashboard(user)
              return user

      print("\nLogin failed: Invalid email or password.\n")
      return None

# Main Information and Transactions
class Info:
    
    def admin_dashboard():
        while True:
            print("\n--- Admin Dashboard ---")
            print("1. View All Students")
            print("2. View All Instructors")
            print("3. View All Courses")
            print("4. Process Enrollment Requests")
            print("5. Drop Student")
            print("6. Add Instructor")
            print("7. Delete Instructor")
            print("8. Add Course")
            print("9. Delete Course")
            print("10. Add Subject to Course")
            print("11. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                students = DataManager.load_data("student.json")
                print("\n--- All Students ---")
                for student in students:
                    print(f"ID: {student['id']}, Name: {student['name']}, Email: {student['email']}")
            elif choice == "2":
                instructors = DataManager.load_data("instructor.json")
                print("\n--- All Instructors ---")
                for instructor in instructors:
                    print(f"ID: {instructor['id']}, Name: {instructor['name']}, Email: {instructor['email']}")
            elif choice == "3":  # View All Courses
              courses = DataManager.load_data("course.json")
              print("\n--- All Courses ---")
              for course in courses:
                  print(f"\nCourse ID: {course['id']}")
                  print(f"Title: {course['title']}")
                  
                  # Use .get() to safely handle missing 'subjects' key
                  subjects = course.get("subjects", [])
                  print("Subjects:")
                  if not subjects:
                      print("  No subjects added to this course.")
                  for subject in subjects:
                      print(f"  Subject ID: {subject['id']}")
                      print(f"  Title: {subject['title']}")
                      print(f"  Days: {subject['days']}")
                      print(f"  Hours: {subject['units']}")
                      print(f"  Instructor ID: {subject['instructor_id']}")
            elif choice == "4":
                Enrollment.process_enrollment_requests()
            elif choice == "5":
                PlatformAdmin.drop_student()
            elif choice == "6":
                PlatformAdmin.add_instructor()
            elif choice == "7":
                PlatformAdmin.delete_instructor()
            elif choice == "8":
                Course.add_course()
            elif choice == "9":
                PlatformAdmin.delete_course()
            elif choice == "10":  
                PlatformAdmin.add_subject_to_course()
            elif choice == "11":
                print("\nLogging out of Admin Dashboard...\n")
                break
            else:
                print("\nInvalid choice. Please try again.\n")
  
    def student_dashboard(student):
        while True:
            print(f"\n--- {student['name']}'s Dashboard ---")
            print("1. Enroll in a Course")
            print("2. View Enrolled Courses")
            print("3. View Assignment")
            print("4. Submit Assignment")
            print("5. View Assignmnent Score")
            print("6. Attendance")
            print("7. View Final grade")
            print("8. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                PlatformAdmin.enroll_in_course(student)
            elif choice == "2":
                Schedule.view_enrolled_courses(student)
            elif choice == "3":
                Student.view_assignments(student)
            elif choice == "4":
                Student.submit_assignment(student)
            elif choice == "5":
                Assignment.view_assignment_score(student)
            elif choice == "6":
                Attendance.mark_attendance(student)
            elif choice == "7":
                Grade.view_final_grade(student)
            elif choice == "8":
                print("\nLogging out of Student Dashboard...\n")
                break
            else:
                print("\nInvalid choice. Please try again.\n")
      
    def instructor_dashboard(instructor):
        while True:
            print(f"\n--- {instructor['name']}'s Dashboard ---")
            print("1. View Assigned Courses and Subjects")
            print("2. Assign Assignment")
            print("3. View submitted assignment")
            print("4. View Attendance")
            print("5. Final Grade")
            print("6. Logout")
            choice = input("Choose an option: ")

            if choice == "1":
                PlatformAdmin.view_assigned_courses_and_subjects(instructor)
            elif choice == "2":
                Instructor.assign_assignment(instructor)
            elif choice =="3":
                Instructor.view_submitted_assignments(instructor)
            elif choice == "4":
                Attendance.view_attendance(instructor)
            elif choice == "5":
                Grade.assign_final_grades(instructor)
            elif choice == "6":
                print("\nLogging out of Instructor Dashboard...\n")
                break
            else:
                print("\nInvalid choice. Please try again.\n")
    
            
      
            
           

# Interactive Main Menu
def main_menu():
    while True:
        print(Person.x)
        print(Person.y)
        print("\n--- Welcome to the E-Learning Platform ---")
        print("1. Student Sign-Up")
        print("2. Instructor Sign-Up")
        print("3. Admin Sign-Up")
        print("4. Student Login")
        print("5. Instructor Login")
        print("6. Admin Login")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            Login.signup("student")
        elif choice == "2":
            Login.signup("instructor")
        elif choice == "3":
            Login.signup("admin")
        elif choice == "4":  # Student Login
            student = Login.login("student")
            if student:  # Only proceed if login is successful
                Info.student_dashboard(student)
        elif choice == "5":
            Login.login("instructor")
        elif choice == "6":
            Login.login("admin")
        elif choice == "7":
            print("\nThank you for using the platform. Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main_menu()

    