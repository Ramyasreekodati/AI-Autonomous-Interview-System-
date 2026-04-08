import cv2
import mediapipe as mp
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ProctoringEngine:
    """
    Phase 2: AI Surveillance System
    Handles real-time monitoring of candidate behavior using MediaPipe and OpenCV.
    """
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        # Landmarks for head pose estimation
        self.face_3d = []
        self.face_2d = []

    def analyze_frame(self, frame):
        """
        Analyzes a single frame for:
        1. Number of faces
        2. Eye contact / Head pose
        3. Basic presence
        """
        if frame is None:
            return {"error": "Empty frame"}

        results = {
            "face_count": 0,
            "looking_at_screen": True,
            "alerts": []
        }

        # Convert frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape

        # 1. Face Detection (Count)
        face_results = self.face_detection.process(rgb_frame)
        if face_results.detections:
            results["face_count"] = len(face_results.detections)
            if results["face_count"] > 1:
                results["alerts"].append("MULTIPLE_FACES")
        else:
            results["alerts"].append("NO_FACE_DETECTED")

        # 2. Head Pose Estimation (Looking Away)
        mesh_results = self.face_mesh.process(rgb_frame)
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    # Key points for nose, chin, eyes corners
                    if idx in [33, 263, 1, 61, 291, 199]:
                        x, y = int(lm.x * w), int(lm.y * h)
                        self.face_2d.append([x, y])
                        self.face_3d.append([x, y, lm.z])

                if len(self.face_2d) == 6:
                    self.face_2d = np.array(self.face_2d, dtype=np.float64)
                    self.face_3d = np.array(self.face_3d, dtype=np.float64)

                    # Camera matrix
                    focal_length = 1 * w
                    cam_matrix = np.array([ [focal_length, 0, h / 2],
                                          [0, focal_length, w / 2],
                                          [0, 0, 1]], dtype=np.float64)
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(self.face_3d, self.face_2d, cam_matrix, dist_matrix)
                    rmat, jac = cv2. Rodrigues(rot_vec)
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    x = angles[0] * 360
                    y = angles[1] * 360

                    # Detect if looking away (Thresholds: ~10-15 degrees)
                    if y < -10 or y > 10 or x < -10 or x > 10:
                        results["looking_at_screen"] = False
                        results["alerts"].append("LOOK_AWAY")

                # 3. Emotion / Stress Estimation (Phase 2.4)
                # Simple geometry-based sentiment (Smiling/Stressed)
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]
                lip_distance = abs(upper_lip.y - lower_lip.y)
                
                if lip_distance > 0.05: # Mouth wide open (Potential stress/shouting/talking)
                    results["alerts"].append("UNUSUAL_MOUTH_MOVEMENT")
                
                # Reset for next call
                self.face_2d = []
                self.face_3d = []

        # 4. Object Detection (Phase 2.3)
        # Note: In a full deployment, we would load YOLO/MobileNet weights here.
        # For now, we provide the hook for detection logic.
        self._detect_objects(frame, results)

        return results

    def _detect_objects(self, frame, results):
        """
        Placeholder for Step 2.3 - Object Detection (Phones, Books).
        In production, this would use a DNN model.
        """
        # Logic would go here:
        # blob = cv2.dnn.blobFromImage(...)
        # detections = self.net.forward()
        # if 'cell phone' in detections: results['alerts'].append('PHONE_DETECTED')
        pass

# Singleton instance
proctoring_engine = ProctoringEngine()
