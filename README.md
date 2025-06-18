<h1 align="center">⚛️ Quantum Algorithms Simulation</h1>

<p align="center">
  <b>DRDO Internship Project – Quantum Computing</b><br>
  Simulating foundational quantum algorithms with <code>Qiskit</code> (No Aer module)
</p>

---

## 📌 Overview

This repository presents simulations of essential quantum algorithms designed for educational and demonstration purposes. All circuits are constructed and visualized using **Qiskit**, and made to run **without the Aer simulator**, ensuring compatibility with basic Python setups.

> 💡 Ideal for visually showcasing how quantum algorithms outperform classical counterparts.

---

## 📂 Algorithms Included

<details>
<summary>🔍 <b>1. Grover's Algorithm</b></summary>

- **Goal:** Find a marked item in an unsorted list using amplitude amplification.
- **Quantum Advantage:** Quadratic speedup (√N queries).
- **Includes:**
  - Target state oracle
  - Diffuser circuit
  - Visualization: ASCII circuit + histogram

</details>

<details>
<summary>🧠 <b>2. Bernstein–Vazirani Algorithm</b></summary>

- **Goal:** Discover a hidden binary string `s` using a single quantum query.
- **Quantum Advantage:** Reduces from N classical queries to 1 quantum query.
- **Includes:**
  - Oracle encoding dot-product with secret `s`
  - Hadamard interferometry
  - Clear histogram of `s`

</details>

<details>
<summary>🧪 <b>3. Deutsch–Jozsa Algorithm</b></summary>

- **Goal:** Determine if a function is constant or balanced.
- **Quantum Advantage:** Only 1 evaluation needed (vs 2ⁿ/2 + 1 classically).
- **Includes:**
  - Oracle for balanced/constant function
  - Hadamard-based interference
  - Output interpretation: all-zeros or otherwise

</details>

<details>
<summary>🧮 <b>4. Shor’s Algorithm (Illustrative)</b></summary>

- **Goal:** Factor integers using period-finding via QPE.
- **Quantum Advantage:** Exponential speedup over classical factoring.
- **Includes:**
  - QPE structure for base `a = 7`, `N = 15`
  - Quantum Fourier Transform
  - Simulated modular exponentiation (placeholder)

> ⚠️ Factoring is not performed due to lack of full modular exponentiation support.

</details>

<details>
<summary>🔐 <b>5. Schnorr’s Algorithm (Simulated Discrete Log)</b></summary>

- **Goal:** Solve for `x` in `a^x ≡ b mod p` (Discrete Log Problem).
- **Use Case:** Foundational to cryptographic schemes like digital signatures.
- **Includes:**
  - Classical brute-force check
  - QPE-style circuit for concept illustration
  - Inverse QFT and register measurement

</details>

<details>
<summary>🧩 <b>6. Simon’s Algorithm</b></summary>

- **Goal:** Find secret bitstring `s` in a 2-to-1 function satisfying `f(x) = f(x⊕s)`.
- **Quantum Advantage:** Exponential speedup over classical brute-force.
- **Includes:**
  - Function oracle with secret mask
  - Hadamard-based pattern discovery
  - ASCII quantum circuit + measurement results

</details>

---

## 🛠️ Tech Stack

| Tool        | Purpose                               |
|-------------|----------------------------------------|
| `Qiskit`    | Quantum circuit simulation & drawing   |
| `Statevector` | Lightweight simulation backend      |
| `matplotlib`| Histograms and result visualization   |

---

## 🧪 How to Run

```bash
# Step 1: Install requirements
pip install qiskit matplotlib

# Step 2: Run any algorithm script
python grover.py
python deutsch_jozsa.py
...
