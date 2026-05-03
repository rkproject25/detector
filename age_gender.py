from deepface import DeepFace
import cv2

 def estimate_age_gender(face_img):
    """Returns (None, None) – age/gender estimation disabled."""
    return None, None

def estimate_age_gender2(face_img):
    """face_img is a BGR numpy array (the face region). Returns (age, gender)."""
    try:
        # DeepFace expects RGB
        rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        result = DeepFace.analyze(rgb, actions=['age','gender'], enforce_detection=False)
        age = result[0]['age']
        gender = result[0]['dominant_gender']
        return age, gender
    except:
        return None, None
