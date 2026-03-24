import cv2
import numpy as np

try:
    import mediapipe as mp
    # Newer mediapipe versions on 3.13 might lack 'solutions' attribute initially or require sub-imports
    mp_face_mesh = getattr(mp.solutions, "face_mesh", None)
except Exception:
    mp_face_mesh = None

class FaceAnalyzer:
    def __init__(self):
        # Fallback to OpenCV HAAR Cascade if MediaPipe fails
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_mesh = None
        if mp_face_mesh:
            try:
                self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
            except:
                self.face_mesh = None

    def analyze_frame(self, frame_bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return {"face_detected": False, "emotion": "Unknown"}

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Try MediaPipe first
        if self.face_mesh:
            results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_face_landmarks:
                return {"face_detected": True, "emotion": "Neutral"}
        
        # Fallback to HAAR Cascade
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            return {"face_detected": True, "emotion": "Neutral"}
        
        return {"face_detected": False, "emotion": "Not Focused"}
