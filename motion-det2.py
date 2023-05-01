import threading
import cv2  # pip install opencv-python
# import imutils  #pip install imutils
import time
# importing mail module
from send_mail import prepare_and_send_email

# start the webcam
cap= cv2.VideoCapture(0)
# cap = cv2.flip(1)
# cap = cv2.flip(cap1,1)

# skipping the first frame
_, _ = cap.read()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Considering the width as 640
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Considering the height as 480

# reading the 2nd frame
_, start_frame = cap.read()
start_frame = cv2.resize(start_frame, (500, 480))  # Resize the first frame
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)  # Change the color image to gray scale image
# cv2.imshow("cam" , start_frame)
# cv2.waitKey(5000)
start_frame = cv2.GaussianBlur(start_frame, (5, 5), 0)  # Smoothen the image ie;blur
# cv2.imshow("cam" , start_frame)
# cv2.waitKey(5000)

next_send_mail = True
count_frame = 0  # to keep track of frames in which motion is observed


def alert(frame):
    global next_send_mail
    next_send_mail = False
    prepare_and_send_email('cai20002@gmail.com',
                           'kumarsubham373@gmail.com',
                           'Alert Alert Alert',
                           'Hi this is Shubham \n\n sending alert mail for motion detection',
                           frame)
    time.sleep(120)
    next_send_mail = True


def motion_detection():
    global count_frame, start_frame, next_send_mail
    while True:
        success, frame = cap.read()  # Reads the frame
        if success:
            frame = cv2.resize(frame, (500, 480))  # resize the frame to width 500
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # change color to gray scale
            # cv2.imshow("cam" , gray_frame)
            # cv2.waitKey(5000)
            gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)  # it will smoothen the image

            difference = cv2.absdiff(gray_frame,
                                     start_frame)  # it will find the absolute difference two gray scaled images
            '''
            difference depicts difference in the pixels of two images'''
            # print(difference)
            # print(type(difference))
            threshold = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)[1]
            '''
            Applied general thresholding
            para1 : image,
            para2 : threshold value it lies [0,255],
            para3 : max value of pixel,
            para4 : type of  thresholding - simple 
            
            return:
            first-op : the threshold value,
            second-op : the threshold image'''
            # print(type(threshold))
            # print(threshold)
            threshold = cv2.dilate(threshold, None, iterations=3)
            '''
            '''
            cnts, res = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # print(cnts)
            # contours are the boundaries that separate an object from its background.
            for contour in cnts:
                if cv2.contourArea(contour) >= 3000:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    frame = cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 3)
                    '''cv2.putText(frame, "STATUS: {}".format('MOTION DETECTED'), (5, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (217, 10, 10), 2)'''

            '''for contour in cnts:
                if cv2.contourArea(contour) >= 1500:
                    count_frame += 1
                    if count_frame >= 5 and next_send_mail is True:
                        count_frame = 0
                        thread_1 = threading.Thread(target=Alert, args=(frame_copy,))
                        thread_1.start()
                
                    (x,y,w,h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame , (x,y) ,((x+w) , (y+h)) , (0,255,0) , 3)
                    cv2.putText(frame, "STATUS: {}".format('MOTION DETECTED'), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (217, 10, 10), 2)'''

            if threshold.sum() > 100:  # threshold.sum() is the sum of the pixels
                if count_frame < 5:
                    count_frame += 1
                elif count_frame == 5 and next_send_mail is True:
                    frame = cv2.putText(frame, "STATUS: {}".format('MOTION DETECTED'), (10, 60),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (0, 0, 255), 2)  # (217,10,10)
                    # time.sleep(30)
                    threading.Thread(target=alert,
                                     args=(frame,)).start()
                    count_frame = 0

            cv2.imshow("stream", frame)
            start_frame = gray_frame
            # key_pressed = cv2.waitKey(0)
            # key = cv2.waitKey(0)

        k = cv2.waitKey(1) & 0xff
        if k == 27: 
            break
    cap.release()
    cv2.destroyAllWindows()


if not cap.isOpened():
    print("Error: Could not connect to your camera.Kindly try again")
else:
    motion_detection()
