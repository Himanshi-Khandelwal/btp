from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
import subprocess
import socket
# Create your views here.


def base(request):
    return render_to_response('base.html')


def choose(request):
    return render_to_response('choose.html')


def input_file(request, fh, code):
    fh.write(str(code))
    fh.close()
    user_input = request.GET.get('user_input')
    fh = open('input.txt', 'w')
    fh.write(str(user_input))
    fh.close()


def code_platform(request):
    if(request.GET.get('codec')):
        code = request.GET.get('codec')
        fh = open('code.c', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo gcc code.c")
        if status[0] == 0:
            a = subprocess.getstatusoutput("./a.out < input.txt ")
            return render(request, 'show.html', {'output': a[1]})
        else:
            b = status[1]
        #    print(type(b))
            a = b.replace('code.c:', '')
            return render(request, 'show.html', {'output': a})

    elif(request.GET.get('codecpp')):
        code = request.GET.get('codecpp')
        fh = open('code.cpp', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo g++ code.cpp")
        if status[0] == 0:
            a = subprocess.getstatusoutput("./a.out < input.txt ")
            return render(request, 'show.html', {'output': a[1]})
        else:
            b = status[1]
            a = b.replace('code.cpp:', '')
            return render(request, 'show.html', {'output': a})

    elif(request.GET.get('codejava')):
        code = request.GET.get('codejava')
        fh = open('code.java', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo javac code.java")
        if status[0] == 0:
            a = subprocess.getstatusoutput("sudo java code < input.txt ")
            return render(request, 'show.html', {'output': a[1]})
        else:
            b = status[1]
        #    print(type(b))
            a = b.replace('code.java:', '')
            return render(request, 'show.html', {'output': a})

    elif(request.GET.get('codeperl')):
        code = request.GET.get('codeperl')
        fh = open('code.pl', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo perl code.pl < input.txt")
        if status[0] == 0:
            return render(request, 'show.html', {'output': status[1]})
        else:
            print ("<h4>Error:</h4>")
        #    b=status[1].split("code.pl")
            b = status[1]
        #    print(type(b))
            a = b.replace('code.pl', '')

            return render(request, 'show.html', {'output': a})

    elif(request.GET.get('codepython')):
        code = request.GET.get('codepython')
        fh = open('code.py', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo python code.py < input.txt")
        if status[0] == 0:
            return render(request, 'show.html', {'output': status[1]})
        else:
            print ("<h4>Error:</h4>")
        #    b=status[1].split("code.py")
            b = status[1]
        #    print(type(b))
            a = b.replace('File "code.py", ','')

            return render(request, 'show.html', {'output': a})

    elif(request.GET.get('codescala')):
        code = request.GET.get('codescala')
        fh = open('code.scala', 'w')
        input_file(request, fh, code)
        status = subprocess.getstatusoutput("sudo scalac code.scala")
        if status[0] == 0:
            a = subprocess.getstatusoutput("sudo scala code < input.txt ")
            return render(request, 'show.html', {'output': a[1]})
        else:
            b = status[1]
            print(type(b))
            a = b.replace('code.scala:','')
            return render(request, 'show.html', {'output': a})

    return render_to_response('code_platform.html')


def docker_list(request):
    z = 1
    k = {}
    for i in subprocess.getoutput("docker images").split('\n'):
        if z == 1:
            z = z+1
            pass
        else:
            j = i.split()
            k[j[0]] = j[1]
    return render(request, 'images.html', {'docker_img': k})


def docker_launch(request):
    imageName = request.GET.get('imagename')
    cName = request.GET.get('cname')
    if subprocess.getstatusoutput("docker inspect {0}".format(cName))[0] == 0:
        resp = 0
    else:
        subprocess.getoutput("docker run  -dit --name {0}  {1}".format(cName, imageName))
        resp = 1
    context = {
            'response': resp,
            'image': imageName,
            'container': cName
    }
    return render(request, 'img-cont.html', context)


def docker_manage(request):
    z = 1
    m = []
    c = []
    d = []
    for i in subprocess.getoutput("docker ps -a").split('\n'):
        if z == 1:
            z = z+1
            pass
        else:
            j = i.split()
            cStatus = subprocess.getoutput("docker inspect {} | jq '.[].State.Status'".format(j[-1]))
            c.append(j[-1])
            d.append(j[1])
            m.append(cStatus)
    return render(request, 'dock_manage.html', {'val': zip(c, d, m)})


def docker_start(request, mycname=None):
    cstartstatus = subprocess.getstatusoutput("docker start {}".format(mycname))
    return redirect('dock-manage')


def docker_remove(request, mycname=None):
    cremovestatus = subprocess.getstatusoutput("docker rm -f {}".format(mycname))
    return redirect('dock-manage')


def docker_stop(request, mycname=None):
    cstopstatus = subprocess.getstatusoutput("docker stop {}".format(mycname))
    return redirect('dock-manage')


def docker_shell(request):
    #ipStatus=subprocess.getoutput("docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(mycname))
    cstartstatus = subprocess.getstatusoutput("docker run -it -p 4200:4200 -e  SIAB_PASSWORD=guest -e SIAB_SUDO=true sspreitzer/shellinabox")

#    shellInstall=subprocess.getstatusoutput("docker exec {0} yum install shellinabox".format(mycname))
#    if shellInstall[0] == 0:
#        subprocess.getoutput("/usr/sbin/shellinaboxd")
#        subprocess.getoutput("https://{0}:4200".format(ipStatus))
#    else:
#        print "Try Again"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return redirect('https://{0}:4200'.format(local_ip_address))


def show_output(request):
    return render_to_response('show.html')


def signup(request):
    print(request.method)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
           # form.save()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
           # username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password2')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            return redirect('base')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('choose')
    return render(request, "login.html", {"form": form})


def logout_view(request):
    django_logout(request)
    return redirect("/")

def terminal(request):
    return render_to_response('terminal.html')
