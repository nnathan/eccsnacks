from binascii import unhexlify, hexlify

import pytest

from curve448 import scalarmult, scalarmult_base


# From RFC7748 section 5.2:
#   Input scalar:
#     3d262fddf9ec8e88495266fea19a34d28882acef045104d0d1aae121
#     700a779c984c24f8cdd78fbff44943eba368f54b29259a4f1c600ad3
#   Input scalar as a number (base 10):
#     599189175373896402783756016145213256157230856
#     085026129926891459468622403380588640249457727
#     683869421921443004045221642549886377526240828
#   Input u-coordinate:
#     06fce640fa3487bfda5f6cf2d5263f8aad88334cbd07437f020f08f9
#     814dc031ddbdc38c19c6da2583fa5429db94ada18aa7a7fb4ef8a086
#   Input u-coordinate as a number (base 10):
#     382239910814107330116229961234899377031416365
#     240571325148346555922438025162094455820962429
#     142971339584360034337310079791515452463053830
#   Output u-coordinate:
#     ce3e4ff95a60dc6697da1db1d85e6afbdf79b50a2412d7546d5f239f
#     e14fbaadeb445fc66a01b0779d98223961111e21766282f73dd96b6f
#
#   Input scalar:
#     203d494428b8399352665ddca42f9de8fef600908e0d461cb021f8c5
#     38345dd77c3e4806e25f46d3315c44e0a5b4371282dd2c8d5be3095f
#   Input scalar as a number (base 10):
#     633254335906970592779259481534862372382525155
#     252028961056404001332122152890562527156973881
#     968934311400345568203929409663925541994577184
#   Input u-coordinate:
#     0fbcc2f993cd56d3305b0b7d9e55d4c1a8fb5dbb52f8e9a1e9b6201b
#     165d015894e56c4d3570bee52fe205e28a78b91cdfbde71ce8d157db
#   Input u-coordinate as a number (base 10):
#     622761797758325444462922068431234180649590390
#     024811299761625153767228042600197997696167956
#     134770744996690267634159427999832340166786063
#   Output u-coordinate:
#     884a02576239ff7a2f2f63b2db6a9ff37047ac13568e1e30fe63c4a7
#     ad1b3ee3a5700df34321d62077e63633c575c1c954514e99da7c179d
@pytest.mark.parametrize(
    argnames='k,u,expected',
    ids=['0', '1'],
    argvalues=[
        (
            # id:0

            # input scalar
            '3d262fddf9ec8e88495266fea19a34d28882acef045104d0d1aae121'
            '700a779c984c24f8cdd78fbff44943eba368f54b29259a4f1c600ad3',

            # input u-coordinate
            '06fce640fa3487bfda5f6cf2d5263f8aad88334cbd07437f020f08f9'
            '814dc031ddbdc38c19c6da2583fa5429db94ada18aa7a7fb4ef8a086',

            # output u-coordinate
            'ce3e4ff95a60dc6697da1db1d85e6afbdf79b50a2412d7546d5f239f'
            'e14fbaadeb445fc66a01b0779d98223961111e21766282f73dd96b6f',
        ),
        (
            # id:1

            # input scalar
            '203d494428b8399352665ddca42f9de8fef600908e0d461cb021f8c5'
            '38345dd77c3e4806e25f46d3315c44e0a5b4371282dd2c8d5be3095f',

            # input u-coordinate
            '0fbcc2f993cd56d3305b0b7d9e55d4c1a8fb5dbb52f8e9a1e9b6201b'
            '165d015894e56c4d3570bee52fe205e28a78b91cdfbde71ce8d157db',

            # output u-coordinate
            '884a02576239ff7a2f2f63b2db6a9ff37047ac13568e1e30fe63c4a7'
            'ad1b3ee3a5700df34321d62077e63633c575c1c954514e99da7c179d',
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
#    For X448:
#      05000000000000000000000000000000000000000000000000000000
#      00000000000000000000000000000000000000000000000000000000
#
#    For each iteration, set k to be the result of calling the function
#    and u to be the old value of k.  The final result is the value left
#    in k.
#
#    X448:
#
#    After one iteration:
#        3f482c8a9f19b01e6c46ee9711d9dc14fd4bf67af30765c2ae2b846a
#        4d23a8cd0db897086239492caf350b51f833868b9bc2b3bca9cf4113
#    After 1,000 iterations:
#        aa3b4749d55b9daf1e5b00288826c467274ce3ebbdd5c17b975e09d4
#        af6c67cf10d087202db88286e2b79fceea3ec353ef54faa26e219f38
#    After 1,000,000 iterations:
#        077f453681caca3693198420bbe515cae0002472519b3e67661a7e89
#        cab94695c8f4bcd66e61b9b9c946da8d524de3d69bd9d9d66b997e37
@pytest.mark.parametrize(
    ids=lambda x: str(x[0]),
    argnames='n,expected',
    argvalues=[
        (1,
         '3f482c8a9f19b01e6c46ee9711d9dc14fd4bf67af30765c2ae2b846a'
         '4d23a8cd0db897086239492caf350b51f833868b9bc2b3bca9cf4113'),
        (1000,
         'aa3b4749d55b9daf1e5b00288826c467274ce3ebbdd5c17b975e09d4'
         'af6c67cf10d087202db88286e2b79fceea3ec353ef54faa26e219f38'),
        #  takes too long to run
        # (1000000,
        #  '077f453681caca3693198420bbe515cae0002472519b3e67661a7e89'
        #  'cab94695c8f4bcd66e61b9b9c946da8d524de3d69bd9d9d66b997e37'),
    ]
)
def test_n(n, expected):
    k = unhexlify(
        '05000000000000000000000000000000000000000000000000000000'
        '00000000000000000000000000000000000000000000000000000000',
    )
    u = k
    for i in xrange(n):
        k, u = scalarmult(k, u), k

    assert hexlify(k) == expected


# From RFC7748 section 6.1
#   Test vector:
#
#   Alice's private key, a:
#     9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28d
#     d9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b
#   Alice's public key, X448(a, 5):
#     9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c
#     22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0
#   Bob's private key, b:
#     1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d
#     6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d
#   Bob's public key, X448(b, 5):
#     3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b430
#     27d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609
#   Their shared secret, K:
#     07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282b
#     b60c0b56fd2464c335543936521c24403085d59a449a5037514a879d
def test_dh():
    a_priv = unhexlify(
        '9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28d'
        'd9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b'
    )
    a_pub = unhexlify(
        '9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c'
        '22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0'
    )
    b_priv = unhexlify(
        '1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d'
        '6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d'
    )
    b_pub = unhexlify(
        '3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b430'
        '27d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609'
    )

    k = (
        '07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282b'
        'b60c0b56fd2464c335543936521c24403085d59a449a5037514a879d'
    )

    assert hexlify(scalarmult_base(a_priv)) == hexlify(a_pub)
    assert hexlify(scalarmult_base(b_priv)) == hexlify(b_pub)
    assert hexlify(scalarmult(a_priv, b_pub)) == k
    assert hexlify(scalarmult(b_priv, a_pub)) == k


def test_invalid_scalar():
    with pytest.raises(ValueError):
        scalarmult_base('\xff' * 64)
