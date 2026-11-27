from google import genai
from dotenv import load_dotenv
from datetime import datetime
import ast
import operator

load_dotenv()
client = genai.Client()

MODEL = "gemini-3.5-flash-lite"
MAX_ROUNDS = 5

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.USub: operator.neg,
    ast.UnaryOp: operator.add,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def calculate(expr):
    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Недопустимое выражение")

    return _eval(ast.parse(expr, mode="eval").body)


get_time_schema = {
    "type": "function",
    "name": "get_time",
    "description": "returns current time There is no need you know my location!",
    "parameters": {"type": "OBJECT", "properties": {}, "required": []},
}

calculate_schema = {
    "type": "function",
    "name": "calculate",
    "description": "returns the result of expression, for example you pass 100 + 2, function returns 102",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "expr": {"type": "STRING", "description": "math expression, e.g. 20+20"}
        },
        "required": ["expr"],
    },
}

functions = {"get_time": get_time, "calculate": calculate}
tools = [get_time_schema, calculate_schema]


def run_tool(step):
    # print(f"[TOOL CALL] {step.name}({step.arguments})")
    func = functions.get(step.name)
    if func is None:
        return f"Error: unknown function '{step.name}'"
    try:
        return str(func(**step.arguments))
    except Exception as e:
        return f"Error: {e}"


def ask(user_text):
    interaction = client.interactions.create(
        model=MODEL,
        input=user_text,
        tools=tools,
    )

    for _ in range(MAX_ROUNDS):
        calls = [s for s in interaction.steps if s.type == "function_call"]
        print(calls)

        if not calls:  # модель ответила текстом, выходим
            return interaction.output_text

        results = [
            {
                "type": "function_result",
                "name": call.name,
                "call_id": call.id,
                "result": run_tool(call),
            }
            for call in calls
        ]

        interaction = client.interactions.create(
            model=MODEL,
            input=results,
            previous_interaction_id=interaction.id,
            tools=tools,
        )

    return "Лимит кругов исчерпан, модель не дала финальный ответ"


if __name__ == "__main__":
    print(ask("Hello! What is current time and 10+2)"))






# 1. Send the user's message and available tools to Gemini.
# 2. Gemini decides which functions need to be called.
# 3. Our program executes the requested functions.
# 4. Send all function results back to Gemini.
# 5. Gemini processes the results and generates a final response.
# 6. If Gemini requests more functions, repeat the process.
