from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import Topic, Webpage, AccessRecord
from first_app.forms import UserForm, UserProfileInfoForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def index(request):
    """
    webpage_list =  AccessRecord.objects.order_by('date')
    date_dict = {'access_records': webpage_list}
    """
    context_dict = {'text':'hello world', 'number':100}
    return render(request, 'first_app/test.html', context = context_dict)


def form_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)

        if form.is_valid():
            print("VALIDAION SUCCESS")
            print(form.cleaned_data['name'])
            print(form.cleaned_data['text'])

    return render(request, 'first_app/form_page.html',{'form': form} )


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice")


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered=True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})



def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("your Account isn't active")

        else:
            print("Someone tried to login")
            return HttpResponse("invalid Login Details Supplied")

    else:
        return render(request, 'first_app/login.html',{})
