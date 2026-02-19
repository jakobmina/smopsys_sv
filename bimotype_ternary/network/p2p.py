import socket
import json
import threading
import time
from typing import Dict, Any, Optional, Callable
from ..core.recursive_engine import RecursiveEngine
from ..integration.encoder import TernaryBiMoTypeEncoder
from ..integration.decoder import TernaryBiMoTypeDecoder

class MetriplecticPeer:
    """
    Handles P2P communication between BiMoType nodes using fingerprints.
    Integrates a Mutual Handshake protocol for security.
    """
    
    def __init__(self, port: int = 5005, db_path: str = "bimotype.sqlite3"):
        self.port = port
        self.engine = RecursiveEngine(db_path)
        self.local_fingerprint = self.engine.generate_fingerprint(session_n=int(time.time() % 1000))
        self.encoder = TernaryBiMoTypeEncoder()
        self.decoder = TernaryBiMoTypeDecoder()
        self.running = False
        self.on_message_received: Optional[Callable[[str, Dict[str, Any]], None]] = None
        self.on_handshake_received: Optional[Callable[[str], None]] = None
        
        # Security: Whitelist of authorized fingerprints
        self.trusted_peers = set()
        # Track pending handshake requests Sent By Us
        self.pending_handshakes = set()

    def add_trusted_peer(self, fingerprint: str):
        """Manually add a peer to the trusted list."""
        self.trusted_peers.add(fingerprint)
        print(f"[P2P] Peer {fingerprint[:8]} added to trusted list.")

    def start_listening(self, thread_callback: Optional[Callable[[threading.Thread], None]] = None):
        """Starts a background thread to listen for incoming packets."""
        self.running = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        if thread_callback:
            thread_callback(thread)
        thread.start()
        print(f"[P2P] Listening on port {self.port}...")
        print(f"[P2P] Local Fingerprint: {self.local_fingerprint}")
        return self.local_fingerprint

    def _listen_loop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', self.port))
            s.listen()
            while self.running:
                try:
                    conn, addr = s.accept()
                    with conn:
                        data = conn.recv(65536)
                        if not data:
                            continue
                        
                        packet_wrapper = json.loads(data.decode())
                        sender_fp = packet_wrapper.get("sender")
                        packet_type = packet_wrapper.get("type", "DATA")
                        payload = packet_wrapper.get("payload")
                        
                        if packet_type == "HANDSHAKE_REQ":
                            print(f"[P2P] Handshake request from {sender_fp[:8]}")
                            if self.on_handshake_received:
                                self.on_handshake_received(sender_fp)
                            else:
                                # Auto-accept if no callback (default behavior for CLI for now)
                                self.add_trusted_peer(sender_fp)
                                # send ack back - we need host/port though
                                # For local testing we might assume sender is at addr[0]
                                self.send_handshake_ack(addr[0], 5005, sender_fp) # Simplification

                        elif packet_type == "HANDSHAKE_ACK":
                            print(f"[P2P] Handshake ACK from {sender_fp[:8]}")
                            self.add_trusted_peer(sender_fp)

                        elif packet_type == "DATA":
                            if sender_fp in self.trusted_peers:
                                if self.on_message_received:
                                    self.on_message_received(sender_fp, payload)
                            else:
                                print(f"[P2P] Ignored DATA packet from untrusted peer {sender_fp[:8]}")
                                
                except Exception as e:
                    if self.running:
                        print(f"[P2P] Error processing packet: {e}")

    def request_handshake(self, target_host: str, target_port: int):
        """Sends a connection request to a peer."""
        wrapper = {
            "sender": self.local_fingerprint,
            "type": "HANDSHAKE_REQ",
            "payload": None
        }
        return self._send_raw(target_host, target_port, wrapper)

    def send_handshake_ack(self, target_host: str, target_port: int, target_fp: str):
        """Sends a confirmation of connection."""
        wrapper = {
            "sender": self.local_fingerprint,
            "type": "HANDSHAKE_ACK",
            "payload": None
        }
        self.add_trusted_peer(target_fp)
        return self._send_raw(target_host, target_port, wrapper)

    def send_packet(self, target_host: str, target_port: int, message: str, target_fp: Optional[str] = None):
        """Encodes and sends a DATA packet if the target is trusted."""
        if target_fp and target_fp not in self.trusted_peers:
            print(f"[P2P] Error: Target peer {target_fp[:8]} is not in trusted list. Perform handshake first.")
            return False
            
        encoded_data = self.encoder.encode_message_with_topology(message)
        packet = self.encoder.create_bimotype_packet_from_ternary(encoded_data)
        
        wrapper = {
            "sender": self.local_fingerprint,
            "type": "DATA",
            "payload": packet
        }
        return self._send_raw(target_host, target_port, wrapper)

    def _send_raw(self, host: str, port: int, wrapper: Dict):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((host, port))
                s.sendall(json.dumps(wrapper).encode())
                return True
        except Exception as e:
            print(f"[P2P] Send failed to {host}:{port}: {e}")
            return False

    def stop(self):
        self.running = False
