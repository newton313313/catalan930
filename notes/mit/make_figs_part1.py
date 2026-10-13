r"""
make_figs_part1.py —— 講義附錄 A 第 1 段（A.1–A.4，動畫 M01–M04）的 TikZ 圖

在 notes/ 或 notes/mit/ 裡執行：
    python mit/make_figs_part1.py
會先檢查 mit/part1.tex 寫到的每一個數字（check_numbers），再寫出 mit/figs_part1.tex
（mit/part1.tex 的第一行用 \input{mit/figs_part1} 讀進來）。

數學資料一律由 codes/utils/counting.py 算出；TikZ 的圖元工具從 notes/make_catalan_figs.py 匯入。
LaTeX 的指令名稱不能含數字，所以圖的巨集用小寫羅馬數字標場景：
    \FigMiCauchy（M01）、\FigMiiBranches（M02）、\FigMiiiWalk（M03）、\FigMivRotations（M04）。
顏色（定義在講義導言區）：cLeft／cRight = 左／右（青／紫紅），cA = 一般卡塔蘭物件（藍），cBad = 紅。
"""
from __future__ import annotations

import math
import re
import sys
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent          # notes/mit
NOTES = HERE.parent                             # notes
sys.path.insert(0, str(NOTES.parent / "codes"))
sys.path.insert(0, str(NOTES))

from make_catalan_figs import emit, node, picture, place, pt  # noqa: E402
from utils.counting import (  # noqa: E402
    LEAF,
    MIT_EXAMPLE_TREE,
    binom_general,
    catalan,
    catalan_from_sqrt,
    cycle_classes,
    cycle_good_to_dyck,
    cycle_words,
    drunkard_fall_prob,
    drunkard_fall_words,
    drunkard_partial_sums,
    dyck_words,
    good_rotations,
    is_dyck,
    is_good_path,
    path_heights,
    raney_A,
    rotate,
    series_mul,
    sqrt_1m4x_coeffs,
    tree_to_dyck,
)

OUT = HERE / "figs_part1.tex"

# ---------------------------------------------------------------- 共用資料
N_TAB = 4                                        # M01 的乘法表 4×4
CAT = [catalan(n) for n in range(N_TAB + 1)]     # C_0..C_4
SQ = series_mul(CAT, CAT, N_TAB)                 # [x^n] C^2，n = 0..3
HALF = Fraction(1, 2)
M_MAX = 5                                        # M02 的表：m = 0..5
WALK = "UUDUDDD"                                 # M03：貫穿例子的 Dyck 路徑再往下一步
V = (2,)                                         # M04：字母 0 = +1、字母 1 = -1
N4 = 3
M4 = 2 * N4 + 1
GOOD = (LEAF, LEAF, LEAF, 1, LEAF, 1, 1)         # +1 接 UUDUDD
BAD = rotate(GOOD, 3)                            # (1,0,1,1,0,0,0)：圖裡的「不好的」序列
GOOD_J = 4                                       # BAD 從第 4 點讀起是好的


def heights_ud(word):
    h, out = 0, [0]
    for c in word:
        h += 1 if c == "U" else -1
        out.append(h)
    return out


def minus_branch(x):
    """(1 - sqrt(1-4x)) / (2x) = 2 / (1 + sqrt(1-4x))，在 x = 0 也有定義。"""
    return 2.0 / (1.0 + math.sqrt(max(0.0, 1.0 - 4.0 * x)))


def plus_branch(x):
    return (1.0 + math.sqrt(max(0.0, 1.0 - 4.0 * x))) / (2.0 * x)


def odd_product(k):
    """1·3·5···k（k < 1 時是空乘積 1）。"""
    out = 1
    for j in range(1, k + 1, 2):
        out *= j
    return out


def main_section_numbers() -> dict:
    """主講義（附錄之前）的節／小節標題 -> 編號，例如 '投票問題' -> '1.9'。"""
    sec = sub = 0
    out = {}
    for line in (NOTES / "chu1987_導讀.tex").read_text(encoding="utf-8").splitlines():
        if line.startswith(r"\appendix"):
            break
        m = re.match(r"\\section\{([^}]*)\}", line)
        if m:
            sec, sub = sec + 1, 0
            out[m.group(1)] = str(sec)
            continue
        m = re.match(r"\\subsection\{([^}]*)\}", line)
        if m:
            sub += 1
            out[m.group(1)] = f"{sec}.{sub}"
    return out


def first_bad_point(heights):
    """第一個高度 <= 0 的點（不含起點）；沒有則 None。"""
    for j, h in enumerate(heights):
        if j > 0 and h <= 0:
            return j
    return None


# =============================================================================
# mit/part1.tex 寫到的數字
# =============================================================================
def check_numbers():
    # ---------------- A.1 Cauchy 乘積（M01）
    assert CAT == [1, 1, 2, 5, 14]
    assert SQ == [1, 2, 5, 14]
    assert [CAT[k] * CAT[1 - k] for k in range(2)] == [1, 1]                  # [x]C^2 = 1+1 = 2
    assert [CAT[k] * CAT[2 - k] for k in range(3)] == [2, 1, 2]               # [x^2]C^2 = 2+1+2 = 5
    assert [CAT[k] * CAT[3 - k] for k in range(4)] == [5, 2, 2, 5]            # [x^3]C^2 = 5+2+2+5 = 14
    c = [catalan(n) for n in range(30)]
    sq = series_mul(c, c, 29)
    assert all(sq[n] == c[n + 1] for n in range(29))                          # C_{n+1} = [x^n] C^2
    assert [0] + sq[:4] == [0, 1, 2, 5, 14]                                   # x C^2 = x + 2x^2 + 5x^3 + 14x^4
    assert [c[0] - 1] + c[1:5] == [0] + sq[:4]                                # C - 1 = x C^2
    # 表中格子的值 C_i C_j
    for i in range(N_TAB):
        for j in range(N_TAB):
            assert CAT[i] * CAT[j] == catalan(i) * catalan(j)

    # ---------------- A.2 閉式（M02）
    s = sqrt_1m4x_coeffs(M_MAX + 1)
    assert s == [1, -2, -2, -4, -10, -28]
    binoms = [binom_general(HALF, m) for m in range(M_MAX + 1)]
    assert binoms == [1, Fraction(1, 2), Fraction(-1, 8), Fraction(1, 16), Fraction(-5, 128), Fraction(7, 256)]
    powers = [(-4) ** m for m in range(M_MAX + 1)]
    assert powers == [1, -4, 16, -64, 256, -1024]
    assert all(b * p == v for b, p, v in zip(binoms, powers, s))
    for m in range(1, 15):
        b = binom_general(HALF, m)
        # binom(1/2,m) = (-1)^{m-1} 1·3···(2m-3) / (2^m m!)
        assert b == Fraction((-1) ** (m - 1) * odd_product(2 * m - 3), 2 ** m * factorial(m))
        lhs = b * (-4) ** m
        assert lhs == -Fraction(2 ** m * odd_product(2 * m - 3), factorial(m))
        # 1·3···(2m-3) = (2m-2)! / (2^{m-1} (m-1)!)
        assert odd_product(2 * m - 3) * 2 ** (m - 1) * factorial(m - 1) == factorial(2 * m - 2)
        assert lhs == -Fraction(2, m) * comb(2 * m - 2, m - 1)
    assert odd_product(-1) == 1 and -Fraction(2, 1) * comb(0, 0) == -2                   # m = 1
    assert [-v for v in s[1:]] == [2, 2, 4, 10, 28]                                        # 1 - sqrt(1-4x)
    cs = catalan_from_sqrt(M_MAX)
    assert cs == [1, 1, 2, 5, 14] == [-v // 2 for v in s[1:]]
    for n in range(20):
        assert Fraction(-1, 2) * (-Fraction(2, n + 1) * comb(2 * n, n)) == catalan(n)
    # 取號：「−」在 0 的值 1、在 1/4 的值 2；「+」在 0.16 的值 5、在 1/4 的值 2
    assert abs(minus_branch(0.0) - 1) < 1e-12 and abs(minus_branch(0.25) - 2) < 1e-12
    assert abs(plus_branch(0.16) - 5) < 1e-9 and abs(plus_branch(0.25) - 2) < 1e-12
    for x in (0.01, 0.1, 0.2):   # 有理化：(1 - sqrt(1-4x)) / (2x) = 2 / (1 + sqrt(1-4x))
        assert abs((1 - math.sqrt(1 - 4 * x)) / (2 * x) - minus_branch(x)) < 1e-12
        assert abs(plus_branch(x) * x - (1 + math.sqrt(1 - 4 * x)) / 2) < 1e-12           # ≈ 1/x
    for x in (0.01, 0.05, 0.1, 0.2, 0.24):   # 級數與閉式一致
        assert abs(sum(catalan(n) * x ** n for n in range(400)) - minus_branch(x)) < 1e-9

    # ---------------- A.3 醉漢走路（M03）
    assert tree_to_dyck(MIT_EXAMPLE_TREE) == "UUDUDD" and WALK == "UUDUDD" + "D"
    assert heights_ud(WALK) == [0, 1, 2, 1, 2, 1, 0, -1]
    assert heights_ud(WALK).index(-1) == 7 == len(WALK)                      # 第 7 步第一次走到 -1
    small = {n: drunkard_fall_words(n) for n in range(4)}
    assert small[0] == ["D"] and small[1] == ["UDD"] and small[2] == ["UDUDD", "UUDDD"]
    assert len(small[3]) == 5 and WALK in small[3]
    for n in range(8):
        words = drunkard_fall_words(n)
        assert words == sorted(d + "D" for d in dyck_words(n)) and len(words) == catalan(n)
        assert all(is_dyck(w[:-1]) for w in words)
    probs = [drunkard_fall_prob(n) for n in range(4)]
    assert probs == [Fraction(1, 2), Fraction(1, 8), Fraction(2, 32), Fraction(5, 128)]
    assert all(p == Fraction(catalan(n), 2 ** (2 * n + 1)) for n, p in enumerate(probs))
    q = Fraction(1, 4)
    assert 1 - 4 * q == 0 and Fraction(1 - 0) / (2 * q) == 2 and HALF * 2 == 1     # C(1/4) = 2
    ps = drunkard_partial_sums(200)
    assert ps[:4] == [Fraction(1, 2), Fraction(5, 8), Fraction(11, 16), Fraction(93, 128)]
    rest = [Fraction(comb(2 * K, K), 4 ** K) for K in range(201)]
    assert rest[:5] == [1, Fraction(1, 2), Fraction(3, 8), Fraction(5, 16), Fraction(35, 128)]
    for K in range(1, 201):
        assert 1 - ps[K - 1] == rest[K]                              # 1 - S_K = binom(2K,K)/4^K
        assert rest[K - 1] - rest[K] == Fraction(catalan(K - 1), 2 ** (2 * K - 1))
        prod = Fraction(1)
        for i in range(1, K + 1):
            prod *= Fraction(2 * i - 1, 2 * i)
        assert prod == rest[K]                                       # = 1/2 · 3/4 ··· (2K-1)/(2K)
        assert rest[K] ** 2 <= Fraction(1, 2 * K + 1)                # <= 1/sqrt(2K+1)
    assert f"{float(rest[100]) * 100:.1f}" == "5.6" and 2 * 100 - 1 == 199  # 前 199 步都沒掉
    assert f"{float(ps[99]):.3f}" == "0.944"
    # C_n ~ 4^n / (sqrt(pi) n^{3/2})：所以 sum C_n / 4^n 收斂（x = 1/4 在收斂半徑上）
    n = 2000
    log_ratio = (math.lgamma(2 * n + 1) - math.lgamma(n + 2) - math.lgamma(n + 1)
                 - n * math.log(4) + 0.5 * math.log(math.pi) + 1.5 * math.log(n))
    assert abs(math.exp(log_ratio) - 1) < 1e-3

    # ---------------- A.4 循環移位（M04）
    assert BAD == (1, LEAF, 1, 1, LEAF, LEAF, LEAF)
    assert BAD.count(LEAF) == N4 + 1 and BAD.count(1) == N4
    hs = path_heights(BAD, V)
    assert hs == [0, -1, 0, -1, -2, -1, 0, 1]
    low = min(hs[:-1])
    assert low == -2 and max(j for j, h in enumerate(hs[:-1]) if h == low) == GOOD_J
    assert good_rotations(BAD, V) == [GOOD_J] and rotate(BAD, GOOD_J) == GOOD
    assert cycle_good_to_dyck(GOOD) == "UUDUDD" == tree_to_dyck(MIT_EXAMPLE_TREE)
    assert path_heights(GOOD, V) == [0, 1, 2, 3, 2, 3, 2, 1]
    words = cycle_words(N4)
    classes = cycle_classes(N4)
    assert len(words) == comb(7, 3) == 35 and len(classes) == 5 == catalan(3)
    assert 35 % 7 == 0 and 35 // 7 == 5 and 35 - 5 == 30
    seen = set()
    for g, rots in classes:
        assert len(rots) == M4 and len(set(rots)) == M4                     # 一圈的 7 種讀法都不同
        assert [is_good_path(r, V) for r in rots] == [True] + [False] * (M4 - 1)
        seen |= set(rots)
    assert seen == set(words)
    assert sorted(cycle_good_to_dyck(g) for g, _ in classes) == sorted(dyck_words(N4))
    for n in range(1, 8):    # 一般 n：每個字恰有 1 種好讀法；好的 = +1 接 Dyck 路徑
        ws = cycle_words(n)
        assert len(ws) == comb(2 * n + 1, n)
        assert all(len(good_rotations(w, V)) == 1 for w in ws)
        assert len(cycle_classes(n)) == catalan(n)
    for n in range(0, 30):
        assert comb(2 * n + 1, n) % (2 * n + 1) == 0
        assert comb(2 * n + 1, n) // (2 * n + 1) == comb(2 * n, n) // (n + 1) == catalan(n)
    # 第 7 節的推廣：v = (2)、t = 1、n = (n) 時 A_1 = binom(2n+1, n) / (2n+1) = C_n
    for n in range(0, 15):
        assert raney_A(1, (n,), V) == Fraction(comb(2 * n + 1, n), 2 * n + 1) == catalan(n)
    # 圖：每種讀法第一個高度 <= 0 的點
    bad_pts = [first_bad_point(path_heights(rotate(BAD, j), V)) for j in range(M4)]
    assert bad_pts == [1, 2, 1, 1, None, 6, 2]

    # ---------------- 內文寫死的主講義節號（主講義的小節沒有 \label，只能寫數字）
    secs = main_section_numbers()
    text = (HERE / "part1.tex").read_text(encoding="utf-8")
    for title, num in [("生成函數 $C=1+xC^2$", "1.12"), ("格子路徑與反射原理", "1.6"),
                       ("投票問題", "1.9"), ("證明第二步：把遞迴變成生成函數的方程", "5"),
                       ("兩條翻譯規則", "5.2")]:
        assert secs[title] == num, (title, secs.get(title), num)
        if num != "5.2":
            assert f"第 {num} 節" in text, num
    assert "「兩條翻譯規則」" in text
    print("附錄 A 第 1 段（A.1–A.4）的數字檢查通過")


# =============================================================================
# 小工具
# =============================================================================
def xpow(k: int) -> str:
    return "" if k == 0 else ("x" if k == 1 else f"x^{k}")


def mono(coef: int, k: int) -> str:
    if k == 0:
        return str(coef)
    return ("" if coef == 1 else str(coef)) + xpow(k)


def pm_path_prims(heights, ux, uy, colors, w=1.1, dot_r=0.03, dots=True):
    """±1 路徑（高度串列 heights），第 j 步的顏色 colors[j]；起點 (0, heights[0]·uy)。"""
    prims = []
    for j in range(len(heights) - 1):
        a = (j * ux, heights[j] * uy)
        b = ((j + 1) * ux, heights[j + 1] * uy)
        prims.append(("line", f"{colors[j]},line width={w}pt,line cap=round", a, b))
    if dots:
        for j, h in enumerate(heights):
            prims.append(("dot", "black!70", (j * ux, h * uy), dot_r))
    return prims


# =============================================================================
# 圖
# =============================================================================
DIAG_FILL = {0: "cA!9", 1: "green!50!black!11", 2: "yellow!45", 3: "orange!20"}


def fig_m01_cauchy() -> str:
    """M01：C(x)·C(x) 的乘法表；格子 (i,j) = C_iC_j x^{i+j}，同一條反對角線 i+j=n 同色；右邊是各條的和。"""
    hw, cw, ch = 1.25, 1.62, 0.78
    lines = []

    def cx(j):
        return hw + (j + 0.5) * cw

    def cy(i):
        return -(i + 1) * ch

    lines += emit([node((hw / 2, 0.0), r"$\times$", "font=\\small,text=gray!70!black")])
    for j in range(N_TAB):
        lines += emit([node((cx(j), 0.0), rf"$C_{j}{xpow(j)}$", "font=\\small,text=cRight")])
    for i in range(N_TAB):
        lines += emit([node((hw / 2, cy(i)), rf"$C_{i}{xpow(i)}$", "font=\\small,text=cLeft")])
    for i in range(N_TAB):
        for j in range(N_TAB):
            n = i + j
            x0, y0, y1 = hw + j * cw, -(i + 1.5) * ch, -(i + 0.5) * ch
            if n in DIAG_FILL:
                lines.append(rf"\fill[{DIAG_FILL[n]}] {pt(x0, y0)} rectangle {pt(x0 + cw, y1)};")
            v = CAT[i] * CAT[j]
            if n < N_TAB:
                top = rf"$\textcolor{{cLeft}}{{C_{i}}}\textcolor{{cRight}}{{C_{j}}}{xpow(n)}$"
                bot = rf"$={mono(v, n)}$"
                lines.append(rf"\node[font=\small] at {pt(cx(j), cy(i) + 0.13)} {{{top}}};")
                lines.append(rf"\node[font=\scriptsize,text=gray!70!black] at {pt(cx(j), cy(i) - 0.19)} {{{bot}}};")
            else:   # x^4 以上：這張表只畫到一部分，淡化
                top = rf"$C_{i}C_{j}{xpow(n)}$"
                lines.append(rf"\node[font=\small,text=gray!55] at {pt(cx(j), cy(i) + 0.13)} {{{top}}};")
                lines.append(rf"\node[font=\scriptsize,text=gray!55] at {pt(cx(j), cy(i) - 0.19)} {{$={mono(v, n)}$}};")
    # 格線
    x_right, y_bot = hw + N_TAB * cw, -(N_TAB + 0.5) * ch
    for i in range(N_TAB + 1):
        y = -(i + 0.5) * ch
        lines.append(rf"\draw[gray!55,line width=0.4pt] {pt(hw, y)} -- {pt(x_right, y)};")
    for j in range(N_TAB + 1):
        x = hw + j * cw
        lines.append(rf"\draw[gray!55,line width=0.4pt] {pt(x, -0.5 * ch)} -- {pt(x, y_bot)};")
    # 右邊：每條反對角線的和
    xl = x_right + 0.75
    for n in range(N_TAB):
        y = -(n + 1) * ch
        terms = [CAT[k] * CAT[n - k] for k in range(n + 1)]
        assert sum(terms) == SQ[n]
        lhs = rf"[{xpow(n) or 'x^0'}]\,C^2"
        rhs = "+".join(map(str, terms)) + (f"={SQ[n]}" if n else "")
        lines.append(rf"\fill[{DIAG_FILL[n]}] {pt(xl, y - 0.17)} rectangle {pt(xl + 0.34, y + 0.17)};")
        lines.append(rf"\draw[gray!55,line width=0.3pt] {pt(xl, y - 0.17)} rectangle {pt(xl + 0.34, y + 0.17)};")
        lines.append(rf"\node[anchor=west,font=\small] at {pt(xl + 0.5, y)} {{${lhs}={rhs}$}};")
    lines.append(rf"\node[anchor=west,font=\footnotesize,text=gray!70!black] at {pt(xl, 0.0)} "
                 r"{同色的格子加起來：};")
    return picture(lines)


def fig_m02_branches() -> str:
    """M02：兩個根在 0 < x <= 1/4 的圖形。「−」從 1 走到 2；「+」在 0 附近爆掉。"""
    sx, sy = 15.0, 0.5           # x = 1/4 -> 3.75 cm；y = 1 -> 0.5 cm
    lines = [
        rf"\draw[-{{Stealth[length=4pt]}},gray!70!black,line width=0.5pt] (0,0) -- {pt(0.25 * sx + 0.45, 0)}"
        r" node[right,font=\small] {$x$};",
        rf"\draw[-{{Stealth[length=4pt]}},gray!70!black,line width=0.5pt] (0,0) -- {pt(0, 5 * sy + 0.35)};",
        rf"\draw[gray!45,dashed,line width=0.4pt] {pt(0.25 * sx, 0)} -- {pt(0.25 * sx, 2 * sy)};",
        rf"\node[below,font=\small] at {pt(0.25 * sx, 0)} {{$\frac14$}};",
        r"\node[below left,font=\small] at (0,0) {$0$};",
    ]
    for y in range(1, 6):
        lines.append(rf"\draw[gray!70!black,line width=0.4pt] {pt(-0.07, y * sy)} -- {pt(0.07, y * sy)};")
        lines.append(rf"\node[left,font=\scriptsize] at {pt(-0.07, y * sy)} {{${y}$}};")
    xs = [0.0025 * k for k in range(101)]
    lines.append(r"\draw[cA,line width=1.3pt] " + " -- ".join(pt(x * sx, minus_branch(x) * sy) for x in xs) + ";")
    xs = [0.16 + 0.001 * k for k in range(91)]
    lines.append(r"\draw[cBad,line width=1.3pt] " + " -- ".join(pt(x * sx, plus_branch(x) * sy) for x in xs) + ";")
    # 「+」往 x -> 0 爆掉的箭頭
    x1, x2 = 0.16, 0.148
    lines.append(rf"\draw[-{{Stealth[length=5pt]}},cBad,line width=1.3pt] {pt(x1 * sx, plus_branch(x1) * sy)}"
                 rf" -- {pt(x2 * sx, plus_branch(x2) * sy)};")
    lines += [
        rf"\fill[cA] {pt(0, sy)} circle (0.07);",
        rf"\fill[black] {pt(0.25 * sx, 2 * sy)} circle (0.05);",
        rf"\node[anchor=north west,font=\scriptsize,text=cA] at {pt(0.04, sy - 0.04)} {{$C(0)=C_0=1$}};",
        rf"\node[right,font=\scriptsize,text=cBad] at {pt(0.165 * sx, 4.75 * sy)} {{取 $+$：$x\to0$ 時 $\to\infty$}};",
        rf"\node[above,font=\scriptsize,text=cA] at {pt(0.13 * sx, minus_branch(0.13) * sy + 0.05)} {{取 $-$}};",
        rf"\node[right,font=\scriptsize] at {pt(0.25 * sx + 0.05, 2 * sy + 0.12)} {{$(\frac14,2)$}};",
    ]
    return picture(lines)


def fig_m03_walk() -> str:
    """M03：左邊是例子 UUDUDD+D 的時間–位置圖；右邊是 n = 0..3 第 2n+1 步第一次掉下去的所有走法。"""
    lines = []
    # ---- 左：時間–位置圖
    ux, uy = 0.52, 0.42
    hs = heights_ud(WALK)
    width = len(WALK) * ux
    for h in (1, 2):
        lines.append(rf"\draw[gray!22,line width=0.3pt] {pt(0, h * uy)} -- {pt(width + 0.1, h * uy)};")
    lines += [
        rf"\draw[gray!60,line width=0.5pt] {pt(0, 0)} -- {pt(width + 0.1, 0)};",
        rf"\draw[cBad,dashed,line width=0.6pt] {pt(0, -uy)} -- {pt(width + 0.1, -uy)}"
        r" node[right,font=\scriptsize,text=cBad] {懸崖};",
        rf"\draw[-{{Stealth[length=4pt]}},gray!70!black,line width=0.5pt] {pt(0, -1.6 * uy)} -- {pt(0, 3.0 * uy)}"
        r" node[above,font=\scriptsize] {位置};",
        rf"\node[font=\scriptsize,text=gray!70!black] at {pt(width / 2, -2.75 * uy)} {{時間（步數）$\to$}};",
    ]
    for h in (-1, 0, 1, 2):
        col = "cBad" if h < 0 else "black"
        lines.append(rf"\node[left,font=\scriptsize,text={col}] at {pt(-0.02, h * uy)} {{${h}$}};")
    colors = ["cA"] * (len(WALK) - 1) + ["cBad"]
    lines += emit(pm_path_prims(hs, ux, uy, colors, w=1.5, dot_r=0.035))
    lines.append(rf"\fill[cBad] {pt(len(WALK) * ux, -uy)} circle (0.07);")
    for j, c in enumerate(WALK):
        col = "cBad" if j == len(WALK) - 1 else "cA"
        lines.append(rf"\node[font=\scriptsize,text={col}] at {pt((j + 0.5) * ux, -1.85 * uy)} {{$\mathrm{{{c}}}$}};")
    # ---- 右：n = 0..3（每一欄的走法排成一塊，塊與塊之間留 COL_GAP，避免相鄰兩欄的走法連在一起）
    u = 0.16
    gap, COL_GAP = 0.22, 0.75
    per_row = [1, 1, 2, 3]                      # n = 3 的 5 條排成 3 + 2
    blocks = [per_row[n] * (2 * n + 1) * u + (per_row[n] - 1) * gap for n in range(4)]
    col_x = [5.4, 6.65]
    for n in (2, 3):
        left = col_x[n - 1] + blocks[n - 1] / 2 + COL_GAP
        col_x.append(left + blocks[n] / 2)
    for n in range(1, 4):                       # 相鄰兩欄的走法不重疊
        assert col_x[n] - blocks[n] / 2 >= col_x[n - 1] + blocks[n - 1] / 2 + 0.5, n
    top_y = 1.05
    for n in range(4):
        words = drunkard_fall_words(n)
        lines.append(rf"\node[font=\small] at {pt(col_x[n], top_y)} {{$n={n}$}};")
        w_len = (2 * n + 1) * u
        if n < 3:
            slots = [(col_x[n] + (k - (len(words) - 1) / 2) * (w_len + gap), 0.4) for k in range(len(words))]
        else:
            slots = [(col_x[n] + (k - 1) * (w_len + gap), 0.4) for k in range(3)]
            slots += [(col_x[n] + (k - 0.5) * (w_len + gap), -0.5) for k in range(2)]
        assert len(slots) == len(words)
        for wd, (sx, sy) in zip(words, slots):
            x0 = sx - w_len / 2
            hh = heights_ud(wd)
            if wd == WALK:   # 左邊那一條：框起來
                lines.append(rf"\draw[cA!60,rounded corners=1.5pt,line width=0.5pt] {pt(x0 - 0.08, sy - u - 0.08)}"
                             rf" rectangle {pt(x0 + w_len + 0.08, sy + max(hh) * u + 0.08)};")
            lines.append(rf"\draw[gray!55,line width=0.3pt] {pt(x0, sy)} -- {pt(x0 + w_len, sy)};")
            lines.append(rf"\draw[cBad!70,dashed,line width=0.3pt] {pt(x0, sy - u)} -- {pt(x0 + w_len, sy - u)};")
            cols = ["cA"] * (len(wd) - 1) + ["cBad"]
            lines += emit(pm_path_prims(hh, u, u, cols, w=1.1, dots=False), x0, sy)
        c, d = catalan(n), 2 ** (2 * n + 1)
        lines.append(rf"\node[font=\small] at {pt(col_x[n], -1.0)} {{${c}$ 條}};")
        lines.append(rf"\node[font=\small] at {pt(col_x[n], -1.6)} {{$\frac{{{c}}}{{{d}}}$}};")
    for y, lab in ((0.4, "走法"), (-1.0, "條數"), (-1.6, "機率")):
        lines.append(rf"\node[anchor=east,font=\scriptsize,text=gray!70!black] at {pt(col_x[0] - 0.4, y)} {{{lab}}};")
    return picture(lines)


def fig_m04_rotations() -> str:
    """M04：BAD 的 7 種循環讀法（從第 j 點出發），只有 j = 4 是好的；紅點 = 第一個高度 <= 0 的點。"""
    u = 0.21
    dx = 2.3
    lines = []
    for j in range(M4):
        word = rotate(BAD, j)
        hs = path_heights(word, V)
        x0 = j * dx
        colors = ["gray!75!black" if s == LEAF else "cA" for s in word]
        if j == GOOD_J:
            lines.append(rf"\fill[green!50!black!8] {pt(x0 - 0.22, -3.05 * u)} rectangle {pt(x0 + M4 * u + 0.22, 3.6 * u)};")
            lines.append(rf"\draw[green!50!black,line width=0.7pt] {pt(x0 - 0.22, -3.05 * u)} rectangle "
                         rf"{pt(x0 + M4 * u + 0.22, 3.6 * u)};")
        lines.append(rf"\draw[gray!60,dashed,line width=0.4pt] {pt(x0 - 0.08, 0)} -- {pt(x0 + M4 * u + 0.08, 0)};")
        lines += emit(pm_path_prims(hs, u, u, colors, w=1.2, dot_r=0.028), x0, 0.0)
        bad = first_bad_point(hs)
        if bad is not None:
            lines.append(rf"\fill[cBad] {pt(x0 + bad * u, hs[bad] * u)} circle (0.075);")
        if j == 0:   # 原序列：最後一個最低點（第 4 點）
            lines.append(rf"\draw[cTop,line width=0.9pt] {pt(x0 + GOOD_J * u, hs[GOOD_J] * u)} circle (0.11);")
        mark = (r"\textcolor{green!50!black}{\checkmark}" if bad is None else r"\textcolor{cBad}{$\times$}")
        lines.append(rf"\node[font=\small] at {pt(x0 + M4 * u / 2, -3.55 * u - 0.12)} {{$j={j}$\ {mark}}};")
    return picture(lines)


FIGURES = [
    ("FigMiCauchy", fig_m01_cauchy),
    ("FigMiiBranches", fig_m02_branches),
    ("FigMiiiWalk", fig_m03_walk),
    ("FigMivRotations", fig_m04_rotations),
]


def main():
    check_numbers()
    parts = [
        "% figs_part1.tex —— 由 mit/make_figs_part1.py 產生，請勿手動修改。\n"
        "% 重新產生：python mit/make_figs_part1.py（在 notes/ 裡）\n"
    ]
    for name, func in FIGURES:
        body = func()
        assert "\n\n" not in body
        parts.append(f"\\newcommand{{\\{name}}}{{%\n{body}}}\n")
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"已寫出 {OUT.name}：{len(FIGURES)} 張圖")


if __name__ == "__main__":
    main()
