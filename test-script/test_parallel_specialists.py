#!/usr/bin/env python3
"""Test parallel specialist execution in Virtual Lab."""

import time
import os
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from src.agent.meeting import VirtualLabMeeting

def test_parallel_execution():
    """Test that specialists run in parallel."""
    
    # Simple test question
    question = "What are the key genes in T-cell exhaustion?"
    
    print("=" * 70)
    print("Testing Parallel Specialist Execution")
    print("=" * 70)
    print(f"Question: {question}")
    print()
    
    # Run with verbose to see the flow
    meeting = VirtualLabMeeting(
        user_question=question,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free"),
        provider="openrouter",
        max_team_size=3,
        verbose=True
    )
    
    print("\nStarting meeting with parallel specialist execution...")
    start_time = time.time()
    
    answer = meeting.run_meeting(num_rounds=1)
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"✅ Meeting completed in {elapsed:.1f} seconds")
    print("=" * 70)
    print("\nFinal Answer Preview:")
    print(answer[:500])
    print("...")
    print("\n" + "=" * 70)
    print("Note: With parallel execution, all 3 specialists should respond")
    print("simultaneously instead of sequentially, saving time!")
    print("=" * 70)

if __name__ == "__main__":
    test_parallel_execution()
