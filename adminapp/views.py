from django.shortcuts import*
from django.contrib.auth import*
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Avg, Count


def Login(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1 = request.POST['password']
        user = authenticate(request, username=username1, password=password1)

        if user is not None:
            login(request, user)

            # Check if user is a superuser
            if user.is_superuser:
                return redirect('dashboard')  # Redirect to superuser dashboard

            # Check if user is a student
            elif user.is_stud:
                return redirect('studdashboard')  # Redirect to student dashboard

            # Check if user is faculty
            elif user.is_fac:
                return redirect('staffdashboard')  # Redirect to faculty dashboard

        else:
            messages.error(request,"Invalid username / password")
            return redirect('Login')

    else:
        return render(request, "login.html")

@login_required()  
def dashboard(request):
    staff_count = User.objects.filter(is_fac=True).count()
    stud_count = User.objects.filter(is_stud=True).count()
    current_page = 'dashboard'
    context = {
        'current_page': current_page,
        'staff_count':staff_count,
        'stud_count':stud_count
    }
    return render(request, 'admin_app/pages/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('Login')



def Addstaff(request):
    if request.method == 'POST':
        # Retrieve data from the form
        fac_id = request.POST['fac_id']
        name = request.POST['name']
        password = request.POST['password']
        dob = request.POST['dob']
        place = request.POST['place']
        address = request.POST['address']
        email = request.POST['email']
        phnnum = request.POST['phoneno']
        photo = request.FILES['photo']

        # Check if fac_id already exists
        if User.objects.filter(id=fac_id).exists():
            messages.error(request, "The faculty ID is already taken.")
        else:
            try:
                # Create a new user/staff record
                User.objects.create_user(
                    id=fac_id,
                    username=name,
                    password=password,
                    dob=dob,
                    place=place,
                    address=address,
                    phone_number=phnnum,
                    email=email,
                    image=photo,
                    is_fac=True
                )
                messages.success(request, f"Staff member added successfully!")
                return redirect('dashboard')  # Adjust the redirection as needed
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'admin_app/pages/Addstaff.html')


def staffdashboard(request):
    current_page = 'staffdashboard'
    current_user = request.user
    context = {
        'current_page': current_page,
        'current_user': current_user
    }
    return render(request, 'admin_app/pages/staffdashboard.html', context)

def add_stud(request):
    if request.method == 'POST':
        studid = request.POST.get('studid')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST['password']
        dob = request.POST.get('dob')
        place = request.POST.get('place')
        photo = request.FILES.get('photo')
        phoneno = request.POST.get('phoneno')
        address = request.POST.get('address')
        name = request.POST.get('username')
        sem = request.POST['semester']
        
        # Check if studid already exists
        if User.objects.filter(id=studid).exists():
            messages.error(request, "The student ID is already taken.")
        else:
            try:
                User.objects.create_user(
                    id=studid,
                    username=name,
                    last_name=lname,  
                    email=email,
                    password=password,
                    dob=dob,
                    place=place,
                    image=photo,
                    phone_number=phoneno,
                    address=address, 
                    first_name=fname,
                    semester=sem,
                    is_stud=True
                )
                messages.success(request, f"Student member added successfully!")
                return redirect('dashboard')  # Adjust the redirection as needed
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'admin_app/pages/Addstud.html')



  
def staff_list(request):
    current_page = 'stafflist'
    facultys = User.objects.filter(is_fac=True)
    context = {
        'current_page': current_page,
        'facultys': facultys
        }
    return render(request, 'admin_app/pages/stafflist.html', context)

def stud_list(request):
    current_page = 'studlist'
    students = User.objects.filter(is_stud=True)
    context = {
        'current_page': current_page,
        'students': students
        }
    return render(request, 'admin_app/pages/studlist.html', context)



def edit_staff(request, faculty_id):
    faculty = get_object_or_404(User, id=faculty_id)  
    if request.method == "POST":
        faculty.id = request.POST.get('fac_id')
        faculty.username = request.POST.get('name')
        faculty.dob = request.POST.get('dob')
        faculty.place = request.POST.get('place')
        faculty.address = request.POST.get('address')
        faculty.email = request.POST.get('email')
        faculty.phone_number = request.POST.get('phoneno')
        if 'photo' in request.FILES:
            faculty.image = request.FILES['photo']

        faculty.save()
        return redirect('stafflist')  # Replace 'staff_list' with your desired redirect view

    return render(request, 'admin_app/pages/editstaff.html', {'faculty': faculty})

def faculty_delete(request, faculty_id):
    # Fetch the faculty instance
    faculty = get_object_or_404(User, id=faculty_id)

    try:
        # Attempt to delete the faculty
        faculty.delete()
        messages.success(request, 'Faculty deleted successfully.')
    except Exception as e:
        # Handle deletion errors
        messages.error(request, f'Error deleting faculty: {e}')
    
    # Redirect to the faculty list page
    return redirect('stafflist')  # Replace with the actual name of your faculty list view

def stud_delete(request, stud_id):
    student = get_object_or_404(User, id=stud_id)

    try:

        student.delete()
        messages.success(request, 'student deleted successfully.')
    except Exception as e:
        # Handle deletion errors
        messages.error(request, f'Error deleting student: {e}')
    
    # Redirect to the faculty list page
    return redirect('studlist') 

def studdashboard(request):
    current_page = 'studdashboard'
    current_user = request.user
    context = {
        'current_page': current_page,
        'student': current_user
    }
    return render(request, 'admin_app/pages/studentdashboard.html', context)

def addtimetable(request):
      if request.method == 'POST':
        photo = request.FILES.get('photo')
        semester = request.POST.get('semester')
        try:
            Timetable.objects.create(
                sem=semester,
                file=photo,
            
            )
            messages.success(request, f"timetable added successfully!")
            return redirect('dashboard')  # Adjust the redirection as needed
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

      return render(request,'admin_app/pages/Addtimetable.html')

def timetable_view(request):
    current_page = 'timetableview'
    try:
        timetables  = Timetable.objects.all()
    except Timetable.DoesNotExist:
        messages.error(request, 'timetable not found')
        return redirect('dashboard')
    context = {
        'current_page': current_page,
        'timetables':timetables
    }
    return render(request, 'admin_app/pages/viewtimetable.html', context)


def timetablestaff_view(request):
    current_page = 'timetablestaff'
    try:
        timetables  = Timetable.objects.all()
    except Timetable.DoesNotExist:
        messages.error(request, 'timetable not found')
        return redirect('staffdashboard')
    context = {
        'current_page': current_page,
        'timetables':timetables
    }
    return render(request, 'admin_app/pages/viewtimetablestaff.html', context)

def update_student(request, student_id):
    # Get the student object or return a 404 if not found
    student = get_object_or_404(User, id=student_id)

    if request.method == "POST":
        # Update the student object with form data
        student.username = request.POST.get('username')
        student.first_name = request.POST.get('firstname')
        student.last_name = request.POST.get('lastname')
        student.email = request.POST.get('email')
        student.dob = request.POST.get('dob')
        student.place = request.POST.get('place')
        student.phone_number = request.POST.get('phoneno')
        student.semester = request.POST.get('semester')
        student.address = request.POST.get('address')

        # Check if a new photo is uploaded
        if request.FILES.get('photo'):
            student.image = request.FILES['photo']


        # Save changes to the database
        student.save()

        messages.success(request, "Student details updated successfully!")
        return redirect('studlist')  # Replace with the name of your redirect URL

    return render(request, 'admin_app/pages/editstud.html', {'student': student})

def addnotification(request):
      if request.method == 'POST':
        description = request.POST.get('notification')
        try:
            Notifications.objects.create(
                description=description )
            messages.success(request, f"Notifications added successfully!")
            return redirect('dashboard')  # Adjust the redirection as needed
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

      return render(request,'admin_app/pages/Addnotification.html')

def view_notifications(request):
    # Fetch all notifications from the database
    current_page = 'viewnotifications'
    notifications = Notifications.objects.all()
    context = {
        'current_page': current_page,
        "notifications": notifications
    }
    
    return render(request, "admin_app/pages/viewnotification.html",context)


def view_notificationsstud(request):
    # Fetch all notifications from the database
    current_page = 'viewnotificationsstud'
    notifications = Notifications.objects.all()
    context = {
        'current_page': current_page,
        "notifications": notifications
    }
    
    return render(request, "admin_app/pages/viewnotificationstud.html",context)



def timetablestud_view(request):
    current_page = 'timetablestud'
    try:
        # Ensure the user has a 'semester' field in their profile
        user_semester = request.user.semester  # Assuming 'semester' exists in the User model or profile
        
        # Filter timetables where 'sem' matches the user's semester
        timetables = Timetable.objects.filter(sem=user_semester)
        
        if not timetables.exists():  # If no matching timetables are found
            messages.warning(request, f"No timetable found for Semester: {user_semester}")
            return redirect('studdashboard')

    except AttributeError:
        messages.error(request, "User does not have a semester field.")
        return redirect('studdashboard')

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('studdashboard')

    context = {
        'current_page': current_page,
        'timetables': timetables
    }
    return render(request, 'admin_app/pages/viewtimetablestud.html', context)



def edit_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)  # Get the timetable instance
    
    if request.method == 'POST':
        # Retrieve form data
        photo = request.FILES.get('photo')
        semester = request.POST.get('semester')

        try:
            # Update fields if provided
            if photo:
                timetable.file = photo
            if semester:
                timetable.sem = semester

            timetable.save()  # Save the updated instance
            messages.success(request, "Timetable updated successfully!")
            return redirect('timetableview')  # Redirect to timetable listing page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    context = {
        'timetable': timetable
    }
    return render(request, 'admin_app/pages/edittimetable.html', context)

def delete_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)  # Get the timetable instance
    try:
        timetable.delete()  # Delete the instance
        messages.success(request, "Timetable deleted successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('timetableview') 


def add_result(request):
    current_page='addresult'
    if request.method == "POST":
        student_id = request.POST.get("student")
        registration_number = request.POST.get("registration_number")
        name = request.POST.get("name")
        programme = request.POST.get("programme", "Master of Computer Applications")
        semester = request.POST.get("semester")
        college = request.POST.get("college")
        course_code = request.POST.get("course_code")
        course_title = request.POST.get("course_title")
        max_mark = request.POST.get("max_mark")
        ca_marks = request.POST.get("ca_marks")
        ese_marks = request.POST.get("ese_marks")
        total_marks = request.POST.get("total_marks")
        grade_sub = request.POST.get("grade_sub")
        result = request.POST.get("result")

        # Ensure the selected student exists
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            messages.error(request, "Selected student does not exist.")
            return redirect("addresult")

        # Create and save the result instance
        result_instance = StudentResult(
            student=student,
            registration_number=registration_number,
            name=name,
            programme=programme,
            semester=semester,
            college=college,
            course_code=course_code,
            course_title=course_title,
            max_mark=max_mark,
            ca_marks=ca_marks,
            ese_marks=ese_marks,
            total_marks=total_marks,
            grade_sub=grade_sub,
            result=result,
        )
        result_instance.save()
        messages.success(request, "Result added successfully!")
        return redirect("addresult")

    # For GET requests, display the form
    users = User.objects.filter(is_stud=True)  # Assuming all users are valid students
    context = {"users": users,'current_page':current_page}
    return render(request, "admin_app/pages/Addresult.html", context)

def view_results(request):
    current_page='viewresult'
    student_id = request.user.id  # Assuming the user is authenticated and `request.user` gives the current user

    try:
        student = User.objects.get(id=student_id)
    except User.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect("studdashboard")

    # Fetch all results for the current student
    results = StudentResult.objects.filter(student=student)

    if not results.exists():
        messages.info(request, "No results found for the selected student.")
        return redirect("studdashboard")
    total_max_marks = sum(result.max_mark for result in results)
    total_ca_marks = sum(result.ca_marks for result in results)
    total_ese_marks = sum(result.ese_marks for result in results)
    total_total_marks = sum(result.total_marks for result in results)
    overall_grade = calculate_overall_grade(results)  # Function to determine overall grade
    
    # Determine the overall status
    overall_status = "Passed" if all(result.result == "P" for result in results) else "Failed"
    

    context = {
        "student": student,
        "results": results,
        "overall_status": overall_status,
        'current_page':current_page,
        'total_marks': total_total_marks,
        'total_courses': results.count(),
        'total_max_marks': total_max_marks,
        'total_ca_marks': total_ca_marks,
        'total_ese_marks': total_ese_marks,
        'total_total_marks': total_total_marks,
        'overall_grade': overall_grade,
    }

    return render(request, "admin_app/pages/viewresultstud.html", context)
def calculate_overall_grade(results):
    # Calculate total obtained marks and total maximum marks
    total_obtained_marks = sum(result.total_marks for result in results)
    total_maximum_marks = sum(result.max_mark for result in results)

    # Avoid division by zero
    if total_maximum_marks == 0:
        return "N/A"

    # Calculate percentage
    percentage = (total_obtained_marks / total_maximum_marks) * 100

    # Determine grade based on percentage
    if percentage >= 90:
        return "O"  # Outstanding
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"  # Fail



def view_all_results(request):
    current_page='allresults'
    results =StudentResult.objects.all() # Use select_related if you have a ForeignKey to optimize queries
    return render(request, "admin_app/pages/manageresult.html", {"results": results,'current_page':current_page})


def edit_result(request, result_id):
    # Fetch the result object using the provided ID
    result = get_object_or_404(StudentResult, id=result_id)

    if request.method == "POST":
        # Update the result object with the data from the form
        result.student_id = request.POST.get("student")
        result.registration_number = request.POST.get("registration_number")
        result.name = request.POST.get("name")
        result.semester = request.POST.get("semester")
        result.college = request.POST.get("college")
        result.course_code = request.POST.get("course_code")
        result.course_title = request.POST.get("course_title")
        result.max_mark = request.POST.get("max_mark")
        result.ca_marks = request.POST.get("ca_marks")
        result.ese_marks = request.POST.get("ese_marks")
        result.total_marks = request.POST.get("total_marks")
        result.grade_sub = request.POST.get("grade_sub")
        result.result = request.POST.get("result")

        # Save the updated result to the database
        result.save()

        # Add a success message and redirect to a results list or detail page
        messages.success(request, "Result updated successfully!")
        return redirect("allresults")  # Change `results_list` to your desired redirect view name

    # Fetch all users to populate the student dropdown
    users = User.objects.all()

    # Render the edit result template with the existing result data
    return render(request, "admin_app/pages/resultedit.html", {"result": result, "users": users})

def delete_result(request, result_id):
    if request.method == "POST":
        result = get_object_or_404(StudentResult, id=result_id)
        result.delete()
        messages.success(request, "Result has been deleted successfully.")
        return redirect("allresults")  # Redirect to the view showing all results
    else:
        messages.error(request, "Invalid request method.")
        return redirect("allresults")

