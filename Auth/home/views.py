from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from matplotlib.pyplot import rcdefaults

from .forms  import NewUserForm
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


# Create your views here.
from .models import *


def home(request):
	name=request.user.username or None
	return render(request,'accounts/home.html',{'name':name})

def homebefore(request):
    	return render(request,'accounts/homebefore.html')

def about(request):
	return render(request,'accounts/about.html')



def registerPage(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
           
			return redirect("login")

		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request,context={'register_form':form} ,template_name='accounts/register.html')


	

def extract(text):
    wbc_re = re.compile(r'(.*[Ll]eu[ck]ocyte.*|.*WBC.*|.*White Blood Cell.*) ([\d,.]+) ')
    rbc_re = re.compile(r'(.*[eE]rythrocyte.*|.*[r,R][b,B][c,C].*|.*[Rr]ed [Bb]lood [Cb]ell.*|.*[Rr]ed [Cc]ell [Cc]ount.*) ([\d,.]+) ')
    hgb_re = re.compile(r'(.*[Hh][a]*emoglobin.*) ([\d,.]+) ')
    pcv_re = re.compile(r'(.*[Pp]acked [Cc]ell [Vv]olume.*|.*[pP][cC][vV].*|.*[Hh][a]*ematocrit) ([\d,.]+) ')
    mcv_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Vv]olume.*|.*[mM][cC][vV].*) ([\d,.]+) ')
    mch_re = re.compile(r'(.*[Mm]ean [Cc]orpuscular [Hh]b.*|.*[mM][cC][hH].*) ([\d,.]+) ')
    mchc_re = re.compile(r'(.*[Mm]ean [Cc]ell [Hh]b Conc.*|.*[mM][cC][hH][cC].*) ([\d,.]+) ')
    rcd_re = re.compile(r'(.*[Rr]ed [Cc]ell [Dd]ist.*|.*[Rr][cC][Dd].*|.*[Rr][Dd][Ww].*) ([\d,.]+) ')
    pc_re = re.compile(r'(.*[Pp]la[Ee]*telet [Cc]ount.*) ([\d,.]+) ')
    mpv_re = re.compile(r'(.*[Mm]ean Pla[eE]*telet [Vv]olume.*|.*[Mm][Pp][Vv].*) ([\d,.]+) ')
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
        wbc = 0.00000000000000
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
        hgb = 0.00000000000000
        flag += 1
        
    pcv = pcv_re.search(text)
    if(pcv != None):
        pcv = pcv_re.search(text).group(2)
        pcv = float(pcv.replace(',',''))
    elif(pcv==None):
        pcv = NULL
        flag += 1
        
    mcv = mcv_re.search(text)
    if(mcv != None):
        mcv = mcv_re.search(text).group(2)
        mcv = float(mcv.replace(',',''))
    elif(mcv==None):
        mcv = 0.00000000000
        flag += 1
        
    mch = mch_re.search(text)
    if(mch != None):
        mch = mch_re.search(text).group(2)
        mch = float(mch.replace(',',''))
    elif(mch==None):
        mch = 0.0000000000
        flag += 1
        
    mchc = mchc_re.search(text)
    if(mchc != None):
        mchc = mchc_re.search(text).group(2)
        mchc = float(mchc.replace(',',''))
    elif(mchc==None):
        mchc = 0.000000000
        flag += 1
        
    rcd = rcd_re.search(text)
    if(rcd != None):
        rcd = rcd_re.search(text).group(2)
        rcd = float(rcd.replace(',',''))
    elif(rcd==None):
        rcd = 0.0000000
        flag += 1
        
    pc = pc_re.search(text)
    if(pc != None):
        pc = pc_re.search(text).group(2)
        pc = float(pc.replace(',',''))
    elif(pc==None):
        pc = 0.00000000000
        flag += 1
        
    mpv = mpv_re.search(text)
    if(mpv != None):
        mpv = mpv_re.search(text).group(2)
        mpv = float(mpv.replace(',',''))
    elif(mpv==None):
        mpv = 0.0000000000000
        flag += 1
        
    if(flag > 5):
        print("Could not find values. Please check if the correct report is uploaded.")
    else:
        print("Leukocyte count: ", wbc)
        print("Red Blood Cell count: ", rbc)
        print("Haemoglobin Count: ", hgb)
        print("Packed Cell Volume: ", pcv)
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
        print(type(uploaded_file.name))
        context['url'] = fs.url(name)
        
        print(uploaded_file)
        if(uploaded_file.name.endswith(".pdf")):
            rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfo(uploaded_file)
            user = request.user.get_username()

            cbc = Cbc()
            cbc.user = request.user
            cbc.rbc = rbc
            cbc.wbc = wbc
            cbc.pc = pc
            cbc.hgb= hgb
            cbc.rcd= rcd
            cbc.mchc= mchc
            cbc.mpv= mpv
            cbc.pcv= pcv
            cbc.mcv= mcv
            cbc.save()
        elif(uploaded_file.name.lower().endswith(('.png', '.jpg', '.jpeg'))):
            rbc, wbc, pc,hgb,rcd,mchc,mpv,pcv,mcv = GetInfoOCR(uploaded_file)
            user = request.user.get_username()

            cbc = Cbc()
            cbc.user = request.user
            cbc.rbc = rbc
            cbc.wbc = wbc
            cbc.pc = pc
            cbc.hgb= hgb
            cbc.rcd= rcd
            cbc.mchc= mchc
            cbc.mpv= mpv
            cbc.pcv= pcv
            cbc.mcv= mcv
            cbc.save()
            
            

        

    return render(request, 'accounts/FILE.html', {'name':name})


def loginPage(request):
		if request.method == 'POST':
			username = request.POST.get('name')
			password =request.POST.get('password') 



			user = authenticate(request,username=username,password=password)
			if user is not None:
				
					login(request, user)
					
					return redirect('home')
			else:
					messages.success(request,"there was error")
					
	
		return render(request, 'accounts/login.html')

def logout_view(request):
		logout(request)
		messages.info(request, "You have successfully logged out.") 
		return redirect("login")


