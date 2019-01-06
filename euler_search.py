"""nvestigate Euler's (Disproven) Conjecture
that at least k terms of k-th powers are reequired
to sum to a k-th power.

A counterexampele discovered on the CDC 6600 for
k = 5 is
    27**5 + 84**5 + 110**5 + 133**5 = 144**5

Here is the result for sums up to 499**5:
0) [72, 67, 47, 46, 43, 19]
1) [94, 84, 79, 37, 23, 21]
2) [107, 100, 80, 57, 43, 7]
3) [144, 133, 110, 84, 27, 0]
4) [144, 134, 94, 92, 86, 38]
5) [188, 168, 158, 74, 46, 42]
6) [214, 200, 160, 114, 86, 14]
7) [216, 201, 141, 138, 129, 57]
8) [282, 252, 237, 111, 69, 63]
9) [288, 266, 220, 168, 54, 0]
10) [288, 268, 188, 184, 172, 76]
11) [321, 300, 240, 171, 129, 21]
12) [360, 335, 235, 230, 215, 95]
13) [365, 347, 259, 191, 120, 78]
14) [376, 336, 316, 148, 92, 84]
15) [415, 395, 261, 258, 202, 79]
16) [427, 412, 296, 139, 26, 4]
17) [428, 400, 320, 228, 172, 28]
18) [432, 399, 330, 252, 81, 0]
19) [432, 402, 282, 276, 258, 114]
20) [435, 416, 314, 139, 105, 31]
21) [470, 420, 395, 185, 115, 105]
22) [480, 430, 404, 101, 91, 54]

USAGE:
    Set K to the desired order
    In the drive loop at the end, seed the list of ranges
    and the range size. The nested setup allows a bit of
    feedback while the code is running.

CAVEATS:
    I've tried K=6 with sums up to 250**6, but I have not
    yet tried to find the limit of the number system. IEEE
    double handles integers up to 2**53 ~ 9E15 but some
    Python support effectively unbounded integers.
"""

from collections import defaultdict
import math

verbose = False
K = 5
RIPK = 1 / K
TMAX = 400   # This table size must be tuned to the search
solutions = []

# The algorithm reduces to finding
#   u = v**K + w**K
# if such a pair (v, w) exists. Create a dictionary of
# candidates, noting there may be more than one.
pairs = defaultdict(list)
for i in range(TMAX):
    for j in range(i, TMAX):
        pairs[i**K + j**K].append([j, i])

def euler_step(s, n, p):
    """Attempt to compute s as the sum of n terms
    of K-th powers, with p giving the partial list
    of terms so far.
    Returns: none"""
    global solutions
    if n > 2:
        # Reduce by trying the possible largest
        # element in range (s/n)**(1/K) to s**(1/K)
        lower = math.ceil(math.pow(s / n, RIPK))
        upper = math.ceil(math.pow(s, RIPK))
        if verbose:
            print("n = {:.0f}) lower = {:.0f} upper = {:.0f} p = {:s}".format(
                n, lower, upper, str(p)))
        for j in range(lower, upper):
            next_s = s - j ** K
            euler_step(next_s, n-1, p + [j])
        return
    else:
        # Try to find s as the sum of two K-th powers.
        if s in pairs:
            if verbose:
                print("s = {:.0f} entry = {:s}".format(s, str(pairs[s])))
            for z in pairs[s]:
                new_sol = sorted(p + z, reverse=True)
                if not new_sol in solutions:
                    solutions.append(new_sol)
        return

for b in [0, 250]:
    print("Trying range {:d}".format(b))
    for i in range(b, b+250):
        euler_step(i ** K, K, [i])
for i, z in enumerate(solutions):
    print("{:d}) {:s}".format(i, str(z)))

# Code for checking the sums.
#for z in extras:
#    print("{:s} check {:.0f} vs {:.0f}".format(str(z),
#                                           z[0] ** K,
#                                           sum([x ** K for x in z[1:]])))
