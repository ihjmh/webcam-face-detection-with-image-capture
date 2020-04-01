#coding
import cv2
import sys
import logging as log
import datetime as dt
import time
from time import sleep
import itchat


log.basicConfig(filename='webcam.log',level=log.INFO)



class Watcher(object):
    """docstring for Watcher"""
    def __init__(self):
        # init camera
        # 上报人脸的阈值
        self.detect_length_max = 100
        self.detect_length_min = 10
        self.video_capture = cv2.VideoCapture(0)
        cascPath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        # init wechat
        self.itchat.auto_login()
        self.itchat.send('login success', toUserName='filehelper')
        self.TAGS_sent_wechat = False
        self.TIME_sent_wechat_time = None

    def inform_wechat(self,filename):
        # didnt sent too much msg to wechat
        if not self.TAGS_sent_wechat:
            itchat.send_image(filename ,toUserName='filehelper')
            itchat.send(u'你背后有人', toUserName='filehelper')
            self.TAGS_sent_wechat = True
            self.TIME_sent_wechat_time = time.time()
        now_time = time.time()
        delta_time = now_time - self.TIME_sent_wechat_time
        if delta_time>1:
            self.TAGS_sent_wechat = False
            self.TIME_sent_wechat_time = None

    def detect_face(self.frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )    
        return faces

    def check_face(self,frame,faces):
        # Draw a rectangle around the faces
        if len(faces) <0:
            return False,None
        # check whether the face in alert threshole
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_length = x - y
            print("faces detected!! face_length:",face_length)
            if face_length < self.detect_length_max  and face_length > self.detect_length_min :
                return True,frame
        return False,None

    def start_detect(self):
        while True:
            if not self.video_capture.isOpened():
                print('Unable to load camera.')
                sleep(5)
                continue
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()
            face_length = 0
            faces = self.detect_face(frame)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
            check_face_result_is_true,frame = self.check_face(frame,faces)

            if check_face_result_is_true:
                file_name = "images/"+time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))+".jpg"
                cv2.imwrite(file_name,frame)
                self.inform_wechat(filename)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Turning off camera.")
                self.video_capture.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

            # # Display the resulting frame
            # cv2.imshow('Video', frame)

        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    watcher = Watcher()
    watcher.start_detect()
