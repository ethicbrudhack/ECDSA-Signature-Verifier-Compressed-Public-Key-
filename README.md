# ✅ ECDSA Signature Verifier (Compressed Public Key)  
`verify_compressed_pubkey.py`

> ⚙️ Verifies an ECDSA `(r, s)` signature for a given message hash (`z`)  
> using a **compressed public key (02/03 format)** on the SECP256k1 curve.

---

## 🚀 Overview

This script reconstructs a **compressed SECP256k1 public key** (02/03 + X) into its full elliptic curve point,  
then verifies whether the provided `(r, s)` pair correctly signs the given 32-byte digest `z`.

It is ideal for validating Bitcoin-style signatures extracted from transaction scripts.

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 🔐 **Compressed key support** | Handles 33-byte pubkeys (prefix 02 / 03) |
| 🧮 **Mathematical EC decompression** | Recomputes Y from X using modular square root |
| ⚙️ **Digest-based verification** | Uses `verify_digest()` for pre-hashed inputs |
| 🧠 **No external dependencies beyond `ecdsa`** | Clean, standalone verification utility |
| 💾 **Minimal and fast** | Works instantly for any single ECDSA signature |

---

## 📂 Inputs

All values are given in **hexadecimal**.

| Parameter | Description |
|------------|-------------|
| `z_hex_big_endian` | 32-byte message digest (SHA-256 or transaction sighash) |
| `r_hex`, `s_hex` | Signature components |
| `public_key_compressed` | 33-byte compressed pubkey (starts with 02 or 03) |

---

### 🧪 Example Configuration

```python
z_hex_big_endian = "dd37695b7387fb2198d0ed977411264e9841bf9e2322a9b6975c31aa44d8e405"

r_hex = "642a1672db4db1fb8b9f7bf855614b59369d55bc4028d3b3e85b616cdc1ad348"
s_hex = "864145195db039847de1f4b0561202b7b03756a1cfedd63636bfda82d18a43e8"

public_key_compressed = "0362a0a96e44ce7ea433cce33feba1410d2c3d3153e5892d17cb553948317214c6"


⚙️ How It Works

Decompress the compressed public key

Extract x and compute y from the elliptic curve equation:

y² = x³ + 7 (mod p)


Resolve correct parity (even/odd) of y using prefix (02 → even, 03 → odd)

Build an ECDSA verifying key

VerifyingKey.from_public_point(point, curve=SECP256k1)

Prepare the signature

Combine r and s into a 64-byte structure using
util.sigencode_string(r, s, SECP256k1.order)

Verify

Execute:

vk.verify_digest(signature, z)

✅ Example Output
Valid Signature
✅ Signature is valid!

Invalid Signature
❌ Signature does not match! Invalid r/s/z combination.

🧠 Internal Math
Decompression Formula
Given compressed key:  prefix || X

y² ≡ x³ + 7  (mod p)
y = pow(y², (p + 1)//4, p)
if parity mismatch → y = p - y

Verification Equation

ECDSA checks:

r ≡ (x₁ mod n)
(x₁, y₁) = (u₁ * G + u₂ * Q)
u₁ = z * s⁻¹ mod n
u₂ = r * s⁻¹ mod n

⚡ Quick Run
python3 verify_compressed_pubkey.py


Output:

✅ Signature is valid!

🧩 Notes

The hash z must be exactly the digest that was signed (e.g., Bitcoin sighash).

For Bitcoin transaction validation, ensure endian consistency — use big-endian for this script.

Invalid length or mismatched parity will result in signature failure.

🔒 Ethical Use

This tool is for forensic validation and educational cryptography research only.
It enables verification of extracted or reconstructed ECDSA signatures from legitimate datasets.

You may:

Verify your own transaction signatures

Audit deterministic or hardware-based ECDSA implementations

You must not:

Use it to validate or test signatures without authorization

Apply it to third-party blockchain data for malicious purposes

⚖️ Respect cryptographic ethics — verification should be lawful and responsible.

🪪 License

MIT License
© 2025 — Author: [Ethicbrudhack]

💡 Summary

This verifier bridges compressed pubkeys and ECDSA math —
letting you confirm that your reconstructed (r, s, z) triples truly correspond
to the public key in its compressed (Bitcoin-native) format.

“Compression is storage; verification is truth.”
— [Ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
