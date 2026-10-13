r"""
make_figs.py —— Raney (1960) 導讀（notes/raney1960_導讀.tex）的圖與表

在 notes/ 或 notes/raney/ 裡執行：
    python raney/make_figs.py
會先檢查講義寫到的每一個數字（check_numbers），再寫出 raney/figs.tex（主檔以 \input{raney/figs} 讀入）。
請改這支程式，不要手改 figs.tex。

數學一律由 codes/utils/raney.py 算出（與 Chu 講義共用 codes/utils/counting.py）。
顏色與 Chu 講義一致：符號 2（弦、2 點群組）= cA 藍、3（三角形）= cB 橘、4 = cC 綠、5 = cD 紫；
另外符號 1（一元運算子、1 點群組）= cU 棕、符號 0（引數、葉子）= 灰。
"""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent            # notes/raney
sys.path.insert(0, str(HERE.parent.parent / "codes"))

from utils import counting as ct  # noqa: E402
from utils.raney import (  # noqa: E402
    L_brute, L_formula, a0_of, a_from_chu, b_from_a, c_from_b, chu_heights, cyclic_variant, exp_series,
    gessel_suffix_code, gould_G, head_ranks, is_list, is_word, kelly_P, kelly_P_brute, lagrange_coeff,
    length_of, list_shifts, lists_with, lstar_coeffs, multinomial, mv_pow, partition_to_word,
    polygon_dissections_brute, prefix_code, ps_mul, ps_pow, raney_proof_trace, rank, solve_w, split_head,
    split_words, thm23_rhs, thm24_rhs, to_chu_path, tree_to_word, trinomial_coeff, word_to_partition,
    word_to_tree,
)

OUT = HERE / "figs.tex"
COL = {0: "gray!70!black", 1: "cU", 2: "cA", 3: "cB", 4: "cC", 5: "cD"}

# 講義裡反覆用到的例子
EX_PLUS1 = (2, 2, 0, 0, 0)                       # (a+b)+c = ++abc
EX_PLUS2 = (2, 0, 2, 0, 0)                       # a+(b+c) = +a+bc
EX_F = (2, 3, 0, 2, 0, 0, 0, 1, 0)               # F(G(x,H(y,z),t),K(u))
EX_F_LABELS = ["F", "G", "x", "H", "y", "z", "t", "K", "u"]
CYC1 = (0, 0, 2, 0, 2)                           # 組成 (1; 0, 2)，只有 k = 2 是字
CYC2 = (0, 0, 2, 0, 0, 3, 0)                     # Chu 講義圖 7 的路徑倒過來讀
CYC3 = (2, 0, 0, 2, 0, 0)                        # k = 0、3 給出同一個字串
TWO_VIEWS = (3, 0, 0, 0, 2, 0, 0)                # 2 字列：3000 | 200
NOTWORD = (0, 2, 0)                              # 秩 −1 但不是字
GESSEL_FIG3 = [(2, ((0, ()), (0, ()))), (1, ((0, ()),))]
CHU_FIG1 = [((3, 4), (0, 1, 2)), ((4, 0), (1, 2, 3)), ((0, 1), (2, 3, 4)), ((1, 2), (3, 4, 0)), ((2, 3), (4, 0, 1))]


def fr(x) -> str:
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = "-" if x < 0 else ""
    return rf"{sign}\tfrac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def wstr(s, sep=r"\,") -> str:
    """字串寫成 $2\,0\,0$，符號依型別上色。"""
    return sep.join(rf"\textcolor{{{COL.get(x, 'black')}}}{{{x}}}" for x in s)


def plain(s) -> str:
    return "".join(str(x) for x in s)


# =============================================================================
# 數字檢查：講義裡寫到的每一個數
# =============================================================================
def check_numbers():
    # 第 1 節：原文第 441 頁的三個例子、Cayley 問題、Problem 4983
    assert [is_word(s) for s in (EX_PLUS1, EX_PLUS2, EX_F)] == [True] * 3
    assert L_formula(1, (1, 2, 1)) == L_brute(1, (1, 2, 1))
    assert a0_of(1, (1, 2, 1)) == 5 and length_of(1, (1, 2, 1)) == 9
    assert [L_formula(1, (0, k)) for k in range(8)] == [1, 1, 2, 5, 14, 42, 132, 429]
    assert len(lists_with(1, (0, 3))) == 5
    assert [kelly_P(n, 1) for n in range(1, 8)] == [1, 1, 2, 5, 14, 42, 132]
    assert [kelly_P(n, 2) for n in (1, 3, 5, 7, 9)] == [1, 1, 3, 12, 55]
    assert [kelly_P(n, 3) for n in (1, 4, 7, 10)] == [1, 1, 4, 22]
    assert kelly_P(4, 2) == 0 and kelly_P_brute(4, 2) == 0 and kelly_P(5, 2) == 3
    assert polygon_dissections_brute(6, 4) == 3 and polygon_dissections_brute(8, 4) == 12
    assert polygon_dissections_brute(8, 5) == 4 == kelly_P(7, 3)

    # 第 2 節：秩、字、字列
    assert head_ranks(EX_F) == [0, 1, 3, 2, 3, 2, 1, 0, 0, -1]
    assert rank(NOTWORD) == -1 and not is_word(NOTWORD) and list_shifts(NOTWORD) == [1]
    assert split_words(TWO_VIEWS) == [(3, 0, 0, 0), (2, 0, 0)] and is_list(TWO_VIEWS, 2)
    assert lists_with(1, (1, 1)) == [(1, 2, 0, 0), (2, 0, 1, 0), (2, 1, 0, 0)]
    assert lists_with(2, (0, 1)) == [(0, 2, 0, 0), (2, 0, 0, 0)]

    # 定理 2.1
    assert list_shifts(CYC1) == [2] and cyclic_variant(CYC1, 2) == (2, 0, 2, 0, 0)
    tr = raney_proof_trace(CYC1)
    assert tr["alpha"] == (2, 0, 2) and rank(tr["alpha"]) == 1
    assert list_shifts(CYC2) == [2, 5]
    tr = raney_proof_trace(CYC2)
    assert tr["alpha"] == (3,) and tr["sigma1"] == (3, 0, 0, 0, 2, 0, 0) and tr["k1"] == 5
    assert tr["words"] == [(3, 0, 0, 0), (2, 0, 0)] and tr["rotations"][1] == (2, 0, 0, 3, 0, 0, 0)
    assert to_chu_path(CYC2, (2, 3)) == (0, 2, 0, 0, 1, 0, 0)          # Chu 講義：↑、三角形、↑、↑、弦、↑、↑
    assert ct.good_rotations(to_chu_path(CYC2, (2, 3)), (2, 3)) == [2, 5]
    assert list_shifts(CYC3) == [0, 3] and cyclic_variant(CYC3, 3) == CYC3
    assert list_shifts((0, 0)) == [0, 1]

    # 定理 2.2：表 \RanLTable 的每一列另外在 table 裡驗證；正文寫到的
    assert multinomial(4, 0, 1, 1) == 30 and length_of(1, (0, 1, 1)) == 6 and L_formula(1, (0, 1, 1)) == 5
    assert multinomial(5, 0, 1, 1) == 42 and length_of(2, (0, 1, 1)) == 7 and L_formula(2, (0, 1, 1)) == 12
    assert [L_formula(1, (0, 0, k)) for k in range(5)] == [1, 1, 3, 12, 55]
    assert L_formula(1, (2, 2)) == 30 == ct.brute_force((2, 2), (1, 2))
    assert L_formula(1, (1, 1)) == 3 == ct.brute_force((1, 1), (1, 2))

    # 定理 2.3、2.4
    assert thm23_rhs(1, 1, (0, 1, 1)) == 12
    assert [L_formula(1, b) * L_formula(1, (0, 1 - b[1], 1 - b[2])) for b in [(0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)]] == [5, 1, 1, 5]
    assert split_head((2, 0, 0, 3, 0, 0, 0), 1) == ((2, 0, 0), (3, 0, 0, 0))
    assert L_formula(3, (0, 0, 1)) == 3 and L_formula(4, (0, 1)) == 4 and thm24_rhs(1, (0, 1, 1)) == 12
    assert L_formula(2, (0, 0, 1)) == 2 and L_formula(3, (0, 1)) == 3 and thm24_rhs(0, (0, 1, 1)) == 5

    # 和 Chu 講義：路徑、例子、Fig. 1
    for (blocks, word) in zip(CHU_FIG1, fig1_words()):
        assert partition_to_word(blocks, 5) == word
    assert sorted(fig1_words()) == lists_with(1, (0, 1, 1))
    assert ct.raney_A(2, (1, 1), (2, 3)) == L_formula(2, (0, 1, 1)) == 12

    # 第 4 節：L* 與 (L*)^2
    Ls = lstar_coeffs(4, 4)
    assert Ls[(1, 1, 0, 0)] == 3 and Ls[(2, 1, 0, 0)] == 6 and Ls[(1, 0, 1, 0)] == 4 and Ls[(0, 2, 0, 0)] == 2
    sq = mv_pow(lstar_coeffs(3, 4), 2, 3, 4)
    assert sq[(0, 1, 0)] == 2 and sq[(1, 1, 0)] == 8 and sq[(0, 2, 0)] == 5
    # 依邊數數平面樹：H(E_i) = x^i → 卡塔蘭數
    for e in range(7):
        assert sum(v for p, v in lstar_coeffs(6, 6).items() if sum(i * c for i, c in enumerate(p, 1)) == e) \
            == comb(2 * e, e) // (e + 1)

    # 第 5 節：Lagrange 反演的例子
    N = 8
    g = geometric(N)
    assert [solve_w(g, N)[n] for n in range(1, 8)] == [1, 1, 2, 5, 14, 42, 132]
    sq2 = poly([1, 2, 1], N)
    assert [solve_w(sq2, N)[n] for n in range(1, 8)] == [1, 2, 5, 14, 42, 132, 429]
    mot = poly([1, 1, 1], N)
    assert [solve_w(mot, N)[n] for n in range(1, 9)] == [1, 1, 2, 4, 9, 21, 51, 127]
    assert len([p for p in lstar_coeffs(2, 3) if sum(i * c for i, c in enumerate(p, 1)) == 3]) == 2
    assert lists_with(1, (3, 0)) + lists_with(1, (1, 1)) == [(1, 1, 1, 0), (1, 2, 0, 0), (2, 0, 1, 0), (2, 1, 0, 0)]
    ex = exp_series(1, N)
    assert [solve_w(ex, N)[n] * factorial(n) for n in range(1, 7)] == [1, 2, 9, 64, 625, 7776]
    odd = poly([2, 3, 0, 1], N)
    assert [solve_w(odd, N)[n] for n in range(1, 6)] == [2, 6, 18, 62, 258]
    assert F(1, 3) * ps_pow(odd, 3, 2)[2] == 18 and 3 * 2 * 9 == 54
    w = solve_w(sq2, N)
    assert [ps_pow(w, 2, N)[n] for n in range(2, 6)] == [1, 4, 14, 48]
    assert all(ps_pow(w, 2, N)[n] == F(2, n) * comb(2 * n, n - 2) for n in range(2, 8))

    # 第 6 節
    assert [trinomial_coeff(3, k) for k in range(7)] == [1, 1, 3, 12, 55, 273, 1428]
    assert [trinomial_coeff(4, k) for k in range(7)] == [1, 1, 4, 22, 140, 969, 7084]
    assert [comb(2 * n, n) // (n + 1) % 2 for n in range(16)] == [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]

    # 第 7 節
    assert [b_from_a(g, 1, n) for n in range(6)] == [1, 1, 2, 5, 14, 42]
    assert [b_from_a(g, 3, n) for n in range(6)] == [1, 3, 9, 28, 90, 297]
    assert b_from_a(g, 2, 3) == 14 == 5 + 2 + 2 + 5
    assert [b_from_a(sq2, 2, n) for n in range(5)] == [1, 4, 14, 48, 165]
    assert [c_from_b(g, 1, k) for k in range(4)] == [1, 1, F(3, 2), F(19, 6)]
    assert gould_G(2, 3, 1, 0) * 6 == 50 and [gould_G(1, i, 1, 0) * gould_G(1, 3 - i, 1, 0) * 6 for i in range(4)] == [16, 9, 9, 16]
    assert [gould_G(F(1, 2), n, 2, 1) for n in range(4)] == [1, F(1, 2), F(7, 8), F(33, 16)]
    assert gould_G(1, 1, 2, 1) == 1 == 2 * gould_G(F(1, 2), 1, 2, 1)
    assert sum(gould_G(F(1, 2), k, 2, 1) * gould_G(F(1, 2), 2 - k, 2, 1) for k in range(3)) == gould_G(1, 2, 2, 1) == 2
    for v in (2, 3):
        for t in (1, 2):
            assert [gould_G(t, n, v, 1) for n in range(5)] == [ct.raney_A(t, (n,), (v,)) for n in range(5)]

    # 第 8 節：Gessel 的補充
    assert gessel_suffix_code(GESSEL_FIG3) == (0, 0, 2, 0, 1) and prefix_code(GESSEL_FIG3) == (2, 0, 0, 1, 0)
    red = [x - 1 for x in gessel_suffix_code(GESSEL_FIG3)]
    assert red == [-1, -1, 1, -1, 0] and head_ranks(gessel_suffix_code(GESSEL_FIG3))[1:] == [-1, -2, -1, -2, -2]
    lc = log_catalan(8)
    assert lc[1:5] == [1, F(3, 2), F(10, 3), F(35, 4)] and all(lc[m] == F(comb(2 * m, m), 2 * m) for m in range(1, 9))
    # c_{p+q}(x) = c_p(x c_{p+q}(x)^q)（Gessel 練習 3.3.2），p = q = 1、p = 2, q = 1
    for p, q in [(1, 1), (2, 1), (1, 2)]:
        cpq = fuss(p + q, 8)
        inner = ps_mul([F(0), F(1)], ps_pow(cpq, q, 8), 8)
        assert compose(fuss(p, 8), inner, 8) == cpq
    # Gessel (2.3.2)：c(x)^k 的係數 = k/(2n+k) C(2n+k, n) = A_k(n)（只有弦）
    for k in (1, 2, 3):
        ck = ps_pow(fuss(2, 8), k, 8)
        assert all(ck[n] == ct.raney_A(k, (n,), (2,)) for n in range(9))
    # 練習的答案
    assert L_formula(1, (0, 0, 0, 2)) == 4 and L_formula(1, (1, 0, 1)) == 4 and L_formula(3, (0, 2)) == 9
    assert L_formula(2, (1, 1)) == 8 and L_formula(1, (2, 1)) == 6
    assert ct.brute_force((1, 1), (1, 3)) == 4 and L_formula(1, a_from_chu((1, 1), (1, 3))) == 4
    assert [solve_w(poly([1, 0, 1], 9), 9)[n] for n in range(1, 10)] == [1, 0, 1, 0, 2, 0, 5, 0, 14]
    assert polygon_dissections_brute(7, 3) == 42 and polygon_dissections_brute(9, 5) == 0
    assert gould_G(1, 3, 1, 0) * 6 == 16
    check_numbers_text()
    print("講義（Raney 導讀）的數字檢查通過")


def check_numbers_text():
    """part4–part6 正文裡寫到、上面還沒檢查的數字。"""
    # 第 5 節：Motzkin 例子 (1/4)[x^3](1+x+x^2)^4 = 16/4
    assert ps_pow(poly([1, 1, 1], 4), 4, 3)[3] == 16
    assert all(lagrange_coeff(geometric(8), n) == F(comb(2 * n - 2, n - 1), n) for n in range(1, 8))
    assert all(lagrange_coeff(poly([1, 2, 1], 8), n) == F(comb(2 * n, n - 1), n) for n in range(1, 8))
    # 單一型 Chu：[x^n]C^k = k/n C(pn+k−1, n−1) = k/(pn+k) C(pn+k, n)
    for p in (2, 3):
        for k in (1, 2, 3):
            ck = ps_pow(fuss(p, 7), k, 7)
            assert all(ck[n] == F(k, n) * comb(p * n + k - 1, n - 1) == ct.raney_A(k, (n,), (p,)) for n in range(1, 8))
    # 第 6 節：三元例子、Chu 第 3.3 節的表
    assert lists_with(1, (0, 0, 2)) == [(3, 0, 0, 3, 0, 0, 0), (3, 0, 3, 0, 0, 0, 0), (3, 3, 0, 0, 0, 0, 0)]
    assert trinomial_coeff(3, 2) == F(comb(6, 2), 5) == 3
    assert [L_formula(1, (0, n1, n2)) for n1, n2 in [(1, 1), (2, 1), (1, 2), (2, 2), (3, 2)]] == [5, 21, 28, 180, 990]
    # 第 7 節：投票數的公式、c(α,k) 的多項式
    alpha = F(3, 7)
    g = geometric(8)
    assert c_from_b(g, alpha, 2) == alpha + alpha ** 2 / 2
    assert c_from_b(g, alpha, 3) == 2 * alpha + alpha ** 2 + alpha ** 3 / 6
    assert sum(comb(3, i) * F(i + 1) ** (i - 1) * F(4 - i) ** (2 - i) for i in range(4)) == 50
    # 練習
    assert is_word((2, 2, 0, 0, 2, 0, 0)) and is_word((2, 0, 2, 2, 0, 0, 0))
    assert head_ranks((2, 2, 0, 0, 2, 0, 0))[1:-1] == [1, 2, 1, 0, 1, 0]
    assert head_ranks((2, 0, 2, 2, 0, 0, 0))[1:-1] == [1, 0, 1, 2, 1, 0]
    assert is_word((2, 1, 0, 0)) and word_to_partition((2, 1, 0, 0), 3) == [(0, 2), (1,)]
    s = (1, 0, 0, 2, 0, 0)
    tr = raney_proof_trace(s)
    assert rank(s) == -3 and list_shifts(s) == [0, 2, 3] and tr["alpha"] == (2,) and tr["k1"] == 3
    assert tr["words"] == [(2, 0, 0), (1, 0), (0,)]
    assert [cyclic_variant(s, k) for k in (0, 2, 3)] == [(1, 0, 0, 2, 0, 0), (0, 2, 0, 0, 1, 0), (2, 0, 0, 1, 0, 0)]
    assert multinomial(7, 0, 0, 0, 2) == 36 and length_of(1, (0, 0, 0, 2)) == 9
    assert multinomial(5, 0, 2) == 21 and multinomial(3, 1, 1) == 20 and length_of(2, (1, 1)) == 5
    assert lists_with(1, (1, 0, 1)) == [(1, 3, 0, 0, 0), (3, 0, 0, 1, 0), (3, 0, 1, 0, 0), (3, 1, 0, 0, 0)]
    assert [word_to_partition(w, 4) for w in lists_with(1, (1, 0, 1))] == [
        [(0,), (1, 2, 3)], [(0, 1, 2), (3,)], [(0, 1, 3), (2,)], [(0, 2, 3), (1,)]]
    assert lists_with(1, (1, 1)) == [(1, 2, 0, 0), (2, 0, 1, 0), (2, 1, 0, 0)]
    assert [word_to_partition(w, 3) for w in lists_with(1, (1, 1))] == [[(0,), (1, 2)], [(0, 1), (2,)], [(0, 2), (1,)]]
    assert fig1_words()[2] == (2, 0, 3, 0, 0, 0)
    # Gessel 的前序碼倒過來 ≠ 後序碼
    assert tuple(reversed(prefix_code(GESSEL_FIG3))) == (0, 1, 0, 0, 2) != gessel_suffix_code(GESSEL_FIG3)


def geometric(N):
    return [F(1)] * (N + 1)


def poly(cs, N):
    return [F(c) for c in cs] + [F(0)] * (N + 1 - len(cs))


def fuss(p, N):
    """c_p(x) = 1 + x c_p^p 的係數。"""
    return [trinomial_coeff(p, k) for k in range(N + 1)]


def compose(f, g, N):
    out = [F(0)] * (N + 1)
    pw = [F(1)] + [F(0)] * N
    for c in f[:N + 1]:
        out = [o + c * x for o, x in zip(out, pw)]
        pw = ps_mul(pw, g, N)
    return out


def log_catalan(N):
    c = fuss(2, N)
    u = [F(0)] + c[1:]
    out, pw = [F(0)] * (N + 1), [F(1)] + [F(0)] * N
    for j in range(1, N + 1):
        pw = ps_mul(pw, u, N)
        out = [a + F((-1) ** (j + 1), j) * b for a, b in zip(out, pw)]
    return out


def fig1_words():
    return [partition_to_word(b, 5) for b in CHU_FIG1]


# =============================================================================
# TikZ：樹、秩路徑、Chu 路徑
# =============================================================================
def layout(tree):
    """回傳 [(x, depth, arity, index)]，葉子依序 x = 0, 1, 2, …；內部節點在小孩的中間；index = 前序位置。"""
    nodes, edges = [], []
    leaf = [0]
    order = [0]

    def rec(t, d):
        k, kids = t
        me = order[0]
        order[0] += 1
        if k == 0:
            x = leaf[0]
            leaf[0] += 1
            nodes.append((x, d, 0, me))
            return me, x
        xs = []
        ids = []
        slot = len(nodes)
        nodes.append(None)
        for kid in kids:
            cid, cx = rec(kid, d + 1)
            ids.append(cid)
            xs.append(cx)
        x = (xs[0] + xs[-1]) / 2
        nodes[slot] = (x, d, k, me)
        for cid in ids:
            edges.append((me, cid))
        return me, x

    rec(tree, 0)
    return nodes, edges


SHAPE = {1: "circle", 2: "circle", 3: "regular polygon,regular polygon sides=3", 4: "rectangle",
         5: "regular polygon,regular polygon sides=5"}


def tree_tikz(word, labels=None, sx=0.55, sy=0.75, small=False) -> str:
    nodes, edges = layout(word_to_tree(word))
    pos = {i: (x, d) for x, d, k, i in nodes}
    ar = {i: k for x, d, k, i in nodes}
    out = [rf"\begin{{tikzpicture}}[x={sx}cm,y={sy}cm,baseline=(n0.base)]"]
    for a, b in edges:
        out.append(rf"\draw[gray!70,line width=0.6pt] (n{a}) -- (n{b});" if False else "")
    for x, d, k, i in sorted(nodes, key=lambda n: n[3]):
        col = COL.get(k, "black")
        if labels:
            style = rf"draw={col},fill={col}!12,line width=0.8pt,circle,inner sep=1.2pt,minimum size=13pt,font=\small"
            if k == 0:
                style = rf"draw=gray!60,fill=gray!8,rectangle,inner sep=1.6pt,minimum size=11pt,font=\small"
            out.append(rf"\node[{style}] (n{i}) at ({x:.3f},{-d}) {{${labels[i]}$}};")
        else:
            if k == 0:
                style = "rectangle,draw=gray!70,fill=gray!15,inner sep=" + ("1.8pt" if small else "2.6pt")
            else:
                ins = {1: "2.4pt", 2: "2.8pt", 3: "2.0pt", 4: "2.6pt", 5: "2.2pt"}[k] if small else \
                      {1: "3.2pt", 2: "3.6pt", 3: "2.6pt", 4: "3.4pt", 5: "2.9pt"}[k]
                style = rf"{SHAPE[k]},draw={col},fill={col}!22,line width=0.8pt,inner sep={ins}"
            out.append(rf"\node[{style}] (n{i}) at ({x:.3f},{-d}) {{}};")
    for a, b in edges:
        out.append(rf"\draw[gray!70,line width=0.6pt] (n{a}) -- (n{b});")
    out.append(r"\end{tikzpicture}")
    return "\n".join(o for o in out if o)


def forest_tikz(words, sx=0.5, sy=0.7, gap=0.9, small=True) -> str:
    return (r"\hspace{%.2fcm}" % gap).join(tree_tikz(w, sx=sx, sy=sy, small=small) for w in words)


def walk_tikz(s, n=None, mode="raney", unit=0.32, labels=True, mark=None, shade=None, ymin=None, ymax=None) -> str:
    """mode = "raney"：秩路徑（前序讀，每個符號 x 走 x−1）；mode = "chu"：Chu 講義的路徑（倒過來讀，每步 1−x）。
    mark：要畫桃紅點的位置清單；shade：(i, j) 用淡黃色標出的區段。"""
    if mode == "raney":
        hs = head_ranks(s)
        seq = list(s)
        floor = -n if n is not None else None
    else:
        hs = chu_heights(s)
        seq = list(reversed(s))
        floor = 0
    m = len(seq)
    lo = min(hs + ([floor] if floor is not None else [])) if ymin is None else ymin
    hi = max(hs) if ymax is None else ymax
    out = [rf"\begin{{tikzpicture}}[x={unit}cm,y={unit}cm,baseline={{([yshift=-0.5ex]current bounding box.center)}}]"]
    if shade:
        i, j = shade
        out.append(rf"\fill[yellow!25] ({i},{lo - 0.4}) rectangle ({j},{hi + 0.4});")
    out.append(rf"\draw[gray!55,dashed] (0,0) -- ({m},0);")
    if floor is not None and floor != 0:
        out.append(rf"\draw[magenta!70!black,dashed] (0,{floor}) -- ({m},{floor});")
    for j, x in enumerate(seq):
        out.append(rf"\draw[{COL[x]},line width=1.3pt,line cap=round] ({j},{hs[j]}) -- ({j + 1},{hs[j + 1]});")
    for j, h in enumerate(hs):
        out.append(rf"\fill ({j},{h}) circle (1.25pt);")
    for j in (mark or []):
        out.append(rf"\fill[magenta!80!black] ({j},{hs[j]}) circle (2.6pt);")
    if labels:
        for j, x in enumerate(seq):
            out.append(rf"\node[font=\tiny,{COL[x]}] at ({j + 0.5},{lo - 0.9}) {{{x}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


# =============================================================================
# 各張圖
# =============================================================================
def fig_intro_trees() -> str:
    t1 = tree_tikz(EX_PLUS1, labels=["+", "+", "a", "b", "c"])
    t2 = tree_tikz(EX_PLUS2, labels=["+", "a", "+", "b", "c"])
    t3 = tree_tikz(EX_F, labels=EX_F_LABELS, sx=0.62)
    cell = r"\begin{tabular}{c}%s\\[4pt]$%s$\\[2pt]{\small 型 %s}\end{tabular}"
    return r"\begin{tabular}{ccc}" + " & ".join([
        cell % (t1, r"(a+b)+c\ \to\ {+}{+}abc", plain(EX_PLUS1)),
        cell % (t2, r"a+(b+c)\ \to\ {+}a{+}bc", plain(EX_PLUS2)),
        cell % (t3, r"F(G(x,H(y,z),t),K(u))", plain(EX_F)),
    ]) + r"\end{tabular}"


def fig_rank_F() -> str:
    hs = head_ranks(EX_F)
    rows = [r"\begin{tabular}{@{}l" + "c" * 10 + "@{}}",
            r"開頭的長度 $j$ & " + " & ".join(str(j) for j in range(10)) + r"\\",
            r"第 $j$ 個符號 & — & " + " & ".join(rf"\textcolor{{{COL[x]}}}{{{x}}}" for x in EX_F) + r"\\",
            r"開頭的秩 & " + " & ".join(str(h) for h in hs) + r"\\",
            r"\end{tabular}"]
    return "\n".join(rows) + r"\qquad" + walk_tikz(EX_F, 1, unit=0.36)


def fig_cayley() -> str:
    cells = []
    for w in lists_with(1, (0, 3)):
        cells.append(r"\begin{tabular}{c}%s\\[3pt]$%s$\\[1pt]{\small $%s$}\end{tabular}"
                     % (tree_tikz(w, sx=0.42, sy=0.5, small=True), wstr(w), paren(w)))
    return r"\begin{tabular}{ccccc}" + " & ".join(cells) + r"\end{tabular}"


def paren(w) -> str:
    letters = iter("abcd")

    def rec(t):
        k, kids = t
        if k == 0:
            return next(letters)
        return "(" + "".join(rec(c) for c in kids) + ")"

    s = rec(word_to_tree(w))
    return s[1:-1]


def fig_chu_fig1() -> str:
    cells = []
    for (chord, tri), w in zip(CHU_FIG1, fig1_words()):
        a, b = (p + 1 for p in chord)
        c, d, e = (p + 1 for p in tri)
        cells.append(r"\begin{tabular}{c}\PaperCfgRoot{%d}{%d}{%d}{%d}{%d}\\[3pt]$%s$\\[3pt]%s\end{tabular}"
                     % (a, b, c, d, e, wstr(w), tree_tikz(w, sx=0.36, sy=0.45, small=True)))
    return r"\begin{tabular}{ccccc}" + " & ".join(cells) + r"\end{tabular}"


def cyc_table(s, both=False) -> str:
    n = -rank(s)
    ks = list_shifts(s)
    rows = []
    for k in range(len(s)):
        v = cyclic_variant(s, k)
        ok = k in ks
        mark = r"\textcolor{green!50!black}{\checkmark}" if ok else r"\textcolor{cBad}{$\times$}"
        cells = [str(k), rf"${wstr(v)}$", walk_tikz(v, n, unit=0.2, labels=False, ymin=-n - 1, ymax=3)]
        if both:
            cells.append(walk_tikz(v, n, mode="chu", unit=0.2, labels=False, ymin=-1, ymax=n + 3))
        cells.append(mark)
        rows.append(" & ".join(cells) + r"\\[2pt]")
    head = r"$k$ & $\sigma g_k$ & 秩路徑 & " + (r"Chu 講義的路徑 & " if both else "") + r"$n$ 字列？\\\midrule"
    return (r"\begin{tabular}{c c c " + ("c " if both else "") + r"c}\toprule " + head + "\n" + "\n".join(rows)
            + r"\bottomrule\end{tabular}")


def fig_alpha() -> str:
    tr = raney_proof_trace(CYC2)
    s1 = tr["sigma1"]
    w1, w2 = tr["words"]
    return (walk_tikz(s1, 2, unit=0.38, shade=(0, len(tr["alpha"])), mark=[len(w1)]) + r"\qquad"
            + r"\begin{tabular}{l}$\sigma_1=\sigma g_{%d}=%s$\\[3pt]$\alpha_1=%s,\quad \alpha_2=%s$\\[3pt]"
              r"$\sigma_2=\alpha_2\alpha_1=%s=\sigma g_{%d}$\end{tabular}"
            % (tr["k1"], wstr(s1), wstr(w1), wstr(w2), wstr(tr["rotations"][1]), tr["ks"][1]))


def fig_two_views() -> str:
    s = TWO_VIEWS
    a = r"\begin{tabular}{c}%s\\[2pt]{\small Raney：秩路徑（由左往右讀 $%s$）}\end{tabular}" % (
        walk_tikz(s, 2, unit=0.38), wstr(s))
    b = r"\begin{tabular}{c}%s\\[2pt]{\small Chu 講義：好路徑（由右往左讀，每步 $1-j$）}\end{tabular}" % (
        walk_tikz(s, 2, mode="chu", unit=0.38))
    c = r"\begin{tabular}{c}%s\\[2pt]{\small 對應的森林（2 棵樹）}\end{tabular}" % forest_tikz(split_words(s), sx=0.45, sy=0.6)
    return a + r"\quad" + b + r"\quad" + c


def fig_thm23() -> str:
    s = (2, 0, 0, 3, 0, 0, 0)
    h, rest = split_head(s, 1)
    return (r"$%s\ =\ \underbrace{%s}_{\text{1 字列}}\ \underbrace{%s}_{\text{1 字列}}$\qquad" % (wstr(s), wstr(h), wstr(rest))
            + walk_tikz(s, 2, unit=0.38, mark=[len(h)]))


def fig_motzkin() -> str:
    ws = lists_with(1, (3, 0)) + lists_with(1, (1, 1))
    cells = [r"\begin{tabular}{c}%s\\[2pt]$%s$\end{tabular}" % (tree_tikz(w, sx=0.45, sy=0.5, small=True), wstr(w)) for w in ws]
    return r"\begin{tabular}{cccc}" + " & ".join(cells) + r"\end{tabular}"


def fig_gessel_codes() -> str:
    f = GESSEL_FIG3
    words = [tree_to_word(t) for t in f]
    suf = gessel_suffix_code(f)
    red = [x - 1 for x in suf]
    pre = prefix_code(f)
    sums = head_ranks(suf)[1:]
    rows = [
        r"\begin{tabular}{@{}ll@{}}",
        r"Raney 的前序碼（2 字列） & $%s$\\" % wstr(pre),
        r"Gessel 的 suffix code $c(T_1)c(T_2)$ & $%s$\\" % wstr(suf),
        r"reduced code（每項減 1） & $%s$\\" % r"\ ".join(str(x) for x in red),
        r"reduced code 的部分和 & $%s$（全部 $<0$，總和 $-2$）\\" % r",\ ".join(str(x) for x in sums),
        r"Chu 講義的路徑高度（取負號） & $%s$\\" % r",\ ".join(str(-x) for x in sums),
        r"\end{tabular}",
    ]
    return forest_tikz(words, sx=0.5, sy=0.7) + r"\qquad" + "\n".join(rows)


def fig_hexagon() -> str:
    """六邊形切成兩個四邊形的 3 種方法（Etherington）。"""
    cells = []
    for d in [(0, 3), (1, 4), (2, 5)]:
        cells.append(
            r"\begin{tikzpicture}[scale=0.55,baseline=-0.5ex]"
            r"\foreach \i in {0,...,5}{\coordinate (h\i) at ({90-60*\i}:1);}"
            r"\draw[cC,line width=1pt,fill=cC!12] (h0)--(h1)--(h2)--(h3)--(h4)--(h5)--cycle;"
            rf"\draw[cC,line width=1.2pt] (h{d[0]})--(h{d[1]});"
            r"\foreach \i in {0,...,5}{\fill (h\i) circle (1.4pt);}\end{tikzpicture}")
    return r"\quad".join(cells)


# =============================================================================
# 表
# =============================================================================
L_ROWS = [  # (n, a, Chu 的 (n⃗, v⃗) 或 None, 白話)
    (1, (0, 3), ((3,), (2,)), r"Cayley：4 個因子的乘積"),
    (1, (0, 0, 3), ((3,), (3,)), r"3 個三元運算"),
    (1, (1, 1), ((1, 1), (1, 2)), r"一元＋二元各 1"),
    (1, (0, 1, 1), ((1, 1), (2, 3)), r"Chu 原文 Fig.~1"),
    (2, (0, 1, 1), ((1, 1), (2, 3)), r"同上，2 字列"),
    (1, (0, 2, 1), ((2, 1), (2, 3)), r"2 弦 1 三角形"),
    (1, (0, 1, 2), ((1, 2), (2, 3)), r"1 弦 2 三角形"),
    (1, (0, 2, 2), ((2, 2), (2, 3)), r"2 弦 2 三角形"),
    (1, (0, 1, 1, 1), ((1, 1, 1), (2, 3, 4)), r"弦、三角形、四邊形各 1"),
    (1, (2, 2), ((2, 2), (1, 2)), r"2 個單點、2 條弦"),
    (3, (0, 2), ((2,), (2,)), r"3 棵二元樹，共 2 個內部節點"),
]


def table_L() -> str:
    rows = [r"\setlength{\tabcolsep}{3.6pt}\begin{tabular}{@{}lccccccl@{}}\toprule",
            r"組成 $(n;a_1,a_2,\ldots)$ & $a_0$ & $m$ & $M(a_0,a_1,\ldots)$ & $\frac{n}{m}M$ & 暴力 & Chu：$t$、$\vn$、$\vv$ & 白話\\\midrule"]
    for n, a, chu, words in L_ROWS:
        a0, m = a0_of(n, a), length_of(n, a)
        Mv = multinomial(a0, *a)
        Lf, Lb = L_formula(n, a), L_brute(n, a)
        assert Lf == Lb
        if chu:
            assert ct.raney_A(n, *chu) == Lf and a_from_chu(*chu) == a
            if n == 1:
                assert ct.brute_force(*chu) == Lf
        comp = "(%d;\\,%s)" % (n, ",".join(str(x) for x in a))
        chu_s = r"$%d$、$(%s)$、$(%s)$" % (n, ",".join(map(str, chu[0])), ",".join(map(str, chu[1])))
        rows.append(rf"${comp}$ & {a0} & {m} & {Mv} & {Lf} & {Lb} & {chu_s} & {words}\\")
    rows.append(r"\bottomrule\end{tabular}")
    return "\n".join(rows)


def table_thm23() -> str:
    a = (0, 1, 1)
    rows = [r"\begin{tabular}{cccc}\toprule $b=(b_1,b_2,b_3)$ & $L(1;b)$ & $L(1;a-b)$ & 乘積\\\midrule"]
    total = 0
    for b in [(0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1)]:
        c = tuple(x - y for x, y in zip(a, b))
        x, y = L_formula(1, b), L_formula(1, c)
        total += x * y
        rows.append(rf"$({b[0]},{b[1]},{b[2]})$ & {x} & {y} & {x * y}\\")
    assert total == L_formula(2, a) == 12
    rows.append(r"\midrule\multicolumn{3}{r}{合計} & $%d=L(2;0,1,1)$\\\bottomrule\end{tabular}" % total)
    return "\n".join(rows)


def table_lstar() -> str:
    Ls = lstar_coeffs(4, 4)
    sq = mv_pow(lstar_coeffs(4, 4), 2, 4, 4)
    items = sorted((p for p in Ls if Ls[p]), key=lambda p: (sum(i * c for i, c in enumerate(p, 1)), [-c for c in p]))
    rows = [r"\begin{tabular}{@{}cl" + "c" * 3 + r"@{}}\toprule 權重 $\sum ip_i$ & 單項式 $E^*_{\bar p}$ & $L(1;\bar p)$ & $L(2;\bar p)$ & 例：$n=1$ 的字\\\midrule"]
    for p in items:
        wgt = sum(i * c for i, c in enumerate(p, 1))
        mono = r"\,".join((rf"E_{i}^{{*{c}}}" if c > 1 else rf"E_{i}^*").replace("*2", "*2").replace(r"^{*", r"^{*") for i, c in enumerate(p, 1) if c) or r"E_0^*"
        mono = mono.replace(r"E_1^{*2}", r"(E_1^*)^2").replace(r"E_1^{*3}", r"(E_1^*)^3").replace(
            r"E_1^{*4}", r"(E_1^*)^4").replace(r"E_2^{*2}", r"(E_2^*)^2")
        ex = lists_with(1, p)
        exs = r"$%s$" % wstr(ex[0]) + (r"、…（共 %d 個）" % len(ex) if len(ex) > 1 else "")
        assert len(ex) == Ls[p] and sq.get(p, 0) == L_formula(2, p)
        rows.append(rf"{wgt} & ${mono}$ & {Ls[p]} & {sq.get(p, 0)} & {exs}\\")
    rows.append(r"\bottomrule\end{tabular}")
    return "\n".join(rows)


def table_trinomial() -> str:
    rows = [r"\begin{tabular}{@{}c|" + "r" * 7 + r"@{}}$n\backslash k$ & " + " & ".join(str(k) for k in range(7)) + r"\\\hline"]
    for n in (2, 3, 4):
        vals = [trinomial_coeff(n, k) for k in range(7)]
        assert all(v == L_formula(1, tuple(k if i == n else 0 for i in range(1, n + 1))) for k, v in enumerate(vals))
        rows.append(rf"{n} & " + " & ".join(fr(v) for v in vals) + r"\\")
    rows.append(r"\end{tabular}")
    return "\n".join(rows)


def table_kelly() -> str:
    rows = [r"\begin{tabular}{@{}c|" + "r" * 10 + r"@{}}$r\backslash n$ & " + " & ".join(str(n) for n in range(1, 11)) + r"\\\hline"]
    for r in (1, 2, 3):
        vals = [kelly_P(n, r) for n in range(1, 11)]
        assert vals == [kelly_P_brute(n, r) for n in range(1, 11)]
        rows.append(rf"{r} & " + " & ".join(str(v) for v in vals) + r"\\")
    rows.append(r"\end{tabular}")
    return "\n".join(rows)


LAGR = [
    (r"\dfrac{1}{1-x}", geometric, r"w=\dfrac{x}{1-w}", r"$C_{n-1}$（卡塔蘭）"),
    (r"(1+x)^2", lambda N: poly([1, 2, 1], N), r"w=x(1+w)^2", r"$C_n$"),
    (r"1+x+x^2", lambda N: poly([1, 1, 1], N), r"w=x(1+w+w^2)", r"Motzkin 數 $M_{n-1}$"),
    (r"e^x", lambda N: exp_series(1, N), r"w=xe^{w}", r"$n^{n-1}/n!$（樹函數）"),
    (r"2+3x+x^3", lambda N: poly([2, 3, 0, 1], N), r"w=x(2+3w+w^3)", r"$a_0\ne1$ 的例子"),
]


def table_lagrange() -> str:
    N = 6
    rows = [r"\setlength{\tabcolsep}{3.5pt}\begin{tabular}{@{}lll" + "c" * N + r"l@{}}\toprule $\bar z=\sum a_n\bar x^n$ & 方程 (5.3) & & "
            + " & ".join(rf"$n={n}$" for n in range(1, N + 1)) + r" & 名稱\\\midrule"]
    for name, mk, eq, note in LAGR:
        phi = mk(N + 1)
        w = solve_w(phi, N)
        lag = [lagrange_coeff(phi, n) for n in range(1, N + 1)]
        assert w[1:] == lag
        rows.append(rf"${name}$ & ${eq}$ & 逐次代入 & " + " & ".join(rf"${fr(x)}$" for x in w[1:]) + rf" & {note}\\")
        rows.append(r" & & 式 (5.5) & " + " & ".join(rf"${fr(x)}$" for x in lag) + r" & \\[2pt]")
    rows.append(r"\bottomrule\end{tabular}")
    return "\n".join(rows)


def table_ballot() -> str:
    g = geometric(8)
    rows = [r"\begin{tabular}{@{}c|" + "r" * 6 + r"@{}}$m\backslash n$ & " + " & ".join(str(n) for n in range(6)) + r"\\\hline"]
    for m in (1, 2, 3):
        vals = [b_from_a(g, m, n) for n in range(6)]
        assert all(v == F(m, m + n) * comb(m + 2 * n - 1, n) for n, v in enumerate(vals) if m + n)
        rows.append(rf"{m} & " + " & ".join(fr(v) for v in vals) + r"\\")
    rows.append(r"\end{tabular}")
    return "\n".join(rows)


def table_notation() -> str:
    return ""  # 記號對照表直接寫在 part1.tex（文字多、不需要計算）


# =============================================================================
def main():
    check_numbers()
    figs = {
        "RanIntroTrees": fig_intro_trees(),
        "RanRankF": fig_rank_F(),
        "RanCayley": fig_cayley(),
        "RanChuFigOne": fig_chu_fig1(),
        "RanCycOne": cyc_table(CYC1),
        "RanCycTwo": cyc_table(CYC2, both=True),
        "RanAlpha": fig_alpha(),
        "RanTwoViews": fig_two_views(),
        "RanThmTwoThree": fig_thm23(),
        "RanMotzkin": fig_motzkin(),
        "RanGesselCodes": fig_gessel_codes(),
        "RanHexagon": fig_hexagon(),
        "RanLTable": table_L(),
        "RanThmTwoThreeTable": table_thm23(),
        "RanLstarTable": table_lstar(),
        "RanTrinomialTable": table_trinomial(),
        "RanKellyTable": table_kelly(),
        "RanLagrangeTable": table_lagrange(),
        "RanBallotTable": table_ballot(),
        "RanNotWord": walk_tikz(NOTWORD, 1, unit=0.36),
        "RanWalkPlusOne": walk_tikz(EX_PLUS1, 1, unit=0.3),
        "RanWalkPlusTwo": walk_tikz(EX_PLUS2, 1, unit=0.3),
        "RanCycThree": cyc_table(CYC3),
    }
    parts = ["% figs.tex —— 由 raney/make_figs.py 產生，請勿手動修改。\n"
             "% 重新產生：python raney/make_figs.py（在 notes/ 裡執行）\n"]
    for name, body in figs.items():
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"寫出 {OUT.name}：{len(figs)} 個圖表")


if __name__ == "__main__":
    main()
