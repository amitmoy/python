from camera import Camera, show_image, recognize_circles
import cv2
import serial
import time
import numpy as np
from Circle import Circle
from Car import Car

LOWER_RED = [0, 150, 150]
UPPER_RED = [70, 255, 255]
LOWER_GREEN = [60, 50, 50]
UPPER_GREEN = [100, 255, 255]

colorsToCatch = [('red', LOWER_RED, UPPER_RED), ('green', LOWER_GREEN, UPPER_GREEN)]

#### init ####
camera = Camera(0, colorsToCatch)

serial = serial.Serial('COM4', 9600)

arduino = Car(0, 0, serial)

frames = camera.catch_frame()

targetCircles = []

while len(targetCircles) < 1:
    frames = camera.catch_frame()
    show_image(frames['regular'])
    print('trying find target')
    redFrame = frames['red']
    targetCircles = recognize_circles(redFrame)
    time.sleep(0.2)


target = targetCircles[0]
target.radius = target.radius+50
print('target found', target)


#### navigation ####

while True:

    frames = camera.catch_frame()
    redFrame = frames['red']
    greenFrame = frames['green']
    regularFrame = frames['regular']

    targetCircles = recognize_circles(redFrame)
    carCircle = recognize_circles(greenFrame)

    cv2.circle(regularFrame, center=(target.x, target.y), radius=target.radius, color=(255,0,0), thickness=5)

    if len(carCircle) > 0:

        arduino.set_circle(carCircle[0])

        for circle in carCircle:
            if target.is_circle_touch(circle.x, circle.y, circle.radius):
                color = (0, 255, 255)
            else:
                color = (0, 255, 0)

            cv2.circle(regularFrame, center=(circle.x, circle.y), radius=circle.radius, color=color, thickness=2)
            cv2.putText(regularFrame, str(circle.get_angle(target.x, target.y)), (circle.x + 5, circle.y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (0, 0, 255))
            cv2.line(regularFrame, (circle.x, circle.y), (target.x, target.y), (255, 255, 200), 2)

    show_image(regularFrame)
    if cv2.waitKey(100) == ord('a'):
        break

    if len(carCircle) > 0:
        if not arduino.is_circle_touch(target.x, target.y, target.radius):
            arduino.drive_forward()
        else:
            arduino.stop()
            break


while True:
    frames = camera.catch_frame()
    cv2.putText(regularFrame, "FINISHEDDDD", (250,250),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                (0, 255, 255))
    show_image(regularFrame)
    if cv2.waitKey(100) == ord('a'):
        break