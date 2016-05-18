from django.shortcuts import render
from kaizing.models import Feedback

def home(request):
    if request.POST:
        feedback = Feedback()
        feedback.name = request.POST['feedback_name']
        print feedback.name
        feedback.phone = request.POST['feedback_phone']
        feedback.email = request.POST['feedback_email']
        feedback.message = request.POST['feedback']
        feedback.save()
    return render(request,'kaizing/mainpage.html')