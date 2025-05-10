from flask import Blueprint, request, jsonify
from langchain_community.chat_models import ChatOpenAI

from app import API_KEY_OPENAI
from app.services.solution_service import solve_math_problem_deepseek, solve_math_problem_agent, \
    solve_math_problem_openai, \
    evaluate_student_answer_openai, evaluate_student_answer_deepseek, evaluate_student_answer_agent
from app.services.utils import clean_latex

solution_bp = Blueprint("solution", __name__)

llm_reasoning = ChatOpenAI(openai_api_key=API_KEY_OPENAI,
                           model_name="ft:gpt-4o-2024-08-06:exmersive:soln-wellaround:BMSGlkkQ", temperature=0.1)

# create ping route
@solution_bp.route("/ping", methods=["GET"])
def ping():
    try:
        response = llm_reasoning.invoke("Ping")
        return jsonify({"success": True, "response": response.content}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 解題接口
@solution_bp.route("/solve", methods=["POST"])
def solve():
    try:
        latex_equation = request.json.get("question", "")
        topic = request.json.get("topic", "")

        if (latex_equation == ""):
            return jsonify({"success": False, "error": "question: No latex equation provided."}), 400
        solution = solve_math_problem_agent(latex_equation, topic)
        # TODO: fix latex
        # for i, step in enumerate(solution.get("steps")):
        #     solution["steps"][i] = clean_latex(solution["steps"][i])

        # data = {"success": True, "solution": solution, "model": "o3-mini"}
        return jsonify({"success": True, "solution": solution, "model": "o3-mini"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@solution_bp.route("/evaluate", methods=["POST"])
def evaluate():
    try:

        steps = request.json.get("steps", "")
        final_answer = request.json.get("final_answer", "")
        question = request.json.get("question", "")
        sampleAnswer = request.json.get("sample_answer", "")

        if (steps == ""):
            return jsonify({"success": False, "error": "steps: No steps provided."}), 400
        if (final_answer == ""):
            return jsonify({"success": False, "error": "answer: No answer provided."}), 400
        evaluation = evaluate_student_answer_agent(question, steps, final_answer, str(sampleAnswer))
        return jsonify({"success": True, "evaluation": evaluation})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
