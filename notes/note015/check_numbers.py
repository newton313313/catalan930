"""
check_numbers.py —— notes/ran_note015_改寫.tex 寫到的每一個數字與主張的檢查

    python note015/check_numbers.py      （在 notes/ 裡執行）

原始筆記是 notes/ran_note015.txt（他人所寫）；改寫版的勘誤也在這裡用程式確認。
"""
import itertools
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "codes"))

import utils.counting as ct  # noqa: E402
from utils.raney import L_formula, is_word  # noqa: E402

random.seed(15)


def prefix(a):
    out, s = [], 0
    for x in a:
        s += x
        out.append(s)
    return out


def rot(a, j):
    return list(a[j:]) + list(a[:j])


def positives(a):
    return sum(p > 0 for p in prefix(a))


def random_seq(n, lo=-5, hi=5):
    a = [random.randint(lo, hi) for _ in range(n - 1)]
    return a + [1 - sum(a)]


def main():
    # 1. Raney 引理（t = 1）：任意整數、和為 1
    for n in range(1, 9):
        for _ in range(2000):
            a = random_seq(n)
            assert [positives(rot(a, j)) for j in range(n)].count(n) == 1
    # 1b. 筆記的構造：最後一個最小前綴和之後開始讀
    for n in range(1, 9):
        for _ in range(2000):
            a = random_seq(n)
            S = prefix(a)
            x = max(i for i in range(1, n + 1) if S[i - 1] == min(S))
            assert positives(rot(a, x % n)) == n
    # 1c. 原文第 19 行的式子：S_{n+i} = S_i + A_{i+1} + … + A_{i+n}（原文寫成 A_i…A_{n+i-1}）
    a = [2, -1, -3, 1, 2]
    ext = a * 3
    S = prefix(ext)
    for i in range(1, 6):
        assert S[i + 5 - 1] == S[i - 1] + sum(ext[i:i + 5]) == S[i - 1] + 1
    # 1d. 一般的 t 需要「每步最多上升 1」：(2, 0) 和為 2，卻只有 1 種好讀法
    assert [positives(rot([2, 0], j)) == 2 for j in range(2)] == [True, False]

    # 2. 加強版：每個 k = 1..n 恰有一個循環移位有 k 個正的前綴和；排序法給出是哪一個
    for n in range(1, 9):
        for _ in range(2000):
            a = random_seq(n)
            assert sorted(positives(rot(a, j)) for j in range(n)) == list(range(1, n + 1))
            S = prefix(a)
            order = sorted(range(1, n + 1), key=lambda i: (S[i - 1], -i))
            for r, i in enumerate(order, 1):
                assert positives(rot(a, i % n)) == n - r + 1
    a = [2, -1, -3, 1, 2]
    assert prefix(a) == [2, 1, -2, -1, 1]
    assert [positives(rot(a, j)) for j in range(5)] == [3, 1, 2, 5, 4]
    S = prefix(a)
    assert sorted(range(1, 6), key=lambda i: (S[i - 1], -i)) == [3, 4, 5, 2, 1]
    assert rot(a, 3) == [1, 2, 2, -1, -3] and prefix(rot(a, 3)) == [1, 3, 5, 4, 1]

    # 3. 例題一：出棧序列 = Dyck 路徑 = C_n；加一個 ↑ 後 = Chu 講義 A_1((n),(2))
    for n in range(0, 9):
        cat = math.comb(2 * n, n) // (n + 1)
        assert math.comb(2 * n + 1, n) // (2 * n + 1) == cat == ct.raney_A(1, (n,), (2,)) == len(ct.good_paths(1, (n,), (2,)))
        cnt = sum(all(p >= 0 for p in prefix([-1 if i in pos else 1 for i in range(2 * n)]))
                  for pos in itertools.combinations(range(2 * n), n))
        assert cnt == cat
    assert [math.comb(2 * n, n) // (n + 1) for n in range(1, 6)] == [1, 2, 5, 14, 42]
    assert math.comb(7, 3) == 35 and 35 // 7 == 5

    # 4. 例題二：暴力（牌有標號） = m!/(m-n+1) = Raney 定理 2.2 的算法
    def deck_count(w, m):
        cards = list(w) + [0] * (m - len(w))
        good = 0
        for perm in itertools.permutations(range(m)):
            draws, ok = 1, True
            for c in perm:
                draws += cards[c] - 1
                if draws < 1:
                    ok = False
                    break
            good += ok
        return good

    def deck_count_words(w, m):
        """同一件事用 Raney 的字：牌序＋底牌 0 是字，而且最後一個符號是底牌。"""
        cards = list(w) + [0] * (m - len(w))
        return sum(is_word(tuple(cards[c] for c in perm) + (0,)) for perm in itertools.permutations(range(m)))

    table = []
    for w, m in [((3,), 3), ((1, 2), 3), ((2, 2), 4), ((1, 3), 4), ((1, 1, 2), 4), ((2, 3), 5), ((1, 1, 3), 5), ((5,), 5)]:
        n = len(w)
        got = deck_count(w, m)
        assert got == deck_count_words(w, m) == math.factorial(m) // (m - n + 1)
        a = [0] * max(w)
        for x in w:
            a[x - 1] += 1
        assert got == L_formula(1, tuple(a)) * math.prod(math.factorial(x) for x in a) * math.factorial(m - n)
        table.append((w, m, got))
    assert table[:3] == [((3,), 3, 2), ((1, 2), 3, 3), ((2, 2), 4, 8)]
    # w = (3), m = 3：特殊牌必須第一張
    assert deck_count((3,), 3) == 2 and math.factorial(3) // 3 == 2
    # w = (1,2), m = 3：L(1;1,1) = 3、標號 1!·1!·1! = 1
    assert L_formula(1, (1, 1)) == 3
    # 「特殊牌」含 w = 0 時，公式的 n 要改成 w >= 1 的張數
    assert deck_count((0, 3), 3) == 2 != math.factorial(3) // (3 - 2 + 1) and math.factorial(3) // (3 - 1 + 1) == 2
    print("ran_note015 改寫版的數字檢查通過；例題二的表：", table)


if __name__ == "__main__":
    main()
