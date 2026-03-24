import cv2
import mediapipe as mp
import numpy as np

class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    
    def analyze_frame(self, frame_bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {"status": "error", "message": "Invalid image"}

        # Process frame
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(img_rgb)

        if results.multi_face_landmarks:
            # Simple check for focus: if face is detected
            return {
                "face_detected": True,
                "landmarks_count": len(results.multi_face_landmarks[0].landmark),
                "emotion_hint": "Neutral" # This would require another model
            }
        
        return {"face_detected": False}
