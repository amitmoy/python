from camera import Camera, show_image, recognize_circles
import cv2
import numpy as np
from Circle import Circle

LOWER_RED = [0, 150, 150]
UPPER_RED = [70, 255, 255]
LOWER_GREEN = [26, 80, 80]
UPPER_GREEN = [100, 255, 255]

colorsToCatch = [('red', LOWER_RED, UPPER_RED), ('green', LOWER_GREEN, UPPER_GREEN)]
camera = Camera(0, colorsToCatch)

testCircle = Circle(399, 133, 25)

while True:
    frames = camera.catch_frame()
    redFrame = frames['red']
    greenFrame = frames['green']
    regularFrame = frames['regular']

    targetCircles = recognize_circles(redFrame)
    carCircle = recognize_circles(greenFrame)

    if carCircle is not None:
        for circle in carCircle:
            if testCircle.is_circle_touch(circle.x, circle.y, circle.radius):
                color = (0, 255, 255)
            else:
                color = (0, 255, 0)

            cv2.circle(regularFrame, center=(circle.x, circle.y), radius=circle.radius, color=color, thickness=2)
            cv2.putText(regularFrame, str(circle.get_angle(testCircle.x, testCircle.y)), (circle.x + 5, circle.y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                        (0, 0, 255))

    if targetCircles is not None:
        for circle in targetCircles:
            if testCircle.is_circle_touch(circle.x, circle.y, circle.radius):
                color = (0, 255, 255)
            else:
                color = (255, 0, 0)

            cv2.circle(regularFrame, center=(circle.x, circle.y), radius=circle.radius, color=color, thickness=2)
            cv2.putText(regularFrame, 'target', (circle.x + 5, circle.y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))

    cv2.circle(regularFrame, center=(testCircle.x, testCircle.y), radius=testCircle.radius, color=(255, 0, 255), thickness=2)
    show_image(regularFrame)



    if cv2.waitKey(300) == ord('a'):
        break

cv2.destroyAllWindows()
