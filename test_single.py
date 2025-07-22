#!/usr/bin/env python3
"""
Test single question to verify SDK fix
"""

from multi_question_executor import MultiQuestionExecutor

def test_single_question():
    try:
        executor = MultiQuestionExecutor()
        questions = executor.load_questions_from_file('questions.txt')
        
        print(f"Loaded {len(questions)} questions for copilot: {executor.copilot_id}")
        print(f"Using SDK version 0.2.63")
        print(f"Testing first question: {questions[0]}")
        
        # Test just one question
        result = executor._execute_single_question(questions[0])
        
        print(f"\nResult:")
        print(f"Success: {result.success}")
        print(f"Execution time: {result.execution_time:.2f}s")
        
        if result.success:
            print(f"Response: {result.result}")
        else:
            print(f"Error: {result.error}")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_single_question()