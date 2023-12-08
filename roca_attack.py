from sage.all import *
import argparse
from roca_generator import generate_modulus

def solve(M, n, a, m):
    # I need to import it in the function otherwise multiprocessing doesn't find it in its context
    from sage_functions import coppersmith_howgrave_univariate

    base = int(65537)
    # the known part of p: 65537^a * M^-1 (mod N)
    known = int(pow(base, a, M) * inverse_mod(M, n))
    # Create the polynom f(x)
    F = PolynomialRing(Zmod(n), implementation='NTL', names=('x',))
    (x,) = F._first_ngens(1)
    pol = x + known
    beta = 0.1
    t = m+1
    # Upper bound for the small root x0
    XX = floor(2 * n**0.5 / M)
    # Find a small root (x0 = k) using Coppersmith's algorithm
    roots = coppersmith_howgrave_univariate(pol, n, beta, m, t, XX)
    # There will be no roots for an incorrect guess of a.
    for k in roots:
        # reconstruct p from the recovered k
        p = int(k*M + pow(base, a, M))
        if n%p == 0:
            return p, n//p

def roca(n):

    keySize = n.bit_length()

    if keySize <= 960:
        M_prime = 0x1b3e6c9433a7735fa5fc479ffe4027e13bea
        m = 5

    elif 992 <= keySize <= 1952:
        M_prime = 0x24683144f41188c2b1d6a217f81f12888e4e6513c43f3f60e72af8bd9728807483425d1e
        m = 4
        print("Have you several days/months to spend on this ?")

    elif 1984 <= keySize <= 3936:
        M_prime = 0x16928dc3e47b44daf289a60e80e1fc6bd7648d7ef60d1890f3e0a9455efe0abdb7a748131413cebd2e36a76a355c1b664be462e115ac330f9c13344f8f3d1034a02c23396e6
        m = 7
        print("You'll change computer before this scripts ends...")

    elif 3968 <= keySize <= 4096:
        print("Just no.")
        return None

    else:
        print("Invalid key size: {}".format(keySize))
        return None

    a3 = Zmod(M_prime)(n).log(65537)
    order = Zmod(M_prime)(65537).multiplicative_order()
    inf = a3 // 2
    sup = (a3 + order) // 2

    # Search 10 000 values at a time, using multiprocess
    # too big chunks is slower, too small chunks also
    chunk_size = 10000
    for inf_a in range(inf, sup, chunk_size):
        # create an array with the parameter for the solve function
        inputs = [((M_prime, n, a, m), {}) for a in range(inf_a, inf_a+chunk_size)]
        # the sage builtin multiprocessing stuff
        from sage.parallel.multiprocessing_sage import parallel_iter
        from multiprocessing import cpu_count

        for k, val in parallel_iter(cpu_count(), solve, inputs):
            if val:
                p = val[0]
                q = val[1]
                print("*** SUCCESS: Factorization found ***\np={}\nq={}".format(p, q))
                return val
def read_modulus(file):
    with open(file, 'r') as f:
        n = f.read()
    return n
if __name__ == "__main__":
    formats = ['decimal', 'hex', 'base64']

    parser = argparse.ArgumentParser(description='ROCA attack')
    parser.add_argument('-n', '--modulus', metavar='N', help='RSA modulus')
    parser.add_argument('-f', '--file', help='File containing the modulus in one line')
    parser.add_argument('--format', help='Format of the modulus (default: %(default)s)', default='decimal', choices=formats)
    parser.add_argument('-g', '--generate', metavar='NPRIMES', help='Generate a weak modulus with n primes', type=int)

    #argument to
    args = parser.parse_args()
    
    if args.generate:
        generate_modulus(args.generate)
        exit(0)

    if args.file:
        try:
            n = read_modulus(args.file)
        except Exception as e:
            print("Error while reading the modulus: {}".format(e))
            exit(1)    
    elif args.modulus:
        n = args.modulus
    else:
        parser.print_help()
        exit(1)
    
    if args.format == 'hex':
        n = int(n, 16)
    elif args.format == 'base64':
        n = int(n, 64)
    else:
        n = int(n)

    print("\n--- Starting ROCA attack ---\n")
    print("Modulus:\nN= {}\n".format(n))
    # For the test values chosen, a is quite close to the minimal value so the search is not too long
    roca(n)
