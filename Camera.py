import cv2
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Setup AES encryption
key = os.urandom(32)  # 256-bit AES key
iv = os.urandom(16)   # Initialization vector

cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
encryptor = cipher.encryptor()

# Initialize OpenCV for camera capture
cap = cv2.VideoCapture(0)  # Capture video from the default camera

# File to save encrypted video
output_file = open("encrypted_video.dat", "wb")

print("Recording and encrypting camera video...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Encode the frame as bytes (using PNG format to get compressed bytes)
    ret, buffer = cv2.imencode('.png', frame)
    frame_bytes = buffer.tobytes()

    # Encrypt the frame bytes
    encrypted_frame = encryptor.update(frame_bytes)

    # Write the encrypted data to file
    output_file.write(encrypted_frame)

    # Display the frame (optional)
    cv2.imshow('Encrypted Video Capture', frame)

    # Stop recording when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
output_file.close()
cv2.destroyAllWindows()

print("Video encrypted and saved to 'encrypted_video.dat'.")
