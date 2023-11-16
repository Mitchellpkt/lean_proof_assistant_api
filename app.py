from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/verify-lean-proof', methods=['POST'])
def verify_lean_proof():
    try:
        # Extract Lean proof from the request
        proof = request.json.get('proof')

        # Write the proof to a temporary file
        with open('temp_proof.lean', 'w') as file:
            file.write(proof)

        # Run Lean to verify the proof
        result = subprocess.run(['lean', 'temp_proof.lean'], capture_output=True, text=True)

        # Process result
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': 'Proof is valid'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Proof is invalid', 'details': result.stderr}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
