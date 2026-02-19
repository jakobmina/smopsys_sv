import pytest
import time
import socket
import threading
from bimotype_ternary.network.p2p import MetriplecticPeer
from bimotype_ternary.network.discovery import PeerDiscovery

def test_p2p_communication():
    # Setup two peers
    peer_a = MetriplecticPeer(port=6000)
    peer_b = MetriplecticPeer(port=6001)
    
    received_messages = []
    
    def on_msg_a(sender, packet):
        decoded = peer_a.decoder.decode_bimotype_packet(packet)
        received_messages.append(decoded.get("decoded_message"))

    peer_a.on_message_received = on_msg_a
    fp_a = peer_a.start_listening()
    fp_b = peer_b.start_listening()
    
    time.sleep(1)
    
    # 1. First attempt without handshake (should fail)
    peer_b.send_packet("127.0.0.1", 6000, "IGNORE_ME", target_fp=fp_a)
    time.sleep(1)
    assert len(received_messages) == 0
    
    # 2. Perform Handshake
    # B requests to A
    peer_b.request_handshake("127.0.0.1", 6000)
    time.sleep(1)
    
    # A accepts B (Automatic in current test environment since on_handshake_received is None)
    # But let's verify A now trusts B
    assert fp_b in peer_a.trusted_peers
    
    # A MUST also handshake back to B or B must trust A
    peer_a.send_handshake_ack("127.0.0.1", 6001, fp_b)
    time.sleep(1)
    assert fp_a in peer_b.trusted_peers
    
    # 3. Successful communication after mutual trust
    message = "SECURE_SIGNAL_H7"
    success = peer_b.send_packet("127.0.0.1", 6000, message, target_fp=fp_a)
    
    assert success is True
    time.sleep(1)
    assert message in received_messages
    
    peer_a.stop()
    peer_b.stop()
    print("Handshake & Secure P2P Test Passed!")

def test_p2p_unauthorized_ignored():
    peer_a = MetriplecticPeer(port=6005)
    received = []
    peer_a.on_message_received = lambda s, p: received.append(p)
    peer_a.start_listening()
    
    peer_b = MetriplecticPeer(port=6006)
    time.sleep(1)
    
    # Send directly via low level or skipping trust check locally (simulating attacker)
    wrapper = {
        "sender": peer_b.local_fingerprint,
        "type": "DATA",
        "payload": {"test": "data"}
    }
    peer_b._send_raw("127.0.0.1", 6005, wrapper)
    
    time.sleep(1)
    assert len(received) == 0 # Should be ignored because not in trusted_peers
    peer_a.stop()
    print("Unauthorized Packet Injection Prevention Test Passed!")

def test_peer_discovery():
    fp = "test_fingerprint_123"
    PeerDiscovery.register_peer(fp, "1.2.3.4", 9999)
    
    resolved = PeerDiscovery.resolve_peer(fp)
    assert resolved == ("1.2.3.4", 9999)
    print("Peer Discovery Test Passed!")
