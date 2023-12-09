from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route("/verify-lean-proof", methods=["POST"])
def verify_lean_proof():
    try:
        # Extract Lean proof from the request
        proof = request.json.get("proof")

        proof_filename = "temp_proof.lean"
        # Write the proof to a temporary file
        with open(proof_filename, "w") as file:
            file.write(proof)

        # Run Lean to verify the proof
        result = subprocess.run(
            ["lean", proof_filename], capture_output=True, text=True
        )

        # Always remove the temporary file after running Lean to verify the proof
        os.remove(proof_filename)

        # Process result
        if result.returncode == 0:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Proof is valid",
                        "output": result.stdout,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Proof is invalid",
                        "output": result.stdout,
                        "error": result.stderr,
                    }
                ),
                400,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
