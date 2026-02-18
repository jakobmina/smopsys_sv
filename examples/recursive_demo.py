import time
import json
from bimotype_ternary.core.session_manager import SessionManager

def run_recursive_cycle(iteration: int):
    print(f"\n{'='*60}")
    print(f" ITERATION {iteration}: RECURSIVE SESSION START")
    print(f"{'='*60}")
    
    sm = SessionManager()
    session_info = sm.start_session(session_number=iteration)
    
    print(f"Session ID:  {session_info['session_id']}")
    print(f"Fingerprint: {session_info['fingerprint'][:32]}...")
    
    prev_context = session_info['previous_context']
    if prev_context:
        print(f"Loaded Context from Previous Session: {json.dumps(prev_context, indent=2)}")
    else:
        print("No previous context found. Starting a new recursive branch.")

    # New information to process in this cycle
    new_info = {
        "processing_load": 10.5 * iteration,
        "quantum_entropy": 0.42 / (iteration + 1),
        "session_metrics": iteration ** 2
    }
    
    print(f"\nProcessing New Information: {json.dumps(new_info, indent=2)}")
    
    # Recursive evolution
    final_output = sm.process_and_evolve(new_info)
    
    print(f"\nEvolved Recursive State (Saved for Iteration {iteration+1}):")
    print(json.dumps(final_output, indent=2))
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Simulate multiple sessions to show recursion
    for i in range(1, 4):
        run_recursive_cycle(i)
        time.sleep(1) # Simulated time gap
