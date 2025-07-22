#!/usr/bin/env python3
"""
Example usage of the MultiQuestionExecutor for executing multiple simultaneous questions
using the AnswerRocket SDK.

Before running this script:
1. Activate the virtual environment: source venv/bin/activate
2. Set environment variables:
   export AR_URL="https://your-instance.com"
   export AR_TOKEN="your_api_token"

Or pass credentials directly to the executor.
"""

import asyncio
import json
from multi_question_executor import MultiQuestionExecutor


def example_threaded_execution():
    """Example using thread-based concurrent execution"""
    print("=== Thread-based Concurrent Execution ===")
    
    executor = MultiQuestionExecutor()
    questions = executor.load_questions_from_file('questions.txt')
    
    print(f"Executing {len(questions)} questions concurrently...")
    results = executor.execute_questions_threaded(questions, max_workers=3)
    
    print("\nResults:")
    for i, result in enumerate(results, 1):
        status = "✓" if result.success else "✗"
        print(f"{status} Question {i}: {result.question}")
        print(f"  Execution time: {result.execution_time:.2f}s")
        if result.success:
            print(f"  Result: {result.result}")
        else:
            print(f"  Error: {result.error}")
        print()
    
    summary = executor.get_summary(results)
    print("Summary:")
    print(json.dumps(summary, indent=2))


async def example_async_execution():
    """Example using async-based concurrent execution"""
    print("\n=== Async-based Concurrent Execution ===")
    
    executor = MultiQuestionExecutor()
    questions = executor.load_questions_from_file('questions.txt')
    
    print(f"Executing {len(questions)} questions asynchronously...")
    results = await executor.execute_questions_async(questions)
    
    print("\nResults:")
    for i, result in enumerate(results, 1):
        status = "✓" if result.success else "✗"
        print(f"{status} Question {i}: {result.question}")
        print(f"  Execution time: {result.execution_time:.2f}s")
        if result.success:
            print(f"  Result: {result.result}")
        else:
            print(f"  Error: {result.error}")
        print()
    
    summary = executor.get_summary(results)
    print("Summary:")
    print(json.dumps(summary, indent=2))


def example_with_custom_credentials():
    """Example passing credentials directly"""
    print("\n=== Custom Credentials Example ===")
    
    questions = [
        "What is the total revenue for this quarter?",
        "Show me the top performing sales representatives"
    ]
    
    try:
        executor = MultiQuestionExecutor(
            url="https://your-instance.com",
            token="your_api_token"
        )
        
        results = executor.execute_questions_threaded(questions)
        
        for result in results:
            print(f"Question: {result.question}")
            print(f"Success: {result.success}")
            if not result.success:
                print(f"Error: {result.error}")
            print()
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please provide valid AnswerRocket credentials")


def main():
    """Run all examples"""
    try:
        # Thread-based execution
        example_threaded_execution()
        
        # Async execution
        asyncio.run(example_async_execution())
        
        # Custom credentials (will likely fail without real credentials)
        example_with_custom_credentials()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set AR_URL and AR_TOKEN environment variables with valid AnswerRocket credentials")


if __name__ == "__main__":
    main()