from flask import Flask, request, jsonify
from vllm import LLMEngine, SamplingParams, EngineArgs

app = Flask(__name__)

try:
    engine_args = EngineArgs(model="Qwen/Qwen2.5-0.5B-Instruct", device="cuda")
    engine = LLMEngine.from_engine_args(engine_args)
except RuntimeError as e:
    print(f"Initialization Error: {e}")
    exit(1)

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")
    sampling_params = SamplingParams(max_tokens=100)
    request_id = "1"
    engine.add_request(request_id, prompt, sampling_params)

    while True:
        outputs = engine.step()
        for output in outputs:
            if output.finished:
                return jsonify({"response": output.outputs[0].text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
