# Copyright 2020 Sebastian Ramacher <sebastian.ramacher@ait.ac.at>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from . cimport cpicnic
from libc.stdint cimport uint8_t


cdef class PrivateKey:
    """ Picnic private key

    This class represents a private key as returned by the key generation algorithm. It supports
    serialization to and from bytes.

    >>> sk, pk = keygen(param)
    >>> sk.param == param
    True
    >>> sk.pk == pk
    True
    >>> sk2 = PrivatKey(bytes(sk))
    >>> sk == sk2
    True
    """

    cdef cpicnic.picnic_privatekey_t key

    def __init__(self, bytes buf=None):
        if buf is not None:
            if cpicnic.picnic_read_private_key(&self.key, buf, len(buf)):
                raise ValueError("Unable to read private key")

    def __dealloc__(self):
        cpicnic.picnic_clear_private_key(&self.key)

    @property
    def param(self):
        """ The corresponding parameter set """
        return <cpicnic.picnic_params_t> self.key.data[0]

    @property
    def pk(self):
        """ The corresponding public key """
        pk = PublicKey()
        if cpicnic.picnic_sk_to_pk(&self.key, &pk.key):
            raise ValueError("Unable to construct public key")
        return pk

    def __bytes__(self):
        buf = bytearray(cpicnic.PICNIC_MAX_PRIVATEKEY_SIZE)
        written = cpicnic.picnic_write_private_key(&self.key, buf, cpicnic.PICNIC_MAX_PRIVATEKEY_SIZE)
        return bytes(buf[:written])

    def __str__(self):
        return "PrivateKey for {}".format(get_parameter_name(self.param))

    def __repr__(self):
        return "PrivateKey({})".format(bytes(self))

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    def __neq__(self, other):
        return bytes(self) != bytes(other)


cdef class PublicKey:
    """ Picnic public key

    This class represents a public key as returned by the key generation algorithm. It supports
    serialization to and from bytes.

    >>> sk, pk = keygen(param)
    >>> pk.param == param
    True
    >>> pk2 = PublicKey(bytes(pk))
    >>> pk == pk2
    True
    """

    cdef cpicnic.picnic_publickey_t key

    def __init__(self, bytes buf=None):
        if buf is not None:
            if cpicnic.picnic_read_public_key(&self.key, buf, len(buf)):
                raise ValueError("Unable to read public key")

    @property
    def param(self):
        """ The corresponding parameter set """
        return <cpicnic.picnic_params_t> self.key.data[0]

    def __bytes__(self):
        buf = bytearray(cpicnic.PICNIC_MAX_PUBLICKEY_SIZE)
        written = cpicnic.picnic_write_public_key(&self.key, buf, cpicnic.PICNIC_MAX_PUBLICKEY_SIZE)
        return bytes(buf[:written])

    def __str__(self):
        return "PublicKey for {}".format(get_parameter_name(self.param))

    def __repr__(self):
        return "PublicKey({})".format(bytes(self))

    def __eq__(self, other):
        return bytes(self) == bytes(other)

    def __neq__(self, other):
        return bytes(self) != bytes(other)


Picnic_L1_FS = cpicnic.Picnic_L1_FS
Picnic_L1_UR = cpicnic.Picnic_L1_UR
Picnic_L3_FS = cpicnic.Picnic_L3_FS
Picnic_L3_UR = cpicnic.Picnic_L3_UR
Picnic_L5_FS = cpicnic.Picnic_L5_FS
Picnic_L5_UR = cpicnic.Picnic_L5_UR
Picnic3_L1 = cpicnic.Picnic3_L1
Picnic3_L3 = cpicnic.Picnic3_L3
Picnic3_L5 = cpicnic.Picnic3_L5
Picnic_L1_full = cpicnic.Picnic_L1_full
Picnic_L3_full = cpicnic.Picnic_L3_full
Picnic_L5_full = cpicnic.Picnic_L5_full


ALL_PARAMETERS = (
        Picnic_L1_FS,
        Picnic_L1_UR,
        Picnic_L3_FS,
        Picnic_L3_UR,
        Picnic_L5_FS,
        Picnic_L5_UR,
        Picnic3_L1,
        Picnic3_L3,
        Picnic3_L5,
        Picnic_L1_full,
        Picnic_L3_full,
        Picnic_L5_full
)
SUPPORTED_PARAMETERS = tuple(param for param in ALL_PARAMETERS
                             if cpicnic.picnic_signature_size(param))
PARAMETER_NAMES = {param: get_parameter_name(param) for param in ALL_PARAMETERS}


cdef inline get_parameter_name(cpicnic.picnic_params_t param):
    name = cpicnic.picnic_get_param_name(param)
    assert name is not NULL
    return name.decode('UTF-8')


def keygen(cpicnic.picnic_params_t param):
    """ Generate a new key pair

    All parameters from SUPPORTED_PARAMETERS are supported.

    >>> sk, pk = keygen(param)
    """

    sk = PrivateKey()
    pk = PublicKey()
    if cpicnic.picnic_keygen(param, &pk.key, &sk.key):
        raise ValueError("Key generation failed")
    return sk, pk


def validate_keypair(PrivateKey sk not None, PublicKey pk not None):
    """ Validate a key pair

    >>> sk, pk = keygen(param)
    >>> validate_keypair(sk, pk)
    True
    """

    return not cpicnic.picnic_validate_keypair(&sk.key, &pk.key)


def sign(PrivateKey sk not None, message):
    """ Sign a message

    Create a signature for the given message. The message is expected to have a bytes-like
    interface.

    >>> sk, pk = keygen(param)
    >>> sig = sign(sk, b"a message")
    >>> sig is not None
    True
    """

    cdef size_t size = cpicnic.picnic_signature_size(sk.param)
    if not size:
        raise ValueError("Parameter set not supported.")

    cdef const uint8_t[::1] msgview = message

    # signature buffer
    sig = bytearray(size)
    if cpicnic.picnic_sign(&sk.key, &msgview[0], msgview.size, sig, &size):
        raise ValueError("Signing failed")

    # shrink signature buffer
    del sig[size:]
    return sig


def verify(PublicKey pk not None, message, signature):
    """ Verify signature of a message

    Verifies a signature. The message is expected to have a bytes-like interface.

    >>> sk, pk = keygen(param)
    >>> sig = sign(sk, b"a message")
    >>> verify(pk, b"a message", sig)
    True
    """

    cdef const uint8_t[::1] msgview = message
    cdef const uint8_t[::1] sigview = signature

    return not cpicnic.picnic_verify(&pk.key, &msgview[0], msgview.size, &sigview[0], sigview.size)

