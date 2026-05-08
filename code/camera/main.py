import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Get the first camere available

ROI_LENGTH = 100


def main():
    i = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        # Define the roi (region of interest)

        h, w = frame.shape[:2] # ?
        cx, cy = w // 2, h // 2

        size = ROI_LENGTH // 2

        x1, y1 = cx - size, cy - size
        x2, y2 = cx + size, cy + size

        roi = frame[y1:y2, x1:x2]

        # Draw the rectangle wit the coordinates of the roi
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

        # Transform the roi colors from bgr to hsv
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Define the upper bound and the lower bound colors that the pixel must have to be considered blue
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Create a mash with
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # This will return a frame showing the real color of the pixel that in the mask have a value of 1. If in the mask they have a value of 0 then the pixel is black
        result = cv2.bitwise_and(roi, roi, mask=mask)

        count = cv2.countNonZero(mask)

        total = roi.shape[0] * roi.shape[1]

        percentage = count / total

        if (percentage > 0.50):
            cv2.putText(frame, f"Color: blue", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Color: none", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
