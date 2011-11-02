import os
from locreep.models import *
from PIL import Image
from time import strftime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

@csrf_exempt
def upload_creep_photo(request):
    creep_id = request.POST['creep_id']
    conversation_id = request.POST['conversation_id']
    
    if request.method == 'POST':
        f=request.FILES['creep_photo'] # this is my file
        
        try:
            tmp = Image.open(f)
            tmp.verify()
        except IOError:
            return render_to_response('error.html', { 'error': 'Invalid image file. Please try another.' }, context_instance=RequestContext(request))
        
        rel_path = '/static/images/creeps/'+creep_id+'.'+strftime("%Y-%m-%d-%H-%M-%S")+'.'+tmp.format
        path = os.path.dirname(__file__) + '/..' + rel_path
        
        destination = open(path, 'wb+')
        
        for chunk in f.chunks():
            destination.write(chunk)
            destination.close()
        
        try:
            creep = Creep.objects.get(id=creep_id)
        except Creep.DoesNotExist:
            return render_to_response("error.html", { 'error': 'Invalid creep.' }, context_instance=RequestContext(request))
        
        creep.photo = rel_path
        creep.save()
        
        return HttpResponseRedirect('/conversations/' + conversation_id)

    return render_to_response('error.html', { 'error': 'Invalid image file. Please try another.' }, context_instance=RequestContext(request))