import argparse
import ast
import json
import math
import operator
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Python Calculator</title>
  <style>
        * { box-sizing: border-box; }
    body {
      min-height: 100vh;
      margin: 0;
      display: grid;
      place-items: center;
      padding: 24px;
      background: radial-gradient(ellipse at top, #20283a 0%, #10131b 60%);
    }
    .calculator {
      width: min(100%, 380px);
      padding: 24px;
      border: 1px solid #30394b;
      border-radius: 24px;
      background: #191e29;
      box-shadow: 0 24px 70px #0008;
    }
    h1 {
      margin: 0 0 18px;
      font-size: 1rem;
      font-weight: 600;
      letter-spacing: .04em;
      color: #b9c3d8;
    }
    .display {
      min-height: 112px;
      margin-bottom: 18px;
      padding: 15px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      justify-content: flex-end;
      overflow: hidden;
      border-radius: 14px;
      background: #10141d;
    }
    #expression {
      width: 100%;
      min-height: 28px;
      overflow-wrap: anywhere;
      text-align: right;
      color: #9ba7bd;
      font-size: 1.05rem;
    }
    #result {
      width: 100%;
      overflow-wrap: anywhere;
      text-align: right;
      font-size: clamp(2rem, 10vw, 2.8rem);
      font-weight: 600;
    }
    .keys {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }
    button {
      min-height: 58px;
      border: 0;
      border-radius: 14px;
      background: #272e3c;
      color: #f5f6fa;
      font: inherit;
      font-size: 1.15rem;
      cursor: pointer;
      transition: background .15s, transform .08s;
    }
    button:hover { background: #343e51; }
    button:active { transform: scale(.96); }
    button.utility { color: #a9c5ff; background: #222d40; }
    button.operator { color: #b9ccff; background: #273755; }
    button.equals { color: #101522; background: #9bb8ff; font-weight: 700; }
    button.equals:hover { background: #b4caff; }
    .hint {
      margin: 16px 2px 0;
      color: #8994a8;
      font-size: .78rem;
      line-height: 1.5;
      text-align: center;
    }
  </style>
</head>
<body>
  <main class="calculator">
    <h1>PYTHON CALCULATOR</h1>
    <section class="display" aria-live="polite" aria-atomic="true">
      <div id="expression"></div>
      <div id="result">0</div>
    </section>
    <section class="keys" aria-label="Calculator buttons">
      <button class="utility" data-action="clear">AC</button>
      <button class="utility" data-action="delete" aria-label="Delete last character">DEL</button>
      <button class="operator" data-value="(">(</button>
      <button class="operator" data-value=")">)</button>
      <button data-value="7">7</button>
      <button data-value="8">8</button>
      <button data-value="9">9</button>
      <button class="operator" data-value="/">÷</button>
      <button data-value="4">4</button>
      <button data-value="5">5</button>
      <button data-value="6">6</button>
      <button class="operator" data-value="*">×</button>
      <button data-value="1">1</button>
      <button data-value="2">2</button>
      <button data-value="3">3</button>
      <button class="operator" data-value="-">−</button>
      <button data-value="0">0</button>
      <button data-value=".">.</button>
      <button class="operator" data-value="+">+</button>
      <button class="equals" data-action="equals">=</button>
    </section>
    <p class="hint">Type with your keyboard, press Enter to calculate, or Esc to clear.</p>
  </main>
  <script>
    const expressionDisplay = document.querySelector("#expression");
    const resultDisplay = document.querySelector("#result");
    let expression = "";
    let justCalculated = false;

    function render() {
      expressionDisplay.textContent = expression.replaceAll("*", "×").replaceAll("/", "÷");
      if (!expression) resultDisplay.textContent = "0";
    }

    function append(value) {
      if (justCalculated && /[0-9.(]/.test(value)) expression = "";
      justCalculated = false;
      expression += value;
      render();
    }

    async function calculate() {
      if (!expression.trim()) return;
      try {
        const response = await fetch("/calculate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ expression })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Could not calculate this expression.");
        resultDisplay.textContent = data.result;
        justCalculated = true;
      } catch (error) {
        resultDisplay.textContent = error.message;
        justCalculated = false;
      }
    }

    document.querySelector(".keys").addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button) return;
      if (button.dataset.action === "clear") {
        expression = "";
        justCalculated = false;
        resultDisplay.textContent = "0";
        render();
      } else if (button.dataset.action === "delete") {
        expression = expression.slice(0, -1);
        justCalculated = false;
        render();
      } else if (button.dataset.action === "equals") {
        calculate();
      } else {
        append(button.dataset.value);
      }
    });

    document.addEventListener("keydown", (event) => {
      if (/^[0-9.+*/()%-]$/.test(event.key)) append(event.key);
      else if (event.key === "Enter" || event.key === "=") {
        event.preventDefault();
        calculate();
      } else if (event.key === "Backspace") {
        expression = expression.slice(0, -1);
        justCalculated = false;
        render();
      } else if (event.key === "Escape") {
        expression = "";
        justCalculated = false;
        resultDisplay.textContent = "0";
        render();
      }
    });
  </script>
</body>
</html>
"""


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _checked(value):
    if type(value) not in (int, float):
        raise ValueError("Complex results are not supported.")
    if isinstance(value, int) and value.bit_length() > 4096:
        raise ValueError("Result is too large.")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("Result is outside the supported range.")
    return value


def calculate(expression):
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter an expression.")
    if len(expression) > 256:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError):
        raise ValueError("Invalid expression.") from None

    if sum(1 for _ in ast.walk(tree)) > 64:
        raise ValueError("Expression is too complex.")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return _checked(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent is too large.")
            try:
                return _checked(_BINARY_OPERATORS[type(node.op)](left, right))
            except (ArithmeticError, OverflowError) as error:
                raise ValueError(str(error) or "Invalid arithmetic operation.") from None
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _checked(_UNARY_OPERATORS[type(node.op)](evaluate(node.operand)))
        raise ValueError("Only numbers and basic arithmetic operators are allowed.")

    result = evaluate(tree)
    if isinstance(result, float):
        return format(result, ".12g")
    return str(result)


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Page not found")
            return
        page = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        if self.path != "/calculate":
            self.send_error(404, "Endpoint not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                raise ValueError("Invalid request size.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Request must contain an expression.")
            result = calculate(payload.get("expression"))
            self._send_json(200, {"result": result})
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})

    def _send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description="Run a browser-based Python calculator.")
    parser.add_argument(
        "--host",
        default=os.environ.get("HOST", "127.0.0.1"),
        help="Host interface to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", "8000")),
        help="Port to listen on (default: 8000)",
    )
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), CalculatorHandler)
    url = "http://{}:{}/".format(args.host if args.host != "0.0.0.0" else "127.0.0.1", args.port)
    if args.host in ("0.0.0.0", "::"):
        print("Calculator listening on {}:{}".format(args.host, args.port))
    else:
        print("Calculator running at {}".format(url))
        webbrowser.open(url)
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping calculator.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
