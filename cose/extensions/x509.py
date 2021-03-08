from typing import List, Union

from cryptography.hazmat.backends import openssl

from cose.algorithms import CoseAlg, CoseAlgorithm
from cose.headers import CoseAttr


class X5Bag:
    def __init__(self, certificates: Union[List[bytes], bytes]):
        if isinstance(certificates, list) and len(certificates) == 1:
            self.certificates = certificates[0]
        else:
            self.certificates = certificates

    def encode(self) -> Union[bytes, List[bytes]]:
        return self.certificates


class X5T:
    @classmethod
    def from_certificate(cls, alg: CoseAlg, certificate: bytes):
        ''' Extract thumbprint from an encoded certificate.
        '''
        return cls(
            alg=alg,
            thumbprint=alg.compute_hash(certificate)
        )

    @classmethod
    def decode(cls, item):
        ''' Decode from a CBOR item.
        '''
        return cls(
            alg=CoseAlgorithm.from_id(item[0]),
            thumbprint=item[1]
        )

    def __init__(self, alg: CoseAlg, thumbprint: bytes):
        self.alg = alg
        self.thumbprint = thumbprint

    def __eq__(self, other: 'X5T'):
        return (
            self.alg == other.alg
            and self.thumbprint == other.thumbprint
        )

    def encode(self):
        ''' Encode to a CBOR item.
        '''
        return [self.alg, self.thumbprint]

    def matches(self, certificate: bytes) -> bool:
        ''' Determine if this thumbprint is for a given certificate.
        '''
        if not self.thumbprint:
            return False
        return self.thumbprint == self.alg.compute_hash(certificate)

class X5U:
    def __init__(self, uri: str):
        self.uri = uri

    def encode(self):
        return self.uri


class X5Chain:
    def __init__(self, cert_chain: Union[List[bytes], bytes], verify: bool = False):
        if isinstance(cert_chain, list) and len(cert_chain) == 1:
            self.cert_chain = cert_chain[0]
        else:
            self.cert_chain = cert_chain

        if verify:
            self.verify_chain()

    def verify_chain(self):
        # TODO: verify certificate chain
        pass

    def encode(self) -> Union[bytes, List[bytes]]:
        return self.cert_chain
