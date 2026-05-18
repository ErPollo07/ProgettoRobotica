import cv2
import numpy as np

#cap = cv2.VideoCapture(0) # Get the first camere available

roi_length = 100

masks = {
    "blue": [
        (np.array([90,   50,  50]), np.array([130, 255, 255]))
    ],
    "red": [
        (np.array([160,   90,  0]), np.array([179, 255, 255])),
        (np.array([0,   90,  0]), np.array([10, 255, 255])),
    ],
    "green": [
        (np.array([40,   90,  0]), np.array([100, 255, 255])),
    ]
}


def get_color() -> str | None:
    colors_percentage = {}

    cap = cv2.VideoCapture(0) # Get the first camere available

    _, frame = cap.read()

    # Define the roi (region of interest)
    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2

    size = roi_length // 2

    x1, y1 = cx - size, cy - size
    x2, y2 = cx + size, cy + size

    # Slice the frame between the two point
    roi = frame[y1:y2, x1:x2]

    # Calculate the total number of the pixel in the roi
    total = roi.shape[0] * roi.shape[1]

    # Draw the rectangle wit the coordinates of the roi
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

    # Calculate the color only when "g" is pressed

    # Transform the roi colors from bgr to hsv
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Cycle through every color that we have to detect
    # Calculate the mask with lower and upper values
    # Calculate the percentage cover by every color
    for color, ranges in masks.items():
        m = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lo, hi) in ranges:
            current_mask = cv2.inRange(hsv, lo, hi)
            m = cv2.bitwise_or(m, current_mask)

        count = cv2.countNonZero(m)
        percentage = count / total

        colors_percentage[color] = percentage

    # Sort the percentage to get the most present color
    colors_percentage = dict(sorted(colors_percentage.items(), key=lambda item: item[1], reverse=True))
    first_key, first_value = next(iter(colors_percentage.items()))


    cap.release()
    cv2.destroyAllWindows()

    if (first_value > 0.70):
        return first_key
    else:
        return None

def main():
    colors_percentage = {}

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        # Define the roi (region of interest)
        h, w = frame.shape[:2] # ?
        cx, cy = w // 2, h // 2

        size = roi_length // 2

        x1, y1 = cx - size, cy - size
        x2, y2 = cx + size, cy + size

        roi = frame[y1:y2, x1:x2]

        total = roi.shape[0] * roi.shape[1]

        # Draw the rectangle wit the coordinates of the roi
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

        # Transform the roi colors from bgr to hsv
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Cycle through every color that we have to detect
        # Calculate the mask with lower and upper values
        # Calculate the percentage cover by every color
        for color, ranges in masks.items():
            m = np.zeros(hsv.shape[:2], dtype=np.uint8)
            for (lo, hi) in ranges:
                current_mask = cv2.inRange(hsv, lo, hi)
                m = cv2.bitwise_or(m, current_mask)

            count = cv2.countNonZero(m)
            percentage = count / total

            colors_percentage[color] = percentage

        # Sort the percentage to get the most present color
        colors_percentage = dict(sorted(colors_percentage.items(), key=lambda item: item[1], reverse=True))
        first_key, first_value = next(iter(colors_percentage.items()))

        # check if the most present color is present enough
        if (first_value > 0.750):
            cv2.putText(frame, f"Color: {first_key}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, f"Color: none", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
