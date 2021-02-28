from camera import Camera, show_image, recognize_circles
import cv2
import numpy as np

LOWER_RED = [0, 50, 50]
UPPER_RED = [5, 255, 255]

colorsToCatch = [('red', LOWER_RED, UPPER_RED)]
camera = Camera(0, colorsToCatch)

while True:
    frames = camera.catch_frame()
    redFrame = frames['red']
    regularFrame = frames['regular']
    circles = recognize_circles(redFrame)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for circle in circles:
            cv2.circle(regularFrame, center=(circle[0], circle[1]), radius=circle[2], color=(0, 255, 0), thickness=2)
            cv2.putText(regularFrame, 'target', (circle[0] + 5, circle[1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255))

    show_image(regularFrame)

    if cv2.waitKey(33) == ord('a'):
        break

cv2.destroyAllWindows()
