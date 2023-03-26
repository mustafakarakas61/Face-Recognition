import cgi
from base64 import b64decode
import face_recognition

formData = cgi.FieldStorage()
faceMatch = 0

image = formData.getvalue("current_image")
email = formData.getvalue("email")
dataURI = image
header, encoded = dataURI.split(",", 1)
data = b64decode(encoded)

with open("image.png", "wb") as f:
    f.write(data)

gotImage = face_recognition.load_image_file("image.png")
existingImage = face_recognition.load_image_file("students/" + email + ".jpg")
gotImageFacialFeatures = face_recognition.face_encodings(gotImage)[0]

existingImageFacialFeatures = face_recognition.face_encodings(existingImage)[0]

results = face_recognition.compare_faces([existingImageFacialFeatures], gotImageFacialFeatures)

if results[0]:
    faceMatch = 1
else:
    faceMatch = 0

print("Content-Type: text/html")
print()

if faceMatch == 1:
    print("<script>alert('welcome ", email, " ')</script>")
else:
    print("<script>alert('Tanınmayan kişi.')</script>")
