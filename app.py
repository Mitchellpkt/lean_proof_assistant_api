from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants for resource limits (adjust as needed)
MAX_PROOF_SIZE = 10_000
TEMP_FILE_PLACEHOLDER = "proof"


@app.route("/verify-lean-proof", methods=["POST"])
def verify_lean_proof():
    proof = request.json.get("proof", "")

    # Input validation
    if not isinstance(proof, str):
        return jsonify({"status": "error", "message": "Proof must be a string"}), 400

    if len(proof) > MAX_PROOF_SIZE:
        return jsonify({"status": "error", "message": "Proof is too large"}), 400

    # Create a temporary file with the proof that will auto-delete on close
    with tempfile.NamedTemporaryFile(
        suffix=".lean", mode="w", delete=False
    ) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(proof)

    try:
        # Run Lean to verify the proof and apply a timeout (e.g., 30 seconds)
        result = subprocess.run(
            ["lean", temp_file_name], capture_output=True, text=True, timeout=30
        )

        # Remove temporary file name from errors
        output = result.stdout.replace(temp_file_name, TEMP_FILE_PLACEHOLDER)
        error = result.stderr.replace(temp_file_name, TEMP_FILE_PLACEHOLDER)

        # Interpret the results
        if result.returncode == 0:
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Proof is valid",
                        "output": output,
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
                        "output": output,
                        "error": error,
                    }
                ),
                400,
            )

    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Verification timed out"}), 400
    except Exception as e:
        logging.error("An error occurred: %s", e)
        sanitized_message = str(e).replace(temp_file_name, TEMP_FILE_PLACEHOLDER)
        return jsonify({"status": "error", "message": sanitized_message}), 500
    finally:
        # Clean up temporary file
        if temp_file_name and os.path.exists(temp_file_name):
            os.remove(temp_file_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
