"""
Scene F55 —— 回到 Grassmannian：Schubert 多項式變 Schur 多項式（Fulton §10.6，書 p.178–182）＋第 9–10 章總結
執行（在 codes/ 內）：manimgl scenes/sceneF55_grassmannian_schur.py SceneF55GrassmannianSchur
"""
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import SkewMob, assert_apart, assert_in_frame, tableau_mob
from utils.schubert import (box_product, descents, grassmannian_partition, grassmannian_perm, perm_str, pipe_dreams,
                            pipe_weight, schubert_poly)
from utils.scene_base import ChuScene
from utils.schubert_draw import BoxDiagramMob, PipeDreamMob
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import elementary_e, lr_coefficient, poly_mul, poly_sum, schur_expand, schur_poly, standard_tableaux

SLOW = 4.6
ACCENT = YELLOW
OK = "#7CE38B"
BAD = PINK
EXAMPLES = [((2, 4, 1, 3), (2, 1), r"\mathfrak S_{2413}=x_1^{2}x_2+x_1x_2^{2}=s_{21}(x_1,x_2)"),
            ((1, 3, 4, 2), (1, 1), r"\mathfrak S_{1342}=x_1x_2+x_1x_3+x_2x_3=e_2(x_1,x_2,x_3)"),
            ((1, 3, 2, 4), (1,), r"\mathfrak S_{1324}=x_1+x_2=s_1(x_1,x_2)")]
BOX6 = [(), (1,), (2,), (1, 1), (2, 1), (2, 2)]
LR_TABS = [((None, None, 1), (None, 1), (2,)), ((None, None, 1), (None, 2), (1,))]
W5 = (2, 1, 5, 4, 3)


def fit(m, w):
    if m.get_width() > w:
        m.set_width(w)
    return m


def tex(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def pad(f, m):
    return {tuple(e) + (0,) * (m - len(e)): c for e, c in f.items()}


def in_ideal(f, m, d):
    """f（d 次齊次、m 個變數）是否在 (e_1, …, e_m) 裡：在 d 次的部分解線性方程。"""
    mons = [e for e in product(range(d + 1), repeat=m) if sum(e) == d]
    gens = []
    for k in range(1, min(d, m) + 1):
        ek = elementary_e(k, m)
        for e in product(range(d - k + 1), repeat=m):
            if sum(e) == d - k:
                gens.append(poly_mul({e: 1}, ek))
    A = np.array([[g.get(e, 0) for e in mons] for g in gens], dtype=float)
    b = np.array([[f.get(e, 0) for e in mons]], dtype=float)
    return np.linalg.matrix_rank(np.vstack([A, b])) == np.linalg.matrix_rank(A)


def lr_ok(S, content):
    """斜表的反向閱讀字（每列由右而左、由上而下）是 lattice word，且內容正確。"""
    word = [x for row in S for x in reversed(row) if x is not None]
    cnt = {}
    for x in word:
        cnt[x] = cnt.get(x, 0) + 1
        if x > 1 and cnt[x] > cnt.get(x - 1, 0):
            return False
    return tuple(cnt.get(k, 0) for k in range(1, len(content) + 1)) == tuple(content)


def check_math():
    for w, lam, _ in EXAMPLES:
        lam_w, r = grassmannian_partition(w)
        assert tuple(x for x in lam_w if x) == lam and descents(w) == [r]
        assert schubert_poly(w) == pad(schur_poly(lam, r), 4)
    assert grassmannian_partition((2, 4, 1, 3)) == ((2, 1), 2) and grassmannian_partition((1, 3, 4, 2)) == ((1, 1, 0), 3)
    assert schubert_poly((1, 3, 4, 2)) == pad(elementary_e(2, 3), 4)
    perms6 = [grassmannian_perm(lam, 2, 4) for lam in BOX6]
    assert [perm_str(w) for w in perms6] == ["1234", "1324", "1423", "2314", "2413", "3412"]
    for lam, w in zip(BOX6, perms6):
        assert schubert_poly(w) == pad(schur_poly(lam, 2), 4) if lam else schubert_poly(w) == {(0, 0, 0, 0): 1}
    s1 = {(1, 0): 1, (0, 1): 1}
    p4 = {(0, 0): 1}
    for _ in range(4):
        p4 = poly_mul(p4, s1)
    assert schur_expand(p4, 2) == {(4,): 1, (3, 1): 3, (2, 2): 2}
    assert p4 == poly_sum([{e: 1 * c for e, c in schur_poly((4,), 2).items()},
                           {e: 3 * c for e, c in schur_poly((3, 1), 2).items()},
                           {e: 2 * c for e, c in schur_poly((2, 2), 2).items()}])
    sig = {(1,): 1}
    for _ in range(3):
        nxt = {}
        for lam, c in sig.items():
            for nu, d in box_product(lam, (1,), 2, 2).items():
                nxt[nu] = nxt.get(nu, 0) + c * d
        sig = nxt
    assert {tuple(x for x in k if x): v for k, v in sig.items()} == {(2, 2): 2}       # σ1^4 = 2σ22
    assert schubert_poly((3, 4, 1, 2)) == {(2, 2, 0, 0): 1} == pad(schur_poly((2, 2), 2), 4)
    assert in_ideal(poly_sum([pad(p4, 4), {(2, 2, 0, 0): -2}]), 4, 4)                  # 在 H*(Fl(4)) 裡相等
    assert in_ideal(pad(schur_poly((4,), 2), 4), 4, 4) and in_ideal(pad(schur_poly((3, 1), 2), 4), 4, 4)
    assert not in_ideal({(2, 2, 0, 0): 1}, 4, 4) and in_ideal({(4, 0, 0, 0): 1}, 4, 4)    # 對照組
    assert len(standard_tableaux((2, 2))) == 2
    assert lr_coefficient((2, 1), (2, 1), (3, 2, 1)) == 2 and all(lr_ok(S, (2, 1)) for S in LR_TABS)
    assert not lr_ok(((None, None, 2), (None, 1), (1,)), (2, 1))
    assert schubert_poly(W5)[(2, 1, 1, 0, 0)] == 2
    assert len([D for D in pipe_dreams(W5) if pipe_weight(D, 5) == (2, 1, 1, 0, 0)]) == 2


# ---------------------------------------------------------------- 1. Grassmann 置換
def perm_with_bar(w, r, fs=40):
    ds = VGroup(*[tex(str(a), fs) for a in w]).arrange(RIGHT, buff=0.22)
    x = (ds[r - 1].get_right()[0] + ds[r].get_left()[0]) / 2
    bar = Line(np.array([x, ds.get_top()[1] + 0.08, 0]), np.array([x, ds.get_bottom()[1] - 0.08, 0]))
    bar.set_stroke(ACCENT, 3)
    return VGroup(ds, bar)


def part_grass(scene):
    head = tex(r"\lambda=(w(r)-r,\ \dots,\ w(2)-2,\ w(1)-1)", 40).move_to(np.array([0, 2.5, 0]))
    rows = []
    for k, (w, lam, s) in enumerate(EXAMPLES):
        y = 1.25 - 1.45 * k
        lam_w, r = grassmannian_partition(w)
        pw = perm_with_bar(w, r).move_to(np.array([-5.5, y, 0]))
        lt = tex(r"\lambda=(%s)" % ",".join(map(str, lam)), 32, MUTED_COLOR).move_to(np.array([-3.65, y, 0]))
        box = BoxDiagramMob(lam, r, 4 - r, cs=0.32).move_to(np.array([-2.25, y, 0]))
        f = fit(tex(s, 34), 7.6).move_to(np.array([-1.35, y, 0]), aligned_edge=LEFT)
        rows.append(VGroup(pw, lt, box, f))
    q = mixed("（", "$r$", " 是唯一的下降位置；", "$\\lambda$", " 落在 ", r"$r\times(m-r)$", " 方框裡）", font_size=24,
              color=MUTED_COLOR).move_to(np.array([0, -2.55, 0]))
    assert_in_frame(head, *rows, q)
    for a, b in zip(rows, rows[1:]):
        assert_apart(a, b, 0.1)
    for row in rows:
        for a, b in zip(row, row[1:]):
            assert_apart(a, b, 0.15)
    assert_apart(rows[-1], q, 0.1)

    scene.say("問：第 9 章的四條線，能不能在旗流形裡再算一次？", wait=SLOW * 0.7)
    scene.say("先找出 Grassmannian 藏在旗流形的哪裡：Grassmann 置換", wait=SLOW * 0.3)
    scene.play(FadeIn(rows[0][0]), run_time=0.7)
    scene.say("$2413$", " 只在位置 2 下降：前兩個數 ", "$2,4$", " 決定一個 ", r"$\lambda$", wait=SLOW * 0.2)
    scene.play(Write(head), run_time=1.2)
    scene.play(FadeIn(rows[0][1]), FadeIn(rows[0][2]), run_time=0.8)
    scene.say(r"$\lambda=(4-2,\ 2-1)=(2,1)$", "，落在 ", r"$2\times2$", " 方框裡", wait=SLOW * 0.5)
    scene.play(FadeIn(rows[0][3], shift=0.2 * RIGHT), run_time=0.9)
    scene.say("命題 8：它的 Schubert 多項式正是 Schur 多項式 ", "$s_{21}(x_1,x_2)$", wait=SLOW * 0.8)
    for k in (1, 2):
        scene.play(FadeIn(rows[k][0]), FadeIn(rows[k][1]), FadeIn(rows[k][2]), run_time=0.8)
        scene.play(FadeIn(rows[k][3], shift=0.2 * RIGHT), run_time=0.9)
        if k == 1:
            scene.say("$1342$", " 在位置 3 下降：", r"$\lambda=(1,1)$", "，得到 ", "$e_2(x_1,x_2,x_3)$", wait=SLOW * 0.7)
        else:
            scene.say("$1324$", "：", r"$\lambda=(1)$", "，就是 ", "$x_1+x_2$", wait=SLOW * 0.6)
    scene.play(FadeIn(q), run_time=0.6)
    scene.say("一般地：", r"$\mathfrak S_w=s_\lambda(x_1,\dots,x_r)$", "，Schubert 多項式推廣了 Schur 多項式", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 2. 投影
def part_projection(scene):
    top = tex(r"p:\ Fl(4)\to Gr(2,4),\qquad E_\bullet\mapsto E_2", 42).move_to(np.array([0, 2.45, 0]))
    flag = VGroup(tex(r"E_1\subset", 38), tex(r"E_2", 38, ACCENT), tex(r"\subset E_3\subset\mathbb C^4", 38))
    flag.arrange(RIGHT, buff=0.12).move_to(np.array([-3.4, 1.3, 0]))
    arr = Arrow(flag[1].get_bottom() + DOWN * 0.1, flag[1].get_bottom() + DOWN * 1.0, buff=0).set_color(GREY_B)
    e2 = tex(r"E_2", 38, ACCENT).next_to(arr, DOWN, buff=0.1)
    prop = tex(r"p^*\sigma_\lambda=\sigma_w", 46, OK).move_to(np.array([3.3, 0.9, 0]))
    cells = VGroup()
    for k, lam in enumerate(BOX6):
        x = -5.0 + 2.0 * k
        b = BoxDiagramMob(lam, 2, 2, cs=0.38).move_to(np.array([x, -1.35, 0]))
        w = tex(perm_str(grassmannian_perm(lam, 2, 4)), 30).next_to(b, DOWN, buff=0.25)
        cells.add(VGroup(b, w))
    assert_in_frame(top, flag, arr, e2, prop, cells)
    assert_apart(VGroup(flag, arr, e2), prop, 0.4)
    assert_apart(VGroup(flag, arr, e2, prop), cells, 0.2)
    assert_apart(top, VGroup(flag, prop), 0.15)

    scene.say("投影：一個旗只記得它的 2 維子空間", wait=SLOW * 0.2)
    scene.play(Write(top), run_time=1.3)
    scene.play(FadeIn(flag), run_time=0.7)
    scene.play(GrowArrow(arr), TransformFromCopy(flag[1], e2), run_time=0.9)
    scene.wait(SLOW * 0.4)
    scene.say("命題 9：", r"$\sigma_\lambda$", " 拉回到 ", "$Fl(4)$", "，就是 Grassmann 置換的 ", r"$\sigma_w$", wait=SLOW * 0.2)
    scene.play(Write(prop), run_time=1.0)
    scene.wait(SLOW * 0.4)
    scene.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cells], lag_ratio=0.15), run_time=1.6)
    scene.say(r"$2\times2$", " 方框裡 6 個 ", r"$\lambda$", "，對上 6 個只在位置 2 下降的置換", wait=SLOW * 0.9)


# ---------------------------------------------------------------- 3. 四條線重算
def shape_in_box(lam, cs=0.24, r=2, n=2):
    g = VGroup()
    for i, row in enumerate(lam):
        for j in range(row):
            inside = i < r and j < n
            sq = Square(cs).move_to(np.array([j * cs, -i * cs, 0])).set_stroke(WHITE, 1.5)
            sq.set_fill(BLUE_C if inside else BAD, 0.6)
            g.add(sq)
    frame = Rectangle(width=n * cs, height=r * cs).move_to(np.array([(n - 1) * cs / 2, -(r - 1) * cs / 2, 0]))
    frame.set_stroke(ACCENT, 2.5)
    return VGroup(g, frame)


def part_four_lines(scene):
    l1 = tex(r"\sigma_1\ \mapsto\ \mathfrak S_{1324}=x_1+x_2=s_1(x_1,x_2)", 40).move_to(np.array([0, 2.45, 0]))
    parts = VGroup(tex(r"(x_1+x_2)^4=", 44), tex(r"s_4", 44), tex(r"+3s_{31}", 44), tex(r"+2s_{22}", 44))
    parts.arrange(RIGHT, buff=0.25).move_to(np.array([0, 1.3, 0]))
    shapes = VGroup(*[shape_in_box(lam).next_to(parts[k], DOWN, buff=0.3) for k, lam in
                      zip((1, 2, 3), ((4,), (3, 1), (2, 2)))])
    crosses = VGroup(*[Line(parts[k].get_corner(DL), parts[k].get_corner(UR)).set_stroke(BAD, 4) for k in (1, 2)])
    l3 = tex(r"(x_1+x_2)^4\equiv 2x_1^{2}x_2^{2}=2\,\mathfrak S_{3412}", 40, OK).move_to(np.array([0, -1.25, 0]))
    l4 = tex(r"\sigma_1^4=2\sigma_{22}", 44, ACCENT).move_to(np.array([0, -2.25, 0]))
    assert_in_frame(l1, parts, shapes, l3, l4)
    assert_apart(l1, parts, 0.2)
    assert_apart(shapes, l3, 0.2)
    assert_apart(l3, l4, 0.15)

    scene.say("四條線重算：", r"$\sigma_1$", " 拉回成 ", "$x_1+x_2$", wait=SLOW * 0.2)
    scene.play(Write(l1), run_time=1.3)
    scene.wait(SLOW * 0.3)
    scene.say("四個條件就是四次方；按 Schur 多項式展開", wait=SLOW * 0.2)
    scene.play(FadeIn(parts), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(s, shift=0.2 * UP) for s in shapes], lag_ratio=0.3), run_time=1.2)
    scene.say("黃框是 ", r"$2\times2$", " 方框；", "$s_4$", "、", "$s_{31}$", " 有格子跑出去", wait=SLOW * 0.5)
    scene.play(ShowCreation(crosses[0]), ShowCreation(crosses[1]), run_time=0.8)
    scene.say("放不進方框的項，在上同調裡是 0（只留方框裡的項）", wait=SLOW * 0.6)
    scene.play(FadeIn(l3, shift=0.2 * UP), run_time=0.9)
    scene.say("在 ", "$H^*(Fl(4))$", " 裡剩下 ", "$2x_1^2x_2^2$", "，而 ", r"$\mathfrak S_{3412}=x_1^2x_2^2$", wait=SLOW * 0.7)
    scene.play(Write(l4), run_time=1.0)
    scene.say("又是 2：和第 9 章的答案一樣，兩條直線", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 4. 三個 2
def part_twos(scene):
    xs = (-4.5, 0.0, 4.5)
    twos = VGroup(*[tex("2", 84, ACCENT).move_to(np.array([x, 1.95, 0])) for x in xs])
    pic1 = VGroup(*[tableau_mob(T, cs=0.5) for T in standard_tableaux((2, 2))]).arrange(RIGHT, buff=0.45)
    pic2 = VGroup(*[SkewMob(S, cs=0.42) for S in LR_TABS]).arrange(RIGHT, buff=0.45)
    two = [D for D in pipe_dreams(W5) if pipe_weight(D, 5) == (2, 1, 1, 0, 0)]
    pic3 = VGroup(*[PipeDreamMob(D, 5, cs=0.3) for D in two]).arrange(RIGHT, buff=0.3)
    for pd in pic3:
        pd.tiles.set_stroke(width=2)
    pics = [pic1, pic2, pic3]
    for p, x in zip(pics, xs):
        p.move_to(np.array([x, 0.25, 0]))
        fit(p, 3.9)
    labs = [mixed("四條線：", "$(2,2)$", " 的標準表", font_size=24),
            mixed("$c^{321}_{21,21}$", "：LR 表", font_size=24),
            mixed(r"$\mathfrak S_{21543}$", " 的係數：pipe dream", font_size=24)]
    for l, x in zip(labs, xs):
        l.move_to(np.array([x, -1.45, 0]))
        fit(l, 4.0)
    where = [zh(s, font_size=22, color=MUTED_COLOR).move_to(np.array([x, -2.15, 0]))
             for s, x in zip(("F49、F55", "F49（第 5 章）", "F53"), xs)]
    assert_in_frame(twos, *pics, *labs, *where)
    for a, b in ((0, 1), (1, 2)):
        assert_apart(VGroup(pics[a], labs[a]), VGroup(pics[b], labs[b]), 0.3)
    for p, l in zip(pics, labs):
        assert_apart(p, l, 0.15)

    scene.say("快問快答：這兩幕出現了三個「2」，各數的是什麼？", wait=SLOW * 0.3)
    scene.play(LaggedStart(*[FadeIn(t, scale=1.3) for t in twos], lag_ratio=0.3), run_time=1.2)
    says = [("四條線：", r"$\sigma_1^4=2\sigma_{22}$", "，數 ", "$(2,2)$", " 的標準表"),
            ("$Gr(3,6)$", " 裡 ", r"$\sigma_{21}^2$", " 中 ", r"$\sigma_{321}$", " 的係數：數 LR 表"),
            (r"$\mathfrak S_{21543}$", " 裡 ", "$x_1^2x_2x_3$", " 的係數：數 pipe dream")]
    for k in range(3):
        scene.say(*says[k], wait=SLOW * 0.1)
        scene.play(FadeIn(pics[k], shift=0.2 * UP), FadeIn(labs[k]), FadeIn(where[k]), run_time=1.0)
        scene.wait(SLOW * 0.7)
    scene.say("三個 2，三種組合物件；係數都是在「數東西」", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 5. 回顧
def part_review(scene):
    items = [("星號＝維數：胞腔一塊塊拼出 ", "$Gr$", " 和 ", "$Fl$"),
             ("二次關係（Plücker）切出 ", "$Gr$", " 和 ", "$Fl$"),
             ("Schubert 計算＝LR 規則，只留方框裡的項",),
             ("差商從 ", r"$\mathfrak S_{w_0}$", " 流下來；", r"$\mathfrak S_w$", " 推廣 Schur 多項式")]
    lines = VGroup(*[mixed(*it, font_size=30) for it in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
    lines.move_to(np.array([0.3, 0.5, 0]))
    marks = VGroup(*[Dot(radius=0.07).set_color(ACCENT).next_to(l, LEFT, buff=0.3) for l in lines])
    end = zh("第 9–10 章完", font_size=44, color=OK).move_to(np.array([0, -2.2, 0]))
    assert_in_frame(lines, marks, end)
    assert_apart(lines, end, 0.3)

    scene.say("第 9–10 章回顧", wait=SLOW * 0.2)
    for l, m in zip(lines, marks):
        scene.play(FadeIn(m), FadeIn(l, shift=0.2 * RIGHT), run_time=0.8)
        scene.wait(SLOW * 0.7)
    scene.play(FadeIn(end, scale=1.1), run_time=0.9)
    scene.say("從六個數認出一個平面，到用多項式數直線：第 9–10 章完", wait=SLOW * 1.2)


class SceneF55GrassmannianSchur(ChuScene):
    def construct(self):
        self.show_header("回到 Grassmannian：Schubert 多項式變 Schur 多項式")
        check_math()
        part_grass(self)
        self.clear_stage()
        part_projection(self)
        self.clear_stage()
        part_four_lines(self)
        self.clear_stage()
        part_twos(self)
        self.clear_stage()
        part_review(self)
        self.wait(1.0)
