

def gaussian_algorithm(a, b):  # solve any system with n equations for n variables
    s = a
    for i in range(len(s)):
        s[i].append(b[i])
    to_triangular(s)
    solve(s)
    return [s[i][-1] for i in range(len(s))]  # solutions are on the right column


def to_triangular(s):  # make a a triangular matrix, changing b accordingly
    for n in range(len(s)):
        for i in range(n, len(s)):  # look for a pivot
            if s[i][n] != 0:
                swap(s, i, n)
                break
        else:  # if there is no pivot
            continue
        for i in range(n+1, len(s)):  # cancel the next lines
            sub(s, i, n, s[i][n]/s[n][n])
            s[i][n] = 0  # an exact zero


def solve(s):  # s is supposed to be triangular
    for n in range(len(s)-1, -1, -1):
        normalize(s, n)  # set the pivot to 1
        for i in range(0, n):  # cancel the above column
            sub(s, i, n, s[i][n])


def normalize(s, i):  # change the pivot value to 1
    for j in range(len(s[i])):
        if s[i][j] != 0:
            c = s[i][j]
            for k in range(j, len(s[i])):
                s[i][k] /= c
            break


def swap(s, i1, i2):  # swap two lines
    s[i1], s[i2] = s[i2], s[i1]


def sub(s, i1, i2, c=1):
    for j in range(len(s[i1])):
        s[i1][j] -= s[i2][j] * c


def print_matrix(m):
    for i in range(len(m)):
        print([m[i][j] for j in range(len(m[i]))])
    print()

