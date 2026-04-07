# test_methods.py

class TestAICustomerServiceBot:
    """A test bench for evaluating CustomerServiceBot implementations. This class provides
    comprehensive testing of all required functionality while offering clear feedback
    about what's working and what needs improvement."""
    
    def __init__(self, bot_instance):
        """Initialize the test bench with a bot instance to test. We'll use this same
        instance across all our tests to evaluate its functionality comprehensively."""
        self.bot = bot_instance
        self.test_results = {}

    def run_all_tests(self) -> dict:
        """Execute all tests and provide a comprehensive evaluation report. This method
        runs each test in sequence, collecting results and generating helpful feedback."""
        
        # Store all test results
        self.test_results = {
            "initialization": self._test_initialization(),
            "example_database": self._test_example_database(),
            "response_generation": self._test_response_generation(),
            "error_handling": self._test_error_handling()
        }
        
        # Calculate overall score and generate report
        return self._generate_report()

    def _test_initialization(self) -> dict:
        """Test the proper initialization of the bot. This verifies that all required
        components are present and correctly configured."""
        
        score = 100
        feedback = []
        
        # Test client initialization
        if not hasattr(self.bot, 'client'):
            score -= 25
            feedback.append("OpenAI client not properly initialized")
        
        # Test tone definitions
        if not hasattr(self.bot, 'valid_tones'):
            score -= 25
            feedback.append("Valid tones not defined")
        else:
            required_tones = {"professional", "friendly", "formal", "empathetic"}
            missing_tones = required_tones - set(self.bot.valid_tones.keys())
            if missing_tones:
                score -= 15
                feedback.append(f"Missing required tones: {missing_tones}")

        # Test example database
        if not hasattr(self.bot, 'example_database'):
            score -= 25
            feedback.append("Example database not initialized")
        else:
            required_categories = {"refund", "technical_support", "general_inquiry"}
            missing_categories = required_categories - set(self.bot.example_database.keys())
            if missing_categories:
                score -= 15
                feedback.append(f"Missing required categories: {missing_categories}")

        return {
            "score": max(0, score),
            "feedback": feedback if feedback else ["All initialization tests passed successfully"]
        }

    def _test_example_database(self) -> dict:
        """Evaluate the quality and structure of the example database. This ensures
        that examples are properly formatted and contain all required information."""
        
        score = 100
        feedback = []
        
        try:
            for category, examples in self.bot.example_database.items():
                # Check example format
                if not isinstance(examples, list):
                    score -= 20
                    feedback.append(f"Examples for {category} should be a list")
                    continue

                # Check example content
                for i, example in enumerate(examples):
                    required_fields = {"customer", "response", "tone"}
                    missing_fields = required_fields - set(example.keys())
                    
                    if missing_fields:
                        score -= 10
                        feedback.append(f"Example {i} in {category} missing fields: {missing_fields}")
                    
                    if 'tone' in example and example['tone'] not in self.bot.valid_tones:
                        score -= 5
                        feedback.append(f"Invalid tone in example {i} of {category}")

        except Exception as e:
            score = 0
            feedback.append(f"Error accessing example database: {str(e)}")

        return {
            "score": max(0, score),
            "feedback": feedback if feedback else ["Example database structure is correct"]
        }

    def _test_response_generation(self) -> dict:
        """Test the bot's ability to generate appropriate responses. This verifies
        that the bot can handle different scenarios and maintain appropriate tone."""
        
        score = 100
        feedback = []
        
        test_cases = [
            {
                "message": "I need a refund for my broken product",
                "category": "refund",
                "tone": "empathetic",
                "expected_elements": ["apology", "refund", "process"]
            },
            {
                "message": "How do I reset my password?",
                "category": "technical_support",
                "tone": "professional",
                "expected_elements": ["steps", "password", "reset"]
            }
        ]

        try:
            for case in test_cases:
                response = self.bot.generate_response(
                    case["message"],
                    case["category"],
                    case["tone"]
                )
                
                # Check response content
                if not response or len(response.split()) < 10:
                    score -= 20
                    feedback.append(f"Response too short for: {case['message']}")
                    continue

                # Check for expected elements
                missing_elements = [
                    elem for elem in case["expected_elements"] 
                    if elem.lower() not in response.lower()
                ]
                if missing_elements:
                    score -= 10
                    feedback.append(f"Response missing elements: {missing_elements}")

        except Exception as e:
            score = 0
            feedback.append(f"Error generating responses: {str(e)}")

        return {
            "score": max(0, score),
            "feedback": feedback if feedback else ["Response generation working correctly"]
        }

    def _test_error_handling(self) -> dict:
        """Test how well the bot handles error cases and invalid inputs. This ensures
        the implementation is robust and gracefully handles problematic situations."""
        
        score = 100
        feedback = []
        
        error_cases = [
            ("", "refund", "professional", "empty message"),
            ("Help", "invalid_category", "professional", "invalid category"),
            ("Help", "refund", "invalid_tone", "invalid tone")
        ]

        for message, category, tone, case_name in error_cases:
            try:
                self.bot.generate_response(message, category, tone)
                score -= 30
                feedback.append(f"Failed to catch {case_name}")
            except ValueError:
                # This is expected
                pass
            except Exception as e:
                score -= 20
                feedback.append(f"Wrong error type for {case_name}: {str(e)}")

        return {
            "score": max(0, score),
            "feedback": feedback if feedback else ["Error handling working correctly"]
        }

    def _generate_report(self) -> dict:
        """Generate a comprehensive report of all test results. This provides clear
        feedback about the implementation's strengths and areas for improvement."""
        
        total_score = sum(result["score"] for result in self.test_results.values())
        average_score = total_score / len(self.test_results)
        
        report = {
            "total_score": average_score,
            "component_scores": self.test_results,
            "summary": []
        }

        # Generate summary feedback
        if average_score >= 90:
            report["summary"].append("Excellent implementation! All major components working well.")
        elif average_score >= 75:
            report["summary"].append("Good implementation with some areas for improvement.")
        elif average_score >= 50:
            report["summary"].append("Implementation needs significant improvement.")
        else:
            report["summary"].append("Implementation requires major revision.")

        # Add specific component feedback
        for component, result in self.test_results.items():
            if result["score"] < 70:
                report["summary"].append(f"{component} needs attention: {', '.join(result['feedback'])}")

        return report

def print_test_results(results: dict):
    """Print the test results in a clear, readable format. This helps students
    understand their implementation's strengths and weaknesses."""
    
    print("\n=== CustomerServiceBot Implementation Test Results ===")
    print(f"\nOverall Score: {results['total_score']:.2f}%")
    
    print("\nComponent Breakdown:")
    for component, result in results['component_scores'].items():
        print(f"\n{component.title()}:")
        print(f"Score: {result['score']}%")
        print("Feedback:")
        for feedback in result['feedback']:
            print(f"- {feedback}")
    
    print("\nSummary:")
    for summary_point in results['summary']:
        print(f"- {summary_point}")