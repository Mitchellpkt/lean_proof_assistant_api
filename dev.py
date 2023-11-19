import subprocess


def verify_lean_proof(proof):
    try:
        # Write the proof to a temporary file
        with open("temp_proof.lean", "w") as file:
            file.write(proof)

        # Run Lean to verify the proof
        run_result = subprocess.run(
            ["/home/bird/.elan/bin/lean", "temp_proof.lean"],
            capture_output=True,
            text=True,
        )

        print(run_result.stdout)

        # Process result
        if run_result.returncode == 0:
            return {"status": "success", "message": "Proof is valid"}
        else:
            return {
                "status": "error",
                "message": "Proof is invalid",
                "details": run_result.stderr,
            }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Example usage
if __name__ == "__main__":
    proof_string_1_plus_1: str = "example : 1 + 1 = 2 := rfl"
    proof_string_graph: str = """import data.set.basic -- import basic set theory
import data.nat.basic -- import basic natural number theory

universe u

-- Define a simple graph
structure simple_graph (V : Type u) :=
(edge : V → V → Prop) -- edge relation
(symm : symmetric edge) -- ensuring edges are symmetric
(loopless : irreflexive edge) -- no loops

-- Define the degree of a vertex
def degree {V : Type u} (G : simple_graph V) (v : V) : ℕ :=
set.cardinal (set_of (λ u, G.edge v u))

-- Prove the proposition
theorem degree_bound {V : Type u} {G : simple_graph V} {v : V} (n : ℕ) :
  finset.card (finset.univ : finset V) = n → degree G v < n :=
begin
  intro h,
  let vertices := finset.univ : finset V,
  have h_vertices : finset.card vertices = n, by rw h,
  
  let neighbors_of_v := set_of (λ u, G.edge v u),
  have h_subset : neighbors_of_v ⊆ vertices.erase v,
    from λ u hu, finset.mem_erase.mpr ⟨λ huv, G.loopless v huv, finset.mem_univ u⟩,

  have h_card_le : set.cardinal neighbors_of_v ≤ finset.card (vertices.erase v),
    from set.cardinal_le_of_subset h_subset,
  rw finset.card_erase_of_mem (finset.mem_univ v) at h_card_le,
  rw ←h_vertices at h_card_le,
  exact nat.lt_succ_iff.mp h_card_le,
end"""
    # result = verify_lean_proof(proof_string_1_plus_1)
    result = verify_lean_proof(proof_string_graph)
    print(result)
