from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import pyaudio

# Load the key and IV used for encryption
key = b'your_32_byte_key'  # Replace with actual key used for encryption
iv = b'your_16_byte_iv'    # Replace with actual IV used for encryption

# Setup AES decryption
cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
decryptor = cipher.decryptor()

# Initialize PyAudio for playback
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

# Read and decrypt the audio data
with open("encrypted_audio.dat", "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()
    decrypted_audio = decryptor.update(encrypted_data)

# Play the decrypted audio
stream.write(decrypted_audio)

# Close stream
stream.stop_stream()
stream.close()
audio.terminate()

print("Audio decrypted and played.")
