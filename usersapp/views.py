from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from .tokens import generate_token
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            subject = "Welcome to My Django-Blog"
            message = "Hello "+user.first_name+"!! \n"+"\nThank you for visiting My Django Blog \n we have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Have a nice day."
            from_email = settings.EMAIL_HOST_USER
            to_list = (user.email,)
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            # Confirmation Email
            current_site=get_current_site(request)
            email_subject="Confirm your email - Django Blog Login!!"
            message2=render_to_string('email_confirmation.html',{
                'name':user.first_name,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.fail_silently = True
            email.send()
            messages.success(request,"please check your email to activate your account.")
            return redirect("home")     
    else:
        form = RegisterForm()
    return render(request,"register.html",{"form":form})


def signin(request):
    if request.user.is_authenticated:
        return redirect("home")
    error=None  
    if request.method =="POST":
            username=request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username,password=password)
            if user is None:
                error="Please enter a correct username and password."
            elif user.is_active is False:
                error="please check your email to activate your account."    
            else:
                login(request,user)
                messages.success(request,f"Hi {user.first_name} {user.last_name}")
                return redirect("home")          
    form=AuthenticationForm()
    return render(request,"login.html",{"form":form,"error":error})    

        
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")    

def activate(request,uidb64,token):
    try:
        usermodel = get_user_model()
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = usermodel.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,usermodel.DoesNotExist):
        user=None
    if user is not None and generate_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        messages.success(request,f"Hi {user.first_name} {user.last_name}")
        return redirect("home")          
    else:
        return render(request,"activation_failed.html")
