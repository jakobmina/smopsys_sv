import json
import os
from typing import Optional, Tuple

class PeerDiscovery:
    """
    Simulated peer discovery. 
    In a real scenario, this would use a DHT or a Relay Server.
    For the MVP, we use a local peer cache.
    """
    
    CACHE_FILE = "peer_cache.json"
    
    @staticmethod
    def register_peer(fingerprint: str, host: str, port: int):
        cache = PeerDiscovery._load_cache()
        cache[fingerprint] = {"host": host, "port": port}
        PeerDiscovery._save_cache(cache)
        print(f"[Discovery] Registered {fingerprint[:8]} at {host}:{port}")

    @staticmethod
    def resolve_peer(fingerprint: str) -> Optional[Tuple[str, int]]:
        cache = PeerDiscovery._load_cache()
        peer = cache.get(fingerprint)
        if peer:
            return peer["host"], peer["port"]
        return None

    @staticmethod
    def _load_cache():
        if os.path.exists(PeerDiscovery.CACHE_FILE):
            try:
                with open(PeerDiscovery.CACHE_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    @staticmethod
    def _save_cache(cache):
        with open(PeerDiscovery.CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
