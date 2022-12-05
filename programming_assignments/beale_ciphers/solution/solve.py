import time
import random


def freivald(X, Y, Q, x, y, n, m, k, v, t, q):
    count = 0
    while True:
        v = [random.randint(0, 1) for i in range(k)]
        for i in range(k):
            t[i] = 0
            q[i] = 0
            for j in range(k):
                t[i] = t[i] + Q[x + i][y + j] * v[j]
                q[i] = q[i] + Y[i][j] * v[j]
        for i in range(k):
            v[i] = 0
            for j in range(k):
                v[i] = v[i] + X[i][j] * t[j]

        for i in range(k):
            if v[i] != q[i]:
                return False
        if count > 10:
            break
        count = count + 1
    return True


def solve():
    n, m, k = map(int, input().split())
    X = []
    Y = []
    Q = []
    v = [0 for i in range(k)]
    t = [0 for i in range(k)]
    q = [0 for i in range(k)]

    for i in range(k):
        X.append(map(int, input().split()))
    for i in range(k):
        Y.append(map(int, input().split()))
    for i in range(n):
        Q.append(map(int, input().split()))

    ans = 0
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            if freivald(X, Y, Q, i, j, n, m, k, v, t, q):
                ans = ans + 1
    print(ans)


def test():
    T = map(int, input().split())[0]
    for i in range(T):
        solve()


if __name__ == '__main__':
    test()
