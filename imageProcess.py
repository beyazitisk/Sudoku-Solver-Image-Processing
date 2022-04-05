import cv2
import numpy as np
from tensorflow.keras.models import load_model


class ImageProcesser():
    model = load_model("modelTrained.h5")
    iniParamters_boxfind = [8, 8]
    iniParamters_solution = [15, 25]
    list_sudo = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def preProcessing(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img = cv2.equalizeHist(img)
        img = img / 255
        return img

    def predict(self, img):
        threshold = 0.8
        img = np.asarray(img)
        img = cv2.resize(img, (32, 32))
        img = self.preProcessing(img)
        img = img.reshape(1, 32, 32, 1)

        classIndex = int(self.model.predict_classes(img))
        # print(classIndex)--
        predictions = self.model.predict(img)
        # print(predictions)
        probVal = np.amax(predictions)
        if probVal < threshold:
            return (0, probVal)
        else:
            return(classIndex, probVal)

    def stackImages(self, scale, imgArray):  # COMPACTOR OF IMAGES
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(
                            imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                    None, scale, scale)
                    if len(imgArray[x][y].shape) == 2:
                        imgArray[x][y] = cv2.cvtColor(
                            imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank] * rows
            hor_con = [imageBlank] * rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(
                        imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                             scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor
        return ver  # b
    # def box_find(self,boxes,counter):
    #     confg = r'--oem 3 --psm 6 outputbase digits'
    #     cv2.imwrite('C:/Users/byzt/PycharmProjects/SudokuDetect/COLLECTOR/output{}.png'.format(counter),boxes)
    #     text = pytesseract.image_to_string(boxes, config=confg)
    #     print(text) #Predicted number in the box
    #     try:
    #         if int(text) != 0:
    #             ImageProcesser.list_sudo[ImageProcesser.iniParamters_boxfind[0]][ImageProcesser.iniParamters_boxfind[1]] = int(text)
    #             ImageProcesser.iniParamters_boxfind[0] = ImageProcesser.iniParamters_boxfind[0] - 1
    #             if ImageProcesser.iniParamters_boxfind[0] < 0:
    #                 ImageProcesser.iniParamters_boxfind[0] =8
    #                 ImageProcesser.iniParamters_boxfind[1] = ImageProcesser.iniParamters_boxfind[1] - 1
    #     except:
    #         ImageProcesser.iniParamters_boxfind[0] -= 1
    #         if ImageProcesser.iniParamters_boxfind[0] < 0:
    #             ImageProcesser.iniParamters_boxfind[0] = 8
    #             ImageProcesser.iniParamters_boxfind[1] -= 1

    def boxFind(self, box):
        digit, predictValue = self.predict(box)
        print(digit, predictValue)

        ImageProcesser.list_sudo[ImageProcesser.iniParamters_boxfind[0]
                                 ][ImageProcesser.iniParamters_boxfind[1]] = digit
        ImageProcesser.iniParamters_boxfind[0] = ImageProcesser.iniParamters_boxfind[0] - 1
        if ImageProcesser.iniParamters_boxfind[0] < 0:
            ImageProcesser.iniParamters_boxfind[0] = 8
            ImageProcesser.iniParamters_boxfind[1] = ImageProcesser.iniParamters_boxfind[1] - 1

    def getContours(self, img_canny, img_contour):  # It takes canny image then finds shapes
        countours, hiearchy = cv2.findContours(
            img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        counter = 0  # Small sudoku square counter to be sure it is 81
        for cnt in countours:
            area = cv2.contourArea(cnt)
            print(area)
            # Threshold values for square areas to be sure it takes only the smallest square
            if (3700 < area < 7100):
                cv2.drawContours(img_contour, cnt, -2, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objcor = (len(approx))
                x, y, w, h = cv2.boundingRect(approx)
                cv2.rectangle(img_contour, (x, y),
                              (x + w, y + h), (255, 0, 0), 1)
                self.boxFind(img_contour[x + 3:x + w,
                                         y:y + h - 4])  # Small square images getting cropped a little bit to get rid of some of the unneccessery lines
                # To see the boxes
                cv2.imshow("Cell", img_contour[x + 3:x + w, y:y + h - 4])
                cv2.imshow("Unresolved", img_contour)
                cv2.waitKey(5)  # To dont skip boxes too fast
                counter += 1
        print(counter)

    def preProcessor(self, img_path, sol_path):
        # solution paper gets resizement and original image transformed into the canny image
        global img, imgCanny, imgContour
        img = cv2.imread(img_path)
        solution_paper = cv2.imread(sol_path)
        resized_solution_paper = cv2.resize(solution_paper, (400, 400))
        imgContour = img.copy()
        # For good results dont touch the threshold values
        imgCanny = cv2.Canny(img, 500, 600)
        self.getContours(imgCanny, imgContour)
        return resized_solution_paper

    def solution_processer(self, solution_list, index_list, solution_paper):
        for i in range(0, 9):
            for j in range(0, 9):
                if (i, j) in index_list:
                    cv2.putText(solution_paper, "{}".format(solution_list[i][j]),
                                (ImageProcesser.iniParamters_solution[0],
                                 ImageProcesser.iniParamters_solution[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    ImageProcesser.iniParamters_solution[0] += 43
                else:
                    cv2.putText(solution_paper, "{}".format(solution_list[i][j]), (ImageProcesser.iniParamters_solution[0],
                                                                                   ImageProcesser.iniParamters_solution[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    ImageProcesser.iniParamters_solution[0] += 43

            if ImageProcesser.iniParamters_solution[0] >= 380:
                ImageProcesser.iniParamters_solution[1] += 46
                ImageProcesser.iniParamters_solution[0] = 15
        return solution_paper
