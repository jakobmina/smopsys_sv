import json
import base64
import zlib
import qrcode
from io import BytesIO
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from bimotype_ternary.examples.generate_metriplectic_keys import MetriplecticKeyGenerator

class QRTransferProtocol:
    """
    Protocol for offline file transfer using Animated QR codes
    and Metriplectic Encryption.
    """
    def __init__(self, h7_index: int, chunk_size: int = 400):
        # We use a smaller chunk_size (e.g. 400 bytes) for better QR readability on screens
        self.h7_index = h7_index
        self.chunk_size = chunk_size
        self.key_gen = MetriplecticKeyGenerator(h7_index)

    def prepare_payload(self, file_bytes: bytes, filename: str) -> list[str]:
        """
        Compresses, encrypts, and chunks a file into QR-ready payload strings.
        """
        # 1. Compress
        compressed_data = zlib.compress(file_bytes)
        
        # 2. Encrypt (Using generated keys)
        # Generate enough keys to cover the byte length
        keys = self.key_gen.generate_key_sequence(len(compressed_data))
        
        # Simple modulo/XOR byte encryption (One-Time Pad simulation)
        encrypted_bytes = bytearray()
        for i in range(len(compressed_data)):
            k = int(abs(keys[i]) * 1000) % 256
            encrypted_bytes.append(compressed_data[i] ^ k)

        # 3. Base64 encode
        b64_data = base64.b64encode(encrypted_bytes).decode('utf-8')
        
        # 4. Chunking
        total_len = len(b64_data)
        chunks = []
        for i in range(0, total_len, self.chunk_size):
            chunks.append(b64_data[i:i + self.chunk_size])

        total_frames = len(chunks)
        
        # 5. Format into QR frames
        # Format: BIMO_QR|filename|frame_idx|total_frames|payload_chunk
        qr_frames = []
        for idx, chunk in enumerate(chunks):
            header = f"BIMO_QR|{filename}|{idx}|{total_frames}|"
            qr_frames.append(header + chunk)
            
        return qr_frames

    def reconstruct_payload(self, frames: dict) -> bytes:
        """
        Reconstructs, decrypts, and decompresses the payload from collected QR frames.
        frames is a dict: {frame_idx (int): "payload_chunk"}
        returns: Tuple(filename, decrypted_bytes)
        """
        if not frames:
            raise ValueError("No frames provided.")
            
        sorted_indices = sorted(frames.keys())
        expected_total = len(frames)
        
        # We expect indices to go from 0 to expected_total - 1
        if sorted_indices[-1] != expected_total - 1:
            raise ValueError(f"Missing frames. Have {len(frames)} but highest index is {sorted_indices[-1]}")

        # Assemble the base64 chunks
        full_b64 = "".join([frames[idx] for idx in sorted_indices])
        
        # 1. Base64 Decode
        try:
            encrypted_bytes = bytearray(base64.b64decode(full_b64))
        except Exception as e:
             raise ValueError(f"Error decoding base64: {e}")

        # 2. Decrypt
        keys = self.key_gen.generate_key_sequence(len(encrypted_bytes))
        decrypted_bytes = bytearray()
        for i in range(len(encrypted_bytes)):
            k = int(abs(keys[i]) * 1000) % 256
            decrypted_bytes.append(encrypted_bytes[i] ^ k)
            
        # 3. Decompress
        try:
            original_bytes = zlib.decompress(decrypted_bytes)
        except Exception as e:
            raise ValueError(f"Error decompressing data (Invalid Key / Corrupted payload?): {e}")
            
        return original_bytes

    def generate_qr_images(self, frames: list[str]) -> list:
        """
        Generates PIL Image objects for each QR frame payload.
        """
        images = []
        for frame_data in frames:
            qr = qrcode.QRCode(
                version=None, # auto
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(frame_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            images.append(img)
            
        return images
        
    @staticmethod
    def parse_qr_frame(qr_data: str):
        """
        Parses a single QR string payload into its header components and data chunk.
        Format: BIMO_QR|filename|frame_idx|total_frames|payload_chunk
        Returns: (filename, frame_idx, total_frames, chunk_data) or None if invalid.
        """
        if not qr_data.startswith("BIMO_QR|"):
            return None
            
        parts = qr_data.split("|", 4)
        if len(parts) != 5:
            return None
            
        _, filename, frame_idx, total_frames, chunk_data = parts
        try:
            return filename, int(frame_idx), int(total_frames), chunk_data
        except ValueError:
            return None

    def scan_animated_qr_from_camera(self, camera_index: int = 0) -> bytes:
        """
        Opens the webcam to scan an animated QR sequence.
        Returns the decrypted bytes once all frames are collected.
        """
        cap = cv2.VideoCapture(camera_index)
        
        frames_collected = {}
        expected_total = None
        target_filename = None
        
        print("Starting camera... Point it at the Animated QR.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Decode QRs in the frame
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                qr_data = obj.data.decode("utf-8")
                
                parsed = self.parse_qr_frame(qr_data)
                if parsed:
                    filename, f_idx, tot, chunk = parsed
                    
                    if expected_total is None:
                        expected_total = tot
                        target_filename = filename
                        
                    # Ignore if it's a different file transfer
                    if filename == target_filename:
                        if f_idx not in frames_collected:
                            frames_collected[f_idx] = chunk
                            print(f"Collected frame {f_idx + 1}/{expected_total}")
                            
            # Draw progress
            progress = len(frames_collected)
            if expected_total:
                text = f"Frames: {progress}/{expected_total} ({(progress/expected_total)*100:.1f}%)"
            else:
                text = "Scanning for BIMO_QR..."
                
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("BiMoType QR Scanner", frame)
            
            # Check completion
            if expected_total and progress == expected_total:
                print("All frames collected!")
                break
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Scan cancelled by user.")
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        if expected_total and len(frames_collected) == expected_total:
            return self.reconstruct_payload(frames_collected), target_filename
        else:
            return None, None
