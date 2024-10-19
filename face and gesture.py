import cv2
import mediapipe as mp
import vonage
import time
import face_recognition

# Nexmo setup
api_key = 'c85ec398'
api_secret = 'Qtd31zpZ35IKesKH'
from_number = '+9159039465'
to_number = '+918894561745'

client = vonage.Client(key=api_key, secret=api_secret)

# Function to send SMS alert
def send_sms_alert():
    response = client.sms.send_message({
        'from': from_number,
        'to': to_number,
        'text': 'Emergency Alert: Immediate assistance required! Here is my current location: . Please contact authorities if necessary.'
    })
    
    if response['messages'][0]['status'] == '0':
        print('Alert sent successfully!')
    else:
        print(f"Failed to send alert: {response['messages'][0]['error-text']}")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Gesture detection logic
def is_signal_for_help(landmarks):
    thumb_up = landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.THUMB_IP].y
    fingers_closed = (landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
                      landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
                      landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y > landmarks[mp_hands.HandLandmark.RING_FINGER_DIP].y and
                      landmarks[mp_hands.HandLandmark.PINKY_TIP].y > landmarks[mp_hands.HandLandmark.PINKY_DIP].y)
    return thumb_up and fingers_closed

# Start video capture
cap = cv2.VideoCapture(0)
gesture_detected = False

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image horizontally for selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB for face recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame using face_recognition
        face_locations = face_recognition.face_locations(rgb_frame)

        # If face is detected, proceed with hand gesture detection
        if len(face_locations) > 0:
            # Process the image and detect hands
            results = hands.process(rgb_frame)

            # Draw hand landmarks if any are detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Check for the specific gesture
                    if is_signal_for_help(hand_landmarks.landmark):
                        if not gesture_detected:  # Send SMS only once per detection
                            send_sms_alert()
                            gesture_detected = True
                            time.sleep(5)  # Prevent multiple alerts in quick succession
                    else:
                        gesture_detected = False  # Reset if gesture is not detected

        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the result
        cv2.imshow('Gesture and Face Detection', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
