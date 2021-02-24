# Creating database 
# It captures images and stores them in datasets  
# folder under the folder name of sub_data
import mysql.connector
import cv2, sys, numpy, os 
haar_file = 'haarcascade_frontalface_default.xml'
# All the faces data will be 
#  present this folder 
datasets = 'datasets'  

#Entering User ID
uid=input('Enter Student ID\n')
  
# These are sub data sets of folder,  

# change the label here 
sub_data = uid     
path = os.path.join(datasets, sub_data) 
if not os.path.isdir(path): 
    os.mkdir(path)  
# defining the size of images  
(width, height) = (130, 100) 

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

img_counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    k = cv2.waitKey(1)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(130, 100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('%s'%(uid), frame)

    if k%256 == 27: #ESC Pressed
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "{}.png".format(uid)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))
        cv2.imwrite('% s/% s.png' % (path, uid), face_resize)
        img_counter += 1
        

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

imgpath='%s.png' % (uid,)
#Saving student image data
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database="atten"
)

#getting student number
mycursor = mydb.cursor()

sql = "SELECT std_num FROM student_data WHERE std_id = (%s)" % (uid,)

mycursor.execute(sql)

myresult = mycursor.fetchall()

for x in myresult:
  stdnum=x

mycursor = mydb.cursor()

sql = "INSERT INTO student_img (img_path, std_num) VALUES ('%s',%s)" % (imgpath,x[0])
mycursor.execute(sql)
mydb.commit()

print(mycursor.rowcount, "was inserted.")

