# Python bindings for Picnic

python-picnic provides Python bindings based on [Cython](https://cython.org/) for the
[Picnic](https://microsoft.github.io/Picnic/) post-quantum signature scheme.

## Dependencies

* `Cython >= 0.28` (only for building)
* `pkgconfig` (only for building)
* [Picnic](https://github.com/IAIK/Picnic)

## Quick installation guilde

python-picnic can be installed via `pip`:
```sh
pip install python-picnic
```
or by running:
```sh
python3 setup.py install
```

Packages for Ubuntu are also available via the [picnic
PPA](https://launchpad.net/~s-ramacher/+archive/ubuntu/picnic):
```sh
sudo add-apt-repository ppa:s-ramacher/picnic
sudo apt update
sudo apt install python3-picnic
```

## Usage

```python3
import picnic

# create keypair
sk, pk = picnic.keygen(picinc.Picnic_L1_full)
# sign a message
sig = picnic.sign(sk, b"a message")
# verify a signature
picnic.verify(pk, b"a message", sig)
```

## License

The code is licensed under the MIT license.
