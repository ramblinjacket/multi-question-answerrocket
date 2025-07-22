#!/usr/bin/env python3
"""
Simple script to run multiple questions concurrently using AnswerRocket SDK
"""

from multi_question_executor import MultiQuestionExecutor

def main():
    try:
        # Load questions and run them
        executor = MultiQuestionExecutor()
        questions = executor.load_questions_from_file('questions.txt')
        
        print(f"Running {len(questions)} questions using copilot: {executor.copilot_id}")
        results = executor.execute_questions_threaded(questions)
        
        # Show results
        for i, result in enumerate(results, 1):
            status = "✓" if result.success else "✗"
            print(f"{status} Question {i}: {result.question}")
            if result.success:
                print(f"  Result: {result.result}")
            else:
                print(f"  Error: {result.error}")
            print()
        
        # Summary
        summary = executor.get_summary(results)
        print(f"Summary: {summary['successful']}/{summary['total_questions']} successful")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()