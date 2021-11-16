from NextPrime import is_prime
import random
from GS_timing import millis


class Elgamal:
    """    
    Steps:
    1.  Find large prime p.
    2.  Find α such that α ∈ Z^*_p
    3.  Find d such that d ∈ {2,...,p-2}
    4.  Find β such that β = α^d % p
    5.  Find i such that i ∈ {2,...,p-2}
    6.  Find k_E such that k_E = α^i % p
    7.  Find k_M such that k_M =  β^i % p
    8.  Find ciphertext such that y = x*k_M % p
    9.  Find k_M such that k_M =  k_E^d % p
    10. Find plaintext such that x = y*k^(-1)_M % p

    plaintext = x
    ciphertext = y
    initiator sends:  (p, α, β)
    receiver sends: (k_E, y)
    """

    def __init__(self, pa=None):
        if not pa:
            self.p = int(input("p: "))                # large prime
            assert is_prime(self.p), "p value is not a prime"
            self.a = int(input("a: "))                # α ∈ Z^*_p
            assert self.a >= 1 and self.a <= self.p-1, "a value is not subset of Z^*_p"
        else:
            self.p, self.a = pa
        self.x = -1                                   # plaintext in bits
        self.d = self.find_d(self.p)                  # private key
        self.b = self.find_b(self.a, self.d, self.p)  # public key (β)
        self.i = -1                                   # choose new i on each run
        self.k_E = -1                                 # ephemeral key
        self.k_M = -1                                 # masking key (sender)
        self.y = -1                                   # ciphertext
        # masking key (receiver)
        self.inv_d_k_M = -1
        self.d_x = -1                                 # deciphered text

    @staticmethod
    def encode_x(x):
        """
        @param string x: literal string
        return binary of string ascii
        """
        # if input is binary
        if x[0:2] == '0b':
            return int(x[2:], 2)
        # if input is integer
        elif x[0:3] == 'int':
            return int(x[3:])
        # if input is string
        else:
            return int(''.join(format(ord(i), 'b') for i in x), 2)

    @staticmethod
    def find_d(p):
        """
        Find d such that d ∈ {2,...,p-2}
        """
        return random.randint(2, p-2)

    @staticmethod
    def find_b(a, d, p):
        """
        Find β such that β = α^d % p
        """
        return (a**d) % p

    @staticmethod
    def find_i(p):
        """
        Find i such that i ∈ {2,...,p-2}
        """
        return random.randint(2, p-2)

    @staticmethod
    def find_k_E(a, i, p):
        """
        Find k_E such that k_E = α^i % p
        """
        return (a**i) % p

    @staticmethod
    def find_k_M(b, i, p):
        """
        Find k_M such that k_M =  β^i % p
        """
        return (b**i) % p

    @staticmethod
    def find_y(x, k_M, p):
        """
        Find ciphertext such that y = x*k_M % p
        """
        return (x*k_M) % p

    @staticmethod
    def find_inv_d_k_M(k_E, d, p):
        """
        Find d_k_M^-1 

        Fermat little theorem: 
            k_E^(p-1) % p = 1
        Then d_k_M^-1 
            = (k_E^d)^-1 ∙ 1 mod p
            = (k_E^d)^-1 ∙ k_E^(p-1) mod p
            = k_E^(p-d-1) mod p
        """
        return (k_E**(p-d-1)) % p

    @staticmethod
    def find_d_x(y, inv_d_k_M, p):
        """     
        Find plaintext such that x = y*(k_M^-1) % p
        """
        return (y*inv_d_k_M) % p

    def run(self, auto=False):
        """
        This function run the elgamal
        @param bool auto: prompt input
        return (ciphertext, plaintext)
        """
        if not auto:
            print(
                "Begin with '0b' for binary or 'int' for integer or '' for literal string")
            self.x = self.encode_x(input("x: "))
            print("-------------------")
        self.i = self.find_i(self.p)
        self.k_E = self.find_k_E(self.a, self.i, self.p)
        self.k_M = self.find_k_M(self.b, self.i, self.p)
        self.y = self.find_y(self.x, self.k_M, self.p)
        self.inv_d_k_M = self.find_inv_d_k_M(self.k_E, self.d, self.p)
        self.d_x = self.find_d_x(self.y, self.inv_d_k_M, self.p)
        return self.y, self.x

    def run_n(self, x):
        """
        This function run elgamal for all x, each time using a new i
        @param list x: list of plaintext
        return: time consumed in milliseconds
        """
        t = 0.
        for i in range(len(x)):
            self.x = self.encode_x(x[i])
            # minimize the effect of unrelated operation for time measurement
            t1 = millis()
            self.run(auto=True)
            t2 = millis()
            t += t2 - t1
        return t

    def __str__(self) -> str:
        s = "*** Results: ***\n"
        s += "p\t: " + str(self.p) + "\n"
        s += "a\t:" + str(self.a) + "\n"
        s += "x\t: " + str(self.x) + "\n"
        s += "d\t: " + str(self.d) + "\n"
        s += "b\t: " + str(self.b) + "\n"
        s += "i\t: " + str(self.i) + "\n"
        s += "k_M\t: " + str(self.k_M) + "\n"
        s += "k_E\t: " + str(self.k_E) + "\n"
        s += "y\t: " + str(self.y) + "\n"
        s += "k_M^-1\t: " + str(self.inv_d_k_M) + "\n"
        s += "d_x\t: " + str(self.d_x)
        return s


if __name__ == "__main__":
    print('*** USING ELGAMAL ENCRYPTION PROTOCOL ***')
    elgamal = Elgamal()
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
        t = elgamal.run_n(x)
        print('Time consumed for ', n, ' runs with ', l, 'string length\t:', t)
    elif opt == 'n':
        ciphertext, deciphertext = elgamal.run()
        print(elgamal)
