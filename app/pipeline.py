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

    def process(self, question, clarification_answers=None):

        # Step 1: Parse intent
        intent = self.intent_parser.parse(question)

        # Step 2: Detect ambiguity
        ambiguities = self.ambiguity_detector.detect(intent)

        # Step 3: Apply clarification answers if provided
        if clarification_answers and ambiguities:

            if isinstance(clarification_answers, dict):

                for ambiguity in ambiguities:
                    if ambiguity in clarification_answers:
                        answer = clarification_answers[ambiguity]

                        intent = self.clarification_engine.apply_clarification(
                            intent,
                            ambiguity,
                            answer
                        )

            elif isinstance(clarification_answers, list):

                for ambiguity, answer in zip(
                    ambiguities,
                    clarification_answers
                ):
                    intent = self.clarification_engine.apply_clarification(
                        intent,
                        ambiguity,
                        answer
                    )

            # Re-check ambiguity after clarification
            ambiguities = self.ambiguity_detector.detect(intent)

        # Step 4: Ask for clarification if ambiguity still exists
        if ambiguities:

            clarification = self.clarification_engine.generate_questions(
                ambiguities
            )

            return {
                "status": "clarification_required",
                "question": question,
                "clarification": clarification,
                "ambiguities": ambiguities,
                "intent": intent.to_dict()
            }

        # Step 5: Generate SQL
        sql = self.sql_generator.generate(intent)

        if not sql:
            return {
                "status": "error",
                "message": "Could not generate a suitable SQL query.",
                "intent": intent.to_dict()
            }

        # Step 6: Validate SQL
        is_valid, validation_message = self.sql_validator.validate(sql)

        if not is_valid:
            return {
                "status": "error",
                "message": validation_message,
                "sql": sql,
                "intent": intent.to_dict()
            }

        # Step 7: Execute SQL
        data, error = self.sql_executor.execute(sql)

        if error:
            return {
                "status": "error",
                "message": error,
                "sql": sql,
                "intent": intent.to_dict()
            }

        # Step 8: Analyze result
        analysis = self.result_analyzer.analyze(data)

        # Step 9: Generate final answer
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