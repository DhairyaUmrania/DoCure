from multiprocessing import context
from site import USER_BASE
from tkinter.tix import Form
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from matplotlib.pyplot import rcdefaults
from numpy import delete
from DoCure.settings import EMAIL_HOST_USER

from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail

from .forms  import NewUserForm,DoctorForm,ConfirmForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.decorators import login_required

import re
# import requests
import pdfplumber
import pandas as pd
import pytesseract
from PIL import Image
from django.contrib.auth.hashers import make_password



# Create your views here.
from .models import *


def home(request):
	name=request.user.username or None
	return render(request,'HtmlFiles/home.html',{'name':name})

def homebefore(request):
            return render(request,'HtmlFiles/homebefore.html')

def Doctorhome(request):
            name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
            return render(request,'HtmlFiles/Doctorhome.html',{'name':name})

def viewDoctor(request):
    context={}
    
    name=request.user.username or None
    user=request.user
    d1 = ConfirmDoctor.objects.exclude(viewdoctor__user = user)
    print(d1)

    
    return render(request,'accounts/viewDoctor.html',context={'name':name,'d1':d1})

def Doctorregister(request):
        if request.method == "POST":
            form = DoctorForm(request.POST)
            if form.is_valid():
                # password = make_password(request.data['password'])
                subject = 'Welcome to Docure'
                message = 'You have Successfully Signed up into our WebApp You can go and Login to our App'
                recepient = str(form['email'].value())
                send_mail(subject, message, EMAIL_HOST_USER,
                              [recepient], fail_silently=False)
                form.save()
                # login(request, user)
                messages.success(request, "Registration successful." )
            
                return redirect("Doctorlogin")

            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = DoctorForm()
        return render(request,context={'register_form':form} ,template_name='HtmlFiles/Doctorregister.html')
def about(request):
	return render(request,'HtmlFiles/about.html')

def confirmForm(request):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():  
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
    return render(request, 'HtmlFiles/home.html')




def registerPage(request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                        subject = 'Welcome to Docure'
                        message = 'You have Successfully Signed up into our WebApp You can go and Login to our App '
                        recepient = str(form['email'].value())
                        send_mail(subject, message, EMAIL_HOST_USER,
                                [recepient], fail_silently=False)
                        user = form.save()
                        login(request, user)
                        messages.success(request, "Registration successful.")

                        return redirect("login")
            # messages.error(
            #     request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
        return render(request, context={'register_form': form}, template_name='HtmlFiles/register.html')


	

def extract(text):
    wbc_re = re.compile(r'(.*[Ll]eu[ck]ocyte\D*|.*WBC\D*|.*White Blood Cell\D*) ([\d,.]+) ')
    rbc_re = re.compile(r'(.*[eE]rythrocyte\D*|.*[r,R][b,B][c,C]\D*|.*[Rr]ed [Bb]lood [Cb]ell\D*|.*[Rr]ed [Cc]ell [Cc]ount\D*) ([\d,.]+) ')
    hgb_re = re.compile(r'(.*[Hh][a]*emoglobin\D*) ([\d,.]+) ')
    pcv_re = re.compile(r'(.*[Pp]acked [Cc]ell [Vv]olume\D*|.*[pP][cC][vV]\D*|.*[Hh][a]*ematocrit\D*) ([\d,.%]+) ')
    mcv_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Vv]olume\D*|.*[mM][cC][vV]\D*|.*[Mm]ean [Cc]ell [Vv]olume\D*) ([\d,.]+) ')
    mch_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Hh]b\D*|.*[mM][cC][hH]\D*) ([\d,.]+) ')
    mchc_re = re.compile(r'(.*[Mm]ean [Cc]ell [Hh]b Conc\D*|.*[mM][cC][hH][cC]\D*|.*[Mm]ean [Cc]ell [Hh]b[\.]* [Cc]onc\D*) ([\d,.]+) ')
    rcd_re = re.compile(r'(.*[Rr]ed [Cc]ell [Dd]ist\D*|.*[Rr][cC][Dd]\D*|.*[Rr][Dd][Ww]\D*) ([\d,.]+) ')
    pc_re = re.compile(r'(.*[Pp]la[Ee]*telet[s]* [Cc]ount\D*|.*[Pp]la[Ee]*telet[s]*\D*) ([\d,.]+) ')
    mpv_re = re.compile(r'(.*[Mm]ean Pla[eE]*telet [Vv]olume\D*|.*[Mm][Pp][Vv]\D*) ([\d,.]+) ')
#     neu_re = re.compile(r'([Nn]eutrophils) ([\d,.]+) ')
#     lym_re = re.compile(r'(.*[Ll]ymphocyte.*) ([\d,.]+) ')
#     mon_re = re.compile(r'(.*[Mm]onocyte.*) ([\d,.]+) ')
#     eos_re = re.compile(r'(.*[Ee]osinophils.*) ([\d,.]+) ')
#     bas_re = re.compile(r'(.*[Bb]asophils.*) ([\d,.]+) ')
   
    flag = 0
   
    wbc = wbc_re.search(text)
    if(wbc != None):
        wbc = wbc_re.search(text).group(2)
        wbc = float(wbc.replace(',',''))
        if(wbc>1000 and wbc<100000):
            wbc /= 1000
    elif(wbc==None):
            wbc = 0.0000000000000
            flag += 1
       
    rbc = rbc_re.search(text)
    if(rbc != None):
        rbc = rbc_re.search(text).group(2)
        rbc = float(rbc.replace(',',''))
    elif(rbc==None):
            rbc = 0.0000000000000
            flag += 1
       
    hgb = hgb_re.search(text)
    if(hgb != None):
        hgb = hgb_re.search(text).group(2)
        hgb = float(hgb.replace(',',''))
    elif(hgb==None):
            hgb = 0.0000000000000
            flag += 1
       
    pcv = pcv_re.search(text)
    if(pcv != None):
        pcv = pcv_re.search(text).group(2)
        pcv = pcv.replace('%','')
        pcv = pcv.replace(',','')
        pcv = float(pcv)
    elif(pcv==None):
            pcv = 0.0000000000000
            flag += 1
       
    mcv = mcv_re.search(text)
    if(mcv != None):
        mcv = mcv_re.search(text).group(2)
        mcv = float(mcv.replace(',',''))
    elif(mcv==None):
            mcv = 0.0000000000000
            flag += 1
       
    mch = mch_re.search(text)
    if(mch != None):
        mch = mch_re.search(text).group(2)
        mch = float(mch.replace(',',''))
    elif(mch==None):
            mch = 0.0000000000000
            flag += 1
       
    mchc = mchc_re.search(text)
    if(mchc != None):
        mchc = mchc_re.search(text).group(2)
        mchc = float(mchc.replace(',',''))
    elif(mchc==None):
            mchc = 0.0000000000000
            flag += 1
       
    rcd = rcd_re.search(text)
    if(rcd != None):
        rcd = rcd_re.search(text).group(2)
        rcd = float(rcd.replace(',',''))
    elif(rcd==None):
            rcd = 0.0000000000000
            flag += 1
       
    pc = pc_re.search(text)
    if(pc != None):
        pc = pc_re.search(text).group(2)
        pc = float(pc.replace(',',''))
    elif(pc==None):
            pc = 0.0000000000000
            flag += 1
       
    mpv = mpv_re.search(text)
    if(mpv != None):
        mpv = mpv_re.search(text).group(2)
        mpv = float(mpv.replace(',',''))
    elif(mpv==None):
            mpv = 0.0000000000000
            flag += 1
       
#     if(flag > 5):
#         print("Could not find values. Please check if the correct report is uploaded.")
#     else:
    print("Leukocyte count: ", wbc)
    print("Red Blood Cell count: ", rbc)
    print("Haemoglobin Count: ", hgb)
    print("Packed Cell Volume: "+ str(pcv) +"%")
    print("Mean Cell Volume: ", mcv)
    print("Mean Corpuscular Hb Conc.: ", mchc)
    print("Red Cell Dist.: ", rcd)
    print("Platelet Count: ", pc)
    print("Mean Platelet Volume: ", mpv)

    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv

        

    	

def GetInfo(path):
    cbc = path
    with pdfplumber.open(cbc, password='9821714272') as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
    rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = extract(text)
    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv

def dashboard(request,rid):
    context={}
    name=request.user.username or None
    all_reports= Cbc.objects.get(user=request.user, id=rid)
    return render(request,'HtmlFiles/dashboard.html',context={'name':name,'all_report':all_reports})


def ViewPatients(request):
    name=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    print(doc)

    current_patients = User.objects.filter(viewdoctor__doctor=doc, viewdoctor__status=1)
    pending_patients = User.objects.filter(viewdoctor__doctor=doc, viewdoctor__status=0)
    print(current_patients)
    print(pending_patients)

    return render(request,'HtmlFiles/viewPatients.html',context={'curr':current_patients,'name':name,'pend':pending_patients})

def pendingReq(request, user_id, ar):
    user = User.objects.get(id=user_id)
    print(user)
    doc=ConfirmDoctor.objects.get(id=request.session['ConfirmDoctor_id'])
    if(ar==1):
        a = ViewDoctor.objects.get(user=user, doctor=doc)
        a.status = 1
        a.save()
    elif(ar==0):
        a = ViewDoctor.objects.get(user=user, doctor=doc)
        a.status = 0
        a.save()
    return redirect("viewPatients")

def docRequest(request, doc_id):
    print(doc_id)
    doc = ConfirmDoctor.objects.get(id=doc_id)
    user=request.user or None
    print(user)
    print(doc)
    v = ViewDoctor(user=user, doctor=doc)
    
    print(v)
    v.save()
    name=request.user.username or None
    d1= ConfirmDoctor.objects.all()
    return render(request,'HtmlFiles/viewDoctor.html',context={'name':name,'d1':d1})

def GetInfoOCR(path):
    cbc = path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\tirth\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' #enter your path here
    text = pytesseract.image_to_string(Image.open(cbc))

    print(text)
    rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv= extract(text)
    return rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv



def FILE(request):
    name=request.user.username or None
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        if(uploaded_file.name.endswith(".pdf")):
            rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfo(uploaded_file)
            user = request.user.get_username()

            # cbc = Cbc()
            # cbc.user = request.user
            # cbc.rbc = rbc
            # cbc.wbc = wbc
            # cbc.pc = pc
            # cbc.hgb= hgb
            # cbc.rcd= rcd
            # cbc.mchc= mchc
            # cbc.mpv= mpv
            # cbc.pcv= pcv
            # cbc.mcv= mcv

            # cbc.save()
            initial = {'rbc': rbc,
                    'wbc': wbc,
                    'pc': pc,
                    'hgb': hgb,
                    'rcd': rcd,
                    'mchc': mchc,
                    'mpv': mpv,
                    'pcv': pcv,
                    'mcv': mcv,
                    }
            form = ConfirmForm(initial=initial)
            context = {
                'form': form
            }
            return render(request, 'HtmlFiles/confirmForm.html', context)
        elif(uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfoOCR(uploaded_file)
            user = request.user.get_username()

            initial = {'rbc': rbc,
                    'wbc': wbc,
                    'pc': pc,
                    'hgb': hgb,
                    'rcd': rcd,
                    'mchc': mchc,
                    'mpv': mpv,
                    'pcv': pcv,
                    'mcv': mcv,
                    }
            form = ConfirmForm(initial=initial)
            context = {
                'form': form
            }
            return render(request, 'HtmlFiles/confirmForm.html', context)
            
            

        

    return render(request, 'HtmlFiles/FILE.html', {'name':name})

def Doctorlogin(request):
            if request.method == 'POST':
                username = request.POST.get('name')
                password =request.POST.get('password') 
                



                user = ConfirmDoctor.objects.filter(username=username,password=password).values()[0]
                if user is not None:
                        # login(request, user)
                        request.session['ConfirmDoctor_id']=user['id']
                        return redirect('Doctorhome')
                else:
                        messages.error(request,'username or password not correct')
	
                        
        
            return render(request, 'HtmlFiles/Doctorlogin.html')

def Doctorlogout_view(request):
		del request.session['doctor_id']
		messages.info(request, "You have successfully logged out.") 
		return redirect("Doctorlogin")

def reports(request):
    user=request.user or None
    all_reports= Cbc.objects.filter(user=user) #.filter(user=request.user)
    return render(request,'HtmlFiles/viewmyreports.html',context={'posts':all_reports})
def loginPage(request):
		if request.method == 'POST':
			username = request.POST.get('name')
			password =request.POST.get('password') 



			user = authenticate(request,username=username,password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					
					return redirect('home')
			else:
					messages.error(request,'username or password not correct')
	
		return render(request, 'HtmlFiles/login.html')

def logout_view(request):
		logout(request)
		messages.info(request, "You have successfully logged out.") 
		return redirect("login")


