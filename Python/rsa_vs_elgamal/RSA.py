from NextPrime import is_prime
from math import gcd
#from modular_inverse import modinv
import random
from GS_timing import millis


class RSA:
    """
    Calculate the public key and private key given 2 prime number and a message in binary

    Steps:
    1. Find two large primes p and q.
    2. Find n such that n = p(q).
    3. Find z such that z = (p-1)(q-1).
    4. Find e such that e ∈ {1,2,...,z-1} subject to gcd(e,z) = 1
    5. Find d such that d = e^-1 % z, and e != d.
    6. Find ciphertext K+(m) = m^e % n = c , and plaintext K-(c) = c^d % n = m

    Public key = (n, e)
    Private key = (d)
    """

    def __init__(self, pq=None):
        if not pq:
            self.p = int(input("p: "))          # large prime
            assert is_prime(self.p), "p value is not a prime"
            self.q = int(input("q: "))          # large prime
            assert is_prime(self.q), "q value is not a prime"
        else:
            self.p, self.q = pq
        self.m = -1                             # plaintext in bits
        self.n = self.find_n(self.p, self.q)    # public key
        self.z = self.find_z(self.p, self.q)
        self.e = self.find_e(self.z)            # public key
        self.d = self.find_d(self.e, self.z)    # private key
        self.c = -1                             # ciphertext
        self.d_m = -1                           # deciphered text

    @staticmethod
    def encode_m(m):
        """
        @param string m: message
        """
        # if input is binary
        if m[0:2] == '0b':
            return int(m[2:], 2)
        # if input is integer
        elif m[0:3] == 'int':
            return int(m[3:])
        # if input is string
        else:
            return int(''.join(format(ord(i), 'b') for i in m), 2)

    @staticmethod
    def find_n(p, q):
        """
        Find n such that n = p(q) 
        """
        return p * q

    @staticmethod
    def find_z(p, q):
        """
        Find z such that z = (p-1)(q-1)
        """
        return (p - 1) * (q - 1)

    @staticmethod
    def find_e(z):
        """
        This mode used the explanation given from CSC652
        Find e such that e ∈ {1,2,...,z-1} subject to gcd(e,z) = 1        
        """
        for _ in range(1, z):
            e = int(random.uniform(1., z))
            if gcd(e, z) == 1:
                return e
        raise Exception('Unable to find e')

    @staticmethod
    def find_d(e, z):
        """
        Find d such that d = e^-1 % z, and e != d
        * Optimize later for debugging purpose
        """
        # Fermat Little Theorem
        if is_prime(z):
            d = (e**(z-2)) % z
            if d != e:
                return d

        d = 2
        while ((d*e) % z) != 1 or d == e:
            d += 1
        return d
        """
        while True:
            d = modinv(e, z)
            if d != e:
                return e
        """

    @staticmethod
    def find_c(m, e, n):
        """
        Find public key K+(m) = m^e % n = c
        return cyphertext
        """
        return (m ** e) % n

    @staticmethod
    def find_d_m(c, d, n):
        """
        Find decyphertext K-(c) = c^d % n = m
        """
        return (c**d) % n

    def run(self, auto=False):
        """ 
        This function run all the process 
        return (ciphertext, deciphered text)
        """
        if not auto:
            print(
                "Begin with '0b' for binary or 'int' for integer or '' for literal string")
            self.m = self.encode_m(input("m: "))
            print("-------------------")
        self.c = self.find_c(self.m, self.e, self.n)
        self.d_m = self.find_d_m(self.c, self.d, self.n)
        return self.c, self.d_m

    def run_n(self, m):
        """
        This function run the rsa for all m               
        @param list m: list of plaintext
        return float: time consumed in milliseconds
        """
        t = 0.
        for i in range(len(m)):
            self.m = self.encode_m(m[i])
            # minimize the effect of unrelated operation for time measurement
            t1 = millis()
            self.run(auto=True)
            t2 = millis()
            t += t2 - t1
        return t

    def run_1(self, m):
        """
        This function run the rsa for m
        @param string m: plaintext
        return float: time consumed in milliseconds
        """
        t = 0.
        self.m = self.encode_m(m)
        t1 = millis()
        self.run(auto=True)
        t2 = millis()
        return t2 - t1

    def __str__(self):
        s = "*** Results: ***\n"
        s += "p: " + str(self.p) + "\n"
        s += "q: " + str(self.q) + "\n"
        s += "m: " + str(self.m) + "\n"
        s += "n: " + str(self.n) + "\n"
        s += "z: " + str(self.z) + "\n"
        s += "e: " + str(self.e) + "\n"
        s += "d: " + str(self.d) + "\n"
        s += "K+(" + str(self.m) + ") = " + str(self.c) + "\n"
        s += "K-(" + str(self.c) + ") = " + str(self.d_m)
        return s

    def bin_to_str(b):
        """
        * In Progress
        Decode ascii to string
        @param string b: a collection of ascii (ex: '0b1011010010001010)
        return string
        """
        if b[:2] == '0b':
            b = b[2:]
        out = ''
        while len(b) > 0:
            out += chr(int(b[:8], 2))
            b = b[8:]
        print(out)


def main():
    print('*** USING RSA ***')
    rsa = RSA()
    opt = input('Multiple runs? (y/n)\t: ')
    if opt == 'y':
        opt = input('Auto generate strings? (y/n)\t:')
        if opt == 'y':
            l = int(input('Length of input string\t: '))
            n = int(input('Number of runs\t: '))
            import string
            x = [''.join(random.choice(string.ascii_letters)
                         for _ in range(l)) for _ in range(n)]
        elif opt == 'n':
            x = input('Please enter list of strings as shown : [I,am,legend]\n').strip(
                '[]').split(',')
        t = rsa.run_n(x)
        print('Time consumed for ', n, ' runs with ', l, 'string length\t:', t)
    elif opt == 'n':
        ciphertext, deciphertext = rsa.run()
        print(rsa)


if __name__ == "__main__":
    main()
