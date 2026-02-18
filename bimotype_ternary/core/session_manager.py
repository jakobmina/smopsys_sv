from typing import Dict, Any
from .recursive_engine import RecursiveEngine

class SessionManager:
    """Coordinates the session lifecycle and recursive data injection."""
    
    def __init__(self, db_path: str = "bimotype.sqlite3"):
        self.engine = RecursiveEngine(db_path)
        self.current_session_id = None
        self.current_fingerprint = None
        
    def start_session(self, session_number: int = 1) -> Dict[str, Any]:
        """
        Initializes a new session:
        1. Generates fingerprint.
        2. Logs audit trail.
        3. Loads previous recursive data.
        """
        self.current_fingerprint = self.engine.generate_fingerprint(session_number)
        self.current_session_id = f"SESSION-{session_number}-{self.current_fingerprint[:8]}"
        
        self.engine.log_audit(self.current_session_id, self.current_fingerprint)
        
        # Load feedback from previous sessions
        previous_data = self.engine.load_previous_feedback()
        
        return {
            "session_id": self.current_session_id,
            "fingerprint": self.current_fingerprint,
            "previous_context": previous_data.get("data", {}),
            "status": "READY"
        }

    def process_and_evolve(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the information through the recursive filter."""
        evolved_data = self.engine.compute_feedback_loop(new_data)
        
        # Save for next session
        self.engine.save_current_feedback(evolved_data, self.current_session_id)
        
        return evolved_data
