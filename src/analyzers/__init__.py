"""
AI-powered error analysis and explanation.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import os
import json
import re


@dataclass
class ErrorAnalysis:
    """Result of AI analysis on a single error."""
    error_type: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    explanation: str  # Plain English explanation
    root_cause: str
    suggestions: List[str]  # Actionable fix suggestions
    code_examples: Optional[List[str]] = None
    related_docs: Optional[List[str]] = None


class AIAnalyzer:
    """Analyzes errors using AI to provide explanations and fixes."""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "claude"):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY')
        self.provider = provider if api_key else ('claude' if os.getenv('ANTHROPIC_API_KEY') else 'openai')
        
        # Cache for repeated errors
        self.cache: Dict[str, ErrorAnalysis] = {}
        
        # Common error patterns knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def analyze(self, error_message: str, stack_trace: Optional[str] = None) -> ErrorAnalysis:
        """Analyze a single error using AI."""
        
        # Check cache first
        cache_key = self._make_cache_key(error_message)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try knowledge base first (faster, no API call)
        kb_result = self._check_knowledge_base(error_message)
        if kb_result:
            self.cache[cache_key] = kb_result
            return kb_result
        
        # Use AI for unknown errors
        if self.api_key:
            analysis = self._analyze_with_ai(error_message, stack_trace)
            self.cache[cache_key] = analysis
            return analysis
        
        # Fallback if no API key
        return self._basic_analysis(error_message)
    
    def batch_analyze(self, errors: List[Dict]) -> List[ErrorAnalysis]:
        """Analyze multiple errors efficiently."""
        results = []
        for error in errors:
            analysis = self.analyze(
                error.get('message', ''),
                error.get('stack_trace')
            )
            results.append(analysis)
        return results
    
    def _analyze_with_ai(self, error_message: str, stack_trace: Optional[str]) -> ErrorAnalysis:
        """Use AI to analyze the error."""
        
        prompt = self._build_prompt(error_message, stack_trace)
        
        try:
            if self.provider == "claude":
                response = self._call_claude(prompt)
            else:
                response = self._call_openai(prompt)
            
            return self._parse_ai_response(response)
        except Exception as e:
            # Fallback to basic analysis if AI fails
            print(f"AI analysis failed: {e}")
            return self._basic_analysis(error_message)
    
    def _build_prompt(self, error_message: str, stack_trace: Optional[str]) -> str:
        """Build the AI prompt."""
        prompt = f"""You are a senior software engineer helping debug an application error.

Analyze this error and provide a clear, actionable response:

ERROR MESSAGE:
{error_message}

"""
        
        if stack_trace:
            prompt += f"""
STACK TRACE:
{stack_trace[:2000]}  # Limit stack trace length

"""
        
        prompt += """
Please provide your analysis in this exact JSON format:
{
  "error_type": "Brief error type (e.g., Database Connection Error)",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "explanation": "Plain English explanation of what happened (2-3 sentences)",
  "root_cause": "The underlying cause (1-2 sentences)",
  "suggestions": [
    "Step 1 to fix",
    "Step 2 to fix",
    "Step 3 to fix"
  ],
  "code_examples": [
    "// Optional code example"
  ]
}

Guidelines:
- Be specific and actionable
- Use simple language (avoid jargon when possible)
- Provide numbered steps
- Include commands/code when relevant
- Be helpful and encouraging
"""
        
        return prompt
    
    def _call_claude(self, prompt: str) -> str:
        """Call Claude API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def _parse_ai_response(self, response: str) -> ErrorAnalysis:
        """Parse AI response into structured format."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]+\}', response)
            if json_match:
                data = json.loads(json_match.group(0))
                return ErrorAnalysis(
                    error_type=data.get('error_type', 'Unknown Error'),
                    severity=data.get('severity', 'MEDIUM'),
                    explanation=data.get('explanation', ''),
                    root_cause=data.get('root_cause', ''),
                    suggestions=data.get('suggestions', []),
                    code_examples=data.get('code_examples', [])
                )
        except (json.JSONDecodeError, AttributeError):
            pass
        
        # Fallback: return basic analysis
        return ErrorAnalysis(
            error_type='Analysis Error',
            severity='MEDIUM',
            explanation=response[:200],
            root_cause='Unable to parse AI response',
            suggestions=['Please try again or check the error manually']
        )
    
    def _basic_analysis(self, error_message: str) -> ErrorAnalysis:
        """Basic analysis without AI."""
        
        # Pattern matching for common errors
        error_lower = error_message.lower()
        
        if 'econnrefused' in error_lower or 'connection refused' in error_lower:
            return ErrorAnalysis(
                error_type='Connection Error',
                severity='HIGH',
                explanation='A connection to a service or database was refused.',
                root_cause='The target service is not running or not accepting connections.',
                suggestions=[
                    'Check if the service is running',
                    'Verify the connection settings (host, port)',
                    'Check firewall rules'
                ]
            )
        
        if 'etimedout' in error_lower or 'timeout' in error_lower:
            return ErrorAnalysis(
                error_type='Timeout Error',
                severity='MEDIUM',
                explanation='An operation took too long and timed out.',
                root_cause='The service is slow or unreachable.',
                suggestions=[
                    'Check network connectivity',
                    'Increase timeout settings',
                    'Check service health'
                ]
            )
        
        if 'enoent' in error_lower or 'no such file' in error_lower:
            return ErrorAnalysis(
                error_type='File Not Found',
                severity='MEDIUM',
                explanation='A required file or directory was not found.',
                root_cause='The file path is incorrect or the file was deleted.',
                suggestions=[
                    'Verify the file path',
                    'Check if the file exists',
                    'Check file permissions'
                ]
            )
        
        if 'permission denied' in error_lower or 'eacces' in error_lower:
            return ErrorAnalysis(
                error_type='Permission Error',
                severity='MEDIUM',
                explanation='Insufficient permissions to perform the operation.',
                root_cause='The user lacks necessary permissions.',
                suggestions=[
                    'Check file/directory permissions',
                    'Run with appropriate privileges',
                    'Check user roles'
                ]
            )
        
        # Generic error
        return ErrorAnalysis(
            error_type='Application Error',
            severity='MEDIUM',
            explanation=f'An error occurred: {error_message[:100]}',
            root_cause='Unknown - requires investigation',
            suggestions=[
                'Check the error message for clues',
                'Review recent changes',
                'Check application logs for more context'
            ]
        )
    
    def _check_knowledge_base(self, error_message: str) -> Optional[ErrorAnalysis]:
        """Check if error matches known patterns."""
        error_lower = error_message.lower()
        
        for pattern, analysis in self.knowledge_base.items():
            if pattern in error_lower:
                return analysis
        
        return None
    
    def _load_knowledge_base(self) -> Dict[str, ErrorAnalysis]:
        """Load common error patterns."""
        return {
            'econnrefused': ErrorAnalysis(
                error_type='Connection Refused',
                severity='HIGH',
                explanation='Cannot connect to the specified host and port.',
                root_cause='The target service is not running or not accessible.',
                suggestions=[
                    'Verify the service is running: `sudo systemctl status <service>`',
                    'Check the connection URL and port',
                    'Test connectivity: `telnet <host> <port>`'
                ]
            ),
            'enoent': ErrorAnalysis(
                error_type='File Not Found',
                severity='MEDIUM',
                explanation='A required file or directory does not exist.',
                root_cause='The file path is incorrect or the file was deleted.',
                suggestions=[
                    'Verify the file path is correct',
                    'Check if the file exists: `ls -la <path>`',
                    'Check file permissions'
                ]
            ),
            'etimedout': ErrorAnalysis(
                error_type='Timeout Error',
                severity='MEDIUM',
                explanation='The operation did not complete within the timeout period.',
                root_cause='Network issues or service is overloaded.',
                suggestions=[
                    'Check network connectivity',
                    'Increase timeout value in config',
                    'Check service health and performance'
                ]
            ),
            'permission denied': ErrorAnalysis(
                error_type='Permission Denied',
                severity='MEDIUM',
                explanation='Insufficient permissions to access the resource.',
                root_cause='The current user lacks necessary permissions.',
                suggestions=[
                    'Check file/directory permissions: `ls -la`',
                    'Run with appropriate privileges (sudo if needed)',
                    'Verify user is in correct group'
                ]
            ),
        }
    
    def _make_cache_key(self, error_message: str) -> str:
        """Create cache key from error message."""
        # Normalize error message for caching
        return error_message.strip().lower()[:100]
