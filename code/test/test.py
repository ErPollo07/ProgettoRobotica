import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")

cv2.createTrackbar("LH", "Trackbars", 0, 179, lambda x: None)
cv2.createTrackbar("LS", "Trackbars", 0, 255, lambda x: None)
cv2.createTrackbar("LV", "Trackbars", 0, 255, lambda x: None)

cv2.createTrackbar("UH", "Trackbars", 179, 179, lambda x: None)
cv2.createTrackbar("US", "Trackbars", 255, 255, lambda x: None)
cv2.createTrackbar("UV", "Trackbars", 255, 255, lambda x: None)

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")

    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    lower = np.array([lh, ls, lv])
    upper = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
