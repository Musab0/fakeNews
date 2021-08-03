from django.shortcuts import get_object_or_404, render
from verifynews.myapp.models import Image
from verifynews.myapp.forms import ImageAdminForm, ImageForm
import subprocess
from scipy.spatial.distance import hamming
# Create your views here.
from django.http import HttpResponse



def user_page(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        
        
        if form.is_valid() and ('user_upload' in request.POST):
            all_images=Image.objects.all()
            form.save() # according to the docs of fileField. the extension added to file name will be added only after the image is saved. This, this save round is important 
            # Get the current instance object to display in the template
            img_obj = form.instance
            adminForm= ImageAdminForm(request.POST, instance=img_obj)
            hash_process= subprocess.check_output(['python','./verifynews/myapp/ThreatExchange/pdq/python/pdqhashing/tools/pdq_photo_hasher_tool.py','./verifynews/media/{}'.format(img_obj.image.name),'--pdq']).decode("utf-8") 
            hash_process= hash_process.split(',')
            img_obj.pdq = hash_process[0]

            
            counter=0
            db_images=len(all_images)
            similar_images=[]
            similarity=[]

            for i in all_images: 
                dist=hamming_distance(i.pdq,img_obj.pdq)
                if  dist > 0.8:
                    counter+=1
                    similar_images.append(i)
                    similarity.append(dist)

            similarity_zip= zip (similarity,similar_images)
            form.save()

            if (counter>0):
                Image.objects.last().delete()

            return render(request, 'user_page.html', {'form': form,'adminForm': adminForm, 'img_obj': img_obj, 'counter':counter, 'db_images':db_images, 'similarity_zip':similarity_zip})
    
        if 'admin_upload' in request.POST:
            img_obj = Image.objects.last()
            adminForm= ImageAdminForm(request.POST, instance=img_obj)
    
            adminForm.save() 
            counter=1
            return render(request, 'user_page.html', {'form': form, 'img_obj': img_obj, 'counter':counter})



    
    
    else:
        form = ImageForm()
        return render(request, 'user_page.html', {'form': form})



def hamming_distance(chaine1, chaine2):
    if len(chaine1) != len(chaine2):
        return -1
    else: 
        return sum(c1 == c2 for c1, c2 in zip(chaine1, chaine2))/len(chaine1)
