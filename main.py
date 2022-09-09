import cv2
import math
import numpy as np
import time

fps_start = 0
fps =0

frameWidth = 720
frameHeight = 423

def Dark_channel(img, r):
    win_size = 2 * r + 1
    B, G, R = cv2.split(img)
    temp = cv2.min(cv2.min(B, G), R)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (win_size, win_size))
    dark = cv2.erode(temp, kernel)
    return dark

def AL_estimation(img, dark_channel):
    h, w = img.shape[:2]
    img_size = h * w
    num_pixel = int(max(math.floor(img_size / 1000), 1))

    img_temp = img.reshape(img_size, 3)
    dark_temp = dark_channel.reshape(img_size, 1)

    index = dark_temp[:, 0].argsort()
    index_use = index[img_size - num_pixel:]

    AL_sum = np.zeros([1, 3])
    for i in range(num_pixel):
        AL_sum = AL_sum + img_temp[index_use[i]]

    AL = AL_sum / num_pixel
    thread = np.array([[0.95, 0.95, 0.95]])
    A = cv2.min(AL, thread)
    return A

def Trans_estimation(img, A, r, omega):

    img_temp = np.empty(img.shape, img.dtype)
    for i in range(3):
        img_temp[:, :, i] = img[:, :, i] / A[0, i]
    trans = 1 - omega * Dark_channel(img_temp, r)
    return trans

def Guided_filter(I, p, r, eps):

    mean_I = cv2.boxFilter(I, cv2.CV_64F, (r, r))
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    corr_I = cv2.boxFilter(I * I, cv2.CV_64F, (r, r))
    corr_Ip = cv2.boxFilter(I * p, cv2.CV_64F, (r, r))

    var_I = corr_I - mean_I * mean_I
    cov_Ip = corr_Ip - mean_I * mean_p

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))

    q = mean_a * I + mean_b  #

    return q

def dehaze(img, r, n=20, thre=0.001, eps=0.001, omega=0.9):
    # img_pro = img.astype('float64')/255
    img_pro = np.float64(img) / 255
    J_dark = Dark_channel(img_pro, r)
    A = AL_estimation(img_pro, J_dark)
    t = Trans_estimation(img_pro, A, r, omega)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = np.float64(img_gray) / 255

    t_ref = Guided_filter(img_gray, t, r * n, eps)

    t_thre = cv2.max(t_ref, thre)
    result = np.empty(img_pro.shape, img_pro.dtype)
    for i in range(3):
        result[:, :, i] = (img_pro[:, :, i] - A[0, i]) / t_thre + A[0, i]

    return result

cap = cv2.VideoCapture(1)
frame_count = 0

while True:
    success, frame = cap.read()
    if success == False:
        break

    J = dehaze(frame, 5, n=8)
    frame = cv2.resize(frame, (frameWidth, frameHeight))
    J = cv2.resize(J, (frameWidth, frameHeight))

    fps_end = time.time()
    time_diff = fps_end - fps_start
    fps = 1 / (time_diff)
    fps_start = fps_end
    fps_text = "FPS:{:.2f}".format(fps)
    cv2.putText(J, fps_text, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 100), 2)

    cv2.imshow('Original Hazy', frame)
    cv2.imshow('Haze removed', J)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()