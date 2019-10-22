
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from random import randint
from django.views.generic import *
from .models import *
from django.http import Http404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .form import HomeForm  
from textblob import TextBlob
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import viewsets
from .serializer import AssemblySerializer
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.conf import settings
import plotly
import PIL
import PIL.Image as Image
import io
from io import *
import numpy as np
from io import BytesIO
import base64
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
        
#from .WebService1 import settings.BASE_DIR as BASE_DIR


# Create your views here.
#Function view starts
# def home(request):
#     #return HttpResponse('Hello home page 1')
#     random_number = randint(1,100000000000)
#     var = 'come will see'
#     some_list = [random_number, randint(1,100000000000), randint(1,100000000000)]
#     return render(request,'home.html',{'var':random_number,'boolean_number':True,'some_list':some_list})


# def about(request):
#     return render(request,'about.html',{})    


# def contact(request):
#     return render(request,'contact.html',{})   

# def product(request):
#     return render(request,'product.html',{})

# def Board_view(request,pk):
#     try:
#         board = Board.objects.get(pk = pk)
#     except Board.DoesNotExist:
#         raise Http404    
#     return render(request,'Board.html',{'board': board})

# def redirectPage(request):
#     response = redirect('about/')
#     return response

# def new_topic(request,pk):
#     board = get_object_or_404(Board,pk=pk)
#     return render(request,'new_topic.html',{'board':board})


# def success(request):
#     #email = request.POST.get('email', '')
#     email = 'chauhanlucky14994@gmail.com'
#     data = """
# Hello there!

# I wanted to personally write an email in order to welcome you to our platform.\
#  We have worked day and night to ensure that you get the best service. I hope \
# that you will continue to use our service. We send out a newsletter once a \
# week. Make sure that you read it. It is usually very informative.

# Cheers!
# ~ Yasoob
#     """
#     send_mail('Welcome!', data, "Yasoob",
#               [email], fail_silently=False)
#     return render(request, 'about.html')
#Function view ends

#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------

#class view starts
# class ProductView(View):
#     def get(self,request,*arg,**kwarg): 
#         return render(request,'product.html',{})       


#Template View
# class Contact(TemplateView):
#     template_name = 'contact.html'
#     title = 'Lucky'#in new django version we dont have to override getContext of TemplateView we can directly this command
#     boards = Board.objects.all()

    
class About(TemplateView):
    template_name = 'about.html'
    #title = 'Lucky'#in new django version we dont have to override getContext of TemplateView we can directly this command
    
    def get(self,request): 
        form = HomeForm()
        return render(request,self.template_name,{"form" : form})

    def post(self,request): 
        form = HomeForm(request.POST)
        if (form.is_valid()):
            text = form.cleaned_data['post']
        
        
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if(polarity < 0.0):
            polarity = 'negative'
        elif(polarity > 0.0):
            polarity = 'positive'  
        elif(polarity == 0.0):
            polarity = 'neutral'


        arg = {"form" : form ,"polarity" : polarity}


        return render(request,self.template_name,arg)


    
class Ignite(TemplateView):
    template_name = 'JohnDeere.html'
    
    def get(self,request): 
        present = ''
        list1=[]
        list2= []
        list3=[]
        list4=[]
        bins = Assembly.objects.all()
        bins = [[str(bin.assemblyLineNO), str(bin.binId) , str(bin.binName), str(bin.timestamp)] for bin in bins]
        
        for i in bins:
            list1.append(i[0])
            list2.append(i[2])
            list3.append(i[3])
        
        for i in list3:
            date1 = i.split('+')
            
            datetime_object = datetime.strptime(date1[0], '%Y-%m-%d %H:%M:%S')
            datetime_object = str(datetime_object).split(' ')[0]+'/'+str(datetime_object).split(' ')[1]
            list4.append(datetime_object)
        
       
        diction = dict()
        diction.update({"name": list2,"date":list4})
        
        pd1 = pd.DataFrame(data = diction)
        #################
        pd0 = pd1['name'].value_counts().reset_index()
        pd5 = pd0.sort_values(by=['index'])
        pd2 = pd0.loc[pd1['name'].value_counts().reset_index()['name'] %2 ==0]
        value = list(pd2['index'])
        
        #################
        
        x1 = pd5['index'].values
        y1 = pd5['name'].values


        fig = plt.figure(figsize=(7,3))
        plt.title("BINS vs No OF BINS ENTERED TODAY")
        plt.xlabel("No OF BINS ENTERED TODAY")
        plt.ylabel("BINS")
        lines = plt.bar(x1, y1)

        # use keyword args
        color=['r','g','b','y']
        pd5 = pd5.reset_index()
        # or MATLAB style string value pairs

        for i in range(len(pd5)):
            plt.setp(lines[i], color=color[i], linewidth=2.0)
            plt.annotate(xy=(pd5['index'][i],pd5['name'][i]+.1),s=pd5['name'][i])
        # plt.grid()
        #fig.savefig('L:/PythonDjango_HerokuDeployment/PythonApp/Application/static/images/images/graph.png')

        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        


        
        
        #################
        gk = pd1.groupby('name')
        gk1 = gk.last().reset_index()
        for i in value:
            gk1 = gk1.loc[gk1['name']!=i]

        ################
        gk1['date1'] = gk1['date'].apply(lambda x : str(x))
        gk1['date1'] = gk1['date1'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d/%H:%M:%S'))
        if len(gk1) != 0:
            latestDate = str(max(gk1['date1'])).strip()
        else:
             latestDate = 'NO'   
        gk1['date1'] = gk1['date'].apply(lambda x: x.replace('/',' '))
        gk1['date1']=gk1['date1'].apply(lambda x: x.strip())




        ##############    
        if (len(gk1['name'].values)==4):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = gk1['date1'].values[3]
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = gk1['name'].values[3]
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = gk1['date'].values[3].split('/')[0]
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = gk1['date'].values[3].split('/')[1]
        elif(len(gk1['name'].values)==3):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = '-'
        elif(len(gk1['name'].values)==2):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = '-'
            d4 = '-' 
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = '-'
            t4 = '-' 
        elif(len(gk1['name'].values)==1):
            date1 = gk1['date1'].values[0]
            date2 = '-'
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = '-'
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = '-'
            d3 = '-'
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = '-'
            t3 = '-'
            t4 = '-'        
        else:
            date1 = '-'
            date2 = '-'
            date3 = '-'
            date4 = '-'
            b1 = '-'
            b2 = '-'
            b3 = '-'
            b4 = '-'
            d1 = '-'
            d2 = '-'
            d3 = '-'
            d4 = '-'
            t1 = '-'
            t2 = '-'
            t3 = '-'
            t4 = '-' 
        return render(request,self.template_name,{"date1":date1,"date2":date2,"date4":date4,"LatestDate":latestDate,"bins" : len(gk1),"b1":b1,"b2":b2,"b3":b3,"b4":b4,"t1":t1,"t2":t2,"t3":t3,"t4":t4,"d1":d1,"d2":d2,"d3":d3,"d4":d4,"image_base64":image_base64})

class ListCreateAssemblyView(viewsets.ModelViewSet):
    
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer       

class IgniteV2(TemplateView):
    template_name = 'JohnDeereNew.html'
    
    def get(self,request): 
        present = ''
        list1=[]
        list2= []
        list3=[]
        list4=[]
        bins = Assembly.objects.all()
        bins = [[str(bin.assemblyLineNO), str(bin.binId) , str(bin.binName), str(bin.timestamp)] for bin in bins]
        
        for i in bins:
            list1.append(i[0])
            list2.append(i[2])
            list3.append(i[3])
        
        for i in list3:
            date1 = i.split('+')
            
            datetime_object = datetime.strptime(date1[0], '%Y-%m-%d %H:%M:%S')
            datetime_object = str(datetime_object).split(' ')[0]+'/'+str(datetime_object).split(' ')[1]
            list4.append(datetime_object)
        
       
        diction = dict()
        diction.update({"name": list2,"date":list4})
        
        pd1 = pd.DataFrame(data = diction)
        #################
        pd0 = pd1['name'].value_counts().reset_index()
        pd5 = pd0.sort_values(by=['index'])
        pd2 = pd0.loc[pd1['name'].value_counts().reset_index()['name'] %2 ==0]
        value = list(pd2['index'])

        #################
        
        x1 = pd5['index'].values
        y1 = pd5['name'].values


        fig = plt.figure(figsize=(7,2))
        plt.title("BINS vs NO OF BINS ENTERED TODAY")
        plt.ylabel("# BINS ENTERED TODAY")
        plt.xlabel("BINS")
        lines = plt.bar(x1, y1)

        # use keyword args
        color=['r','g','b','y']
        pd5 = pd5.reset_index()
        # or MATLAB style string value pairs

        for i in range(len(pd5)):
            plt.setp(lines[i], color=color[i], linewidth=2.0)
            plt.annotate(xy=(pd5['index'][i],pd5['name'][i]+.1),s=pd5['name'][i])
        plt.grid()
        

        
        plt.plot(x1,y1)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        

        # canvas = fig.canvas
        # buf, size = canvas.print_to_buffer()
        # image = Image.frombuffer('RGBA', size, buf, 'raw', 'RGBA', 0, 1)
        # buffer=io.BytesIO()
        # image.save(buffer,'PNG')
        # image_base64 = buffer.getvalue()
        # image_base64 = base64.b64encode(image_base64).decode('utf-8')
        # buffer.close() 
        
        
        

        


        #################
        gk = pd1.groupby('name')
        gk1 = gk.last().reset_index()
        for i in value:
            gk1 = gk1.loc[gk1['name']!=i]

        ################
        gk1['date1'] = gk1['date'].apply(lambda x : str(x))
        gk1['date1'] = gk1['date1'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d/%H:%M:%S'))
        if len(gk1) != 0:
            latestDate = str(max(gk1['date1'])).strip()
        else:
             latestDate = 'NO'   
        gk1['date1'] = gk1['date'].apply(lambda x: x.replace('/',' '))
        gk1['date1']=gk1['date1'].apply(lambda x: x.strip())




        ##############    
        if (len(gk1['name'].values)==4):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = gk1['date1'].values[3]
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = gk1['name'].values[3]
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = gk1['date'].values[3].split('/')[0]
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = gk1['date'].values[3].split('/')[1]
        elif(len(gk1['name'].values)==3):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = '-'
        elif(len(gk1['name'].values)==2):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = '-'
            d4 = '-' 
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = '-'
            t4 = '-' 
        elif(len(gk1['name'].values)==1):
            date1 = gk1['date1'].values[0]
            date2 = '-'
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = '-'
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = '-'
            d3 = '-'
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = '-'
            t3 = '-'
            t4 = '-'        
        else:
            date1 = '-'
            date2 = '-'
            date3 = '-'
            date4 = '-'
            b1 = '-'
            b2 = '-'
            b3 = '-'
            b4 = '-'
            d1 = '-'
            d2 = '-'
            d3 = '-'
            d4 = '-'
            t1 = '-'
            t2 = '-'
            t3 = '-'
            t4 = '-' 
        return render(request,self.template_name,{"date1":date1,"date2":date2,"date4":date4,"LatestDate":latestDate,"bins" : len(gk1),"b1":b1,"b2":b2,"b3":b3,"b4":b4,"t1":t1,"t2":t2,"t3":t3,"t4":t4,"d1":d1,"d2":d2,"d3":d3,"d4":d4,"image_base64":image_base64})


class get_more_tables(TemplateView):
    template_name = 'update.html'
    def get(self,request):
        #increment = int(request.GET['append_increment'])
        
        present = ''
        list1=[]
        list2= []
        list3=[]
        list4=[]
        bins = Assembly.objects.all()
        bins = [[str(bin.assemblyLineNO), str(bin.binId) , str(bin.binName), str(bin.timestamp)] for bin in bins]
            
        for i in bins:
            list1.append(i[0])
            list2.append(i[2])
            list3.append(i[3])
            
        for i in list3:
            date1 = i.split('+')
                
            datetime_object = datetime.strptime(date1[0], '%Y-%m-%d %H:%M:%S')
            datetime_object = str(datetime_object).split(' ')[0]+'/'+str(datetime_object).split(' ')[1]
            list4.append(datetime_object)
            
        
        diction = dict()
        diction.update({"name": list2,"date":list4})
            
        pd1 = pd.DataFrame(data = diction)
            #################
        pd0 = pd1['name'].value_counts().reset_index()
        pd2 = pd0.loc[pd1['name'].value_counts().reset_index()['name'] %2 ==0]
        value = list(pd2['index'])
            

            


        #################
        gk = pd1.groupby('name')
        gk1 = gk.last().reset_index()
        for i in value:
            gk1 = gk1.loc[gk1['name']!=i]

        ################
        gk1['date1'] = gk1['date'].apply(lambda x : str(x))
        gk1['date1'] = gk1['date1'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d/%H:%M:%S'))
        latestDate = str(max(gk1['date1'])).strip()
        gk1['date1'] = gk1['date'].apply(lambda x: x.replace('/',' '))
        gk1['date1']=gk1['date1'].apply(lambda x: x.strip())




            ##############    
        if (len(gk1['name'].values)==4):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = gk1['date1'].values[3]
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = gk1['name'].values[3]
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = gk1['date'].values[3].split('/')[0]
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = gk1['date'].values[3].split('/')[1]
        elif(len(gk1['name'].values)==3):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = gk1['date1'].values[2]
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = gk1['name'].values[2]
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = gk1['date'].values[2].split('/')[0]
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = gk1['date'].values[2].split('/')[1]
            t4 = '-'
        elif(len(gk1['name'].values)==2):
            date1 = gk1['date1'].values[0]
            date2 = gk1['date1'].values[1]
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = gk1['name'].values[1]
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = gk1['date'].values[1].split('/')[0]
            d3 = '-'
            d4 = '-' 
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = gk1['date'].values[1].split('/')[1]
            t3 = '-'
            t4 = '-' 
        elif(len(gk1['name'].values)==1):
            date1 = gk1['date1'].values[0]
            date2 = '-'
            date3 = '-'
            date4 = '-'
            b1 = gk1['name'].values[0]
            b2 = '-'
            b3 = '-'
            b4 = '-'
            d1 = gk1['date'].values[0].split('/')[0]
            d2 = '-'
            d3 = '-'
            d4 = '-'
            t1 = gk1['date'].values[0].split('/')[1]
            t2 = '-'
            t3 = '-'
            t4 = '-'        
            
        return render(request,self.template_name,{"date1":date1,"date2":date2,"date4":date4,"LatestDate":latestDate,"bins" : len(gk1),"b1":b1,"b2":b2,"b3":b3,"b4":b4,"t1":t1,"t2":t2,"t3":t3,"t4":t4,"d1":d1,"d2":d2,"d3":d3,"d4":d4})
 