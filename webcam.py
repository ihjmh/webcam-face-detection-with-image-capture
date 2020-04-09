#coding
import cv2
import sys
import logging as log
import datetime as dt
import time
from time import sleep
import itchat

# itchat
itchat.auto_login()
itchat.send('Hello, filehelper', toUserName='filehelper')

# detect face
cascPath = "haarcascade_frontalface_default.xml"
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)

def send_msg(filename):
    itchat.send_image(filename ,toUserName='filehelper')
    itchat.send(u'你背后有人', toUserName='filehelper')

def start_detect():
    anterior = 0
    faceCascade = cv2.CascadeClassifier(cascPath)
    # 上报人脸的阈值
    detect_length_max = 100
    detect_length_min = 10

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        face_length = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
        try:
            if len(faces) >0:
                face_length = x -y
                print("faces detected!! face_length:",face_length)
                if face_length < detect_length_max  and face_length > detect_length_min :
                    file_name = "images/"+time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))+".jpg"
                    # print ("the file_name is:",file_name)
                    cv2.imwrite(file_name,frame)
                    send_msg(file_name)
        except:
            pass

        # # Display the resulting frame
        # cv2.imshow('Video', frame)

        # if cv2.waitKey(1) & 0xFF == ord('s'): 
            
        #     check, frame = video_capture.read()
        #     cv2.imshow("Capturing", frame)
        #     cv2.imwrite(filename='saved_img.jpg', img=frame)
        #     video_capture.release()
        #     img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
        #     img_new = cv2.imshow("Captured Image", img_new)
        #     cv2.waitKey(1650)
        #     print("Image Saved")
        #     print("Program End")
        #     cv2.destroyAllWindows()
        
        #     break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Turning off camera.")
            video_capture.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

        # # Display the resulting frame
        # cv2.imshow('Video', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start_detect()
