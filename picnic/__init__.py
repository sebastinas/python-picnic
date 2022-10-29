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

""" Python bindings for Picnic

Picnic is a familiy of post-quantum secure digital signatures. This modules provides Python-bindings
for Picnic.

>>> sk, pk = picnic.keygen(picinc.Picnic_L1_full)
>>> sig = picnic.sign(sk, b"a message")
>>> picnic.verify(pk, b"a message", sig)
True
"""

import struct
from typing import Optional, Tuple

from ._picnic import (
    PrivateKey,
    PublicKey,
    keygen,
    sign,
    verify,
    validate_keypair,
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
    Picnic_L5_full,
    ALL_PARAMETERS,
    SUPPORTED_PARAMETERS,
    PARAMETER_NAMES,
)

__license__ = "MIT/Expat"
__version__ = "1.0.1"
__docformat__ = "reStructuredText"


def unpack_nist_signature(sig: bytes) -> Tuple[bytes, bytes]:
    """Unpack message and signature from a signature with the encoding of the NIST PQC competition"""

    (siglen,) = struct.unpack_from("<I", sig)
    msglen = len(sig) - siglen - 4
    return sig[4 : 4 + msglen], sig[4 + msglen :]


def pack_nist_signature(msg: bytes, sig: bytes) -> bytes:
    """Pack message and signature with the encoding of the NIST PQC competition"""

    return struct.pack("<I{}B{}B".format(len(msg), len(sig)), len(sig), *msg, *sig)


def sign_nist(sk: PrivateKey, msg: bytes) -> bytes:
    """Sign a message and encode signature for NIST PQC competition

    :param sk: the private key
    :param msg: the message to sign
    :type sk: PrivateKey
    :type msg: bytes-like
    :returns: a signature
    :rtype: bytes
    """

    sig = sign(sk, msg)
    return pack_nist_signature(msg, sig)


def verify_nist(pk: PublicKey, sig: bytes) -> Optional[bytes]:
    """Verify a signature encoded for the NIST PQC competition and return signed message

    :param pk: the public key
    :param sig: NIST PQC encoded signature to verify
    :type pk: PublicKey
    :type sig: bytes-like
    :returns: the signed message or None on failure
    :rtype: bytes
    """

    msg, sig = unpack_nist_signature(sig)
    return msg if verify(pk, msg, sig) else None
