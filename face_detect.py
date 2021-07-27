import sys
import dlib
import cv2
import secrets
import os

if len(sys.argv) < 3:
    print(
        "Call this program like this:\n"
        f"python {os.path.basename(__file__)} Format:0-img/1-vid Path:*.jpg/*.mp4\n"
        )
    exit()
   

MODEL_PATH = '/mnt/c/Users/titus/webapps/vanilla/cnn/mmod_human_face_detector.dat'
PRED_PATH = '/mnt/c/Users/titus/webapps/vanilla/cnn/shape_predictor_5_face_landmarks.dat'
FACE_PATH = 'data/faces/' 
try:
    cnn_face_detector = dlib.cnn_face_detection_model_v1(MODEL_PATH)
    sp = dlib.shape_predictor(PRED_PATH)
except Exception as error:
    print(f'{error}')
    exit()

def extractFaces(img, des):
    # The 1 in the second argument indicates that we should upsample the image
    # 1 time.  This will make everything bigger and allow us to detect more
    # faces.
    faces = cnn_face_detector(img, 1)
    
    if len(faces) == 0:
        print("Sorry, there were no faces found in '{}'".format(img))
        return
    # Find the 5 face landmarks we need to do the alignment.
    face_features = dlib.full_object_detections()
    for features in faces:
        features = features.rect
        face_features.append(sp(img, features))
    
    print(dlib.DLIB_USE_CUDA)
    window = dlib.image_window()
    images = dlib.get_face_chips(img, face_features, size=320)
    for image in images:
        window.set_image(image)
        dlib.hit_enter_to_continue()

    '''
    This detector returns a mmod_rectangles object. This object contains a list of mmod_rectangle objects.
    These objects can be accessed by simply iterating over the mmod_rectangles object
    The mmod_rectangle object has two member variables, a dlib.rectangle object, and a confidence score.
    
    It is also possible to pass a list of images to the detector.
        - like this: dets = cnn_face_detector([image list], upsample_num, batch_size = 128)

    In this case it will return a mmod_rectangless object.
    This object behaves just like a list of lists and can be iterated over.
    '''
    print("Number of faces detected: {}".format(len(faces)))
    for i, face in enumerate(faces):
        print("Detection {}: Confidence: {}".format(i, face.confidence))
        cropFace = img[face.rect.top():face.rect.bottom(),face.rect.left():face.rect.right()]
        try:
            cropFace = cv2.resize(cropFace,(255,255))
            cv2.imwrite(f'{des}face_{secrets.token_urlsafe(4)}.png',cropFace)
        except Exception as error:
            print(f'*** Face skipped due to irregular image format error: {error} found ***')
            pass

def video(files, captureInterval):
    if captureInterval <= 0:
        print('capture interval must be more than 0')
        exit()
    for i,f in enumerate(files):
        print(f"#### Processing file {i}: {f} ####")
        # make sure input is file format
        if not os.path.isfile(f):
            print('invalid video format')
            pass
        
        # make sure running supported video format
        try:
            vid = cv2.VideoCapture(f)
        except Exception as error:
            print(f'Cannot proccess this video format: {error}')
            pass
        
        currentFrame = 0
        frame_per_second = vid.get(cv2.CAP_PROP_FPS)
        total_frame = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
        while(True):
            sys.stdout.write('\r' + f'Current frame: {currentFrame} with {total_frame - currentFrame} frames left to process. ')
            sys.stdout.flush()
            ret, frame = vid.read()
            # if video is still left and if the current frame matches 
            # the capture interval continue creating faces
            if ret:
                if currentFrame % (round(frame_per_second) * captureInterval) == 0:
                    extractFaces(frame,FACE_PATH)
                currentFrame += 1
            else:
                break
        vid.release()
        cv2.destroyAllWindows()
            
def images(files):
    for i,f in enumerate(files):
        print(f"#### Processing file {i}: {f} ####")
        try:
            img = cv2.imread(f)
        except Exception as error:
            print(f'Error: {error} found, please check image format')
    
        extractFaces(img,FACE_PATH)
        
if __name__=='__main__':
    if sys.argv[1] == '0':
        images(sys.argv[2:])
    
    if sys.argv[1] == '1':
        video(sys.argv[2:], 10)
    



