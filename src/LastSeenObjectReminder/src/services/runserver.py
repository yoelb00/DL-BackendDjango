import flask
import numpy as np
import cv2
import time
import os
import subprocess

#from .src.services.detection import detectByImage
from .src.services import detection
from json import dumps as jsonstring

app = flask.Flask(__name__)
app.config["DEBUG"] = True


class Request:
  def __init__(self, cameraId, imageData):
    self.cameraId = cameraId
    self.imageData = imageData

# @app.route('/')
# def HealthCheck():
#     return "Ok"

@app.route('/')
def DetectObjectsByImage():
    return True


app.run()
