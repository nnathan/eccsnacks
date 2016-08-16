# dh_448.py
# Demonstrates generating keypair for Alice & Bob, and lastly
# compute Diffie-Hellman and compare keys.

from os import urandom
from eccsnacks.curve448 import scalarmult, scalarmult_base

# Private keys in Curve25519 can be any 56-byte string.
a = urandom(56)
a_pub = scalarmult_base(a)

b = urandom(56)
b_pub = scalarmult_base(b)

# perform Diffie-Hellman computation for alice and bob
k_ab = scalarmult(a, b_pub)
k_ba = scalarmult(b, a_pub)

# keys should be the same
assert k_ab == k_ba
