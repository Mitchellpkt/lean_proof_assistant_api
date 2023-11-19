import subprocess


def verify_lean_proof(proof):
    try:
        # Write the proof to a temporary file
        with open("temp_proof.lean", "w") as file:
            file.write(proof)

        # Run Lean to verify the proof
        result = subprocess.run(
            ["/home/bird/.elan/bin/lean", "temp_proof.lean"],
            capture_output=True,
            text=True,
        )

        # Process result
        if result.returncode == 0:
            return {"status": "success", "message": "Proof is valid"}
        else:
            return {
                "status": "error",
                "message": "Proof is invalid",
                "details": result.stderr,
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Example usage
if __name__ == "__main__":
    proof_string = "example : 1 + 1 = 2 := rfl"
    result = verify_lean_proof(proof_string)
    print(result)
