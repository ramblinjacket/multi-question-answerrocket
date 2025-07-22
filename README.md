# Multi-Question Executor for AnswerRocket

A Python tool for executing multiple AnswerRocket questions simultaneously using concurrent processing. This tool allows you to run multiple natural language queries against your AnswerRocket instance in parallel, significantly reducing total execution time.

## Features

- **Concurrent Execution**: Run multiple questions simultaneously using threading or async processing
- **File-based Question Input**: Load questions from a simple text file
- **Comprehensive Error Handling**: Individual error tracking per question
- **Performance Metrics**: Execution time tracking and success rate reporting
- **Flexible Configuration**: Environment variables or direct credential passing
- **Results Aggregation**: Detailed summary statistics and error reporting

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure AnswerRocket Credentials

**Option A: Environment Variables (Recommended)**
```bash
export AR_URL="https://your-instance.answerrocket.com"
export AR_TOKEN="your_api_token"
```

**Option B: Direct Configuration**
Pass credentials directly when creating the executor (see usage examples below).

## Usage

### 1. Add Your Questions

Edit the `questions.txt` file with your questions, one per line:

```
What are the top 5 sales regions by revenue?
Show me monthly revenue trends for the last 12 months
What is the average customer acquisition cost?
Which products have the highest profit margins?
```

### 2. Run the Example Script

```bash
python example_usage.py
```

This will execute all questions from `questions.txt` using both threaded and async execution methods.

### 3. Custom Implementation

```python
from multi_question_executor import MultiQuestionExecutor

# Initialize executor
executor = MultiQuestionExecutor()

# Load questions from file
questions = executor.load_questions_from_file('questions.txt')

# Execute questions concurrently
results = executor.execute_questions_threaded(questions, max_workers=5)

# Display results
for result in results:
    if result.success:
        print(f"✓ {result.question}")
        print(f"  Result: {result.result}")
    else:
        print(f"✗ {result.question}")
        print(f"  Error: {result.error}")
    print(f"  Time: {result.execution_time:.2f}s\n")

# Get summary statistics
summary = executor.get_summary(results)
print(f"Success rate: {summary['success_rate']:.1%}")
print(f"Total time: {summary['total_execution_time']:.2f}s")
```

## API Reference

### MultiQuestionExecutor

#### Constructor
```python
MultiQuestionExecutor(url=None, token=None)
```
- `url`: AnswerRocket instance URL (optional if `AR_URL` env var is set)
- `token`: API token (optional if `AR_TOKEN` env var is set)

#### Methods

**`load_questions_from_file(file_path)`**
- Load questions from a text file, one question per line
- Returns: `List[str]`

**`execute_questions_threaded(questions, max_workers=None)`**
- Execute questions using thread-based concurrency
- `questions`: List of question strings
- `max_workers`: Maximum number of concurrent threads (default: min(10, question_count))
- Returns: `List[QuestionResult]`

**`execute_questions_async(questions)`**
- Execute questions using async concurrency (must be called with `await`)
- `questions`: List of question strings  
- Returns: `List[QuestionResult]`

**`get_summary(results)`**
- Generate summary statistics from results
- `results`: List of QuestionResult objects
- Returns: Dictionary with metrics (total, success rate, timing, errors)

### QuestionResult

Result object containing:
- `question`: Original question string
- `result`: AnswerRocket response (if successful)
- `success`: Boolean success status
- `error`: Error message (if failed)
- `execution_time`: Time taken in seconds

## Examples

### Basic Usage
```python
executor = MultiQuestionExecutor()
questions = ["What is total revenue?", "Show top customers"]
results = executor.execute_questions_threaded(questions)
```

### With Custom Credentials
```python
executor = MultiQuestionExecutor(
    url="https://demo.answerrocket.com",
    token="your_token_here"
)
questions = executor.load_questions_from_file('my_questions.txt')
results = executor.execute_questions_threaded(questions, max_workers=3)
```

### Async Execution
```python
import asyncio

async def run_questions():
    executor = MultiQuestionExecutor()
    questions = executor.load_questions_from_file('questions.txt')
    results = await executor.execute_questions_async(questions)
    return results

results = asyncio.run(run_questions())
```

## File Structure

```
multi-question/
├── multi_question_executor.py  # Main executor class
├── example_usage.py           # Usage examples
├── questions.txt             # Your questions file
├── requirements.txt          # Python dependencies
├── venv/                    # Virtual environment
└── README.md               # This file
```

## Configuration

### Environment Variables
- `AR_URL`: Your AnswerRocket instance URL
- `AR_TOKEN`: Your AnswerRocket API token

### Performance Tuning
- Adjust `max_workers` parameter for thread-based execution
- Use async execution for better resource utilization with many questions
- Monitor execution times and adjust concurrency based on your AnswerRocket instance limits

## Error Handling

The tool provides robust error handling:
- Individual question failures don't stop execution of other questions
- Detailed error messages for troubleshooting
- Summary statistics include error counts and details
- Failed questions are clearly marked in results

## Troubleshooting

**Authentication Errors**
- Verify `AR_URL` and `AR_TOKEN` are correctly set
- Check that your token has necessary permissions

**Connection Issues**
- Ensure your AnswerRocket instance is accessible
- Check firewall/proxy settings if applicable

**Performance Issues**
- Reduce `max_workers` if hitting rate limits
- Monitor your AnswerRocket instance resource usage
- Consider breaking large question sets into smaller batches