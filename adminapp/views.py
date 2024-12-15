from django.shortcuts import*
from django.contrib.auth import*
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


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
            error = "Invalid username / password"
            return HttpResponse(error)

    else:
        return render(request, "login.html")

# @login_required(login_url='/login/')  
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
        phnnum=request.POST['phoneno']
        photo = request.FILES['photo']
        

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
       
        # Redirect to the dashboard or another page
        return redirect('dashboard') 
    else:
        # Render the form page
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
        sem=request.POST['semester']
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
            messages.success(request, f"Stud member {User.username} added successfully!")
            return redirect('dashboard')  # Adjust the redirection as needed
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request,'admin_app/pages/Addstud.html')


  
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