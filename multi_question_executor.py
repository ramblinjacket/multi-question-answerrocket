import asyncio
import concurrent.futures
import os
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from answer_rocket import AnswerRocketClient
import time


@dataclass
class QuestionResult:
    question: str
    result: Any
    success: bool
    error: Optional[str] = None
    execution_time: float = 0.0


class MultiQuestionExecutor:
    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        self.copilot_id = None
        self.url = url or os.environ.get('AR_URL')
        self.token = token or os.environ.get('AR_TOKEN')
        
        if not self.url or not self.token:
            raise ValueError("AnswerRocket URL and token must be provided via parameters or AR_URL/AR_TOKEN environment variables")
    
    def load_questions_from_file(self, file_path: str) -> List[str]:
        """Load questions from a text file and extract copilot_id from header"""
        questions = []
        copilot_id = None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                    
                # Parse copilot_id from header
                if line.startswith('# COPILOT_ID:'):
                    copilot_id = line.split(':', 1)[1].strip()
                    continue
                    
                # Skip other comments
                if line.startswith('#'):
                    continue
                    
                questions.append(line)
        
        if not copilot_id:
            raise ValueError(f"No COPILOT_ID found in {file_path}. Add '# COPILOT_ID: your-copilot-id' to the top of the file.")
        
        self.copilot_id = copilot_id
        return questions
    
    def _create_client(self) -> AnswerRocketClient:
        return AnswerRocketClient(url=self.url, token=self.token)
    
    def _execute_single_question(self, question: str) -> QuestionResult:
        if not self.copilot_id:
            raise ValueError("No copilot_id set. Load questions from file first using load_questions_from_file().")
            
        start_time = time.time()
        try:
            client = self._create_client()
            result = client.chat.ask_question(self.copilot_id, question)
            execution_time = time.time() - start_time
            
            return QuestionResult(
                question=question,
                result=result,
                success=True,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return QuestionResult(
                question=question,
                result=None,
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def execute_questions_threaded(self, questions: List[str], max_workers: Optional[int] = None) -> List[QuestionResult]:
        if max_workers is None:
            max_workers = min(len(questions), 10)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_question = {
                executor.submit(self._execute_single_question, question): question 
                for question in questions
            }
            
            results = []
            for future in concurrent.futures.as_completed(future_to_question):
                result = future.result()
                results.append(result)
            
            results.sort(key=lambda x: questions.index(x.question))
            return results
    
    async def _execute_single_question_async(self, question: str) -> QuestionResult:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._execute_single_question, question)
    
    async def execute_questions_async(self, questions: List[str]) -> List[QuestionResult]:
        tasks = [self._execute_single_question_async(question) for question in questions]
        results = await asyncio.gather(*tasks)
        
        results_dict = {result.question: result for result in results}
        return [results_dict[question] for question in questions]
    
    def get_summary(self, results: List[QuestionResult]) -> Dict[str, Any]:
        total_questions = len(results)
        successful_questions = sum(1 for r in results if r.success)
        failed_questions = total_questions - successful_questions
        total_time = sum(r.execution_time for r in results)
        avg_time = total_time / total_questions if total_questions > 0 else 0
        
        return {
            'total_questions': total_questions,
            'successful': successful_questions,
            'failed': failed_questions,
            'success_rate': successful_questions / total_questions if total_questions > 0 else 0,
            'total_execution_time': total_time,
            'average_execution_time': avg_time,
            'errors': [{'question': r.question, 'error': r.error} for r in results if not r.success]
        }