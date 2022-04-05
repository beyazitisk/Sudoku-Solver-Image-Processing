import numpy as np
import cv2
from tensorflow.keras.models import load_model
class DigitOcr:
    ########### PARAMETER ##############
    threshold = 0.80  # MINIMUM PROBABILITY TO CLASSIFY
    def __init__(self,model):
        self.model=model

    def preProcessing(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.equalizeHist(img)
        img = img / 255
        return img
    def predict(self,img):
        img = np.asarray(img)
        img = cv2.resize(img, (32, 32))
        img = self.preProcessing(img)
        img = img.reshape(1, 32, 32, 1)

        classIndex = int(self.model.predict_classes(img))
        # print(classIndex)--
        predictions = self.model.predict(img)
        # print(predictions)
        probVal = np.amax(predictions)
        if probVal < self.threshold:
            return (0, probVal);
        else:
            return(classIndex, probVal)