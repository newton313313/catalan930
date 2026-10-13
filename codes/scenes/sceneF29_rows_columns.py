"""
Scene F29 —— 座位表與兩種洗牌（Fulton §7.1，書 p.83–85；原大綱卡 F702、F703）
執行（在 codes/ 內）：manimgl scenes/sceneF29_rows_columns.py SceneF29RowsColumns

(3,2) 的兩根長條收成左對齊的格子、共軛 (2,2,1)；(2,1) 的 6 個編號挑出 2 個標準表；(3,2) 的 5 個標準表；
R(T)（藍）、C(T)（橙）；a_T = e+(12)、b_T = e-(13)、c_T = b_T a_T 的四項（乘法表）；R(σT) = σR(T)σ⁻¹；
(3,2) 只報 #R = 12、#C = 4。
"""
import sys
from math import factorial, prod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import act, col_group, compose, gr_mul, load, row_group, sign, symmetrizers
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, perm_tex
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import conjugate, corners, is_standard

SH21 = load("shape21")
SH32 = load("shape32")
YS = load("young_symmetrizer21")
TA = tuple(map(tuple, SH21["Ta"]))
TB = tuple(map(tuple, SH21["Tb"]))
E3, S12, S13, S23 = (1, 2, 3), (2, 1, 3), (3, 2, 1), (1, 3, 2)
NUMBERINGS = [tuple(map(tuple, r["rows"])) for r in SH21["all_numberings"]]
STD32 = [tuple(map(tuple, T)) for T in SH32["standard"]]


def first_descent(T):
    """第一個違規的兩格（列裡變小或行裡變小）；標準表傳回 None。"""
    for i, r in enumerate(T):
        for j, v in enumerate(r):
            if j + 1 < len(r) and v > r[j + 1]:
                return (i, j), (i, j + 1)
            if i + 1 < len(T) and j < len(T[i + 1]) and v > T[i + 1][j]:
                return (i, j), (i + 1, j)
    return None


def cell_of(T, v):
    return next((i, j) for i, r in enumerate(T) for j, x in enumerate(r) if x == v)


def check_math():
    lam = tuple(SH32["lambda"])
    assert conjugate(lam) == tuple(SH32["transpose"]) == (2, 2, 1)
    assert [i for i, T in enumerate(NUMBERINGS) if is_standard(T)] == [0, 1]
    assert NUMBERINGS[0] == TA and NUMBERINGS[1] == TB
    assert all(first_descent(T) is not None for T in NUMBERINGS[2:])
    assert len(STD32) == SH32["f"] == 5 and all(is_standard(T) for T in STD32)
    assert all(cell_of(T, 5) in corners(lam) for T in STD32)
    assert set(map(tuple, SH21["row_group_Ta"])) == set(row_group(TA))
    assert set(map(tuple, SH21["row_group_Ta"])) == {E3, S12}
    assert set(map(tuple, SH21["column_group_Ta"])) == set(col_group(TA)) == {E3, S13}
    assert act(S12, TA) == ((2, 1), (3,)) and act(S13, TA) == ((3, 2), (1,)) and sign(S13) == -1
    a, b, c = symmetrizers(TA)
    assert c == {tuple(t["perm"]): t["coef"] for t in YS["c_terms"]}
    assert compose(S13, S12) == (2, 3, 1) and perm_tex((2, 3, 1)) == r"(1\,2\,3)"
    assert c == {E3: 1, S12: 1, S13: -1, (2, 3, 1): -1}
    assert gr_mul(a, b) != c and gr_mul(a, b)[(3, 1, 2)] == -1          # a_T b_T 多的是 -(1 3 2)
    assert act(S23, TA) == TB
    conj = {compose(compose(S23, p), S23) for p in row_group(TA)}        # (2 3)^{-1} = (2 3)
    assert conj == set(row_group(TB)) == {E3, S13}
    assert prod(factorial(x) for x in lam) == SH32["row_group_size"] == 12
    assert prod(factorial(x) for x in SH32["transpose"]) == SH32["column_group_size"] == 4
    T = STD32[0]
    assert T == ((1, 2, 3), (4, 5)) and SH32["row_group_size"] * SH32["column_group_size"] == 48


def cells_box(d, cells, color, buff=0.05, sw=5):
    return SurroundingRectangle(d.cell_group(cells), buff=buff, color=color, stroke_width=sw)


# =============================================================================
def part_shapes(scene):
    lam = tuple(SH32["lambda"])
    cs = 0.7
    d = YoungDiagramMob(lam, cell_size=cs, top_left=np.array([-5.2, 1.5, 0]))
    bars = VGroup(*[Rectangle(width=l * cs, height=0.45 * cs, stroke_width=0, fill_color=ROW_COLOR, fill_opacity=0.7)
                    for l in lam]).arrange(DOWN, buff=0.35).move_to(d)
    lam_tex = Tex(r"\lambda=(3,2)", font_size=44).next_to(d, UP, buff=0.5)
    scene.play(LaggedStartMap(GrowFromEdge, bars, edge=LEFT, lag_ratio=0.3), FadeIn(lam_tex), run_time=1.2)
    scene.say("分割 ", "$(3,2)$", "：兩根長條，長 3 和長 2", wait=3.0)
    rows = [d.cell_group([(i, j) for j in range(l)]) for i, l in enumerate(lam)]
    scene.play(*[Transform(b, r.copy()) for b, r in zip(bars, rows)], run_time=1.2)
    scene.remove(bars)
    scene.add(d)
    rlabs = VGroup(*[Tex(str(l), font_size=34, fill_color=ROW_COLOR).next_to(rows[i], RIGHT, buff=0.25)
                     for i, l in enumerate(lam)])
    heights = conjugate(lam)
    clabs = VGroup(*[Tex(str(h), font_size=34, fill_color=COL_COLOR).next_to(d.cell(0, j), DOWN, buff=0.2 + cs * (h - 1))
                     for j, h in enumerate(heights)])
    for lab in clabs:
        lab.set_y(d.get_bottom()[1] - 0.3)
    scene.play(FadeIn(rlabs), run_time=0.6)
    scene.say("切成方格、靠左對齊：橫的是列，列長 3、2", wait=3.5)
    scene.play(FadeIn(clabs), run_time=0.6)
    scene.say("直的是行：三行的高度是 2、2、1", wait=3.5)

    dc = YoungDiagramMob(heights, cell_size=cs, top_left=np.array([1.2, 1.5, 0]))
    conj_tex = Tex(r"\tilde\lambda=(2,2,1)", font_size=44).next_to(dc, UP, buff=0.5)
    conj_tex.align_to(lam_tex, UP)
    crow = VGroup(*[Tex(str(h), font_size=34, fill_color=COL_COLOR).next_to(dc.cell(i, h - 1), RIGHT, buff=0.25)
                    for i, h in enumerate(heights)])
    assert_in_frame(d, rlabs, clabs, dc, crow, lam_tex, conj_tex)
    assert_apart(VGroup(d, rlabs, clabs), dc)
    scene.play(FadeIn(dc), FadeIn(conj_tex), run_time=1.0)
    scene.play(*[TransformFromCopy(a, b) for a, b in zip(clabs, crow)], run_time=1.5)
    scene.say("共軛：把每一行的高度當成新的列長，得到 ", "$(2,2,1)$", wait=3.5)
    scene.say("這是交換「列長」和「行高」，不是把圖上下翻轉", wait=5.0)


def part_standard21(scene):
    tabs = VGroup(*[tableau_mob(T, cs=0.6) for T in NUMBERINGS]).arrange(RIGHT, buff=0.75).move_to(0.7 * UP)
    assert_in_frame(tabs)
    scene.play(LaggedStartMap(FadeIn, tabs, lag_ratio=0.2), run_time=1.5)
    scene.say("形狀 ", "$(2,1)$", " 填入 1、2、3：共有 6 種編號", wait=3.5)
    scene.say("標準表：每一列往右變大、每一行往下變大", wait=3.5)
    marks, dims = VGroup(), []
    for k, (T, d) in enumerate(zip(NUMBERINGS, tabs)):
        bad = first_descent(T)
        if bad is None:
            continue
        box = cells_box(d, bad, NEG_COLOR, buff=0.04)
        tag = zh("下降", font_size=22, color=NEG_COLOR).next_to(d, DOWN, buff=0.25)
        marks.add(box, tag)
        dims.append(d)
    scene.play(LaggedStartMap(ShowCreation, VGroup(*marks[0::2]), lag_ratio=0.25),
               LaggedStartMap(FadeIn, VGroup(*marks[1::2]), lag_ratio=0.25), run_time=1.8)
    scene.say("非標準的四個：紅紫框是第一個變小的地方", wait=4.5)
    names = VGroup(*[Tex(n, font_size=38, fill_color=POS_COLOR).next_to(tabs[k], DOWN, buff=0.25)
                     for k, n in ((0, "T_a"), (1, "T_b"))])
    keep = VGroup(*[SurroundingRectangle(tabs[k], buff=0.12, color=POS_COLOR, stroke_width=3) for k in (0, 1)])
    scene.play(*[d.animate.set_opacity(0.25) for d in dims], marks.animate.set_opacity(0.25),
               ShowCreation(keep), FadeIn(names), run_time=1.2)
    f21 = Tex(r"f^{(2,1)}=2", font_size=44, fill_color=POS_COLOR).move_to(1.6 * DOWN)
    scene.play(Write(f21), run_time=0.8)
    scene.say("只剩 ", "$T_a=12/3$", " 和 ", "$T_b=13/2$", wait=4.0)
    return tabs


def part_standard32(scene):
    tabs = VGroup(*[tableau_mob(T, cs=0.6) for T in STD32]).arrange(RIGHT, buff=0.7).move_to(0.9 * UP)
    hl = VGroup(*[d.cell(*cell_of(T, 5)).copy().set_fill(OP_COLOR, opacity=0.45).set_stroke(width=0)
                  for T, d in zip(STD32, tabs)])
    f32 = Tex(r"f^{(3,2)}=5", font_size=44, fill_color=POS_COLOR).move_to(0.7 * DOWN)
    note = mixed("這裡 ", "$1,\\dots,n$", " 每個只用一次；可以重複的半標準表，要等 Kostka 數才登場",
                 font_size=26, color=MUTED_COLOR).move_to(1.8 * DOWN)
    assert_in_frame(tabs, f32, note)
    scene.play(LaggedStartMap(FadeIn, tabs, lag_ratio=0.2), run_time=1.5)
    scene.say("形狀 ", "$(3,2)$", " 的標準表一共 5 張", wait=4.5)
    scene.play(FadeIn(hl), run_time=0.8)
    scene.say("最大的 5 一定坐在角落：拿掉它還是一個形狀", wait=3.5)
    scene.play(Write(f32), FadeIn(note), run_time=1.0)
    scene.say("先記下 ", "$f^{(2,1)}=2$", "、", "$f^{(3,2)}=5$", "：為什麼是模組的維度，之後再證", wait=4.0)


def part_symmetrizers(scene):
    d = tableau_mob(TA, cs=0.75, center=np.array([-5.3, 1.85, 0]))
    rbox = cells_box(d, [(0, 0), (0, 1)], ROW_COLOR)
    cbox = cells_box(d, [(0, 0), (1, 0)], COL_COLOR, buff=0.12, sw=4)
    Rt = Tex(r"R(T)=\{e,(1\,2)\}", font_size=40, fill_color=ROW_COLOR).move_to(np.array([-2.1, 2.3, 0]))
    Ct = Tex(r"C(T)=\{e,(1\,3)\}", font_size=40, fill_color=COL_COLOR).move_to(np.array([-2.1, 1.4, 0]))
    scene.play(FadeIn(d), run_time=0.8)
    scene.play(ShowCreation(rbox), FadeIn(Rt), run_time=1.0)
    scene.say("列群 ", "$R(T)$", "：只在同一列裡互換的排列", wait=3.0)
    scene.play(ShowCreation(cbox), FadeIn(Ct), run_time=1.0)
    scene.say("行群 ", "$C(T)$", "：只在同一行裡互換的排列", wait=3.0)

    def moved(p, color, extra=None):
        parts = [Tex(perm_tex(p) + "T=", font_size=38, fill_color=color), tableau_mob(act(p, TA), cs=0.5)]
        if extra is not None:
            parts.append(extra)
        return VGroup(*parts).arrange(RIGHT, buff=0.25)

    m12 = moved(S12, ROW_COLOR).move_to(np.array([3.3, 2.15, 0]))
    m13 = moved(S13, COL_COLOR, Tex(r"\operatorname{sgn}=-1", font_size=34, fill_color=NEG_COLOR))
    m13.move_to(np.array([3.6, 0.85, 0]))
    scene.play(TransformFromCopy(d, m12[1]), FadeIn(m12[0]), run_time=1.0)
    scene.say("換標號 ", "$(1\\,2)$", "：得到 ", "$21/3$", wait=2.5)
    scene.play(TransformFromCopy(d, m13[1]), FadeIn(m13[0]), FadeIn(m13[2]), run_time=1.0)
    scene.say("換標號 ", "$(1\\,3)$", "：得到 ", "$32/1$", "，這個交換的符號是 ", "$-1$", wait=3.0)

    aT = Tex(r"a_T=e+(1\,2)", font_size=42, fill_color=ROW_COLOR)
    bT = Tex(r"b_T=e-(1\,3)", font_size=42, fill_color=COL_COLOR)
    ab = VGroup(aT, bT).arrange(RIGHT, buff=1.2).move_to(np.array([-3.0, -0.25, 0]))
    assert_in_frame(d, rbox, cbox, Rt, Ct, m12, m13, ab)
    assert_apart(VGroup(Rt, Ct), VGroup(m12, m13))
    assert_apart(VGroup(m12, m13), ab)
    scene.play(Write(aT), run_time=1.0)
    scene.play(Write(bT), run_time=1.0)
    scene.say("這裡的 ", "$+$", " 是群代數裡的形式和：兩項並排，不是先後執行", wait=4.0)

    c_def = VGroup(Tex(r"c_T=b_T\,a_T=", font_size=40), Tex(r"(e-(1\,3))", font_size=40, fill_color=COL_COLOR),
                   Tex(r"(e+(1\,2))", font_size=40, fill_color=ROW_COLOR)).arrange(RIGHT, buff=0.12)
    c_def.move_to(np.array([-3.0, -1.4, 0]))
    cw, rh = 1.55, 0.62
    tbl = VGroup()
    origin = np.array([2.0, -0.55, 0])
    heads_c = [(r"e", ROW_COLOR), (r"(1\,2)", ROW_COLOR)]
    heads_r = [(r"e", COL_COLOR), (r"-(1\,3)", COL_COLOR)]
    for j, (t, col) in enumerate(heads_c):
        tbl.add(Tex(t, font_size=34, fill_color=col).move_to(origin + (j + 1) * cw * RIGHT))
    for i, (t, col) in enumerate(heads_r):
        tbl.add(Tex(t, font_size=34, fill_color=col).move_to(origin + (i + 1) * rh * 1.4 * DOWN))
    tbl.add(Line(origin + 0.5 * cw * RIGHT + 0.35 * DOWN, origin + 2.6 * cw * RIGHT + 0.35 * DOWN, stroke_color=GREY_B, stroke_width=2))
    tbl.add(Line(origin + 0.55 * cw * RIGHT + 0.25 * UP, origin + 0.55 * cw * RIGHT + 3.2 * rh * DOWN, stroke_color=GREY_B, stroke_width=2))
    cells = VGroup()
    for i, q in enumerate((E3, S13)):
        for j, p in enumerate((E3, S12)):
            g = compose(q, p)
            coef = sign(q)
            body = perm_tex(g)
            t = Tex(("-" if coef < 0 else "+") + body, font_size=34, fill_color=NEG_COLOR if coef < 0 else POS_COLOR)
            t.move_to(origin + (j + 1) * cw * RIGHT + (i + 1) * rh * 1.4 * DOWN)
            cells.add(t)
    assert_in_frame(c_def, tbl, cells)
    assert_apart(c_def, VGroup(tbl, cells))
    scene.play(FadeOut(m12), FadeOut(m13), run_time=0.5)
    scene.play(Write(c_def), run_time=1.2)
    scene.say("Young 對稱化子 ", "$c_T=b_T\\,a_T$", "：先列求和，再對每一項做行交錯", wait=3.5)
    scene.play(FadeIn(tbl), run_time=0.8)
    scene.play(LaggedStartMap(FadeIn, cells, lag_ratio=0.3), run_time=1.6)
    scene.say("乘法表展開成四項：", "$(1\\,3)(1\\,2)=(1\\,2\\,3)$", "，符號跟著 ", "$b_T$", wait=5.5)
    scene.say("順序不能換：", "$a_T\\,b_T$", " 的最後一項是 ", "$-(1\\,3\\,2)$", "，所以 ", "$a_Tb_T\\ne b_Ta_T$", wait=5.5)


def part_conjugate(scene):
    d = tableau_mob(TA, cs=0.8, center=np.array([-4.2, 0.9, 0]))
    rbox = cells_box(d, [(0, 0), (0, 1)], ROW_COLOR)
    sig = Tex(r"\sigma=(2\,3)", font_size=42, fill_color=OP_COLOR).next_to(d, UP, buff=0.5)
    f1 = Tex(r"R(\sigma T)=\sigma\,R(T)\,\sigma^{-1}", font_size=44).move_to(np.array([2.4, 1.6, 0]))
    f2 = Tex(r"\{e,(1\,3)\}=(2\,3)\{e,(1\,2)\}(2\,3)", font_size=40, fill_color=ROW_COLOR).next_to(f1, DOWN, buff=0.6)
    assert_in_frame(d, sig, f1, f2)
    assert_apart(VGroup(d, sig), VGroup(f1, f2))
    scene.play(FadeIn(d), ShowCreation(rbox), run_time=1.0)
    scene.say("把編號整個換掉：", "$\\sigma=(2\\,3)$", " 把 2、3 對調", wait=2.0)
    scene.play(FadeIn(sig), run_time=0.6)
    newT = act(S23, TA)
    anims = []
    for i, r in enumerate(newT):
        for j, v in enumerate(r):
            old = d.entry(i, j)
            if old.tab_value != v:
                anims.append(Transform(old, Tex(str(v), font_size=56 * 0.8, fill_color=OP_COLOR).move_to(old)))
    scene.play(*anims, run_time=1.2)
    scene.say("格子沒動，只換了標號：", "$\\sigma T_a=13/2=T_b$", "，框跟著格子走", wait=3.5)
    scene.play(Write(f1), run_time=1.0)
    scene.play(FadeIn(f2), run_time=1.0)
    scene.say("新的列群，就是舊的列群用 ", "$\\sigma$", " 共軛", wait=4.0)


def part_big(scene):
    T = STD32[0]
    d = tableau_mob(T, cs=0.75, center=np.array([-4.0, 0.7, 0]))
    rb = VGroup(*[cells_box(d, [(i, j) for j in range(len(r))], ROW_COLOR) for i, r in enumerate(T)])
    cb = VGroup(*[cells_box(d, [(i, j) for i in range(len(T)) if j < len(T[i])], COL_COLOR, buff=0.12, sw=3)
                  for j in range(len(T[0]))])
    ex = VGroup(Tex(r"(4\,5)\in R(T)", font_size=38, fill_color=ROW_COLOR),
                Tex(r"(1\,4)\in C(T)", font_size=38, fill_color=COL_COLOR)).arrange(DOWN, buff=0.4)
    cnt = VGroup(Tex(r"\#R(T)=3!\cdot 2!=12", font_size=40, fill_color=ROW_COLOR),
                 Tex(r"\#C(T)=2!\cdot 2!\cdot 1!=4", font_size=40, fill_color=COL_COLOR)).arrange(DOWN, buff=0.4)
    right = VGroup(ex, cnt).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(np.array([2.6, 0.7, 0]))
    assert_in_frame(d, rb, cb, right)
    assert_apart(VGroup(d, cb), right)
    scene.play(FadeIn(d), ShowCreation(rb), FadeIn(ex[0]), run_time=1.2)
    scene.wait(1.5)
    scene.play(rb.animate.set_stroke(opacity=0.3), ShowCreation(cb), FadeIn(ex[1]), run_time=1.0)
    scene.wait(1.5)
    scene.say("大一點的 ", "$(3,2)$", "：列裡換、行裡換，各舉一例就好", wait=3.5)
    scene.play(Write(cnt), run_time=1.2)
    scene.say("只報數目：", "$\\#R=12$", "、", "$\\#C=4$", "，不必播 48 個組合", wait=4.0)


class SceneF29RowsColumns(ChuScene):
    def construct(self):
        self.show_header("座位表與兩種洗牌")
        check_math()
        part_shapes(self)
        self.clear_stage()
        part_standard21(self)
        self.clear_stage()
        part_standard32(self)
        self.clear_stage()
        part_symmetrizers(self)
        self.clear_stage()
        part_conjugate(self)
        self.clear_stage()
        part_big(self)
        self.wait(1.0)
