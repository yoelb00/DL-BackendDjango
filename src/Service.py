from src.LastSeenObjectReminder.src.services import detection
import cv2,time,numpy,os
import numpy as np
dataFolder = os.path.abspath('./Data')
from PIL import Image
import shutil   
class Service():
    def __init__(self):
        print('Service')
        self.status = ''
    def Identify(self,cameraID,inImage):
        try:
            image,className = detection.detectByImage(inImage)

            self.saveImage(className,cameraID,image)
            self.status = 'Done'
        except Exception as error:
            self.status = str(error)
            

    def getLastIdentification(self,lable=None):
        file = self.getIdentified(lable)
        return file

    def getIdentified(self,className):
        print('getIdentified')
        #os.open(r'{0}\{1}\{2}'.format(dataFolder, cameraID, lable))
        file = ''
        lastTime = 0
        fileList = []
        for baseFolder, y, files in os.walk(r'{0}'.format(dataFolder)):
            for file in files:
                if (os.path.basename(os.path.dirname(os.path.join(baseFolder,file))) == className) and len(files)>0:
                    print(os.path.join(baseFolder,file))
                    timeRecorded = file.split('_')[1]
                    timeRecorded = float(timeRecorded[:timeRecorded.find('.j')])
                    if timeRecorded>lastTime:
                        lastTime=timeRecorded
                        file = file
            if lastTime>0:
                fileList.append("{0}\{1}".format(baseFolder,file))
            lastTime=0
        return fileList

    def toString(self):
        self.status = 'Done'
        return "bla"

    def saveImage(self, className,camId,inImage):
        try:
            shutil.rmtree('{0}\{1}\{2}'.format(dataFolder,camId,className))
            os.makedirs('{0}\{1}'.format(dataFolder,camId), mode=0o777,exist_ok=True) # create camId folder
            os.makedirs('{0}\{1}\{2}'.format(dataFolder,camId,className ), mode=0o777, exist_ok=True) # create className folder
            inImage.save(r'{0}\{1}\{2}\outImage_{3}.jpeg'.format(dataFolder,camId,className, str(time.time()))) # save image
        except Exception as error:
            return str(error)

    def status(self):
        return self.status
