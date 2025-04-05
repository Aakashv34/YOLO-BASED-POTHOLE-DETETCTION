
# # Create your views here.
from django.shortcuts import render
from .forms import DetectionForm
from django.conf import settings
from .models import DetectionHistory
from .yolo_integration import detect_pothole  
import os
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



from django.contrib.auth.models import User
from django.contrib import messages

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'signup.html')

        # Create user
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('defi')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.decorators import login_required

def upload_image(request):
    if request.method == 'POST':
        form = DetectionForm(request.POST, request.FILES)
        if form.is_valid():
            detection = form.save(commit=False)
            uploaded_file = request.FILES['image']

            # Save the uploaded image
            image_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(image_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Perform pothole detection
            output_dir = os.path.join(settings.MEDIA_ROOT, 'detections')  
            marked_image_folder, box_count, average_confidence  = detect_pothole(image_path, output_dir) 

            # Get all folders starting with 'detection_results'
            folders = [folder for folder in os.listdir(output_dir) if folder.startswith('detection_results_orginal1')]

            # Find the latest folder
            latest_folder = max(folders, key=lambda f: int(''.join(filter(str.isdigit, f))))

            # Construct the path to the marked image in the latest folder
            marked_image_path = os.path.join(output_dir, latest_folder, os.path.basename(uploaded_file.name))
            
            # Check if the marked image exists
            if os.path.exists(marked_image_path):
                relative_marked_image_path = os.path.relpath(marked_image_path, settings.MEDIA_ROOT).replace("\\", "/")
            else:
                relative_marked_image_path = None

            # Save the detection details
            detection.image = uploaded_file
            detection.result = "Pothole Detected" if box_count > 0 else "No Potholes Detected"
            detection.confidence = average_confidence * 100  
            detection.user = request.user
            detection.save()

            return render(request, 'detection/success.html', {
                'detection': detection,
                'detection_image': f"{settings.MEDIA_URL}{relative_marked_image_path}",
                'box_count': box_count,  
                'confidence': average_confidence * 100   
            })

    else:
        form = DetectionForm()
    return render(request, 'detection/upload.html', {'form': form})


# def detection_history(request):
#     history = DetectionHistory.objects.all().order_by('-detected_at')  # Retrieve all detections, latest first
#     return render(request, 'detection/history.html', {'history': history})

@login_required
def save_detection_history(request, detection_result, uploaded_image):
    # Save detection history for the logged-in user
    history = DetectionHistory.objects.create(
        user=request.user,
        image=uploaded_image,
        detection_result=detection_result
    )
    history.save()
    return redirect('history')  

@login_required
def detection_history(request):
    
    user_history = DetectionHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'history': user_history})



def user_logout(request):
    logout(request)  # Terminate the user session
    return redirect('login')  # Redirect to the login page


@login_required
def defination(request):
    context = {
        'definition': "A pothole is a depression or hole in a road surface caused by wear, weather conditions, and the gradual breakdown of materials, often leading to unsafe driving conditions."
    }
    return render(request, 'defination.html', context)



