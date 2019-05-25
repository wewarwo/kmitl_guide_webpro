from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from map.forms import SignUpForm
from map.models import location, comment, contact, question


# Create your views here.
def index(request):
    location_list = location.objects.all()
    comment_list = comment.objects.all()
    location_type = ('Faculty', 'Coffee', 'Food', 'ATM', 'Parking', 'Shop', 'Bank', 'Other')
    context = {
        'page_title': 'KMITL GUIDE',
        'selected_type': location_type,
        'location_list': location_list,
        'comment_list': comment_list,
        'location_type': location_type,
        'map_center': '{lat: 13.7284118, lng: 100.7761338}',
        'zoom': 17,
        'nfound': 0,
        'logerr': 0
    }
    if request.method == 'GET':
        context['nfound'] = 3
        try:
            for i in location_list:
                if request.GET['search_name'] in i.location_name:
                    context['map_center'] = i.coordinate
                    context['zoom'] = 23
                    context['nfound'] = 0
                    break
        except MultiValueDictKeyError:
            context['nfound'] = 0
    return render(request, template_name='map/index.html', context=context)


def my_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('index')





def my_logout(request):
    logout(request)
    return redirect('index')


def add_comment(request):
    com1 = comment.objects.create(
        location_id=int(request.GET['locid']),
        user_id=request.user.id,
        user_name=request.user.username,
        content=request.GET['com1'],
        create_date=now()
    )

    return redirect('index')


def add_location(request):
    # print(request.GET)
    # print(request.GET['locname'])
    # print(request.GET['loccoor'].split()[0].strip("(").strip(","))
    # print(request.GET['loccoor'].split()[1].strip(")"))
    lat, lng = request.GET['loccoor'].split()[0].strip("(").strip(","), request.GET['loccoor'].split()[1].strip(")")
    print(lat, lng)
    coord = "{lat: " + lat + ",lng: " + lng + "}"
    print(coord)
    loc1 = location.objects.create(
        location_name=request.GET['locname'],
        coordinate=coord,
        descript=request.GET['loccon'],
        location_type=request.GET['loctype'],
        img_path="n",
        zone_id=1,
    )

    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            quest1 = question.objects.create(
                user_id=User.objects.get(username=form.cleaned_data.get('username')).id,
                question=form.cleaned_data.get('question'),
                answer=form.cleaned_data.get('answer'),
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'map/register.html', {'form': form})


@permission_required('location.can_delete')
def delete(request):
    if request.method == 'GET':
        location.objects.filter(id=request.GET['locid2']).delete()
    return redirect('index');


def home(request):
    context = {}
    return render(request, template_name='map/home.html', context=context)


def reset(request):
    # print(request)
    alert_nof = 0
    setans = 0
    setpwd = 0
    question1 = ""
    answer1 = ""
    username1 = ""
    alert_text = ""
    # print(User.objects.get(username='leo'))
    # print (request.POST.get('BUT'))
    if request.method == 'POST':
        if request.POST.get('BUT') == 'req':
            username = request.POST.get('username')
            try:
                user1 = User.objects.get(username=username)
                if user1.is_superuser:
                    alert_nof = 1
                    alert_text = "Admin account can not reset password"
                else:
                    username1 = user1.username
                    question1 = question.objects.get(user_id=user1.id).question
                    setans = 1

            except User.DoesNotExist:
                alert_nof = 1
                alert_text = "Username is not exist."

        if request.POST.get('BUT') == 'ans':
            username = request.POST.get('username')
            answer = request.POST.get('ans')
            try:
                user1 = User.objects.get(username=username)
                if question.objects.get(user_id=user1.id).answer != answer:
                    alert_nof = 1
                    alert_text = "Incorrect answer"
                    username1 = user1.username
                    question1 = question.objects.get(user_id=user1.id).question
                else:
                    username1 = user1.username
                    setans = 0;
                    setpwd = 1;

            except User.DoesNotExist:
                alert_nof = 1
                alert_text = "Username is not exist."

        if request.POST.get('BUT') == 'setpwd':
            username = request.POST.get('username')
            pwd1 = request.POST.get('npass1')
            pwd2 = request.POST.get('npass2')
            try:
                user1 = User.objects.get(username=username)
                print(pwd1, '===', pwd2)
                if pwd1 != pwd2:
                    alert_nof = 1
                    alert_text = "Passwords is not matched"
                    username1 = user1.username
                    setpwd = 1
                else:
                    user1.set_password(pwd1)
                    user1.save()
                    user1 = authenticate(request, username=username, password=pwd1)
                    login(request, user1)
                    return redirect('index')
                    # alert_nof = 1
                    # alert_text = "Passwords is matched"
                    # username1 = user1.username

            except User.DoesNotExist:
                alert_nof = 1
                alert_text = "Username is not exist."
    context = {
        'username1': username1,
        'alertnof': alert_nof,
        'alert_text': alert_text,
        'setans': setans,
        'setpwd': setpwd,
        'question': question1,
        'answer': answer1
    }

    return render(request, template_name='map/reset.html', context=context)


def filtered(request):
    lis = request.GET.getlist('filter_item')
    print(lis)
    print("\n", lis, "\n")
    # return redirect('index')
    location_list = location.objects.all()
    comment_list = comment.objects.all()
    location_type = ('Faculty', 'Coffee', 'Food', 'ATM', 'Parking', 'Shop', 'Bank', 'Other')
    context = {
        'page_title': 'KMITL GUIDE',
        'selected_type': lis,
        'location_list': location_list,
        'comment_list': comment_list,
        'location_type': location_type,
        'map_center': '{lat: 13.7284118, lng: 100.7761338}',
        'zoom': 17,
        'nfound': 0,
        'logerr': 0
    }
    if request.method == 'GET':
        context['nfound'] = 3
        try:
            for i in location_list:
                if request.GET['search_name'] in i.location_name:
                    context['map_center'] = i.coordinate
                    context['zoom'] = 23
                    context['nfound'] = 0
                    break
        except MultiValueDictKeyError:
            context['nfound'] = 0
    return render(request, template_name='map/index.html', context=context)

def contactadmin(request):
    if request.method == 'POST':
        if request.POST.get('subject')and request.POST.get('des'):
            contact1 = contact.objects.create(
                subject= request.POST.get('subject'),
                Description= request.POST.get('des'),
                Subject_type= request.POST.get('stype'),
                Location = request.POST.get('location'),
            )
            print("Added contact")
            return redirect('index')

    location_list = location.objects.order_by('location_name').all()
    context = {'location_list': location_list}
    return render(request, template_name='map/contactad.html', context=context)

def contactListPage(request):
    contact_list = contact.objects.all()
    context = {'contact_list': contact_list}
    return render(request, template_name='map/contact_list.html', context=context)

def deletemsg(request):
    if request.method == 'GET':
        contact.objects.filter(id=request.GET['msg_id']).delete()
    return redirect('contact_page');