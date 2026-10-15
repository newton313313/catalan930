"""
Scene F51 —— 吃多項式的機器：上同調環與差商（Fulton §10.2 命題 3、§10.3，書 p.161–170）
執行（在 codes/ 內）：manimgl scenes/sceneF51_divided_differences.py SceneF51DividedDifferences
"""
import sys
from collections import Counter
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.schubert import (act_right, divided_difference, length, perms, poly_str, schubert_poly,
                            staircase_monomials, swap_vars)
from utils.schubert_draw import poly_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import elementary_e, poly_mul, poly_sum

SLOW = 3.6
X1 = {(1, 0, 0): 1}
TOP = {(2, 1, 0): 1}
MACHINE = [({(2, 0, 0): 1}, {(1, 0, 0): 1, (0, 1, 0): 1}),
           ({(1, 1, 0): 1}, {}),
           ({(0, 1, 0): 1}, {(0, 0, 0): -1}),
           ({(3, 0, 0): 1}, {(2, 0, 0): 1, (1, 1, 0): 1, (0, 2, 0): 1})]
DIFF = {(1, 0, 0): 1, (0, 1, 0): -1}                    # x_1 − x_2
ACCENT = YELLOW
GOOD = "#7CE38B"


def neg(f):
    return {e: -c for e, c in f.items()}


def run(f, steps):
    out = [f]
    for i in steps:
        out.append(divided_difference(out[-1], i))
    return out


def fit(m, w):
    if m.get_width() > w:
        m.set_width(w)
    return m


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def check_math():
    st = staircase_monomials(3)
    assert len(st) == 6 and all(e[0] <= 2 and e[1] <= 1 and e[2] == 0 for e in st)
    by_deg = Counter(sum(e) for e in st)
    assert [by_deg[k] for k in range(4)] == [1, 2, 2, 1]
    cells = Counter(length(w) for w in perms(3))
    assert [cells[k] for k in range(4)] == [1, 2, 2, 1]
    assert sorted(length(w) for w in perms(3)) == [0, 1, 1, 2, 2, 3]
    e1, e2, e3 = (elementary_e(k, 3) for k in (1, 2, 3))
    assert [poly_str(e) for e in (e1, e2, e3)] == ["x_1+x_2+x_3", "x_1x_2+x_1x_3+x_2x_3", "x_1x_2x_3"]
    assert poly_sum([poly_mul({(2, 0, 0): 1}, e1), neg(poly_mul(X1, e2)), e3]) == {(3, 0, 0): 1}   # x1^3 ∈ (e)
    f = {(2, 0, 0): 1}                                          # 開場的小例子
    assert swap_vars(f, 1) == {(0, 2, 0): 1}
    assert poly_mul(DIFF, MACHINE[0][1]) == poly_sum([f, neg(swap_vars(f, 1))])
    for f, g in MACHINE:
        assert divided_difference(f, 1) == g
        assert poly_mul(DIFF, g) == poly_sum([f, neg(swap_vars(f, 1))])          # 真的整除
        assert divided_difference(g, 1) == {}                                     # ∂² = 0
        num = poly_sum([f, neg(swap_vars(f, 1))])
        assert swap_vars(num, 1) == neg(num)                                      # 分子反對稱
    assert [poly_str(g) for _, g in MACHINE] == ["x_1+x_2", "0", "-1", "x_1^{2}+x_1x_2+x_2^{2}"]
    p121, p212 = run(TOP, [1, 2, 1]), run(TOP, [2, 1, 2])
    assert [poly_str(g) for g in p121] == ["x_1^{2}x_2", "x_1x_2", "x_1", "1"]
    assert [poly_str(g) for g in p212] == ["x_1^{2}x_2", "x_1^{2}", "x_1+x_2", "1"]
    for e in product(range(4), repeat=3):                                         # 辮關係、Leibniz：每個單項式都驗
        m = {e: 1}
        assert run(m, [1, 2, 1])[-1] == run(m, [2, 1, 2])[-1]
        for g in ({(1, 0, 0): 1}, {(0, 2, 1): 1}, {(1, 1, 0): 1, (0, 0, 2): -3}):
            lhs = divided_difference(poly_mul(m, g), 1)
            rhs = poly_sum([poly_mul(divided_difference(m, 1), g), poly_mul(swap_vars(m, 1), divided_difference(g, 1))])
            assert lhs == rhs
    assert divided_difference(X1, 1) == {(0, 0, 0): 1} and swap_vars(X1, 1) == {(0, 1, 0): 1}
    assert divided_difference({(2, 0, 0): 1}, 1) == poly_sum([X1, {(0, 1, 0): 1}])     # Leibniz 的驗算 = x1+x2
    for w in perms(3):                                                             # 命題 4
        for i in (1, 2):
            dd = divided_difference(schubert_poly(w), i)
            assert dd == (schubert_poly(act_right(w, i)) if w[i - 1] > w[i] else {})
    assert act_right((3, 2, 1), 1) == (2, 3, 1) and act_right((3, 2, 1), 2) == (3, 1, 2)
    assert schubert_poly((2, 3, 1)) == {(1, 1, 0): 1}


# ---------------------------------------------------------------- 1. 問題
def part_question(scene):
    big = tex(r"\partial_i f=\frac{f-s_if}{x_i-x_{i+1}}", 64).move_to(np.array([0, 1.75, 0]))
    note = mixed("$s_if$", "：把 ", "$x_i$", " 和 ", "$x_{i+1}$", " 對調", font_size=26, color=MUTED_COLOR)
    note.next_to(big, DOWN, buff=0.35)
    lines = VGroup(
        tex(r"f=x_1^{2},\qquad s_1f=x_2^{2}", 40),
        tex(r"f-s_1f=x_1^{2}-x_2^{2}=(x_1-x_2)(x_1+x_2)", 40),
        tex(r"\partial_1f=x_1+x_2", 44, ACCENT),
    ).arrange(DOWN, buff=0.4).move_to(np.array([0, -1.25, 0]))
    assert_in_frame(big, note, lines)
    assert_apart(note, lines, 0.2)

    scene.say("問：把兩個變數對調、相減、再除以它們的差", wait=SLOW * 0.4)
    scene.play(Write(big), run_time=1.6)
    scene.play(FadeIn(note, shift=0.2 * UP), run_time=0.6)
    scene.say("一定除得盡嗎？除出來的又是什麼？", wait=SLOW * 0.7)
    scene.say("先試一個：", "$f=x_1^2$", "，對調 ", "$x_1,x_2$", " 得 ", "$x_2^2$", wait=SLOW * 0.2)
    scene.play(FadeIn(lines[0], shift=0.2 * UP), run_time=0.8)
    scene.wait(SLOW * 0.5)
    scene.say("相減以後剛好有 ", "$x_1-x_2$", " 這個因式", wait=SLOW * 0.2)
    scene.play(FadeIn(lines[1], shift=0.2 * UP), run_time=0.8)
    scene.wait(SLOW * 0.6)
    scene.play(Write(lines[2]), run_time=1.0)
    scene.say("這就是差商 ", r"$\partial_1$", "：吃進一個多項式，吐出一個次數少 1 的", wait=SLOW * 0.9)
    scene.say("它從哪裡來？先看它住的地方：旗流形的上同調環", wait=SLOW * 0.6)


# ---------------------------------------------------------------- 2. 命題 3
def part_ring(scene):
    ring = tex(r"H^*(Fl(3))=\mathbb Z[x_1,x_2,x_3]/(e_1,e_2,e_3)", 42).move_to(np.array([0, 2.6, 0]))
    es = VGroup(tex(r"e_1=x_1+x_2+x_3", 34), tex(r"e_2=x_1x_2+x_1x_3+x_2x_3", 34), tex(r"e_3=x_1x_2x_3", 34))
    es.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(np.array([-3.5, 1.0, 0]))
    kill = fit(tex(r"x_1^{3}=x_1^{2}e_1-x_1e_2+e_3=0", 36, ACCENT), 6.0).move_to(np.array([-3.5, -0.75, 0]))
    elim = fit(tex(r"x_3=e_1-x_1-x_2=-x_1-x_2", 34), 6.0).move_to(np.array([-3.5, -1.6, 0]))
    cols = [["1"], ["x_1", "x_2"], ["x_1^{2}", "x_1x_2"], ["x_1^{2}x_2"]]
    xs = [1.15, 2.55, 4.0, 5.6]
    heads = VGroup(*[zh("次數 %d" % k, font_size=22, color=MUTED_COLOR).move_to(np.array([x, 1.85, 0]))
                     for k, x in enumerate(xs)])
    monos = VGroup(*[VGroup(*[tex(s, 38).move_to(np.array([x, 1.1 - 0.7 * a, 0])) for a, s in enumerate(c)])
                     for c, x in zip(cols, xs)])
    rule = Line(np.array([0.4, -0.15, 0]), np.array([6.5, -0.15, 0])).set_stroke(GREY_C, 1.5)
    counts = VGroup(*[tex(str(len(c)), 40, ACCENT).move_to(np.array([x, -0.65, 0])) for c, x in zip(cols, xs)])
    f50 = fit(mixed("F50 的胞腔：", r"$\ell(w)=0,1,1,2,2,3$", font_size=24, color=MUTED_COLOR), 6.0)
    f50.move_to(np.array([3.45, -1.6, 0]))
    assert_in_frame(ring, es, kill, elim, heads, monos, counts, f50, rule)
    for m in (es, kill, elim):
        assert_apart(m, VGroup(heads, monos, counts, f50), 0.3)
    assert_apart(ring, heads, 0.15)

    scene.say("命題 3：旗流形的上同調，是一個多項式環的商", wait=SLOW * 0.2)
    scene.play(Write(ring), run_time=1.6)
    scene.wait(SLOW * 0.5)
    scene.say("除掉的是基本對稱多項式 ", "$e_1,e_2,e_3$", wait=SLOW * 0.2)
    scene.play(LaggedStart(*[FadeIn(e, shift=0.2 * RIGHT) for e in es], lag_ratio=0.3), run_time=1.4)
    scene.say("所以每個（非常數的）對稱多項式在這裡都等於 0", wait=SLOW * 0.7)
    scene.play(FadeIn(kill, shift=0.2 * UP), run_time=0.8)
    scene.say("例如 ", "$x_1^3=0$", "：", "$x_1$", " 的次方最多到 2", wait=SLOW * 0.7)
    scene.play(FadeIn(elim, shift=0.2 * UP), run_time=0.8)
    scene.say("$x_3$", " 也能用 ", "$x_1,x_2$", " 換掉；同理 ", "$x_2$", " 最多一次", wait=SLOW * 0.7)
    scene.say("剩下的基底：", "$x_1^{i_1}x_2^{i_2}$", "，", r"$i_1\le 2,\ i_2\le 1$", "，共 6 個", wait=SLOW * 0.2)
    scene.play(FadeIn(heads), run_time=0.5)
    for c in monos:
        scene.play(LaggedStart(*[FadeIn(t, shift=0.2 * DOWN) for t in c], lag_ratio=0.3), run_time=0.7)
    scene.wait(SLOW * 0.3)
    scene.play(ShowCreation(rule), LaggedStart(*[FadeIn(c) for c in counts], lag_ratio=0.2), run_time=1.0)
    scene.say("按次數數：1, 2, 2, 1", wait=SLOW * 0.5)
    scene.play(FadeIn(f50, shift=0.2 * UP), run_time=0.7)
    scene.say("和 F50 按星號數胞腔的結果一模一樣：6 個胞腔，6 個基底", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 3. 差商機器
def part_machine(scene):
    formula = fit(tex(r"\partial_1 f=\frac{f-s_1f}{x_1-x_2}", 40), 5.0).move_to(np.array([-3.6, 2.3, 0]))
    anti = fit(tex(r"s_1(f-s_1f)=-(f-s_1f)", 34, MUTED_COLOR), 5.4).move_to(np.array([3.3, 2.3, 0]))
    box_c = np.array([0, 0.55, 0])
    rect = RoundedRectangle(width=2.4, height=1.4, corner_radius=0.2).set_stroke(TEAL_B, 3).move_to(box_c)
    lab = tex(r"\partial_1", 64, TEAL_B).move_to(box_c)
    arrows = VGroup(Arrow(np.array([-3.1, 0.55, 0]), np.array([-1.25, 0.55, 0]), buff=0),
                    Arrow(np.array([1.25, 0.55, 0]), np.array([3.0, 0.55, 0]), buff=0)).set_color(GREY_B)
    in_pos, out_pos = np.array([-4.4, 0.55, 0]), np.array([3.2, 0.55, 0])
    log_pos = [np.array([-6.2, -1.15, 0]), np.array([-6.2, -2.1, 0]), np.array([0.9, -1.15, 0]), np.array([0.9, -2.1, 0])]
    rows = [tex(poly_str(f) + r"\ \mapsto\ " + poly_str(g), 34).move_to(p, aligned_edge=LEFT)
            for (f, g), p in zip(MACHINE, log_pos)]
    eaten = zh("對稱的被吃掉", font_size=24, color=ACCENT).next_to(rows[1], RIGHT, buff=0.35)
    assert_in_frame(formula, anti, rect, arrows, *rows, eaten)
    assert_apart(eaten, rows[3], 0.3)
    assert_apart(formula, anti, 0.3)

    scene.say("把 ", r"$\partial_1$", " 做成一台機器，先確定它一定除得盡", wait=SLOW * 0.2)
    scene.play(FadeIn(formula), run_time=0.8)
    scene.play(FadeIn(anti), run_time=0.8)
    scene.say("分子對調 ", "$x_1,x_2$", " 會變號：它是反對稱的", wait=SLOW * 0.7)
    scene.say("反對稱多項式在 ", "$x_1=x_2$", " 時等於 0，所以被 ", "$x_1-x_2$", " 整除", wait=SLOW * 0.8)
    scene.play(ShowCreation(rect), FadeIn(lab), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.0)
    says =[("$x_1^2$", " 進去，", "$x_1+x_2$", " 出來（開場那一題）"),
            ("$x_1x_2$", " 對調後不變，分子是 0：對稱的被吃掉"),
            ("$x_2$", " 進去，", "$(x_2-x_1)/(x_1-x_2)=-1$"),
            ("$x_1^3$", " 進去：", "$(x_1^3-x_2^3)/(x_1-x_2)$", "，三項")]
    for k, ((f, g), row) in enumerate(zip(MACHINE, rows)):
        inp = poly_tex(f, font_size=46).move_to(in_pos)
        out = poly_tex(g, font_size=46).move_to(out_pos, aligned_edge=LEFT)
        scene.play(FadeIn(inp, shift=0.3 * RIGHT), run_time=0.5)
        scene.play(inp.animate.move_to(box_c).scale(0.2).set_opacity(0), run_time=0.7)
        scene.remove(inp)
        scene.play(Indicate(lab, scale_factor=1.15), run_time=0.5)
        scene.play(FadeIn(out, shift=0.4 * RIGHT), run_time=0.6)
        scene.say(*says[k], wait=SLOW * 0.5)
        anims = [FadeOut(out), FadeIn(row, shift=0.2 * DOWN)]
        if k == 1:
            anims.append(FadeIn(eaten))
        scene.play(*anims, run_time=0.6)
    scene.say("每次都除得盡，次數少 1；對稱的部分一進去就變成 0", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 4. 規則
def part_rules(scene):
    fs = 34
    tag_x, fx = -6.6, -4.7
    rows = [
        ("平方是零", [(r"\partial_i^2=0", 2.45),
                      (r"x_1^{3}\xrightarrow{\partial_1}x_1^{2}+x_1x_2+x_2^{2}\xrightarrow{\partial_1}0", 1.7)]),
        ("辮關係", [(r"\partial_1\partial_2\partial_1=\partial_2\partial_1\partial_2", 0.75),
                    (r"x_1^{2}x_2\xrightarrow{\partial_1}x_1x_2\xrightarrow{\partial_2}x_1\xrightarrow{\partial_1}1", 0.0),
                    (r"x_1^{2}x_2\xrightarrow{\partial_2}x_1^{2}\xrightarrow{\partial_1}x_1+x_2\xrightarrow{\partial_2}1", -0.75)]),
        ("Leibniz", [(r"\partial_i(fg)=\partial_if\cdot g+s_if\cdot\partial_ig", -1.7),
                     (r"\partial_1(x_1\cdot x_1)=1\cdot x_1+x_2\cdot 1=x_1+x_2", -2.45)]),
    ]
    groups = []
    for name, lines in rows:
        tag = zh(name, font_size=24, color=MUTED_COLOR).move_to(np.array([tag_x, lines[0][1], 0]), aligned_edge=LEFT)
        ts = [fit(tex(s, fs, ACCENT if k == 0 else WHITE), 10.8).move_to(np.array([fx, y, 0]), aligned_edge=LEFT)
              for k, (s, y) in enumerate(lines)]
        groups.append((tag, ts))
    allm = [m for tag, ts in groups for m in [tag, *ts]]
    assert_in_frame(*allm)
    for tag, ts in groups:
        assert_apart(tag, ts[0], 0.2)

    tag, ts = groups[0]
    scene.say("這台機器有三條規則。第一條：連做兩次就變 0", wait=SLOW * 0.2)
    scene.play(FadeIn(tag), Write(ts[0]), run_time=0.9)
    scene.play(FadeIn(ts[1], shift=0.2 * RIGHT), run_time=0.9)
    scene.say(r"$\partial_i f$", " 對 ", "$x_i,x_{i+1}$", " 已經對稱，再吃一次只剩 0", wait=SLOW * 0.9)
    tag, ts = groups[1]
    scene.say("第二條：辮關係，從 ", "$x_1^2x_2$", " 出發走兩條路", wait=SLOW * 0.2)
    scene.play(FadeIn(tag), Write(ts[0]), run_time=0.9)
    scene.play(FadeIn(ts[1], shift=0.2 * RIGHT), run_time=0.9)
    scene.wait(SLOW * 0.4)
    scene.play(FadeIn(ts[2], shift=0.2 * RIGHT), run_time=0.9)
    scene.say("先 ", r"$\partial_1$", " 或先 ", r"$\partial_2$", "，最後都到 1", wait=SLOW * 0.9)
    tag, ts = groups[2]
    scene.say("第三條：乘積的微分法則，右邊要先對調一下", wait=SLOW * 0.2)
    scene.play(FadeIn(tag), Write(ts[0]), run_time=0.9)
    scene.wait(SLOW * 0.4)
    scene.play(FadeIn(ts[1], shift=0.2 * RIGHT), run_time=0.9)
    scene.say("驗算：", "$x_1\\cdot x_1$", " 又得到 ", "$x_1+x_2$", "，和機器吐的一樣", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 5. 幾何
def part_geometry(scene):
    xs = [-5.5, -4.65, -3.8, -2.95, -2.1]
    fibers = VGroup(*[Ellipse(width=0.45, height=1.5).move_to(np.array([x, 0.85, 0])) for x in xs])
    fibers.set_stroke(GREY_B, 2)
    fibers[2].set_stroke(ACCENT, 3)
    base = Line(np.array([-6.0, -1.7, 0]), np.array([-1.6, -1.7, 0])).set_stroke(WHITE, 3)
    dots = VGroup(*[Dot(np.array([x, -1.7, 0]), radius=0.06) for x in xs])
    dots[2].set_color(ACCENT)
    fl = tex(r"Fl(3)", 38).move_to(np.array([-6.0, 2.15, 0]))
    p1 = tex(r"\mathbb P^1", 34, ACCENT).move_to(np.array([-3.8, 2.0, 0]))
    arr = Arrow(np.array([-1.1, 0.7, 0]), np.array([-1.1, -1.45, 0]), buff=0).set_color(GREY_B)
    pi = tex(r"\pi_i", 34).next_to(arr, RIGHT, buff=0.12)
    blab = mixed("少了 ", "$E_i$", " 的旗", font_size=24, color=MUTED_COLOR).move_to(np.array([-3.8, -2.3, 0]))
    pic = VGroup(fibers, base, dots, fl, p1, arr, pi, blab)
    prop = fit(tex(r"w(i)>w(i+1)\Rightarrow\partial_i\sigma_w=\sigma_{ws_i}", 38, ACCENT), 5.9)
    prop.move_to(np.array([3.6, 1.65, 0]))
    ex = fit(tex(r"\partial_1\sigma_{321}=\sigma_{231},\qquad\partial_2\sigma_{321}=\sigma_{312}", 34), 5.9)
    ex.move_to(np.array([3.6, 0.7, 0]))
    zero = fit(tex(r"w(i)<w(i+1)\Rightarrow\partial_i\sigma_w=0", 34), 5.9).move_to(np.array([3.6, -0.35, 0]))
    link = fit(tex(r"\partial_1(x_1x_2)=0\ \leftrightarrow\ \partial_1\sigma_{231}=0", 34, MUTED_COLOR), 5.9)
    link.move_to(np.array([3.6, -1.35, 0]))
    assert_in_frame(pic, prop, ex, zero, link)
    for m in (prop, ex, zero, link):
        assert_apart(pic, m, 0.3)

    scene.say("差商的幾何意義：旗流形上的一個 ", r"$\mathbb P^1$", " 叢", wait=SLOW * 0.2)
    scene.play(ShowCreation(base), FadeIn(dots), FadeIn(fl), run_time=1.0)
    scene.play(LaggedStart(*[ShowCreation(f) for f in fibers], lag_ratio=0.2), run_time=1.4)
    scene.play(GrowArrow(arr), FadeIn(pi), FadeIn(blab), run_time=0.8)
    scene.say("忘掉 ", "$E_i$", "：夾在 ", "$E_{i-1}\\subset E_{i+1}$", " 之間的 ", "$E_i$", " 跑遍一條 ", r"$\mathbb P^1$",
              wait=SLOW * 0.3)
    scene.play(FadeIn(p1, shift=0.2 * DOWN), Indicate(fibers[2]), run_time=1.0)
    scene.wait(SLOW * 0.5)
    scene.say(r"$\partial_i$", " ＝沿著這個 ", r"$\mathbb P^1$", " 叢先拉回再推出（Lemma 9）", wait=SLOW * 0.9)
    scene.say("推出時一條 ", r"$\mathbb P^1$", " 被積掉，所以次數少 1", wait=SLOW * 0.8)
    scene.say("命題 4：在下降的位置做 ", r"$\partial_i$", "，Schubert 類往下走一格", wait=SLOW * 0.2)
    scene.play(Write(prop), run_time=1.2)
    scene.wait(SLOW * 0.5)
    scene.play(FadeIn(ex, shift=0.2 * UP), run_time=0.8)
    scene.say("$w=321$", "：兩個位置都下降，", r"$\partial_1,\partial_2$", " 各降到一個長度 2 的類", wait=SLOW * 0.8)
    scene.play(FadeIn(zero, shift=0.2 * UP), run_time=0.8)
    scene.say("不是下降的位置，就整個吃掉", wait=SLOW * 0.5)
    scene.play(FadeIn(link, shift=0.2 * UP), run_time=0.8)
    scene.say("剛才被吃掉的 ", "$x_1x_2$", "，正是 ", r"$\sigma_{231}$", "，而 ", "$2<3$", wait=SLOW * 1.0)
    scene.say("一台機器，把 Schubert 類一個一個降下來", wait=SLOW * 1.2)


class SceneF51DividedDifferences(ChuScene):
    def construct(self):
        self.show_header("吃多項式的機器：上同調環與差商")
        check_math()
        part_question(self)
        self.clear_stage()
        part_ring(self)
        self.clear_stage()
        part_machine(self)
        self.clear_stage()
        part_rules(self)
        self.clear_stage()
        part_geometry(self)
        self.wait(1.0)
