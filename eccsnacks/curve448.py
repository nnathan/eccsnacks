__all__ = ['scalarmult', 'scalarmult_base']

# implementation is a translation of the pseudocode
# specified in RFC7748: https://tools.ietf.org/html/rfc7748

P = 2 ** 448 - 2 ** 224 - 1
A24 = 39081


def cswap(swap, x_2, x_3):
    dummy = swap * ((x_2 - x_3) % P)
    x_2 = x_2 - dummy
    x_2 %= P
    x_3 = x_3 + dummy
    x_3 %= P
    return (x_2, x_3)


def X448(k, u):
    x_1 = u
    x_2 = 1
    z_2 = 0
    x_3 = u
    z_3 = 1
    swap = 0

    for t in reversed(xrange(448)):
        k_t = (k >> t) & 1
        swap ^= k_t
        x_2, x_3 = cswap(swap, x_2, x_3)
        z_2, z_3 = cswap(swap, z_2, z_3)
        swap = k_t

        A = x_2 + z_2
        A %= P

        AA = A * A
        AA %= P

        B = x_2 - z_2
        B %= P

        BB = B * B
        BB %= P

        E = AA - BB
        E %= P

        C = x_3 + z_3
        C %= P

        D = x_3 - z_3
        D %= P

        DA = D * A
        DA %= P

        CB = C * B
        CB %= P

        x_3 = ((DA + CB) % P)**2
        x_3 %= P

        z_3 = x_1 * (((DA - CB) % P)**2) % P
        z_3 %= P

        x_2 = AA * BB
        x_2 %= P

        z_2 = E * ((AA + (A24 * E) % P) % P)
        z_2 %= P

    x_2, x_3 = cswap(swap, x_2, x_3)
    z_2, z_3 = cswap(swap, z_2, z_3)

    return (x_2 * pow(z_2, P - 2, P)) % P


# Equivalent to RFC7748 decodeUCoordinate followed by decodeLittleEndian
def unpack(s):
    if len(s) != 56:
        raise ValueError('Invalid Curve448 scalar (len=%d)' % len(s))
    return sum(ord(s[i]) << (8 * i) for i in range(56))


def pack(n):
    return ''.join([chr((n >> (8 * i)) & 255) for i in range(56)])


def clamp(n):
    n &= ~3
    n |= 128 << 8 * 55
    return n


def scalarmult(n, p):
    '''
       Expects n and p in the form as 56-byte strings.

       Multiplies group element p by integer n. Returns the resulting group
       element as 56-byte string.
    '''
    n = clamp(unpack(n))
    p = unpack(p)
    return pack(X448(n, p))


def scalarmult_base(n):
    '''
       Expects n in the form as 56-byte string.

       Computes scalar product of standard group element (5) and n.
       Returns the resulting group element as 56-byte string.
    '''
    n = clamp(unpack(n))
    return pack(X448(n, 5))
