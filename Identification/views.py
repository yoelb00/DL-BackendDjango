# -*- coding: utf-8 -*-
from django.http import HttpResponse
#from src.services import detection

import os,cv2
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import base64
from numpy.core.function_base import logspace
from rest_framework.parsers import JSONParser
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt



#from .forms import *
def saveLog(name,log):
    with open(r"C:\Users\Yoel\Desktop\DL-FinalProject\DL-FinalProject\dl-backend\{0}.txt".format(name), "w") as f:
        f.write(str(log))
# Create your views here.
try:
    from src import Service
    service = Service.Service()
except Exception as error:
    saveLog('service',error)



@csrf_exempt
def index(request):
    try:
        if request.method == 'POST':
            print('-------------------------------------')
            data = JSONParser().parse(request)
            cameraID = data['cameraId']
            image = data['image']
            img = imread(BytesIO(base64.b64decode(image)))
            cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
            try:
                service.Identify(cameraID=cameraID,inImage=cv2_img)
            except:
                HttpResponse('')
            return HttpResponse('done')
        else:
            return HttpResponse('only post request allowed')
    except Exception as error:
        return str(error)
