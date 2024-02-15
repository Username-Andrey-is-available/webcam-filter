import cv2

# Функция для применения фильтра
def apply_filter(frame, filter_type):
    if filter_type == "gray":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == "red":
        red_channel = frame[:, :, 2]
        return cv2.merge([red_channel, red_channel, red_channel])
    elif filter_type == "blue":
        blue_channel = frame[:, :, 0]
        return cv2.merge([blue_channel, blue_channel, blue_channel])
    elif filter_type == "blur":
        return cv2.GaussianBlur(frame, (15, 15), 0)
    elif filter_type == "auto_white_balance":
        result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(result)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        result = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return result
    elif filter_type == "auto_contrast":
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

# Основная часть программы
cap = cv2.VideoCapture(0)  # 0 означает использование первой вебкамеры

current_filter = None

while True:
    ret, frame = cap.read()

    if current_filter is not None:
        filtered_frame = apply_filter(frame, current_filter)
        cv2.imshow("Filtered Webcam", filtered_frame)
    else:
        cv2.imshow("Original Webcam", frame)

    key = cv2.waitKey(1)

    # Переключение фильтров по нажатию клавиш
    if key == ord("1"):
        current_filter = "gray"
    elif key == ord("2"):
        current_filter = "red"
    elif key == ord("3"):
        current_filter = "blue"
    elif key == ord("4"):
        current_filter = "blur"
    elif key == ord("5"):
        current_filter = "auto_white_balance"
    elif key == ord("6"):
        current_filter = "auto_contrast"
    elif key == 27:  # Нажатие клавиши Esc для выхода
        break

cap.release()
cv2.destroyAllWindows()
