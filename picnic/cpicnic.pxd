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

from libc.stdint cimport uint8_t

cdef extern from "<picnic.h>" nogil:
  cdef enum:
    PICNIC_MAX_PUBLICKEY_SIZE
    PICNIC_MAX_PRIVATEKEY_SIZE

  ctypedef struct picnic_publickey_t:
    uint8_t[PICNIC_MAX_PUBLICKEY_SIZE] data

  ctypedef struct picnic_privatekey_t:
    uint8_t[PICNIC_MAX_PRIVATEKEY_SIZE] data

  ctypedef enum picnic_params_t:
    Picnic_L1_FS
    Picnic_L1_UR
    Picnic_L3_FS
    Picnic_L3_UR
    Picnic_L5_FS
    Picnic_L5_UR
    Picnic3_L1
    Picnic3_L3
    Picnic3_L5
    Picnic_L1_full
    Picnic_L3_full
    Picnic_L5_full

  const char* picnic_get_param_name(picnic_params_t parameters)
  size_t picnic_signature_size(picnic_params_t parameters)

  int picnic_keygen(picnic_params_t parameters, picnic_publickey_t* pk, picnic_privatekey_t* sk)
  int picnic_sign(const picnic_privatekey_t* sk, const uint8_t* message, size_t message_len, uint8_t* signature, size_t* signature_len)
  int picnic_verify(const picnic_publickey_t* pk, const uint8_t* message, size_t message_len, const uint8_t* signature, size_t signature_len)

  int picnic_write_public_key(const picnic_publickey_t* key, uint8_t* buf, size_t buflen)
  int picnic_read_public_key(picnic_publickey_t* key, const uint8_t* buf, size_t buflen)

  int picnic_write_private_key(const picnic_privatekey_t* key, uint8_t* buf, size_t buflen)
  int picnic_read_private_key(picnic_privatekey_t* key, const uint8_t* buf, size_t buflen)

  int picnic_validate_keypair(const picnic_privatekey_t* privatekey, const picnic_publickey_t* publickey)
  void picnic_clear_private_key(picnic_privatekey_t* key)
  int picnic_sk_to_pk(const picnic_privatekey_t* privatekey, picnic_publickey_t* publickey)
