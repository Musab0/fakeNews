from django.shortcuts import get_object_or_404, render
from verifynews.myapp.models import Image, Upload, User
from verifynews.myapp.forms import ImageAdminForm, ImageForm, UserForm
import subprocess
from itertools import chain
import os
from django.shortcuts import redirect
from scipy.spatial.distance import hamming
# Create your views here.
from django.http import HttpResponse, JsonResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from verifynews.myapp.consumers import ChatConsumer


def user_page(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        imageform = ImageForm(request.POST, request.FILES)
        userform = UserForm(request.POST)

        
            
        if imageform.is_valid() and ('user_upload' in request.POST):  #"user_upload" is the name of the upload button

            all_images=Image.objects.all()
            img_obj=imageform.save() # according to the docs of fileField. the extension added to file name will be added only after the image is saved. This, this save round is important 
            # Get the current instance object to display in the template
            img_obj = imageform.instance
            img_obj.set_fileType()
            img_obj.save()


            
            
            
            userform.is_valid()
            try: 
                user_obj=User.objects.get(phone = userform.instance.phone) # if the phone number belong to a user in the database. assign that object toe user_obj
            except:
                user_obj= userform.instance 
                userform.save() 

            db_images=len(all_images)

            if img_obj.fileType=="image":

                hash_process= subprocess.check_output(['python','./verifynews/myapp/ThreatExchange/pdq/python/pdqhashing/tools/pdq_photo_hasher_tool.py','./verifynews/media/{}'.format(img_obj.image.name),'--pdq']).decode("utf-8") 
                hash_process= hash_process.split(',')
                img_obj.pdq = hash_process[0]

                counter=0
                similar_images=[]
                similarity=[]

                for i in all_images.filter(fileType='image'): 
                    dist=hamming_distance(i.pdq,img_obj.pdq)
                    if  dist > 0.6:
                        counter+=1
                        similar_images.append(i)
                        similarity.append(dist)

                similarity_zip= zip (similarity,similar_images)
                imageform.save()

                if (counter>0):
                    img_obj=similar_images[0] #first similar image 
                    Image.objects.last().delete()
            
            elif img_obj.fileType=="video":
                generate_tmk(img_obj)
                db_images=img_obj.image.name

                counter=0
                similar_images=[]
                similarity=[]
                for i in all_images.filter(fileType='video'): 
                    if(img_obj.pdq==i.pdq):continue
                    if(compare_tmk(img_obj.pdq,i.pdq)):
                        counter+=1
                        similar_images.append(i)
                        similarity.append(1)
                similarity_zip= zip (similarity,similar_images)
                imageform.save()

                if (counter>0):
                    img_obj=similar_images[0] #first similar image 
                    Image.objects.last().delete()
  

            user_obj.Image.add(img_obj)
            adminForm= ImageAdminForm(request.POST, instance=img_obj)
            return render(request, 'user_page.html', {'userform': userform, 'imageform': imageform,'adminForm': adminForm, 'user_obj':user_obj,'img_obj': img_obj, 'counter':counter, 'db_images':db_images, 'similarity_zip':similarity_zip})
    
        if 'admin_upload' in request.POST:
            img_obj = Image.objects.last()
            adminForm= ImageAdminForm(request.POST, instance=img_obj)
    
            adminForm.save() 
            counter=1
            return render(request, 'user_page.html', {'imageform': imageform, 'img_obj': img_obj, 'counter':counter})
    
    else:
        imageform = ImageForm()
        userform = UserForm()
        return render(request, 'user_page.html', {'userform': userform,'imageform': imageform, 'server_setting':check_server()})


def home_page(request):
    

    if request.method =='POST':
        userform = UserForm(request.POST)
        userform.is_valid()
        try: 
            user_obj=User.objects.get(phone = userform.instance.phone) # if the phone number belong to a user in the database. assign that object toe user_obj
        except:
            user_obj= userform.instance 
            userform.save() 
        return redirect("/myapp/"+user_obj.phone)

    else:
        userform = UserForm()
        return render(request, 'home_page.html', {'userform': userform,'server_setting': check_server(),})







def room(request, room_name):

    imageform = ImageForm(request.POST or None, request.FILES or None)
    data={}
    if request.is_ajax():
        if imageform.is_valid():
            imageform.save()
            
            data['status']='ok'
            return JsonResponse(data)



















    username = request.GET.get('username', 'Anonymous')
    return render(request, 'room.html', {'room_name': room_name, 'username': username,'imageform': imageform,})



def admin_page(request):
       
    if request.method =='POST':
        adminform=ImageAdminForm(request.POST)
        adminform.is_valid()
        img_id = request.POST.get('image_id')
        img_obj=Image.objects.filter(id=img_id)[0]
        adminform=ImageAdminForm(request.POST,instance=img_obj)
        adminform.save()

        adminform=ImageAdminForm()

        if(img_obj.category != 'unsorted'):
            for phoneNumber in img_obj.upload_set.all():
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)('chat_'+phoneNumber.user.phone, {
                "type": "chat.message",
                "message": "It is " + img_obj.category + "\rTitle: " + img_obj.title + "\rDescriptio:" + img_obj.description 
                })


        # real_images=Image.objects.filter(category='real').order_by('-date')
        # fake_images=Image.objects.filter(category='fake').order_by('-date')
        # unsorted_images=Image.objects.filter(category='unsorted').order_by('-date')
        # all_images=list(chain(unsorted_images,fake_images, real_images))
        return redirect("/myapp/admin_page") # to avoid Form resubmission on page refresh 
        # return render(request, 'admin_page.html',{'all_images':all_images, 'adminform':adminform, 'img_obj':img_obj})
        

    else: 

        adminform=ImageAdminForm()

        real_images=Image.objects.filter(category='real').order_by('-date')
        fake_images=Image.objects.filter(category='fake').order_by('-date')
        unsorted_images=Image.objects.filter(category='unsorted').order_by('-date')
        all_images=list(chain(unsorted_images,fake_images, real_images))
        return render(request, 'admin_page.html',{'all_images':all_images, 'adminform':adminform})



















def hamming_distance(chaine1, chaine2): #move this to another file 
    if len(chaine1) != len(chaine2):
        return -1
    else: 
        return sum(c1 == c2 for c1, c2 in zip(chaine1, chaine2))/len(chaine1)



def generate_tmk(img_obj):
    subprocess.run(['./verifynews/myapp/ThreatExchange/tmk/cpp/tmk-hash-video', '-f', '/usr/bin/ffmpeg', '-i', './verifynews/media/{}'.format(img_obj.image.name), '-d', './verifynews/media/images'])
    img_obj.pdq = os.path.splitext(img_obj.image.name)[0] + '.tmk' # [1] returns path+filename


def compare_tmk(f1,f2):
    proc = subprocess.run(['./verifynews/myapp/ThreatExchange/tmk/cpp/tmk-compare-two-tmks', './verifynews/media/'+f1 ,'./verifynews/media/'+f2],  capture_output=True)
    if proc.returncode==0:
        return 1 # if they match 
    else: 
        return 0


def check_server():
    if os.environ.get('SERVER_GATEWAY_INTERFACE') == 'Web':
        server_setting = 'server: WSGI'
    elif os.environ.get('SERVER_GATEWAY_INTERFACE') == 'Asynchronous':
        server_setting = 'server: ASGI'
    else: 
        server_setting='server not set'
    return server_setting