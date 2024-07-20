from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
from .forms import CreateRecordForm,UpdateRecordForm
from django.contrib import messages
# Create your views here.

def home(request):
   return render(request,'index.html')

#----------Register ----------------------#
def register(request):
   form=CreateUserForm()
   if request.method=="POST":
      form=CreateUserForm(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,"Account created successfully !")
         return redirect('my_login')

   context = {'form':form} 
   return render(request,'register.html',context=context)     


#--------------Login User -------------------------------

def my_login(request):
   form=LoginForm()
   if request.method=="POST":
      form=LoginForm(request,data=request.POST)
      if form.is_valid():
         username = request.POST.get('username')
         password = request.POST.get('password')

         user=authenticate(request,username=username,password=password)
         if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
   context={'form':form}
   return render(request,'my_login.html',context=context)         

def user_logout(request):
   auth.logout(request)
   return redirect('my_login')

@login_required(login_url='my_login')
def dashboard(request):
   my_records = Record.objects.all()
   context = {'records':my_records}

   return render(request,'dashboard.html',context=context)


#--------view for create record -------------------------
@login_required(login_url='my_login')
def create_record(request):
   form = CreateRecordForm()
   if request.method == 'POST':
      form = CreateRecordForm(request.POST)
      if form.is_valid():
         form.save()
         messages.success(request,"Record Created successfully !")
         return redirect('dashboard')
   context = {'form':form}
   return render(request,'create_record.html',context=context)   

#--------Update record -------------------------
@login_required(login_url='my_login')
def update_record(request,pk):
   record = Record.objects.get(id=pk)
   form = UpdateRecordForm(instance=record)
   if request.method == 'POST':
      form = UpdateRecordForm(request.POST,instance=record)
      if form.is_valid():
         form.save()
         return redirect('dashboard')
   context = {'form':form}
   return render(request,'update_record.html',context=context)   

#--------view a  record -------------------------
@login_required(login_url='my_login')
def singular_record(request,pk):
   all_record = Record.objects.get(id=pk)
   
   context = {'record':all_record}
   return render(request,'view_record.html',context=context)   

#----------------Delete a Record -----------------------------

@login_required(login_url='my_login')
def delete_record(request,pk):
   record = Record.objects.get(id=pk)
   record.delete()
   messages.success(request,"Record deleted successfully !")
   return redirect('dashboard')