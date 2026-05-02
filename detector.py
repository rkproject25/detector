from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np

# CPU only
device = torch.device('cpu')

# Load models once (reused across all calls)
print("[detector] Loading MTCNN and FaceNet models...")
mtcnn = MTCNN(
    keep_all=True,
    device=device,
    min_face_size=40,
    thresholds=[0.6, 0.7, 0.7],
    post_process=True
)

resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
print("[detector] Models loaded successfully.")


def get_frame_embeddings(frame_rgb):
    """
    Takes a RGB numpy frame.
    Returns list of (box, embedding) for every face detected.
    box = [x1, y1, x2, y2]
    embedding = numpy array of shape (512,)
    """
    img = Image.fromarray(frame_rgb)

    boxes, probs = mtcnn.detect(img)

    if boxes is None or len(boxes) == 0:
        return []

    faces = mtcnn(img)
    if faces is None:
        return []

    results = []
    with torch.no_grad():
        embeddings = resnet(faces.to(device)).cpu().numpy()

    for box, prob, emb in zip(boxes, probs, embeddings):
        if prob < 0.90:  # skip low-confidence detections
            continue
        results.append((box, emb))

    return results


def encode_reference_image(image_path):
    """
    Takes path to a missing person's photo.
    Returns a single embedding (512,) numpy array.
    Raises ValueError if no face found.
    """
    img = Image.open(image_path).convert('RGB')

    face = mtcnn(img)

    if face is None:
        raise ValueError(f"No face detected in reference image: {image_path}")

    # If multiple faces detected, take the first (largest/most confident)
    if face.ndim == 4:
        face = face[0].unsqueeze(0)
    else:
        face = face.unsqueeze(0)

    with torch.no_grad():
        embedding = resnet(face.to(device)).cpu().numpy()[0]

    return embedding 