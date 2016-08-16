from binascii import unhexlify, hexlify

import pytest

from curve25519 import scalarmult, scalarmult_base


# From RFC7748 section 5.2:
#
#   Input scalar:
#     a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4
#   Input scalar as a number (base 10):
#     31029842492115040904895560451863089656
#     472772604678260265531221036453811406496
#   Input u-coordinate:
#     e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c
#   Input u-coordinate as a number (base 10):
#     34426434033919594451155107781188821651
#     316167215306631574996226621102155684838
#   Output u-coordinate:
#     c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552
#
#   Input scalar:
#     4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d
#   Input scalar as a number (base 10):
#     35156891815674817266734212754503633747
#     128614016119564763269015315466259359304
#   Input u-coordinate:
#     e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493
#   Input u-coordinate as a number (base 10):
#     88838573511839298940907593866106493194
#     17338800022198945255395922347792736741
#   Output u-coordinate:
#     95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957
@pytest.mark.parametrize(
    argnames="k,u,expected",
    ids=['0', '1'],
    argvalues=[
        (
            # 0
            'a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4',
            'e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c',
            'c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552',
        ),
        (
            # 1
            '4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d',
            'e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493',
            '95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957',
        ),
    ],
)
def test_kat(k, u, expected):
    k = unhexlify(k)
    u = unhexlify(u)
    assert hexlify(scalarmult(k, u)) == expected


# From RFC7748 section 5.2:
#
#    Initially, set k and u to be the following values:
#
#    For X25519:
#      0900000000000000000000000000000000000000000000000000000000000000
#
#    For each iteration, set k to be the result of calling the function
#    and u to be the old value of k.  The final result is the value left
#    in k.
#
#    X25519:
#
#    After one iteration:
#        422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079
#    After 1,000 iterations:
#        684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51
#    After 1,000,000 iterations:
#        7c3911e0ab2586fd864497297e575e6f3bc601c0883c30df5f4dd2d24f665424
@pytest.mark.parametrize(
    ids=lambda x: str(x[0]),
    argnames="n,expected",
    argvalues=[
        (1, "422c8e7a6227d7bca1350b3e2bb7279f7897b87bb6854b783c60e80311ae3079"),
        (1000, "684cf59ba83309552800ef566f2f4d3c1c3887c49360e3875f2eb94d99532c51"),
        # takes too long to run
        # (1000000, "7c3911e0ab2586fd864497297e575e6f3bc601c0883c30df5f4dd2d24f665424"),
    ]
)
def test_n(n, expected):
    k = unhexlify('0900000000000000000000000000000000000000000000000000000000000000')
    u = k
    for i in xrange(n):
        k, u = scalarmult(k, u), k

    assert hexlify(k) == expected


# From RFC7748 section 6.1
#   Test vector:
#
#   Alice's private key, a:
#     77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a
#   Alice's public key, X25519(a, 9):
#     8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a
#   Bob's private key, b:
#     5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb
#   Bob's public key, X25519(b, 9):
#     de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f
#   Their shared secret, K:
#     4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742
def test_dh():
    a_priv = unhexlify('77076d0a7318a57d3c16c17251b26645df4c2f87ebc0992ab177fba51db92c2a')
    a_pub = unhexlify('8520f0098930a754748b7ddcb43ef75a0dbf3a0d26381af4eba4a98eaa9b4e6a')
    b_priv = unhexlify('5dab087e624a8a4b79e17f8b83800ee66f3bb1292618b6fd1c2f8b27ff88e0eb')
    b_pub = unhexlify('de9edb7d7b7dc1b4d35b61c2ece435373f8343c85b78674dadfc7e146f882b4f')
    k = '4a5d9d5ba4ce2de1728e3bf480350f25e07e21c947d19e3376f09b3c1e161742'

    assert hexlify(scalarmult_base(a_priv)) == hexlify(a_pub)
    assert hexlify(scalarmult_base(b_priv)) == hexlify(b_pub)
    assert hexlify(scalarmult(a_priv, b_pub)) == k
    assert hexlify(scalarmult(b_priv, a_pub)) == k


def test_invalid_scalar():
    with pytest.raises(ValueError):
        scalarmult_base('\xff' * 64)
