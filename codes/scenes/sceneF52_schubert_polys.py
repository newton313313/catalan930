"""
Scene F52 —— 從最頂端流下來：Schubert 多項式（Fulton §10.4，書 p.170–173）
執行（在 codes/ 內）：manimgl scenes/sceneF52_schubert_polys.py SceneF52SchubertPolys
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.schubert import (act_right, bruhat_covers, descents, divided_difference, length, perm_str, perms,
                            poly_str, schubert_path, schubert_poly, w0)
from utils.scene_base import ChuScene
from utils.schubert_draw import HasseMob
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import elementary_e, poly_mul

SLOW = 4.2
ACCENT = YELLOW
OP = TEAL_B
LEVELS3 = [[(1, 2, 3)], [(2, 1, 3), (1, 3, 2)], [(2, 3, 1), (3, 1, 2)], [(3, 2, 1)]]
WEAK = [((3, 2, 1), (2, 3, 1), 1), ((3, 2, 1), (3, 1, 2), 2), ((2, 3, 1), (2, 1, 3), 2),
        ((3, 1, 2), (1, 3, 2), 1), ((2, 1, 3), (1, 2, 3), 1), ((1, 3, 2), (1, 2, 3), 2)]
STEPS = [1, 4, 3, 2, 3]
SI = [(2, 1, 3, 4), (1, 3, 2, 4), (1, 2, 4, 3)]
DEG2 = [(3, 1, 2, 4), (2, 3, 1, 4), (1, 4, 2, 3)]


def fit(m, w):
    if m.get_width() > w:
        m.set_width(w)
    return m


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def strip(f, k):
    """把 {指數: 係數} 的指數截成前 k 個變數（後面必須都是 0）。"""
    assert all(not any(e[k:]) for e in f)
    return {e[:k]: c for e, c in f.items()}


def S_tex(w):
    return r"\mathfrak S_{%s}=%s" % (perm_str(w), poly_str(schubert_poly(w)))


def check_math():
    assert schubert_poly(w0(2)) == {(1, 0): 1}
    assert schubert_poly(w0(3)) == {(2, 1, 0): 1} and schubert_poly(w0(4)) == {(3, 2, 1, 0): 1}
    expect = {(3, 2, 1): "x_1^{2}x_2", (2, 3, 1): "x_1x_2", (3, 1, 2): "x_1^{2}", (2, 1, 3): "x_1",
              (1, 3, 2): "x_1+x_2", (1, 2, 3): "1"}
    assert {w: poly_str(schubert_poly(w)) for w in perms(3)} == expect
    assert sorted(w for lv in LEVELS3 for w in lv) == sorted(perms(3))
    assert all(length(w) == k for k, lv in enumerate(LEVELS3) for w in lv)
    for up, lo, i in WEAK:
        assert act_right(up, i) == lo and up[i - 1] > up[i]
        assert divided_difference(schubert_poly(up), i) == schubert_poly(lo)
    covers = set(bruhat_covers(3))
    assert len(covers) == 8 and {(lo, up) for up, lo, _ in WEAK} <= covers
    assert covers - {(lo, up) for up, lo, _ in WEAK} == {((1, 3, 2), (2, 3, 1)), ((2, 1, 3), (3, 1, 2))}
    path = schubert_path(5, STEPS)
    assert [perm_str(w) for w, _ in path] == ["54321", "45321", "45312", "45132", "41532", "41352"]
    assert [len(f) for _, f in path] == [1, 1, 1, 2, 5, 3]
    assert poly_str(path[0][1]) == "x_1^{4}x_2^{3}x_3^{2}x_4" and poly_str(path[2][1]) == "x_1^{3}x_2^{3}x_3^{2}"
    last = poly_mul({(3, 0, 0, 0, 0): 1}, {(0,) + e + (0,): c for e, c in elementary_e(2, 3).items()})
    assert path[-1][1] == last                                       # x1^3 (x2x3 + x2x4 + x3x4)
    for k, w in enumerate(SI):                                       # 𝔖_{s_i} = x1 + … + xi
        assert schubert_poly(w) == {tuple(1 if a == b else 0 for b in range(4)): 1 for a in range(k + 1)}
    for w in perms(3):                                               # 穩定：S3 → S4 → S5 一樣
        f3 = schubert_poly(w)
        assert strip(schubert_poly(w + (4,)), 3) == f3 and strip(schubert_poly(w + (4, 5)), 3) == f3
    assert strip(schubert_poly((1, 3, 2, 4)), 3) == schubert_poly((1, 3, 2))
    deg2 = [w for w in perms(4) if length(w) == 2 and all(d <= 2 for d in descents(w))]
    assert sorted(deg2) == sorted(DEG2)
    polys = [strip(schubert_poly(w), 2) for w in DEG2]
    assert [poly_str(f) for f in polys] == ["x_1^{2}", "x_1x_2", "x_1^{2}+x_1x_2+x_2^{2}"]
    mons = [(2, 0), (1, 1), (0, 2)]
    M = np.array([[f.get(e, 0) for e in mons] for f in polys])
    assert round(abs(np.linalg.det(M))) == 1                          # 是 Z 上的基底（行列式 ±1）
    assert schubert_poly((2, 1, 3)) == {(1, 0, 0): 1}                 # σ213 = x1 ≡ −x2 − x3 (mod e1)
    assert elementary_e(1, 3) == {(1, 0, 0): 1, (0, 1, 0): 1, (0, 0, 1): 1}


# ---------------------------------------------------------------- 1. 最頂端
def part_top(scene):
    lemma = tex(r"\mathfrak S_{w_0}=x_1^{m-1}x_2^{m-2}\cdots x_{m-1}", 52, ACCENT).move_to(np.array([0, 2.1, 0]))
    exs = VGroup(*[tex(S_tex(w0(m)), 40) for m in (2, 3, 4)]).arrange(RIGHT, buff=1.0)
    exs.move_to(np.array([0, 0.75, 0]))
    fit(exs, 12.5)
    rule = tex(r"w(i)>w(i+1)\ \Rightarrow\ \mathfrak S_{ws_i}=\partial_i\mathfrak S_w", 46).move_to(np.array([0, -0.75, 0]))
    note = mixed("（", r"$ws_i$", "：把第 ", "$i,i+1$", " 個位置對調，長度少 1）", font_size=26, color=MUTED_COLOR)
    note.next_to(rule, DOWN, buff=0.35)
    box = SurroundingRectangle(rule, buff=0.2).set_stroke(OP, 2)
    assert_in_frame(lemma, exs, rule, note, box)
    assert_apart(lemma, exs, 0.2)
    assert_apart(exs, box, 0.2)

    scene.say("問：知道最頂端的一個多項式，其他的能不能全部推出來？", wait=SLOW * 0.8)
    scene.say("最頂端是最長的置換 ", "$w_0=m\\cdots 21$", "，Lemma 10 給它一個單項式", wait=SLOW * 0.2)
    scene.play(Write(lemma), run_time=1.4)
    scene.wait(SLOW * 0.4)
    scene.play(LaggedStart(*[FadeIn(e, shift=0.2 * UP) for e in exs], lag_ratio=0.4), run_time=1.5)
    scene.say("$m=3$", "：", "$x_1^2x_2$", "；", "$m=4$", "：", "$x_1^3x_2^2x_3$", wait=SLOW * 0.8)
    scene.say("其餘的全部交給 F51 的機器：在下降的位置做 ", r"$\partial_i$", wait=SLOW * 0.2)
    scene.play(Write(rule), run_time=1.4)
    scene.play(ShowCreation(box), FadeIn(note), run_time=0.8)
    scene.say("這樣得到的多項式叫 Schubert 多項式 ", r"$\mathfrak S_w$", "（Lascoux–Schützenberger）", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 2. S3 的 Hasse 圖
def part_hasse(scene):
    cx = -2.4
    hasse = HasseMob(LEVELS3, bruhat_covers(3), label=lambda w: poly_str(schubert_poly(w)), dx=3.4, dy=1.45,
                     font_size=36)
    hasse.shift(cx * RIGHT)
    hasse.edges.set_stroke(GREY_D, 1.5)
    tags = VGroup()
    for w, node in hasse.node.items():
        t = tex(perm_str(w), 26, MUTED_COLOR)
        x = node.get_center()[0]
        side = LEFT if x < cx - 0.1 else RIGHT if x > cx + 0.1 else UP if length(w) == 3 else DOWN
        tags.add(t.next_to(node, side, buff=0.25))
    elabs = {}
    for up, lo, i in WEAK:
        e = hasse.edge[(lo, up)]
        mid = e.get_center()
        elabs[(up, lo)] = tex(r"\partial_%d" % i, 28, OP).move_to(mid + (0.38 if mid[0] > cx else -0.38) * RIGHT)
    calc = [tex(r"\partial_%d(%s)=%s" % (i, poly_str(schubert_poly(up)), poly_str(schubert_poly(lo))), 30)
            for up, lo, i in WEAK]
    for k, c in enumerate(calc):
        c.move_to(np.array([2.6, 2.2 - 0.72 * k, 0]), aligned_edge=LEFT)
    same = zh("兩條路，同一個 1", font_size=26, color=ACCENT).next_to(calc[-1], DOWN, buff=0.45)
    same.align_to(calc[-1], LEFT)
    assert_in_frame(hasse, tags, *elabs.values(), *calc, same)
    assert_apart(VGroup(hasse, tags, *elabs.values()), VGroup(*calc, same), 0.3)
    for t in tags:
        for l in elabs.values():
            assert_apart(t, l, 0.05)

    top = (3, 2, 1)
    scene.say("$S_3$", " 的六個置換排成 Hasse 圖，每一層長度少 1", wait=SLOW * 0.2)
    scene.play(FadeIn(hasse.edges), FadeIn(tags), run_time=1.2)
    scene.play(FadeIn(hasse.node[top], scale=1.2), run_time=0.8)
    scene.say("從最頂端 ", r"$\mathfrak S_{321}=x_1^2x_2$", " 出發，沿著 ", r"$\partial_i$", " 往下流", wait=SLOW * 0.5)
    texts = {
        0: ("$321$", " 在位置 1 下降：", r"$\partial_1$", " 給 ", r"$\mathfrak S_{231}=x_1x_2$"),
        1: ("位置 2 也下降：", r"$\partial_2$", " 給 ", r"$\mathfrak S_{312}=x_1^2$"),
        2: ("$231$", " 只在位置 2 下降：", r"$\mathfrak S_{213}=x_1$"),
        3: ("$312$", " 只在位置 1 下降：", r"$\mathfrak S_{132}=x_1+x_2$"),
        4: ("左邊這條路走到底：", r"$\partial_1(x_1)=1$"),
        5: ("右邊這條路：", r"$\partial_2(x_1+x_2)=1$", "，也到 1"),
    }
    for k, (up, lo, i) in enumerate(WEAK):
        e = hasse.edge[(lo, up)]
        scene.say(*texts[k], wait=0.0)
        anims = [e.animate.set_stroke(OP, 3), FadeIn(elabs[(up, lo)])]
        if k < 5:
            anims.append(TransformFromCopy(hasse.node[up], hasse.node[lo]))
        else:
            anims.append(Indicate(hasse.node[lo], scale_factor=1.4))
        scene.play(*anims, FadeIn(calc[k], shift=0.2 * LEFT), run_time=1.1)
        scene.wait(SLOW * 0.6)
    scene.play(FadeIn(same, shift=0.2 * UP), run_time=0.6)
    scene.say("兩條路 ", r"$\partial_1\partial_2\partial_1=\partial_2\partial_1\partial_2$", "：到同一處，結果一樣", wait=SLOW * 0.9)
    cross = [hasse.edge[c] for c in [((1, 3, 2), (2, 3, 1)), ((2, 1, 3), (3, 1, 2))]]
    scene.play(*[c.animate.set_stroke(PINK, 2.5) for c in cross], run_time=0.6)
    scene.say("中間兩條灰線也是 Bruhat 序的邊（F54），但不是一次 ", r"$\partial_i$", wait=SLOW * 0.9)
    scene.play(*[c.animate.set_stroke(GREY_D, 1.5) for c in cross], run_time=0.4)


# ---------------------------------------------------------------- 3. 長途旅行
def perm_digits(w, hi=()):
    g = VGroup(*[tex(str(a), 40, ACCENT if k in hi else WHITE) for k, a in enumerate(w)]).arrange(RIGHT, buff=0.1)
    return g


def part_trip(scene):
    path = schubert_path(5, STEPS)
    rows = []
    for k, (w, f) in enumerate(path):
        y = 2.45 - 0.86 * k
        hi = (STEPS[k - 1] - 1, STEPS[k - 1]) if k else ()
        lab = tex(r"\xrightarrow{\partial_%d}" % STEPS[k - 1], 34, OP) if k else tex(r"w_0", 30, MUTED_COLOR)
        lab.move_to(np.array([-6.0, y, 0]))
        pd = perm_digits(w, hi).move_to(np.array([-4.6, y, 0]))
        poly = fit(tex(poly_str(f), 40), 9.8).move_to(np.array([-3.3, y, 0]), aligned_edge=LEFT)
        rows.append(VGroup(lab, pd, poly))
    fac = tex(r"=x_1^{3}(x_2x_3+x_2x_4+x_3x_4)", 40, ACCENT).next_to(rows[-1][2], DOWN, buff=0.3)
    fac.align_to(rows[-1][2], LEFT)
    assert_in_frame(*rows, fac)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a, b, 0.1)

    scene.say("書上的長途旅行：", "$S_5$", "，從 ", "$54321$", " 走五步", wait=SLOW * 0.2)
    scene.play(FadeIn(rows[0]), run_time=0.8)
    says = [("$\\partial_1$", "：", "$x_1$", " 的次方少 1"),
            ("$\\partial_4$", "：", "$x_4$", " 和 ", "$x_5$", " 對調，", "$x_4$", " 被除掉"),
            ("$\\partial_3$", "：", "$x_3^2$", " 變成 ", "$x_3+x_4$", "，兩項"),
            ("$\\partial_2$", "：變成 5 項"),
            ("$\\partial_3$", "：又收回 3 項")]
    for k in range(1, len(rows)):
        scene.play(TransformFromCopy(rows[k - 1][1], rows[k][1]), FadeIn(rows[k][0]), run_time=0.8)
        scene.play(FadeIn(rows[k][2], shift=0.2 * RIGHT), run_time=0.7)
        scene.say(*says[k - 1], wait=SLOW * 0.55)
    scene.play(Write(fac), run_time=1.2)
    scene.say("最後是 ", "$x_1^3$", " 乘上 ", "$x_2,x_3,x_4$", " 的 ", "$e_2$", "：係數全是正的", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 4. 性質
def part_props(scene):
    h1 = zh("簡單對換", font_size=24, color=MUTED_COLOR).move_to(np.array([-3.4, 2.65, 0]))
    si = VGroup(*[tex(S_tex(w), 34) for w in SI]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    si.next_to(h1, DOWN, buff=0.3)
    h2 = zh("穩定：不隨 m 改變", font_size=24, color=MUTED_COLOR).move_to(np.array([3.4, 2.65, 0]))
    st = VGroup(tex(r"m=3:\ \mathfrak S_{132}=x_1+x_2", 34), tex(r"m=4:\ \mathfrak S_{1324}=x_1+x_2", 34),
                tex(r"m=5:\ \mathfrak S_{13245}=x_1+x_2", 34)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    st.next_to(h2, DOWN, buff=0.3)
    h3 = mixed("命題 6：次數 2、只用 ", "$x_1,x_2$", " 的 Schubert 多項式", font_size=24, color=MUTED_COLOR)
    h3.move_to(np.array([0, -0.55, 0]))
    sch = VGroup(*[tex(S_tex(w), 32) for w in DEG2]).arrange(RIGHT, buff=0.7).move_to(np.array([0, -1.3, 0]))
    fit(sch, 12.6)
    mon = tex(r"x_1^{2},\qquad x_1x_2,\qquad x_2^{2}", 32, MUTED_COLOR).move_to(np.array([0, -2.2, 0]))
    canon = tex(r"\sigma_{213}=x_1=-x_2-x_3=\cdots", 34, ACCENT)
    assert_in_frame(h1, si, h2, st, h3, sch, mon)
    assert_apart(VGroup(h1, si), VGroup(h2, st), 0.3)
    assert_apart(VGroup(si, st), h3, 0.2)
    assert_apart(sch, mon, 0.2)

    scene.say("幾個性質。簡單對換 ", "$s_i$", " 的 Schubert 多項式是前 ", "$i$", " 個變數的和", wait=SLOW * 0.2)
    scene.play(FadeIn(h1), LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in si], lag_ratio=0.3), run_time=1.5)
    scene.wait(SLOW * 0.6)
    scene.say("在 ", "$S_3$", "、", "$S_4$", "、", "$S_5$", " 裡算同一個置換，答案一樣：和 ", "$m$", " 無關", wait=SLOW * 0.2)
    scene.play(FadeIn(h2), LaggedStart(*[FadeIn(t, shift=0.2 * RIGHT) for t in st], lag_ratio=0.3), run_time=1.5)
    scene.wait(SLOW * 0.7)
    scene.say("所以 ", r"$\mathfrak S_w$", " 對所有 ", "$S_\\infty$", " 的置換都有定義", wait=SLOW * 0.6)
    scene.say("命題 6：下降都在 ", "$k$", " 以內的 ", r"$\mathfrak S_w$", "，正好是 ", r"$\mathbb Z[x_1,\dots,x_k]$", " 的基底",
              wait=SLOW * 0.2)
    scene.play(FadeIn(h3), run_time=0.6)
    scene.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in sch], lag_ratio=0.3), run_time=1.4)
    scene.play(FadeIn(mon, shift=0.2 * UP), run_time=0.8)
    scene.say("三個對三個單項式，換算矩陣是三角形、對角線是 1", wait=SLOW * 0.9)
    scene.play(FadeOut(VGroup(h3, sch, mon)), run_time=0.6)
    canon.move_to(np.array([0, -1.3, 0]))
    assert_in_frame(canon)
    scene.say("在 ", "$H^*(Fl(3))$", " 裡，同一個類有很多種寫法（", "$e_1=0$", "）", wait=SLOW * 0.2)
    scene.play(Write(canon), run_time=1.2)
    scene.wait(SLOW * 0.5)
    scene.say("Schubert 多項式就是把 ", r"$\sigma_w$", " 寫成 ", "$x$", " 的多項式的「標準答案」", wait=SLOW * 1.3)


class SceneF52SchubertPolys(ChuScene):
    def construct(self):
        self.show_header("從最頂端流下來：Schubert 多項式")
        check_math()
        part_top(self)
        self.clear_stage()
        part_hasse(self)
        self.clear_stage()
        part_trip(self)
        self.clear_stage()
        part_props(self)
        self.wait(1.0)
