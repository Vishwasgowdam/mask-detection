from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from PIL import  ImageTk, Image
import tkinter
import os
from tkinter import messagebox
from pygame import mixer
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import pygame
z=0
a=0
b=0
d=0
e=0

def Img():
    r = Toplevel()
    r.title("About Us")

    canvas = Canvas(r, height=600, width=600)
    canvas.pack()
    my_image = PhotoImage(file=r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\aboutus.png", master= window)
    canvas.create_image(0, 0, anchor=NW, image=my_image)
    r.mainloop()

def Play_music():
    pygame.mixer.music.load('narration.mpeg')
    pygame.mixer.music.play()

def Pause_music():
    pygame.mixer.music.pause()

def Ok():
    uname = t1.get()
    password = t2.get()

    if (uname == "" and password == ""):
        messagebox.showinfo("", "Blank Not allowed")


    elif (uname == "admin" and password == "123"):

        messagebox.showinfo("", "Login Success")
        window.destroy()
        admin = Tk()
        admin.title("Welcome Admin")
        admin.geometry("600x600")

        def Cmds():
            r = Toplevel()
            r.title("User Manual")

            canvas = Canvas(r, height=669, width=1200)
            canvas.pack()
            my_image = PhotoImage(file=r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\manual.png", master=admin)
            canvas.create_image(0, 0, anchor=NW, image=my_image)
            r.mainloop()
        
        def live_cam():
            capture = cv2.VideoCapture(0)

            while (True):

                ret, frame = capture.read()

                cv2.imshow('video', frame)

                if cv2.waitKey(1) == 27:
                    break

            capture.release()
            cv2.destroyAllWindows()

        def open_folder():
            os.startfile(r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\database")
            pass

        def auto():
            global a
            a = 1
            print("auto screenshot enabled")
            pass

        def no_auto():
            global a
            a = 0
            print("auto screenshot disabled")
            pass
        def no_buzzer():
            global d
            d=0
            print("buzzer disabled")
            pass
        def buzzer():
            global d
            d=1
            print("buzzer enabled")
            pass   
        def no_ann():
            global e
            e=0
            print("announcement disabled")
            pass
        def ann():
            global e
            e=1
            print("announcement enabled")
            pass   

        def detect():

            def detect_and_predict_mask(frame, faceNet, maskNet):
                # grab the dimensions of the frame and then construct a blob
                # from it
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                             (104.0, 177.0, 123.0))

                # pass the blob through the network and obtain the face detections
                faceNet.setInput(blob)
                detections = faceNet.forward()
                print(detections.shape)

                # initialize our list of faces, their corresponding locations,
                # and the list of predictions from our face mask network
                faces = []
                locs = []
                preds = []

                # loop over the detections
                for i in range(0, detections.shape[2]):
                    # extract the confidence (i.e., probability) associated with
                    # the detection
                    confidence = detections[0, 0, i, 2]

                    # filter out weak detections by ensuring the confidence is
                    # greater than the minimum confidence
                    if confidence > 0.5:
                        # compute the (x, y)-coordinates of the bounding box for
                        # the object
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # ensure the bounding boxes fall within the dimensions of
                        # the frame
                        (startX, startY) = (max(0, startX), max(0, startY))
                        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                        # extract the face ROI, convert it from BGR to RGB channel
                        # ordering, resize it to 224x224, and preprocess it
                        face = frame[startY:endY, startX:endX]
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                        face = cv2.resize(face, (224, 224))
                        face = img_to_array(face)
                        face = preprocess_input(face)

                        # add the face and bounding boxes to their respective
                        # lists
                        faces.append(face)
                        locs.append((startX, startY, endX, endY))

                # only make a predictions if at least one face was detected
                if len(faces) > 0:
                    # for faster inference we'll make batch predictions on *all*
                    # faces at the same time rather than one-by-one predictions
                    # in the above `for` loop
                    faces = np.array(faces, dtype="float32")
                    preds = maskNet.predict(faces, batch_size=32)

                # return a 2-tuple of the face locations and their corresponding
                # locations
                return (locs, preds)

            # load our serialized face detector model from disk
            prototxtPath = r"face_detector\deploy.prototxt"
            weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
            faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

            # load the face mask detector model from disk
            maskNet = load_model("mask_detector.model")

            mixer.init()
            sound = mixer.Sound('alarm.wav')
#             announce= mixer.Sound('announce.mp3')
            announce= mixer.Sound('girl.mpeg')
            def screenshot(vs):
                global z
                z += 1

                cv2.imshow("screenshot", vs.read())
                outfile = r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\database\%i.jpg" % (z)
                cv2.imwrite(outfile, vs.read())  # or saves it to disk

                cv2.destroyAllWindows()

            def auto_ss(b):
                global a
                if (a == 1 and b % 10 == 0):
                    screenshot(vs)
            def auto_announce(b):
                global a
                if ( e == 1 and b%30 == 0):        
                    announce.play()
                    print ("announce")
                    pass
            # initialize the video stream
            print("[INFO] starting video stream...")
            vs = VideoStream(src=0).start()

            # loop over the frames from the video stream
            while True:
                # grab the frame from the threaded video stream and resize it
                # to have a maximum width of 400 pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                # detect faces in the frame and determine if they are wearing a
                # face mask or not
                (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

                # global a,b
                #                 print (a,b)

                # loop over the detected face locations and their corresponding
                # locations
                for (box, pred) in zip(locs, preds):
                    # unpack the bounding box and predictions
                    (startX, startY, endX, endY) = box
                    (mask, withoutMask) = pred
                    #                     global a,b

                    # determine the class label and color we'll use to draw
                    # the bounding box and text
                    label = "Mask" if mask > withoutMask else "No Mask"
                    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                    if (label == "Mask"):
                        print("No Beep")


                    else:
                        global d
                        if d==1:                        
                            sound.play()
                            print("Beep")
                        global b
                        b += 1
                        auto_ss(b)
                        auto_announce(b)

                    # include the probability in the label
                    label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                    # display the label and bounding box rectangle on the output
                    # frame
                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                # show the output frame
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
                if key == ord('c'):  # calls screenshot function when 'c' is pressed
                    screenshot(vs)
            # do a bit of cleanup
            cv2.destroyAllWindows()
            vs.stop()

        D = Canvas(bg="blue", height=850, width=300)
        filename = PhotoImage(file=r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\bg.png")
        background_label = Label(image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1.15)

        load2 = Image.open(r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\gt1.png")
        photo2 = ImageTk.PhotoImage(load2)

        header1 = tk.Button(admin, image=photo2)
        header1.place(x=5, y=0)

        canvas2 = Canvas(admin, width=400, height=350, bg="gray")
        canvas2.place(x=100, y=100)

        l3 = tk.Label(canvas2, text="Camera Feed", font=("Calibiri", 12), bg='teal',bd='5')
        l3.place(x=30, y=15)
        #Label(admin, text="camera feed").place(x=10, y=10)
        #Button(admin, text="start", command=live_cam, height=1, width=13).place(x=180, y=10)
        b2 = tk.Button(canvas2, text="      Start      ", font=("Calibiri", 10), bg="red", command=live_cam)
        b2.place(x=240, y=15)


        #Label(admin, text="mask detection").place(x=10, y=40)
        #button(admin, text="start", command=detect, height=1, width=13).place(x=180, y=40)
        l4 = tk.Label(canvas2, text=" Mask Detect ", font=("Calibiri", 12), bg='teal',bd='5')
        l4.place(x=30, y=65)
        # Label(admin, text="camera feed").place(x=10, y=10)
        # Button(admin, text="start", command=live_cam, height=1, width=13).place(x=180, y=10)
        b3 = tk.Button(canvas2, text="      Start      ", font=("Calibiri", 10), bg="red", command=detect)
        b3.place(x=240, y=65)

        l5 = tk.Label(canvas2, text=" Database Folder ", font=("Calibiri", 12), bg='teal',bd='5')
        l5.place(x=30, y=115)
        b4 = tk.Button(canvas2, text="      Open      ", font=("Calibiri", 10), bg="red", command=open_folder)
        b4.place(x=240, y=115)

        l6 = tk.Label(canvas2, text="Automatic Screenshot", font=("Calibiri", 12), bg='teal',bd='5')
        l6.place(x=30, y=175)
        b5 = tk.Button(canvas2, text="Enable", font=("Calibiri", 10), bg="red", command=auto)
        b5.place(x=230, y=175)
        b6 = tk.Button(canvas2, text="Disable", font=("Calibiri", 10), bg="red", command=no_auto)
        b6.place(x=294, y=175)
        
        l7 = tk.Label(canvas2, text="Buzzer Alarm", font=("Calibiri", 12), bg='teal',bd='5')
        l7.place(x=30, y=235)
        b7 = tk.Button(canvas2, text="Enable", font=("Calibiri", 10), bg="red", command=buzzer)
        b7.place(x=230, y=235)
        b8 = tk.Button(canvas2, text="Disable", font=("Calibiri", 10), bg="red", command=no_buzzer)
        b8.place(x=294, y=235)
        
        l8 = tk.Label(canvas2, text="Automatic Announcement", font=("Calibiri", 12), bg='teal',bd='5')
        l8.place(x=30, y=295)
        b9 = tk.Button(canvas2, text="Enable", font=("Calibiri", 10), bg="red", command=ann)
        b9.place(x=230, y=295)
        b10 = tk.Button(canvas2, text="Disable", font=("Calibiri", 10), bg="red", command=no_ann)
        b10.place(x=294, y=295)

        b11 = tk.Button(admin, text="User Manual", font=("Calibiri", 12), bg="green",command=Cmds)
        b11.place(x=450, y=555)
        
        
        
        admin.mainloop()

    else:
        messagebox.showinfo("", "Incorrent Username and Password")

window=tk.Tk()
window.title("Mask Detection")

load5=Image.open("play.png")
play=ImageTk.PhotoImage(load5)
load6=Image.open("pause.png")
pause=ImageTk.PhotoImage(load6)

C = Canvas(bg="blue", height=850, width=300)
filename = PhotoImage(file=r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\bg2.png ")
background_label = Label(image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1.3)

load1=Image.open(r"C:\Users\artem\Desktop\project\trial\experiment\Face-Mask-Detection-master\GUI\gt1.png")
photo1=ImageTk.PhotoImage(load1)


header=tk.Button(window, image=photo1)
header.place(x=5,y=0)


canvas1=Canvas(window,width=350, height=150, bg="gray")
canvas1.place(x=100,y=200)


l1=tk.Label(canvas1, text="Username", font=("Calibiri",12),bg="orange")
l1.place(x=50,y=35)
t1=tk.Entry(canvas1, width=25,bd=2)
t1.place(x=150,y=35)

l2=tk.Label(canvas1, text="Password", font=("Calibiri",12),bg="orange")
l2.place(x=50,y=65)
t2=tk.Entry(canvas1, width=25,bd=2)
t2.place(x=150,y=65)
t2.config(show="*")

b1=tk.Button(canvas1,text="Login", font=("Calibiri",12),bg="red", command=Ok )
b1.place(x=180,y=105)

b8=tk.Button(window,text="About Us", font=("Calibiri",12),bg="green",command=Img)
b8.place(x=480,y=365)

lel=tk.Label(window, text="Made By TES-35", font=("Calibiri",12),bg="orange")
lel.place(x=0,y=372)

btn12=Button(window,text='Play', width=14,image=play, command=Play_music)
btn12.place(x=10,y=180)


btn13=Button(window, width=14,text='Pause', image=pause, command=Pause_music)
btn13.place(x=10,y=270)




window.geometry("620x400")
window.mainloop()