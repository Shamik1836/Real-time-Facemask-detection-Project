import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
Datadirectory="/content/drive/MyDrive/datasets/"
Classes=["WithMask","NoMask"]
training_Data=[]
img_size=224
def create_training_Data():
    
    for category in Classes:
        path=os.path.join(Datadirectory,category)
        class_num=Classes.index(category)
        for img in os.listdir(path):
            
            try:
                img_array=cv2.imread(os.path.join(path,img))
                new_array=cv2.resize(img_array,(img_size,img_size))
                training_Data.append([new_array,class_num])
            except Exception as e :
                pass
print(len(training_Data))
X=[]
y=[]
for features,label in training_Data:
    X.append(features)
    y.append(label)
X=np.array(X).reshape(-1,img_size,img_size,3)
X=X/255.0
Y=np.array(y)
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
model=tf.keras.applications.mobilenet.MobileNet() ##Pre trained model
base_input=model.layers[0].input
base_output=model.layers[-4].output
Flat_layer=layers.Flatten()(base_output)
final_output=layers.Dense(1)(Flat_layer)
final_output=layers.Activation('sigmoid')(final_output)
new_model=keras.Model(inputs=base_input,outputs=final_output)
new_model.compile(loss="binary_crossentropy",optimizer="adam",metrics=["accuracy"])
new_model.fit(X,Y,epochs=1,validation_split=0.1)
new_model.save('my_model.h5')
new_model=tf.keras.models.load_model('my_model.h5')
import cv2
path="haarcascade_frontalface_default.xml"
font_scale=1.5
font=cv2.FONT_HERSHEY_PLAIN
rectangle_bgr=(255,255,255)
img=np.zeros((500,500))
text="Some text in the box"
(text_width,text_height)=cv2.getTextSize(text,font,fontScale=font_scale,thickness=1)[0]
text_offset_x=10
text_offset_y=img.shape[0]-25
box_coords=((text_offset_x,text_offset_y),(text_offset_x+text_width+2,text_offset_y-text_height-2))
cv2.rectangle(img,box_coords[0],box_coords[1],rectangle_bgr,cv2.FILLED)
cv2.putText(img,text,(text_offset_x,text_offset_y),font,fontScale=font_scale,color=(0,0,0),thickness=1)
cap=cv2.VideoCapture(0)
if not cap.isOpened():
    cap=cv2.VideoCapture[0]
else:
    raise IOError("Cannot open Webcam")
while True:
    ret,frame=cv2.read()
    faceCascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.1, 4)
    for x,y,w,h in faces:
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=frame[y:y+h,x:x+w]
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        facess=faceCascade.detectMultiScale(roi_gray)
        if len(faces)==0:
            print("Face Not Detected")
        else:
            for (ex,ey,ew,eh) in faces:
                face_roi=roi_color[ey:ey+eh,ex:ex+ew]
    final_image=cv2.resize(face_roi,(224,224))
    final_image=np.expand_dims(final_image,axis=0)
    final_image=final_image/255.0
    font=cv2.FONT_HERSHEY_SIMPLEX
    Predictions=new_model.predict(final_image)
    font_scale=1.5
    font=cv2.FONT_HERSHEY_PLAIN
    if (Predictions>0):
        status="No Mask"
        x1,y1,w1,h1=0,0,175,75
        cv2.rectangle(frame,(x1,x1),(x1+w1,y1+h1),(0,0,0),-1)
        cv2.putText(frame,status,(x1+int(w1/10),y1+int(h1/2)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
    else:
        status="Face Mask"
        x1,y1,w1,h1=0,0,175,75
        cv2.rectangle(frame,(x1,x1),(x1+w1,y1+h1),(0,0,0),-1)
        cv2.putText(frame,status,(x1+int(w1/10),y1+int(h1/2)),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.putText(frame,status,(100,150),font,3,(0,0,255),2,cv2.LINE_4)    
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
cv2.imshow('Face Mask Detection',frame)
if cv2.waitKey(2) & 0xFF==ord('q'):
    break;
cap.release()
cv2.destroyAllWindows()
