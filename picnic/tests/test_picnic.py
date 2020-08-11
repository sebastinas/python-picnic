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

import os.path
import unittest
import picnic


msg = b"a message to sign"
msg2 = b"a message to verify"


class PicnicBase:
    def test_keygen(self):
        sk, pk = picnic.keygen(self.param)
        self.assertIsNotNone(pk)
        self.assertIsNotNone(sk)
        self.assertEqual(pk.param, self.param)
        self.assertEqual(sk.param, self.param)
        self.assertTrue(picnic.validate_keypair(sk, pk))
        self.assertEqual(sk.pk, pk)

    def test_sign_and_verify(self):
        sk, pk = picnic.keygen(self.param)
        sig = picnic.sign(sk, msg)
        self.assertIsNotNone(sig)
        self.assertTrue(picnic.verify(pk, msg, sig))

    def test_verify_wrong_msg(self):
        sk, pk = picnic.keygen(self.param)
        sig = picnic.sign(sk, msg)
        self.assertIsNotNone(sig)
        self.assertFalse(picnic.verify(pk, msg2, sig))

    def test_key_serialization(self):
        sk, pk = picnic.keygen(self.param)
        pk2 = picnic.PublicKey(bytes(pk))
        sk2 = picnic.PrivateKey(bytes(sk))
        self.assertEqual(pk, pk2)
        self.assertEqual(sk, sk2)
        self.assertTrue(picnic.validate_keypair(sk, pk2))
        self.assertTrue(picnic.validate_keypair(sk2, pk))

        sig = picnic.sign(sk, msg)
        self.assertTrue(picnic.verify(pk2, msg, sig))
        sig = picnic.sign(sk2, msg)
        self.assertTrue(picnic.verify(pk, msg, sig))


@unittest.skipIf(
    picnic.Picnic_L1_FS not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL1FS(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L1_FS


@unittest.skipIf(
    picnic.Picnic_L1_UR not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL1UR(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L1_UR


@unittest.skipIf(
    picnic.Picnic_L1_full not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL1Full(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L1_full


@unittest.skipIf(
    picnic.Picnic_L3_FS not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL3FS(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L3_FS


@unittest.skipIf(
    picnic.Picnic_L3_UR not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL3UR(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L3_UR


@unittest.skipIf(
    picnic.Picnic_L3_full not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL3Full(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L3_full


@unittest.skipIf(
    picnic.Picnic_L5_FS not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL5FS(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L5_FS


@unittest.skipIf(
    picnic.Picnic_L5_UR not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL5UR(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L5_UR


@unittest.skipIf(
    picnic.Picnic_L5_full not in picnic.SUPPORTED_PARAMETERS, "not supported"
)
class TestPicnicL5Full(PicnicBase, unittest.TestCase):
    param = picnic.Picnic_L5_full


@unittest.skipIf(picnic.Picnic3_L1 not in picnic.SUPPORTED_PARAMETERS, "not supported")
class TestPicnic3L1(PicnicBase, unittest.TestCase):
    param = picnic.Picnic3_L1


@unittest.skipIf(picnic.Picnic3_L3 not in picnic.SUPPORTED_PARAMETERS, "not supported")
class TestPicnic3L3(PicnicBase, unittest.TestCase):
    param = picnic.Picnic3_L3


@unittest.skipIf(picnic.Picnic3_L5 not in picnic.SUPPORTED_PARAMETERS, "not supported")
class TestPicnic3L5(PicnicBase, unittest.TestCase):
    param = picnic.Picnic3_L5


class TestVectorData:
    pass


class VectorMeta(type):
    """
    Test functions are generated in metaclass due to the way some
    test loaders work.
    """

    def __init__(self, name, bases, attrs):
        super().__init__(name, bases, attrs)

    def __new__(cls, name, bases, attrs):
        tests = (
            (picnic.Picnic_L1_FS, "kat_l1_fs.txt"),
            (picnic.Picnic_L1_UR, "kat_l1_ur.txt"),
            (picnic.Picnic_L1_full, "kat_l1_full.txt"),
            (picnic.Picnic_L3_FS, "kat_l3_fs.txt"),
            (picnic.Picnic_L3_UR, "kat_l3_ur.txt"),
            (picnic.Picnic_L3_full, "kat_l3_full.txt"),
            (picnic.Picnic_L5_FS, "kat_l5_fs.txt"),
            (picnic.Picnic_L5_UR, "kat_l5_ur.txt"),
            (picnic.Picnic_L5_full, "kat_l5_full.txt"),
            (picnic.Picnic3_L1, "kat_picnic3_l1.txt"),
            (picnic.Picnic3_L3, "kat_picnic3_l3.txt"),
            (picnic.Picnic3_L5, "kat_picnic3_l5.txt"),
        )

        for param, filename in tests:
            for tv in cls.read_test_vector(filename):

                def func(self):
                    return self.run_tv(tv)

                func.__name__ = "test_{}_{}".format(
                    picnic.PARAMETER_NAMES[param], tv.count
                )
                attrs[func.__name__] = func

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def read_test_vector(cls, filename):
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            for line in f:
                if " = " not in line:
                    continue

                name, value = line.rstrip().split(" = ")
                if name == "count":
                    # start new test vector
                    data = TestVectorData()
                    data.count = int(value)
                elif "len" in name:
                    setattr(data, name, int(value))
                else:
                    setattr(data, name, bytes.fromhex(value))
                if name == "sm":
                    # finish current test vector
                    yield data


class TestVector(unittest.TestCase, metaclass=VectorMeta):
    def run_tv(self, tv):
        sk = picnic.PrivateKey(tv.sk)
        pk = picnic.PublicKey(tv.pk)
        sig = picnic.sign(sk, tv.msg)

        msg2, sig2 = picnic.unpack_nist_signature(tv.sm)
        self.assertEqual(sig, sig2)
        self.assertTrue(picnic.verify(pk, tv.msg, sig2))

        sig2 = picnic.pack_nist_signature(tv.msg, sig)
        self.assertEqual(sig2, tv.sm)


if __name__ == "__main__":
    unittest.main()
