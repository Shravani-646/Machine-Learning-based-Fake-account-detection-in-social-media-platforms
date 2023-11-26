from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,FeatureSetForm,CloneFeatureSetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from .ml_model import get_values,predict
from .clone_logic import get_profile_values,get_profiles
from django.contrib import messages
from .forms import UserInputForm
from automation.get_details import get_profile_data
from .interpretation import prediction_explain
# Create your views here.
def home_page(request):
    return render(request,'accounts/home.html')


@login_required(login_url="login")
def get_jupyter_notebook(request):
    return render(request,'accounts/notebook.html')

@login_required(login_url="login")
def get_model_predicted_explanation(request):
    return render(request,'accounts/explanation.html')

def user_registration(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    else:
        if request.method == "GET":
            form = UserRegistrationForm()
            context = {'form':form}
            return render(request,'accounts/signup.html',context)
        if request.method == "POST":
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}!')
                form.save()
                return redirect('login')
            context = {'form':form}
            return render(request,'accounts/signup.html',context)
        

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    else:
        if request.method == "GET":
            form = UserRegistrationForm()
            context = {'form':form}
            return render(request,'accounts/login.html',context)
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user=user)
                return redirect("prediction_form")
            messages.info(request,'Username or password is incorrect please try again')
            return redirect('login')
            

def logout_user(request):
    logout(request)
    return redirect("home-page")


@login_required(login_url="login")
def prediction_form(request):
    if request.method == "GET":
        form = FeatureSetForm()
        context = {'form':form}
        return render(request,'accounts/prediction_form.html',context)
    elif request.method == "POST":
        row_df = []
        row_df.append(get_values(request.POST))
        result = (predict(row_df))[0]
        prediction_explain(row_df[0])
        context = {'result':result}
        return render(request,'accounts/result.html',context)
        
@login_required(login_url="login")
def clone_prediction_form(request):
    if request.method == "GET":
        form = CloneFeatureSetForm()
        context = {'form':form}
        return render(request,'accounts/clone_prediction_form.html',context)
    elif request.method == "POST":
        row_df = get_profile_values(request.POST)
        context = get_profiles(row_df)
        profile_names = {}
        context["data"] = get_profiles(row_df)
        if(len(context)>2):
            context["count"] = (len(context))-2 
            no_of_rows = 0
            if context["count"] % 3 == 0:
                no_of_rows = context["count"] / 3
            else:
                no_of_rows = context["count"] // 3 + 1
            counter = 1
            index = 1
            row_index = 1
            while no_of_rows > 1:
                if(index==no_of_rows and counter==context["count"]):
                    break
                index = index+1
                profile_names["row"+str(row_index)] = ["p"+str(j) for j in range(counter,counter+6)]
                counter = counter+6
                row_index = row_index+1
                no_of_rows = no_of_rows - 2
            if(counter<len(context["data"])):
                remaining_profiles = context["count"] - counter
                profile_names["row"+str(row_index)] = ["p"+str(i) for i in range(counter,counter+remaining_profiles+1)]
                context["profile_names"] = profile_names
        if(len(context)==2):
            context = {'input_from_user':get_profile_values(request.POST),'count':0}
        print(context)
        return render(request,'accounts/clone_or_not.html',context)
    

#api integration
@login_required(login_url="login")
def index(request):
    if request.method == "GET":
        form = UserInputForm()
        context = {'form':form}
        return render(request,'accounts/automation.html',context)
    elif request.method == "POST":
        p_url = request.POST["profile_url"]
        print(p_url)
        data = get_profile_data(profile_url=p_url)
        print(data)
        if len(data[0]) == 8:
            prediction_explain(data[0])
            
            result = (predict(data))[0]
            context = {'result':result}
        else:
            context = {'result':'Could not find the data with this username.'}
        return render(request,'accounts/result.html',context)
        