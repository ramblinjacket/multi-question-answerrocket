# Multi-Question Executor for AnswerRocket

## Project Overview
A Python tool for executing multiple AnswerRocket questions simultaneously using concurrent processing. Reduces total execution time by running natural language queries in parallel against AnswerRocket instances.

## Project Setup

### Virtual Environment
- Created with: `python3 -m venv venv`
- Activate with: `source venv/bin/activate`

### Dependencies
- answerrocket-client (0.2.62) - AnswerRocket Python SDK
- Standard library: asyncio, concurrent.futures, dataclasses, typing

### Project Structure
```
multi-question/
├── multi_question_executor.py  # Main executor class
├── example_usage.py           # Usage examples  
├── questions.txt             # Questions file (one per line)
├── requirements.txt          # Python dependencies
├── venv/                    # Virtual environment
├── README.md               # User documentation
└── CLAUDE.md              # This file
```

## Key Components

### MultiQuestionExecutor Class (`multi_question_executor.py`)
- **Purpose**: Main class for concurrent question execution
- **Key Methods**:
  - `load_questions_from_file(file_path)`: Load questions from text file
  - `execute_questions_threaded(questions, max_workers)`: Thread-based execution
  - `execute_questions_async(questions)`: Async-based execution
  - `get_summary(results)`: Generate performance statistics

### QuestionResult Dataclass
- **Purpose**: Container for individual question results
- **Fields**: question, result, success, error, execution_time

### Questions Input (`questions.txt`)
- **Format**: One question per line, plain text
- **Purpose**: Simple way to manage multiple questions
- **Usage**: Edit this file to add/remove questions

## AnswerRocket SDK Integration

### Import Syntax
```python
from answer_rocket import AnswerRocketClient
```

### Authentication
```python
# Environment variables (recommended)
export AR_URL="https://your-instance.answerrocket.com" 
export AR_TOKEN="your_api_token"

# Client initialization
client = AnswerRocketClient(url=self.url, token=self.token)
```

### Question Execution
```python
# Execute natural language question
result = client.chat.ask(question)
```

## Common Operations

### Running the Tool
1. Set environment variables: `AR_URL` and `AR_TOKEN`
2. Edit `questions.txt` with desired questions
3. Run: `python example_usage.py`

### Adding New Questions
- Edit `questions.txt`
- Add one question per line
- Empty lines are ignored

### Custom Implementation
```python
from multi_question_executor import MultiQuestionExecutor

executor = MultiQuestionExecutor()
questions = executor.load_questions_from_file('questions.txt')
results = executor.execute_questions_threaded(questions)
```

## Performance Considerations
- **Default max_workers**: min(10, question_count)
- **Thread vs Async**: Use async for higher concurrency, threads for simplicity
- **Rate Limiting**: Adjust max_workers based on AnswerRocket instance limits
- **Error Isolation**: Individual question failures don't affect others

## Testing and Validation
- No specific test framework currently configured
- Manual testing via `example_usage.py`
- Error handling validated through exception catching
- Performance metrics tracked via execution timing

## Common Issues
- **Import Error**: Ensure correct import syntax `from answer_rocket import AnswerRocketClient`
- **Authentication**: Verify AR_URL and AR_TOKEN environment variables
- **File Not Found**: Ensure questions.txt exists in working directory
- **Concurrency**: Reduce max_workers if hitting AnswerRocket rate limits