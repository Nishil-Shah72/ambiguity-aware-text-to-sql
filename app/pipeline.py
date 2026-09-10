from app.schema_reader import get_database_schema
from app.intent_parser import IntentParser
from app.ambiguity_detector import AmbiguityDetector
from app.clarification_engine import ClarificationEngine
from app.sql_generator import SQLGenerator
from app.sql_validator import SQLValidator
from app.sql_executor import SQLExecutor
from app.result_analyzer import ResultAnalyzer
from app.answer_generator import AnswerGenerator


class TextToSQLPipeline:

    def __init__(self):
        self.schema = get_database_schema()

        self.intent_parser = IntentParser(self.schema)
        self.ambiguity_detector = AmbiguityDetector(self.schema)
        self.clarification_engine = ClarificationEngine()
        self.sql_generator = SQLGenerator(self.schema)
        self.sql_validator = SQLValidator()
        self.sql_executor = SQLExecutor()
        self.result_analyzer = ResultAnalyzer()
        self.answer_generator = AnswerGenerator()

    def process(self, question):

        # Step 1: Parse intent
        intent = self.intent_parser.parse(question)

        # Step 2: Detect ambiguity
        ambiguities = self.ambiguity_detector.detect(intent)

        # Step 3: Ask for clarification if needed
        if ambiguities:
            clarification = self.clarification_engine.generate_questions(
                ambiguities
            )

            return {
                "status": "clarification_required",
                "question": question,
                "clarification": clarification,
                "intent": intent.to_dict()
            }

        # Step 4: Generate SQL
        sql = self.sql_generator.generate(intent)

        # Step 5: Validate SQL
        is_valid, validation_message = self.sql_validator.validate(sql)

        if not is_valid:
            return {
                "status": "error",
                "message": validation_message
            }

        # Step 6: Execute SQL
        data, error = self.sql_executor.execute(sql)

        if error:
            return {
                "status": "error",
                "message": error,
                "sql": sql
            }

        # Step 7: Analyze result
        analysis = self.result_analyzer.analyze(data)

        # Step 8: Generate final answer
        answer = self.answer_generator.generate(
            question,
            analysis
        )

        return {
            "status": "success",
            "question": question,
            "intent": intent.to_dict(),
            "sql": sql,
            "analysis": analysis,
            "answer": answer
        }