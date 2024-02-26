import cv2
import matplotlib.pyplot as plt

imagePath = 'kusay.jpg'

#Reads the image as Color Image (By fefault as BGR not RGB)
img = cv2.imread(imagePath)

# Convert to Gray Image for better computation efficiancy
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Load the Classifier
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Face detection
face = face_classifier.detectMultiScale(
    gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
)

# Drawing a Bounding Box
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)

# convert the image from the BGR format to RGB:
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


plt.figure(figsize=(20,10))
plt.imshow(img_rgb)
plt.axis('on')

plt.show()

#------------------------------------------------------------
print(gray_image.shape)
print(img.shape)