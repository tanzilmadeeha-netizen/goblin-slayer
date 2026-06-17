import mediapipe as mp

print("MediaPipe:", mp.__version__)
print("PoseLandmarker exists:", hasattr(mp.tasks.vision, "PoseLandmarker"))