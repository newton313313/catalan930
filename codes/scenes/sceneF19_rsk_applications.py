"""
Scene F19 —— R-S-K 的應用（Fulton《Young Tableaux》§4.3，書 p.50–57）

    Proposition 2：K_λμ 與 μ 的順序無關。只有兩種數時：λ = (r+s+t, r)，第 2 列全是 2、頭上 r 格是 1，
        第 1 列其餘是 s 個 1、t 個 2；對調 s、t。例 r=2, s=3, t=1：λ = (6,2)，內容 (5,3) ↔ (3,5)
        一般情形：固定 P，Q ↔ 列和為 μ 的矩陣 A；只動第 k、k+1 列（P(A) = P(B)·P(C)·P(D)）→ Schur 多項式對稱
        例：K_{(3,2),(2,2,1)} = K_{(3,2),(2,1,2)} = K_{(3,2),(1,2,2)} = 2
    (3) Cauchy–Littlewood：A ↔ (P,Q)，Π (x_j y_i)^{a(i,j)} = x^P y^Q（CH4_MATRIX：x_1^5 x_2^4 y_1^3 y_2^2 y_3^4）
        驗算：2×2、元素和 3 的矩陣 20 個 = Σ d_λ(2)² = 16 + 4 + 0
    (4) n! = Σ (f^λ)²（3! = 1+4+1）、(5) mⁿ = Σ d_λ(m) f^λ（2³ = 4·1+2·2+0·1）、(6) Σ f^λ = 對合數（n=4：10）
    鉤長公式（M13 做過，只回顧）：f^{(6,5,5,3)} = 19!/Π h = 6,651,216
    Stanley 鉤–內容公式：d_λ(m) = Π (m + j − i)/h(i,j)，d_{(6,5,5,3)}(5) = 3,360（直接列舉 ssyt 驗算）
    Exercise 12：最長遞增 ℓ、最長遞減 k 的排列數 = Σ (f^λ)²（λ 恰 k 列、ℓ 行）；S₄、ℓ = k = 2：4 個

數字全部由 utils/tableaux.py 算出並 assert（f^{(6,5,5,3)} 另用 utils/counting.py 的角落遞迴核對）。

試渲染（在 C:\\mypython\\manim\\projects\\combkit）：
    python tools/render_check.py ../catalan930/codes/scenes/sceneF19_rsk_applications.py SceneF19RSKApplications
           --config ../catalan930/codes/custom_config.yml
"""
import sys
from collections import Counter
from itertools import permutations, product as iproduct
from math import comb, factorial, prod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.counting import hook_lengths as counting_hook_lengths, syt_count
from utils.fulton_draw import assert_apart, assert_in_frame, labeled, tableau_mob, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH4_HOOK_SHAPE, CH4_MATRIX, CH4_P, CH4_Q, conjugate, content, count_involutions, hook_content_count, kostka,
    max_increasing, partitions, rsk_matrix, shape, ssyt, standard_tableaux, young_boxes,
)

R, S_, T_ = 2, 3, 1
LAM2 = (R + S_ + T_, R)
T1 = ((1,) * (R + S_) + (2,) * T_, (2,) * R)
T2 = ((1,) * (R + T_) + (2,) * S_, (2,) * R)
K_LAM, K_MUS = (3, 2), ((2, 2, 1), (2, 1, 2), (1, 2, 2))
MATS = [((a, b), (c, d)) for a, b, c, d in iproduct(range(4), repeat=4) if a + b + c + d == 3]
HOOK, M5 = CH4_HOOK_SHAPE, 5
VAL_COLORS = {1: TEAL, 2: GOLD}
SHAPE_COLORS = {(3,): TEAL, (2, 1): GOLD, (1, 1, 1): MUTED_COLOR}


def f_count(lam):
    return len(standard_tableaux(lam))


def d_count(lam, m):
    return len(ssyt(lam, m))


def hooks(lam):
    lt = conjugate(lam)
    return [[(lam[i] - j) + (lt[j] - i) - 1 for j in range(r)] for i, r in enumerate(lam)]


def numerators(lam, m):
    return [[m + j - i for j in range(r)] for i, r in enumerate(lam)]


def big(n):
    return f"{n:,}".replace(",", "{,}")


def ex12_perms(n, ell, k):
    return [w for w in permutations(range(1, n + 1))
            if max_increasing(w)[0] == ell and max_increasing(w, 1, decreasing=True)[0] == k]


def check_math():
    # Proposition 2：只有兩種數
    assert LAM2 == (6, 2) and content(T1) == (R + S_, R + T_) == (5, 3) and content(T2) == (3, 5)
    assert ssyt(LAM2, content=(5, 3)) == [T1] and ssyt(LAM2, content=(3, 5)) == [T2]
    for lam in partitions(8, max_parts=2):
        for a in range(9):
            assert kostka(lam, (a, 8 - a)) == kostka(lam, (8 - a, a)) == int(len(lam) < 2 or lam[1] <= min(a, 8 - a))
    assert [kostka(K_LAM, mu) for mu in K_MUS] == [2, 2, 2]
    # (3)：A ↔ (P, Q) 的那一項
    assert rsk_matrix(CH4_MATRIX) == (CH4_P, CH4_Q)
    assert content(CH4_P) == tuple(map(sum, zip(*CH4_MATRIX))) == (5, 4)
    assert content(CH4_Q) == tuple(map(sum, CH4_MATRIX)) == (3, 2, 4)
    # 2×2、元素和 3：20 個矩陣 ↔ 20 對 (P, Q)
    pairs = {rsk_matrix(M) for M in MATS}
    assert len(MATS) == comb(6, 3) == 20 == len(pairs)
    assert pairs == {(P, Q) for lam in partitions(3) for P in ssyt(lam, 2) for Q in ssyt(lam, 2)}
    assert Counter(shape(rsk_matrix(M)[0]) for M in MATS) == {(3,): 16, (2, 1): 4}
    assert [d_count(lam, 2) for lam in partitions(3)] == [4, 2, 0]
    # (4)(5)(6)
    assert [f_count(lam) for lam in partitions(3)] == [1, 2, 1]
    assert sum(f_count(lam) ** 2 for lam in partitions(3)) == factorial(3) == 6
    assert sum(d_count(lam, 2) * f_count(lam) for lam in partitions(3)) == 2 ** 3 == 8
    assert [f_count(lam) for lam in partitions(4)] == [1, 3, 2, 3, 1]
    assert sum(f_count(lam) for lam in partitions(4)) == count_involutions(4) == 10
    # 鉤長公式、鉤–內容公式
    H = hooks(HOOK)
    assert H == [list(r) for r in counting_hook_lengths(HOOK)] == [[9, 8, 7, 5, 4, 1], [7, 6, 5, 3, 2], [6, 5, 4, 2, 1],
                                                                   [3, 2, 1]]
    hp = prod(prod(r) for r in H)
    assert sum(HOOK) == 19 and factorial(19) % hp == 0 and factorial(19) // hp == syt_count(HOOK) == 6651216
    num = prod(prod(r) for r in numerators(HOOK, M5))
    assert num % hp == 0 and num // hp == hook_content_count(HOOK, M5) == len(ssyt(HOOK, M5)) == 3360
    # Exercise 12
    assert ex12_perms(4, 2, 2) == [(2, 1, 4, 3), (2, 4, 1, 3), (3, 1, 4, 2), (3, 4, 1, 2)]
    for ell in range(1, 5):
        for k in range(1, 5):
            assert len(ex12_perms(4, ell, k)) == sum(f_count(lam) ** 2 for lam in partitions(4)
                                                    if len(lam) == k and lam[0] == ell)


def mini_matrix(M, font_size=28, dx=0.45, dy=0.42, color=WHITE):
    """小矩陣（數字 + 左右圓括號）。"""
    ents = VGroup(*[Tex(str(a), font_size=font_size, fill_color=color).move_to(np.array([j * dx, -i * dy, 0.0]))
                    for i, row in enumerate(M) for j, a in enumerate(row)])
    h = (len(M) - 1) * dy + 0.5
    lp = Tex("(", font_size=font_size, fill_color=color).stretch_to_fit_height(h).next_to(ents, LEFT, buff=0.1)
    rp = Tex(")", font_size=font_size, fill_color=color).stretch_to_fit_height(h).next_to(ents, RIGHT, buff=0.1)
    return VGroup(lp, ents, rp)


# =============================================================================
# 第 1 段：Proposition 2
# =============================================================================
def part_two_letters(scene):
    stmt = mixed("Proposition 2：", "$K_{\\lambda\\mu}$", " 與 ", "$\\mu$", " 的順序無關", font_size=30)
    stmt.move_to(2.7 * UP)
    cs = 0.62
    d1 = tableau_mob(T1, cs, center=np.array([-3.6, 0.45, 0.0]))
    d2 = tableau_mob(T2, cs, center=np.array([3.6, 0.45, 0.0]))
    for d, T in ((d1, T1), (d2, T2)):
        for i, j in young_boxes(LAM2):
            d.cell(i, j).set_fill(VAL_COLORS[T[i][j]], opacity=0.3)

    def braces(d, segs):
        out = VGroup()
        for name, j0, j1, row, side in segs:
            b = Brace(VGroup(*[d.cell(row, j) for j in range(j0, j1)]), side, buff=0.08)
            out.add(VGroup(b, Tex(name, font_size=32).next_to(b, side, buff=0.08)))
        return out

    br_r = [braces(d, [("r", 0, R, 0, UP), ("r", 0, R, 1, DOWN)]) for d in (d1, d2)]
    br1 = braces(d1, [("s", R, R + S_, 0, UP), ("t", R + S_, R + S_ + T_, 0, UP)])
    br2 = braces(d2, [("t", R, R + T_, 0, UP), ("s", R + T_, R + T_ + S_, 0, UP)])
    c1 = mixed("內容 ", f"$(r+s,r+t)=({R + S_},{R + T_})$", font_size=24).next_to(br_r[0], DOWN, buff=0.3)
    c2 = mixed("內容 ", f"$(r+t,r+s)=({R + T_},{R + S_})$", font_size=24).next_to(br_r[1], DOWN, buff=0.3)
    arrow = Arrow(d1.get_right() + 0.35 * RIGHT, d2.get_left() + 0.35 * LEFT, buff=0.0, thickness=3,
                  fill_color=GREY_B)
    alab = Tex(r"s\leftrightarrow t", font_size=36, fill_color=YELLOW).next_to(arrow, UP, buff=0.12)
    note = mixed("形狀都是 ", f"$\\lambda=(r+s+t,r)={tuple_str(LAM2)}$", "，這裡 ",
                 f"$r={R},\\ s={S_},\\ t={T_}$", font_size=26, color=MUTED_COLOR).move_to(2.15 * DOWN)
    assert_in_frame(stmt, d1, d2, *br_r, br1, br2, c1, c2, arrow, alab, note)
    assert_apart(stmt, VGroup(br_r[0], br1, br_r[1], br2), gap=0.2)
    assert_apart(VGroup(d1, br_r[0], br1, c1), VGroup(d2, br_r[1], br2, c2, alab), gap=0.3)
    assert_apart(VGroup(c1, c2), note, gap=0.3)

    scene.say("Proposition 2：形狀 ", "$\\lambda$", "、內容 ", "$\\mu$", " 的表有 ", "$K_{\\lambda\\mu}$",
              " 張，這個數與 ", "$\\mu$", " 的順序無關")
    scene.play(FadeIn(stmt), run_time=0.6)
    scene.wait(1.0)
    scene.say("先看只有 1、2 兩種數：第 2 列只能全是 2，它頭上的 ", "$r$", " 格只能是 1")
    scene.play(FadeIn(d1), run_time=0.7)
    scene.play(FadeIn(br_r[0]), run_time=0.5)
    scene.wait(1.0)
    scene.say("第 1 列其餘是 ", "$s$", " 個 1 接 ", "$t$", " 個 2：這樣的表恰好一張")
    scene.play(FadeIn(br1), FadeIn(c1), run_time=0.6)
    scene.wait(1.2)
    scene.say("把 ", "$s$", "、", "$t$", " 對調：內容 ", "$(5,3)$", " 的表與內容 ", "$(3,5)$", " 的表一對一")
    scene.play(GrowArrow(arrow), FadeIn(alab), run_time=0.5)
    scene.play(TransformFromCopy(d1, d2), run_time=0.9)
    scene.play(FadeIn(br_r[1]), FadeIn(br2), FadeIn(c2), FadeIn(note, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)


def part_general(scene):
    box = Rectangle(width=2.4, height=3.0).set_stroke(WHITE, 2.5).move_to(np.array([-4.3, 0.25, 0.0]))
    l, r, top = box.get_left()[0], box.get_right()[0], box.get_top()[1]
    y1, y2 = top - 1.1, top - 1.9
    seps = VGroup(*[Line(np.array([l, y, 0.0]), np.array([r, y, 0.0]), stroke_width=2.5) for y in (y1, y2)])
    band = Rectangle(width=2.4, height=y1 - y2).set_fill(YELLOW, opacity=0.2).set_stroke(width=0)
    band.move_to(np.array([box.get_x(), (y1 + y2) / 2, 0.0]))
    names = VGroup(*[Tex(n, font_size=40).move_to(np.array([box.get_x(), y, 0.0]))
                     for n, y in (("B", (top + y1) / 2), ("C", (y1 + y2) / 2), ("D", (y2 + box.get_bottom()[1]) / 2))])
    rows = VGroup(*[Tex(n, font_size=28, fill_color=YELLOW).move_to(np.array([l - 0.45, y, 0.0]))
                    for n, y in (("k", y1 - 0.2), ("k+1", y2 + 0.2))])
    a_lab = Tex("A", font_size=40).next_to(box, UP, buff=0.2)
    eq1 = Tex(r"P(A)=P(B)\cdot P(C)\cdot P(D)", font_size=38).move_to(np.array([2.2, 1.7, 0.0]))
    eq2 = mixed("$C$", " 換成兩列的和對調的 ", "$C'$", "，而 ", "$P(C')=P(C)$", font_size=26)
    eq2.move_to(np.array([2.2, 0.8, 0.0]))
    eq3 = Tex("=".join(f"K_{{{tuple_str(K_LAM)},{tuple_str(mu)}}}" for mu in K_MUS) + f"={kostka(K_LAM, K_MUS[0])}",
              font_size=34).move_to(np.array([2.2, -0.35, 0.0]))
    concl = mixed("所以 Schur 多項式 ", "$s_{\\lambda}(x_1,\\ldots,x_m)$", " 是對稱多項式", font_size=28,
                  color=OK_COLOR).move_to(2.25 * DOWN)
    left = VGroup(box, rows, a_lab)
    assert_in_frame(left, eq1, eq2, eq3, concl)
    for m in (eq1, eq2, eq3):
        assert_apart(left, m, gap=0.4)
    assert_apart(eq1, eq2, gap=0.2)
    assert_apart(eq2, eq3, gap=0.2)
    assert_apart(VGroup(left, eq3), concl, gap=0.2)

    scene.say("一般情形用 R-S-K：固定 ", "$P$", "，內容為 ", "$\\mu$", " 的 ", "$Q$", " ⟷ 列和為 ", "$\\mu$",
              " 的矩陣 ", "$A$")
    scene.play(ShowCreation(box), ShowCreation(seps), FadeIn(names), FadeIn(a_lab), run_time=0.8)
    scene.wait(0.8)
    scene.say("要對調 ", "$\\mu_k$", "、", "$\\mu_{k+1}$", "：只動中間兩列 ", "$C$", "，", "$P$", " 不變")
    scene.play(FadeIn(band), FadeIn(rows), run_time=0.4)
    scene.play(Write(eq1), run_time=0.8)
    scene.play(FadeIn(eq2, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.4)
    scene.say("所以 ", "$K_{\\lambda\\mu}$", " 不管 ", "$\\mu$", " 怎麼排都一樣，例如：")
    scene.play(FadeIn(eq3, shift=0.1 * UP), run_time=0.7)
    scene.wait(1.0)
    scene.say("$s_\\lambda$", " 裡每個單項式的係數都是 Kostka 數：Schur 多項式是對稱的")
    scene.play(FadeIn(concl, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)


# =============================================================================
# 第 2 段：Cauchy–Littlewood 恆等式
# =============================================================================
def part_cauchy(scene):
    top = VGroup(Tex("(3)", font_size=36, fill_color=MUTED_COLOR),
                 Tex(r"\prod_{i,j}\frac{1}{1-x_i y_j}=\sum_{\lambda}s_{\lambda}(x_1,\ldots,x_n)\,"
                     r"s_{\lambda}(y_1,\ldots,y_m)", font_size=40)).arrange(RIGHT, buff=0.4).move_to(2.35 * UP)
    a_item = VGroup(Tex("A=", font_size=40), mini_matrix(CH4_MATRIX, font_size=36, dx=0.6, dy=0.55))
    a_item.arrange(RIGHT, buff=0.15).move_to(np.array([-5.1, -0.1, 0.0]))
    xs, ys = content(CH4_P), content(CH4_Q)
    xP = "".join(f"x_{j}^{{{e}}}" for j, e in enumerate(xs, 1))
    yQ = "".join(f"y_{i}^{{{e}}}" for i, e in enumerate(ys, 1))
    mono = Tex(r"\prod_{i,j}(x_j y_i)^{a(i,j)}=" + xP + r"\," + yQ, font_size=38).move_to(np.array([1.0, 0.75, 0.0]))
    pq = VGroup(labeled("P=", tableau_mob(CH4_P, 0.4), font_size=34, buff=0.15),
                labeled("Q=", tableau_mob(CH4_Q, 0.4), font_size=34, buff=0.15)).arrange(RIGHT, buff=0.7)
    pq.move_to(np.array([1.0, -0.7, 0.0]))
    cts = VGroup(Tex(r"x^{P}=" + xP, font_size=32, fill_color=TEAL).next_to(pq[0], DOWN, buff=0.3),
                 Tex(r"y^{Q}=" + yQ, font_size=32, fill_color=GOLD).next_to(pq[1], DOWN, buff=0.3))
    assert_in_frame(top, a_item, mono, pq, cts)
    assert_apart(top, VGroup(a_item, mono), gap=0.3)
    assert_apart(a_item, VGroup(mono, pq, cts), gap=0.4)
    assert_apart(mono, pq, gap=0.3)
    assert_apart(cts[0], cts[1], gap=0.3)

    scene.say("Cauchy–Littlewood 恆等式：左邊展開後，每一項對應一個非負整數矩陣 ", "$A$")
    scene.play(FadeIn(top, shift=0.1 * DOWN), run_time=1.0)
    scene.wait(1.0)
    scene.say("$A$", " 給出的項是 ", "$\\prod(x_jy_i)^{a(i,j)}$", "；若 ", "$A\\leftrightarrow(P,Q)$",
              "，它恰好是 ", "$x^Py^Q$")
    scene.play(FadeIn(a_item), run_time=0.6)
    scene.play(FadeIn(mono, shift=0.1 * RIGHT), run_time=0.8)
    scene.play(FadeIn(pq), run_time=0.7)
    scene.play(FadeIn(cts, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.6)
    scene.say("右邊是所有同形狀 ", "$(P,Q)$", " 的 ", "$x^Py^Q$", " 之和：R-S-K 讓兩邊一項一項相等")
    scene.wait(1.8)


def part_count20(scene):
    head = mixed("驗算：", "$2\\times 2$", "、元素和為 3 的矩陣共 ", f"$\\binom{{6}}{{3}}={len(MATS)}$", " 個",
                 font_size=28).move_to(2.65 * UP)
    shapes = [shape(rsk_matrix(M)[0]) for M in MATS]
    items = VGroup(*[mini_matrix(M, font_size=28, dx=0.42, dy=0.36, color=SHAPE_COLORS[sh])
                     for M, sh in zip(MATS, shapes)])
    items.arrange_in_grid(n_rows=4, n_cols=5, h_buff=0.5, v_buff=0.22).move_to(np.array([-2.7, -0.3, 0.0]))
    tally = VGroup()
    for lam in partitions(3):
        d, n = d_count(lam, 2), shapes.count(lam)
        assert n == d ** 2
        tally.add(mixed(f"$\\lambda={tuple_str(lam)}$", "：", f"$d_\\lambda(2)^2={d}^2={n}$", font_size=26,
                        color=SHAPE_COLORS[lam]))
    total = "+".join(str(d_count(lam, 2) ** 2) for lam in partitions(3))
    tally.add(Tex(total + f"={len(MATS)}", font_size=40, fill_color=OK_COLOR))
    tally.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(np.array([3.9, 0.0, 0.0]))
    assert_in_frame(head, items, tally)
    assert_apart(head, items, gap=0.25)
    assert_apart(items, tally, gap=0.4)

    scene.say("小驗算：", "$2\\times 2$", "、元素和為 3 的矩陣共 20 個；依 R-S-K 得到的形狀上色")
    scene.play(FadeIn(head), run_time=0.5)
    scene.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in items], lag_ratio=0.06), run_time=1.4)
    scene.wait(0.8)
    scene.say("形狀 ", "$(3)$", " 的有 ", "$4^2$", " 個、", "$(2,1)$", " 的有 ", "$2^2$", " 個：",
              "$20=\\sum_\\lambda d_\\lambda(2)^2$")
    scene.play(LaggedStart(*[FadeIn(t, shift=0.1 * LEFT) for t in tally], lag_ratio=0.3), run_time=1.2)
    scene.wait(2.0)


# =============================================================================
# 第 3 段：(4)(5)(6)
# =============================================================================
def part_identities(scene):
    lams = partitions(3)
    xs = [-4.2, -2.75, -1.3]
    diags = VGroup(*[YoungDiagramMob(lam, cell_size=0.4).move_to(np.array([x, 0.0, 0.0])).align_to(2.5 * UP, UP)
                     for lam, x in zip(lams, xs)])
    rows_y = (0.75, 0.05)
    vals = VGroup(*[Tex(str(v), font_size=36).move_to(np.array([x, y, 0.0]))
                    for y, fn in zip(rows_y, (f_count, lambda lam: d_count(lam, 2))) for lam, x in zip(lams, xs)
                    for v in [fn(lam)]])
    heads = VGroup(*[Tex(t, font_size=34, fill_color=MUTED_COLOR).move_to(np.array([-5.9, y, 0.0]))
                     for t, y in ((r"\lambda", 1.9), (r"f^{\lambda}", rows_y[0]), (r"d_{\lambda}(2)", rows_y[1]))])
    f3, d3 = [f_count(lam) for lam in lams], [d_count(lam, 2) for lam in lams]
    f4 = [f_count(lam) for lam in partitions(4)]
    ids = VGroup(
        VGroup(Tex(r"(4)\quad n!=\sum_{\lambda\vdash n}(f^{\lambda})^2", font_size=32),
               Tex(r"3!=" + "+".join(f"{f}^2" for f in f3) + f"={sum(f * f for f in f3)}", font_size=32,
                   fill_color=GOLD)),
        VGroup(Tex(r"(5)\quad m^n=\sum_{\lambda\vdash n}d_{\lambda}(m)\,f^{\lambda}", font_size=32),
               Tex(r"2^3=" + "+".join(f"{d}\\cdot {f}" for d, f in zip(d3, f3)) + f"={sum(d * f for d, f in zip(d3, f3))}",
                   font_size=32, fill_color=GOLD)),
        VGroup(Tex(r"(6)\quad\sum_{\lambda\vdash n}f^{\lambda}=\#\{w\in S_n:w=w^{-1}\}", font_size=32),
               Tex(r"n=4:\ " + "+".join(map(str, f4)) + f"={count_involutions(4)}", font_size=32, fill_color=GOLD)),
    )
    for g in ids:
        g.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    ids.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(np.array([3.2, 0.5, 0.0]))
    table = VGroup(diags, vals, heads)
    assert sum(f * f for f in f3) == factorial(3) and sum(d * f for d, f in zip(d3, f3)) == 2 ** 3
    assert sum(f4) == count_involutions(4)
    assert_in_frame(table, ids)
    assert_apart(table, ids, gap=0.4)
    assert_apart(diags, vals, gap=0.15)

    scene.say("R-S-K 也給出計數恆等式：", "$f^\\lambda$", " ＝ 標準表個數，", "$d_\\lambda(m)$", " ＝ 數字在 ",
              "$[m]$", " 的表的個數")
    scene.play(FadeIn(heads), LaggedStart(*[FadeIn(d) for d in diags], lag_ratio=0.2), run_time=0.9)
    scene.play(FadeIn(vals), run_time=0.6)
    scene.wait(1.2)
    scene.say("(4) 排列 ⟷ 同形狀的一對標準表")
    scene.play(FadeIn(ids[0], shift=0.1 * LEFT), run_time=0.8)
    scene.wait(1.4)
    scene.say("(5) 長 ", "$n$", "、字母在 ", "$[m]$", " 的字 ⟷ ", "$(P,Q)$", "，其中 ", "$Q$", " 是標準表")
    scene.play(FadeIn(ids[1], shift=0.1 * LEFT), run_time=0.8)
    scene.wait(1.6)
    scene.say("(6) 對合 ⟷ 標準表（由對稱定理）：", "$S_4$", " 有 10 個對合")
    scene.play(FadeIn(ids[2], shift=0.1 * LEFT), run_time=0.8)
    scene.wait(1.6)


# =============================================================================
# 第 4 段：鉤長公式回顧、Stanley 鉤–內容公式
# =============================================================================
def part_hooks(scene):
    H, NUM = hooks(HOOK), numerators(HOOK, M5)
    left = YoungDiagramMob(HOOK, cell_size=0.5, entries=H, font_size=26, center=np.array([-3.4, 0.85, 0.0]))
    right = YoungDiagramMob(HOOK, cell_size=0.5, entries=NUM, font_size=26, center=np.array([3.3, 0.85, 0.0]))
    lt = mixed("鉤長 ", "$h(i,j)$", font_size=26).next_to(left, UP, buff=0.3)
    rt = mixed("$m+j-i$", "（", "$m=5$", "，對角線是 ", "$m$", "）", font_size=26).next_to(right, UP, buff=0.3)
    diag = VGroup(*[right.cell(i, i).copy().set_fill(GOLD, opacity=0.35).set_stroke(width=0)
                    for i in range(len(HOOK)) if i < HOOK[i]])
    hp, num = prod(prod(r) for r in H), prod(prod(r) for r in NUM)
    f_eq = Tex(rf"f^{{\lambda}}=\frac{{{sum(HOOK)}!}}{{\prod h(i,j)}}={big(factorial(sum(HOOK)) // hp)}", font_size=36)
    d_eq = Tex(rf"d_{{\lambda}}({M5})=\prod\frac{{{M5}+j-i}}{{h(i,j)}}={big(num // hp)}", font_size=36)
    f_eq.next_to(left, DOWN, buff=0.45)
    d_eq.next_to(right, DOWN, buff=0.45)
    note = mixed("直接列舉：", "$\\lambda=(6,5,5,3)$", " 形、數字在 ", "$[5]$", f" 的表也是 {len(ssyt(HOOK, M5))} 張",
                 font_size=24, color=MUTED_COLOR).move_to(2.3 * DOWN)
    assert num // hp == hook_content_count(HOOK, M5) and factorial(sum(HOOK)) // hp == syt_count(HOOK)
    assert_in_frame(left, right, lt, rt, f_eq, d_eq, note)
    assert_apart(VGroup(left, lt, f_eq), VGroup(right, rt, d_eq), gap=0.4)
    assert_apart(VGroup(f_eq, d_eq), note, gap=0.3)

    scene.say("回顧鉤長公式：", "$\\lambda=(6,5,5,3)$", " 的標準表有 ", "$19!/\\prod h(i,j)$", " 張")
    scene.play(FadeIn(left), FadeIn(lt), run_time=0.8)
    scene.play(FadeIn(f_eq, shift=0.1 * UP), run_time=0.8)
    scene.wait(1.4)
    scene.say("Stanley 的鉤–內容公式：對角線寫 ", "$m$", "，往右一格加 1、往下一格減 1")
    scene.play(FadeIn(right), FadeIn(rt), run_time=0.8)
    scene.play(FadeIn(diag), run_time=0.5)
    scene.wait(1.2)
    scene.say("這些數的乘積除以鉤長的乘積，就是數字在 ", "$[m]$", " 的表的個數 ", "$d_\\lambda(m)$")
    scene.play(FadeIn(d_eq, shift=0.1 * UP), run_time=0.8)
    scene.wait(1.4)
    scene.say("用電腦直接列舉也是 3360 張；這個公式書上留到第 6 章證明")
    scene.play(FadeIn(note, shift=0.1 * UP), run_time=0.5)
    scene.wait(1.6)


def part_ex12(scene):
    perms = ex12_perms(4, 2, 2)
    lam = (2, 2)
    stmt = mixed("Exercise 12：最長遞增長 ", "$\\ell$", "、最長遞減長 ", "$k$", " 的排列個數 ＝ ",
                 "$\\sum(f^{\\lambda})^2$", font_size=28)
    sub = mixed("（", "$\\lambda$", " 恰有 ", "$k$", " 列、", "$\\ell$", " 行）", font_size=24, color=MUTED_COLOR)
    VGroup(stmt, sub).arrange(DOWN, buff=0.3).move_to(2.1 * UP)
    d = YoungDiagramMob(lam, cell_size=0.6).move_to(np.array([-4.0, -0.3, 0.0]))
    d_lab = Tex(r"\lambda=" + tuple_str(lam), font_size=34).next_to(d, DOWN, buff=0.3)
    words = Tex(r"\quad ".join("".join(map(str, w)) for w in perms), font_size=42).move_to(np.array([1.4, 0.1, 0.0]))
    cnt = Tex(rf"(f^{{{tuple_str(lam)}}})^2={f_count(lam)}^2={len(perms)}", font_size=38, fill_color=OK_COLOR)
    cnt.next_to(words, DOWN, buff=0.45)
    assert len(perms) == f_count(lam) ** 2
    assert_in_frame(stmt, sub, d, d_lab, words, cnt)
    assert_apart(VGroup(stmt, sub), VGroup(d, words), gap=0.4)
    assert_apart(VGroup(d, d_lab), VGroup(words, cnt), gap=0.5)

    scene.say("Exercise 12：最長遞增長＝", "$P$", " 的第一列長，最長遞減長＝列數，所以個數是 ", "$\\sum(f^\\lambda)^2$")
    scene.play(FadeIn(stmt), FadeIn(sub), run_time=0.8)
    scene.wait(1.2)
    scene.say("例：", "$S_4$", " 裡兩者都是 2 的排列，形狀只能是 ", "$(2,2)$", "：共 ", "$2^2=4$", " 個")
    scene.play(FadeIn(d), FadeIn(d_lab), FadeIn(words, shift=0.1 * UP), run_time=0.8)
    scene.play(FadeIn(cnt, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.0)


class SceneF19RSKApplications(ChuScene):
    def construct(self):
        self.show_header("R-S-K 的應用")
        check_math()
        part_two_letters(self)
        self.clear_stage()
        part_general(self)
        self.clear_stage()
        part_cauchy(self)
        self.clear_stage()
        part_count20(self)
        self.clear_stage()
        part_identities(self)
        self.clear_stage()
        part_hooks(self)
        self.clear_stage()
        part_ex12(self)
        self.wait(1.0)
