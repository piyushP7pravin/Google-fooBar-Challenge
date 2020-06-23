'''Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel. 

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly. 

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as :
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Java cases --
Input:
Solution.solution({{0, 2, 1, 0, 0}, {0, 0, 0, 3, 4}, {0, 0, 0, 0, 0}, {0, 0, 0, 0,0}, {0, 0, 0, 0, 0}})
Output:
    [7, 6, 8, 21]

Input:
Solution.solution({{0, 1, 0, 0, 0, 1}, {4, 0, 0, 3, 2, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}})
Output:
    [0, 3, 2, 9, 14]

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
'''
from fractions import Fraction

def gcd(x, y):
    def gcd_(x, y):
        if y == 0:
            return x
        return gcd_(y, x%y)
    return gcd_(abs(x), abs(y))

def simplify(x, y):
    g = gcd(x, y)
    return Fraction(int(x/g), int(y/g))

def lcm(x, y):
    return int(x*y/gcd(x,y))

def trans(m):
    sum_list = list(map(sum, m))
    bool_indices = list(map(lambda x: x == 0, sum_list))
    indices = set([i for i, x in enumerate(bool_indices) if x])
    new_mat = []
    for i in range(len(m)):
        new_mat.append(list(map(lambda x: Fraction(0, 1) if(sum_list[i] == 0) else simplify(x, sum_list[i]), m[i])))
    transform_mat = []
    zeros_mat = []
    for i in range(len(new_mat)):
        if i not in indices:
            transform_mat.append(new_mat[i])
        else:
            zeros_mat.append(new_mat[i])
    transform_mat.extend(zeros_mat)
    tmat = []
    for i in range(len(transform_mat)):
        tmat.append([])
        extend_mat = []
        for j in range(len(transform_mat)):
            if j not in indices:
                tmat[i].append(transform_mat[i][j])
            else:
                extend_mat.append(transform_mat[i][j])
        tmat[i].extend(extend_mat)
    return [tmat, len(zeros_mat)]

def copy_m(m):
    cmat = []
    for i in range(len(m)):
        cmat.append([])
        for j in range(len(m[i])):
            cmat[i].append(Fraction(m[i][j].numerator, m[i][j].denominator))
    return cmat

def gauss_elmination(mat, values):
    m = copy_m(mat)
    for i in range(len(m)):
        index = -1
        for j in range(i, len(m)):
            if m[j][i].numerator != 0:
                index = j
                break
        m[i], m[index] = m[index], m[j]
        values[i], values[index] = values[index], values[i]
        for j in range(i+1, len(m)):
            if m[j][i].numerator == 0:
                continue
            ratio = -m[j][i]/m[i][i]
            for k in range(i, len(m)):
                m[j][k] += ratio * m[i][k]
            values[j] += ratio * values[i]
    res = [0 for i in range(len(m))]
    for i in range(len(m)):
        index = len(m) -1 -i
        end = len(m) - 1
        while end > index:
            values[index] -= m[index][end] * res[end]
            end -= 1
        res[index] = values[index]/m[index][index]
    return res

def transpose(m):
    tmat = []
    for i in range(len(m)):
        for j in range(len(m)):
            if i == 0:
                tmat.append([])
            tmat[j].append(m[i][j])
    return tmat

def inverse(m):
    tmat = transpose(m)
    mat_inv = []
    for i in range(len(tmat)):
        values = [Fraction(int(i==j), 1) for j in range(len(m))]
        mat_inv.append(gauss_elmination(tmat, values))
    return mat_inv

def mult(m1, m2):
    result = []
    for i in range(len(m1)):
        result.append([])
        for j in range(len(m2[0])):
            result[i].append(Fraction(0, 1))
            for k in range(len(m1[0])):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def get_QR(m, len_R):
    len_Q = len(m) - len_R
    Q = []
    R = []
    for i in range(len_Q):
        Q.append([int(i==j)-m[i][j] for j in range(len_Q)])
        R.append(m[i][len_Q:])
    return [Q, R]

def solution(m):
    # your code here
    sol = trans(m)
    if sol[1] == len(m):
        return [1, 1]
    Q, R = get_QR(*sol)
    inv = inverse(Q)
    sol = mult(inv, R)
    row = sol[0]
    l = 1
    for item in row:
        l = lcm(l, item.denominator)
    sol = list(map(lambda x: int(x.numerator*l/x.denominator), row))
    sol.append(l)
    return sol
