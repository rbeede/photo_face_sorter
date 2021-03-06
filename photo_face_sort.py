#!/usr/bin/env python3

# https://www.rodneybeede.com

# Inception: 2022


# Based off https://github.com/ageitgey/face_recognition/issues/359
# but kept it to using only a single CPU so running on a Raspberry Pi
# or other shared-system would not consume all the CPU.
# It takes longer but only uses 1 core on a multi-user system.


# Raspberry Pi 4+ install trick
#
# sudo apt-get install -y cmake
# sudo apt-get install -y python3-pip
# sudo pip3 install face_recognition
# sudo pip3 install pathlib




# https://github.com/ageitgey/face_recognition
import face_recognition

import argparse
from pathlib import Path
import glob



# If filename has a face (only looks at first face in the image) that has been seen before
# then it returns the index code for that face
# If filename has no recognized faces then it returns the last index of faces where the new face is stored
# If filename had no faces returns negative
def add_faces(filename, existing_faces):
    image = face_recognition.load_image_file(filename)
    encodings = face_recognition.face_encodings(image)
    
    if not encodings:
        # no faces found so return negative number
        return -2147483648
        
    first_face = encodings[0]

    for i, existing_encoding in enumerate(existing_faces):
        if face_recognition.compare_faces([existing_encoding], first_face)[0]:
            return i  # The face in filename matched a previous filename's face so return the index code

    # Never seen a matching face (new face) so return last index where it is stored
    existing_faces.append(first_face)
    return len(existing_faces) - 1


def main(args):
    print(f"Searching directory {args.directory} for images and faces")

    faces = []

    for photo_file in Path(args.directory).rglob('*'):
        # We only want to iterate once so check for multiple file-types here
        if not photo_file.suffix.lower() in ['.png','.jpg']:
            continue
        else:
            print(f"Looking at file {photo_file}", flush=True)

            # modifies global  faces[]
            face_idx = add_faces(photo_file, faces)

            print(f"{photo_file}\t{face_idx}", flush=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='https://www.rodneybeede.com/')

    parser.add_argument('--directory', required=True, action='store', type=Path, help='Directory to recurse for image files')

    args = parser.parse_args()

    main(args)