# -*- coding: utf-8 -*-
from django.http import HttpResponse
#from src.services import detection
from src import Service
import os
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import BytesIO
from django.http import HttpResponseNotFound
import json
#from .forms import *
dataFolder = os.path.abspath('./Data')
def saveLog(name,log):
    with open(r"C:\Users\Yoel\Desktop\DL-FinalProject\DL-FinalProject\dl-backend\{0}.txt".format(name), "w") as f:
        f.write(str(log))
def convertToByte(path):
    with open(path, "rb") as f:
        image_binary = f.read()
        base64_encode = base64.b64encode(image_binary)
        return base64_encode.decode('utf8')

try:
    service = Service.Service()
except Exception as error:
    saveLog('service',error)

@csrf_exempt
def index(request):
    print('------------getLastIdentification-------------')
    try:
        if request.method == 'POST':
            label = str(request.POST.get('label'))
            outImgs = [convertToByte(img) for img in service.getIdentified(label)]
            print(len(outImgs))
            return HttpResponse(json.dumps(outImgs))
        else:
            return HttpResponse('only post request allowed')
    except Exception as error:
        return HttpResponseNotFound(error)