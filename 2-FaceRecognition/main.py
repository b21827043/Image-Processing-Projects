import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import face_recognition

#Encoding face and their names.
known_face_encoding = []
known_face_names = []


def build_encoded_images(path):

    name_of_files = [f for f in listdir(path) if isfile(join(path, f))]
    len_image = len(name_of_files)
    print("{} images found.".format(len_image))

    for name in name_of_files:
        image = cv2.imread(path+name)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_encoding = face_recognition.face_encodings(rgb_image)[0]
        known_face_encoding.append(image_encoding)
    print("Encoding images loaded.")

    global known_face_names
    known_face_names = [x.split('.')[0] for x in name_of_files]

# Detect face
def detect_face(known_face_encodings,known_face_names,frame):


    frame_resize = 0.25
    small_frame = cv2.resize(frame, (0, 0), fx=frame_resize, fy=frame_resize)

    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)


    face_locations = np.array(face_locations)
    face_locations = face_locations / frame_resize
    return face_locations.astype(int), face_names




# Creates encoded images.
build_encoded_images("images/")


# Load Camera
cap = cv2.VideoCapture(0)



# Show camera on screen.
while True:

    ret, frame = cap.read()


    # Detect face
    face_locations , names = detect_face(known_face_encoding,known_face_names,frame)

    for face_loc, name in zip(face_locations, names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

    cv2.imshow("Frame",frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()