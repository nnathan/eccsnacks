# eccsnacks

This package contains a simple reference implementation of Curve25519 and Curve448 (goldilocks) as specified in [RFC7748](https://tools.ietf.org/html/rfc7748).

**Caution:** this implementation is inadvisable for use if timing invariance matters. Future versions of this package may implement a C backend.

*eccsnacks* is a play on the word [ecchacks](http://ecchacks.cr.yp.to/), a cool site by djb and Tanja Lange.

## Installation

`pip install eccsnacks`

## Usage

These examples demonstrate the [Diffie-Hellman operation](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) for each curve.

#### Curve25519:

```python
from os import urandom
from eccsnacks.curve25519 import scalarmult, scalarmult_base

# Private keys in Curve25519 can be any 32-byte string.
a = urandom(32)
a_pub = scalarmult_base(a)

b = urandom(32)
b_pub = scalarmult_base(b)

# perform Diffie-Hellman computation for alice and bob
k_ab = scalarmult(a, b_pub)
k_ba = scalarmult(b, a_pub)

# keys should be the same
assert k_ab == k_ba
```

#### Curve448:

```python
from os import urandom
from eccsnacks.curve448 import scalarmult, scalarmult_base

# Private keys in Curve448 can be any 32-byte string.
a = urandom(56)
a_pub = scalarmult_base(a)

b = urandom(56)
b_pub = scalarmult_base(b)

# perform Diffie-Hellman computation for alice and bob
k_ab = scalarmult(a, b_pub)
k_ba = scalarmult(b, a_pub)

# keys should be the same
assert k_ab == k_ba
```

## Todo

 * Fast timing invariant implementation of both curves in C.
 * More curves.

## Alternatives

 * [curve25519-donna](https://pypi.python.org/pypi/curve25519-donna)
 * [python-pure25519](https://github.com/warner/python-pure25519)
 * [pynacl](https://github.com/pyca/pynacl)
 * [pysodium](https://github.com/stef/pysodium)
 * ... and more can be found [on pypi](https://pypi.org/search/?q=curve25519)


## Acknowledgements

* Matthew Dempsky for [slownacl](https://github.com/openalias/dnscrypt-python/tree/master/slownacl) which initially served as a baseline when implementing Curve25519.

* djb for Curve25519

* Mike Hamburg for Curve448
