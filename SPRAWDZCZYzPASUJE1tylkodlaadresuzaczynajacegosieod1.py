import hashlib
from ecdsa import VerifyingKey, SECP256k1, util, ellipticcurve

def decompress_pubkey(compressed_hex):
    """
    Dekompresja skompresowanego klucza publicznego.
    """
    compressed = bytes.fromhex(compressed_hex)
    prefix = compressed[0]
    x = int.from_bytes(compressed[1:], "big")
    curve = SECP256k1.curve
    p = curve.p()
    # Dla SECP256k1: y^2 = x^3 + 7 mod p
    y_sq = (x**3 + 7) % p
    # Obliczamy pierwiastek modularny (używając p+1//4, bo p % 4 == 3)
    y = pow(y_sq, (p+1)//4, p)
    # Ustal poprawną parzystość y
    if (prefix == 0x02 and y % 2 != 0) or (prefix == 0x03 and y % 2 == 0):
        y = p - y
    return ellipticcurve.Point(curve, x, y)

# -------------------
# Dane z Twojej transakcji:
# Hash obliczony (z) w formacie big endian:
z_hex_big_endian = "dd37695b7387fb2198d0ed977411264e9841bf9e2322a9b6975c31aa44d8e405"
z = bytes.fromhex(z_hex_big_endian)

# Podpis (r, s) z sigscript:
r_hex = "642a1672db4db1fb8b9f7bf855614b59369d55bc4028d3b3e85b616cdc1ad348"
s_hex = "864145195db039847de1f4b0561202b7b03756a1cfedd63636bfda82d18a43e8"
r = int(r_hex, 16)
s = int(s_hex, 16)
# Tworzymy podpis jako ciąg 64 bajtów (r || s)
signature = util.sigencode_string(r, s, SECP256k1.order)

# Klucz publiczny (skompresowany) z sigscript:
public_key_compressed = "0362a0a96e44ce7ea433cce33feba1410d2c3d3153e5892d17cb553948317214c6"
point = decompress_pubkey(public_key_compressed)
vk = VerifyingKey.from_public_point(point, curve=SECP256k1)

# -------------------
# Weryfikacja podpisu:
try:
    # Używamy verify_digest, bo już mamy obliczony hash (z) jako digest
    verified = vk.verify_digest(signature, z)
    print("✅ Podpis jest poprawny!")
except Exception as e:
    print("❌ Podpis nie pasuje!", e)
