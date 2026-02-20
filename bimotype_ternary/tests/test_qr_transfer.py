import pytest
import os
from bimotype_ternary.crypto.qr_transfer import QRTransferProtocol

def test_qr_transfer_cycle():
    """
    Tests the full offline transfer cycle (encrypt -> chunk -> QR -> reconstruct -> decrypt).
    """
    # 1. Setup
    original_text = "Metriplectic Topologies and the Search for Quantum Harmony. " * 50
    original_bytes = original_text.encode('utf-8')
    h7_seed = 42
    
    protocol = QRTransferProtocol(h7_index=h7_seed, chunk_size=50)
    
    # 2. Prepare payload (Encrypt & Chunk)
    qr_frames = protocol.prepare_payload(original_bytes, "message.txt")
    
    # Verify framing
    assert len(qr_frames) > 1
    
    first_frame = qr_frames[0]
    parsed = protocol.parse_qr_frame(first_frame)
    assert parsed is not None
    filename, f_idx, tot, chunk = parsed
    assert filename == "message.txt"
    assert f_idx == 0
    assert tot == len(qr_frames)
    
    # 3. Reconstruct payload (Decrypt)
    # Simulate scanning frames in random order
    received_frames = {}
    for frame_data in reversed(qr_frames):
        parsed = protocol.parse_qr_frame(frame_data)
        if parsed:
            _, idx, _, chunk_data = parsed
            received_frames[idx] = chunk_data
            
    reconstructed_bytes = protocol.reconstruct_payload(received_frames)
    
    # 4. Verify Identity
    assert reconstructed_bytes == original_bytes

def test_qr_image_generation():
    h7_seed = 42
    protocol = QRTransferProtocol(h7_index=h7_seed, chunk_size=300)
    
    qr_frames = protocol.prepare_payload(b"Small test", "test.txt")
    images = protocol.generate_qr_images(qr_frames)
    
    assert len(images) == len(qr_frames)
    assert images[0].size[0] > 0
