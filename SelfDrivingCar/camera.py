import cv2
import numpy as np
from Circle import Circle

def show_image(frameToShow):
    cv2.imshow('frame', frameToShow)


def recognize_circles(frame):
    grayColoredFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(grayColoredFrame, cv2.HOUGH_GRADIENT, 1.1, 150, param1=200, param2=20, minRadius=2, maxRadius=60)
    if circles is not None:
        fixedCircles = np.round(circles[0, :]).astype("int")
        res = []

        for circle in fixedCircles:
            res.append(Circle(circle[0], circle[1], circle[2]))

        return res


class Camera:

    def __init__(self, cameraSourceNumber, maskedFramesTuples):
        self.cv = cv2.VideoCapture(cameraSourceNumber)
        self.maskTuples = maskedFramesTuples
        # set resolution
        self.cv.set(3, 640)
        self.cv.set(4, 480)

    def catch_frame(self):
        succeed, frame = self.cv.read()
        if succeed:
            masksDictionary = {'regular': frame}
            for mask in self.maskTuples:
                frameConvertedToHSVColor = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                maskColorOnlyFrame = cv2.inRange(frameConvertedToHSVColor, np.array(mask[1]), np.array(mask[2]))
                oneColorFrame = cv2.bitwise_and(frame, frame, mask=maskColorOnlyFrame)

                # blurring the frame
                blurredOneColorFrame = cv2.GaussianBlur(oneColorFrame, (5, 5), 2, 2)

                masksDictionary[mask[0]] = blurredOneColorFrame

            return masksDictionary
        else:
            return False
