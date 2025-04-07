import cv2
import joblib
import numpy as np
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render, redirect
from keras.src.saving import load_model

from user.forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import packaging
import requests
# Create your views here.


def index_page(request):
    return render(request, 'users/index.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'users/login.html', context)


def register_page(request):
    if request.method != 'POST':
        form = CustomUserForm()
    else:
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


###
def classify_food(request):
    predicted_class = None  # 預設值，避免未定義錯誤

    if request.method == 'POST' and 'food_image' in request.FILES:
        # Read image file
        food_image = request.FILES['food_image'].read()
        model = load_model('media/ai_model/trained_model2.h5')
        class_indices = joblib.load('media/ai_model/class_indices.joblib')

        # Convert image to OpenCV format
        food_image = cv2.imdecode(np.frombuffer(food_image, np.uint8), cv2.IMREAD_COLOR)
        food_image = cv2.resize(food_image, (221, 221)) / 255.0
        food_image = np.expand_dims(food_image, axis=0)

        # Predict
        predictions = model.predict(food_image)
        predicted_label = np.argmax(predictions)  # This is an integer

        # Get class name from class_indices
        predicted_class = next((key for key, value in class_indices.items() if value == predicted_label), "Unknown")

    return render(request, 'recognition.html', {'result': predicted_class})


def record_page(request):
    return render(request, 'record.html')

#def recongnition(request):
#   return render(request, 'recognition.html')
