"""
Scene F42 —— 把數字換成向量：Schur 模（Fulton §8.1，書 p.104–112；原大綱卡 F800）
執行（在 codes/ 內）：manimgl scenes/sceneF42_schur_module.py SceneF42SchurModule

(2,1) 的標號 1,2,3 換成 v_1,v_2,v_3 ∈ E；一列 → Sym^n E、一行 → ∧^n E；
E^λ = 各行外冪的張量積模掉交換關係（與 F39 同一條，只換符號）；基底 = 半標準表（m=2 兩個、m=3 八個）；
第 7 章數標準表 f^λ = 2（固定），第 8 章數半標準表 d_λ(m) = m(m²−1)/3（隨 m 變）。
"""
import sys
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import hook_content_count, ssyt, standard_tableaux

LAM = (2, 1)
T0 = ((1, 3), (2,))          # 交換關係的例子：第 2 行頂端的 3 與第 1 行的數交換
SLOW = 3.0                   # 旁白停頓倍率


def exchange21(T):
    """(2,1) 形：第 2 行唯一的數依序與第 1 行的每個數交換（行內上下位置不變）→ [S1, S2]。"""
    (a, c), (b,) = T
    return [((c, a), (b,)), ((a, b), (c,))]


def polytabloid21(T):
    """(2,1) 形的 e_T = {T} − {第 1 行對調後的 T}；tabloid 記成 (第 1 列的集合, 第 2 列的集合)。"""
    (a, c), (b,) = T
    out = {}
    for s, (x, y) in ((1, (a, b)), (-1, (b, a))):
        key = (frozenset((x, c)), frozenset((y,)))
        out[key] = out.get(key, 0) + s
    return {k: v for k, v in out.items() if v}


def vec_sum(*vs):
    out = {}
    for v in vs:
        for k, c in v.items():
            out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c}


def vec_label(T):
    return [["v_" + str(x) for x in r] for r in T]


def wedge_tex(T):
    """(2,1) 形的向量表 → (v_a ∧ v_b) ⊗ v_c（第 1 行外積、第 2 行單獨）。"""
    (a, c), (b,) = T
    return r"(v_%d\wedge v_%d)\otimes v_%d" % (a, b, c)


def vec_diagram(lam, labels, cs=0.8, center=ORIGIN, color=WHITE):
    return YoungDiagramMob(lam, cell_size=cs, center=center, entries=labels, font_size=40 * cs, entry_color=color)


def mark_value(d, T, v, color=OP_COLOR):
    """把表 d 裡數值 v 所在的格子塗色（回傳動畫）。"""
    i, j = next((i, j) for i, r in enumerate(T) for j, x in enumerate(r) if x == v)
    return [d.cell(i, j).animate.set_fill(color, opacity=0.35), d.entry(i, j).animate.set_fill(color)]


def check_math():
    assert ssyt(LAM, 2) == [((1, 1), (2,)), ((1, 2), (2,))]
    for m in range(1, 7):
        d = len(ssyt(LAM, m))
        assert d == hook_content_count(LAM, m) == m * (m * m - 1) // 3
        assert d == m * comb(m, 2) - comb(m, 3)          # dim(∧²E ⊗ E) − dim ∧³E
    assert len(ssyt(LAM, 3)) == 8 and len(standard_tableaux(LAM)) == 2
    S1, S2 = exchange21(T0)
    assert (S1, S2) == (((3, 1), (2,)), ((1, 2), (3,)))
    assert polytabloid21(T0) == vec_sum(polytabloid21(S1), polytabloid21(S2))   # 第 7 章：e_T = e_S1 + e_S2
    assert wedge_tex(T0) == r"(v_1\wedge v_2)\otimes v_3"


# ---------------------------------------------------------------- 1. 數字換成向量
def part_vectors(scene):
    num = tableau_mob(((1, 2), (3,)), cs=1.0, center=np.array([-3.4, 0.9, 0]))
    vec = vec_diagram(LAM, vec_label(((1, 2), (3,))), cs=1.0, center=np.array([3.4, 0.9, 0]))
    gvec = vec_diagram(LAM, [["gv_1", "gv_2"], ["gv_3"]], cs=1.0, center=vec.get_center(), color=OP_COLOR)
    arrow = Arrow(num.get_right(), vec.get_left(), buff=0.6).set_color(OP_COLOR)
    lab_num = mixed("第 7 章：格子放數字，", r"$S_3$", " 換數字", font_size=26).next_to(num, DOWN, buff=0.5)
    lab_vec = mixed("第 8 章：格子放向量 ", r"$v_i\in E$", font_size=26).next_to(vec, DOWN, buff=0.5)
    lab_g = mixed(r"$g\in GL(E)$", " 同時作用在每一格", font_size=26, color=OP_COLOR).next_to(lab_vec, DOWN, buff=0.35)
    assert_in_frame(num, vec, lab_num, lab_vec, lab_g)
    assert_apart(lab_num, lab_vec)

    scene.say("第 7 章：形狀 (2,1) 的格子裡放 1、2、3", wait=SLOW * 1.0)
    scene.play(FadeIn(num), FadeIn(lab_num, shift=0.2 * UP), run_time=1.0)
    scene.wait(SLOW * 1.0)
    scene.say("第 8 章只改一件事：把每個數字換成一個向量", wait=SLOW * 0.5)
    scene.play(GrowArrow(arrow), TransformFromCopy(num.cells, vec.cells), run_time=1.0)
    scene.play(*[TransformFromCopy(num.entry(i, j), vec.entry(i, j)) for i, j in ((0, 0), (0, 1), (1, 0))],
               run_time=1.2)
    scene.play(FadeIn(lab_vec, shift=0.2 * UP), run_time=0.7)
    scene.say(r"$E=\mathbb C^m$", "：", "$m$", " 維的向量空間；", "$v_1,v_2,v_3$", " 是 ", "$E$", " 裡的向量",
              wait=SLOW * 1.5)
    keep = vec.entries.copy()
    scene.say("作用的群換成 ", r"$GL(E)$", "：一個矩陣 ", "$g$", " 同時作用在每一格", wait=SLOW * 0.3)
    scene.play(Transform(vec.entries, gvec.entries), FadeIn(lab_g, shift=0.2 * UP), run_time=1.2)
    scene.wait(SLOW * 1.2)
    scene.play(Transform(vec.entries, keep), FadeOut(lab_g), run_time=0.9)
    scene.say("問題：這些「向量表」會張成什麼空間？", wait=SLOW * 1.2)
    scene.say("答案叫做 Schur 模 ", r"$E^\lambda$", "；這一幕把它一步一步拼出來", wait=SLOW * 1.0)


# ---------------------------------------------------------------- 2. 一列與一行
def part_extremes(scene):
    row = vec_diagram((3,), [["v_1", "v_2", "v_3"]], cs=0.85, center=np.array([-3.4, 1.4, 0]))
    row.cells.set_fill(ROW_COLOR, opacity=0.25)
    col = vec_diagram((1, 1, 1), [["v_1"], ["v_2"], ["v_3"]], cs=0.7, center=np.array([3.4, 1.15, 0]))
    col.cells.set_fill(COL_COLOR, opacity=0.25)
    row_tag = zh("一列（row）", font_size=26, color=ROW_COLOR).move_to(np.array([-3.4, 2.75, 0]))
    col_tag = zh("一行（column）", font_size=26, color=COL_COLOR).next_to(col, LEFT, buff=0.4)
    row_eq = VGroup(Tex(r"v_1v_2v_3", font_size=40), Tex("=", font_size=40, fill_color=POS_COLOR),
                    Tex(r"v_2v_1v_3", font_size=40)).arrange(RIGHT, buff=0.15).move_to(np.array([-3.4, -0.7, 0]))
    col_eq = VGroup(Tex(r"v_1\wedge v_2\wedge v_3=", font_size=40), Tex("-", font_size=40, fill_color=NEG_COLOR),
                    Tex(r"v_2\wedge v_1\wedge v_3", font_size=40)).arrange(RIGHT, buff=0.1)
    col_eq.move_to(np.array([3.4, -0.7, 0]))
    row_name = Tex(r"E^{(n)}=\operatorname{Sym}^nE", font_size=44, fill_color=ROW_COLOR).move_to(np.array([-3.4, -1.85, 0]))
    col_name = Tex(r"E^{(1^n)}={\textstyle\bigwedge^n}E", font_size=44, fill_color=COL_COLOR).move_to(np.array([3.4, -1.85, 0]))
    row_note = zh("對稱冪：順序不重要", font_size=24, color=ROW_COLOR).next_to(row_name, DOWN, buff=0.25)
    col_note = zh("外冪：交換兩個就變號", font_size=24, color=COL_COLOR).next_to(col_name, DOWN, buff=0.25)
    assert_in_frame(row, col, row_tag, col_tag, row_eq, col_eq, row_name, col_name, row_note, col_note)
    assert_apart(row_eq, col_eq)
    assert_apart(col_tag, row)

    scene.say("先看兩個極端：只有一列、或只有一行", wait=SLOW * 0.8)
    scene.play(FadeIn(row), FadeIn(row_tag), FadeIn(col), FadeIn(col_tag), run_time=1.0)
    scene.say("一列：同一列裡的向量可以隨便換位置", wait=SLOW * 0.3)
    scene.play(Swap(row.entry(0, 0), row.entry(0, 1)), run_time=1.0)
    scene.play(Write(row_eq), run_time=1.0)
    scene.play(FadeIn(row_name, shift=0.2 * UP), FadeIn(row_note), run_time=0.8)
    scene.say("這就是對稱冪 ", r"$\operatorname{Sym}^nE$", "：像多項式一樣可交換", wait=SLOW * 1.2)
    scene.say("一行：同一行裡交換兩個向量，要多一個負號", wait=SLOW * 0.3)
    scene.play(Swap(col.entry(0, 0), col.entry(1, 0)), run_time=1.0)
    scene.play(Write(col_eq), run_time=1.0)
    scene.play(Indicate(col_eq[1], color=NEG_COLOR), run_time=0.8)
    scene.play(FadeIn(col_name, shift=0.2 * UP), FadeIn(col_note), run_time=0.8)
    scene.say("這就是外冪 ", r"${\textstyle\bigwedge^n}E$", "：兩個相同就是 0", wait=SLOW * 1.2)
    scene.say("一般形狀：列像對稱冪、行像外冪，兩種規則要同時遵守", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 3. 定義：模掉同一條交換關係
def part_relation(scene):
    S1, S2 = exchange21(T0)
    small = vec_diagram(LAM, vec_label(((1, 3), (2,))), cs=0.6, center=np.array([-5.3, 2.3, 0]))
    small.cell(0, 0).set_fill(COL_COLOR, opacity=0.3)
    small.cell(1, 0).set_fill(COL_COLOR, opacity=0.3)
    small.cell(0, 1).set_fill(COL_COLOR, opacity=0.15)
    defn = mixed(r"$E^{(2,1)}=\big({\textstyle\bigwedge^2}E\big)\otimes E$", "  模掉交換關係", font_size=30)
    defn.next_to(small, RIGHT, buff=0.6)

    def relation(diags):
        return VGroup(diags[0], Tex("=", font_size=40), diags[1], Tex("+", font_size=40, fill_color=POS_COLOR),
                      diags[2]).arrange(RIGHT, buff=0.3)

    nums = [tableau_mob(T, cs=0.55) for T in (T0, S1, S2)]
    vecs = [vec_diagram(LAM, vec_label(T), cs=0.62) for T in (T0, S1, S2)]
    left = relation(nums).move_to(np.array([-3.5, 0.25, 0]))
    right = relation(vecs).move_to(np.array([3.4, 0.25, 0]))
    head_l = mixed("第 7 章（F39）：", r"$S^\lambda$", font_size=26, color=MUTED_COLOR).next_to(left, UP, buff=0.45)
    head_r = mixed("第 8 章：", r"$E^\lambda$", font_size=26, color=MUTED_COLOR).next_to(right, UP, buff=0.45)
    head_r.align_to(head_l, DOWN)
    trans = Tex(" = ".join([wedge_tex(T0), wedge_tex(S1)]) + "+" + wedge_tex(S2), font_size=36)
    trans.move_to(np.array([0, -1.25, 0]))
    m = 3
    dim = Tex(r"m=3:\quad\dim E^{(2,1)}=%d\cdot%d-%d=%d" % (comb(m, 2), m, comb(m, 3), len(ssyt(LAM, m))),
              font_size=36, fill_color=POS_COLOR).move_to(np.array([0, -2.3, 0]))
    assert_in_frame(small, defn, left, right, head_l, head_r, trans, dim)
    assert_apart(left, right, 0.3)
    assert_apart(defn, head_r)
    assert_apart(trans, VGroup(left, right))

    scene.say("形狀 (2,1)：先按行（column）做外積，再把各行乘在一起", wait=SLOW * 0.3)
    scene.play(FadeIn(small), Write(defn[0]), run_time=1.2)
    scene.wait(SLOW * 1.0)
    scene.say("但還要再模掉一條關係，就是 F39 看過的那一條", wait=SLOW * 0.3)
    scene.play(FadeIn(defn[1]), run_time=0.6)
    scene.play(FadeIn(head_l), FadeIn(left), run_time=1.0)
    scene.say("第 2 行頂端的 3，輪流和第 1 行的數交換，加起來等於原來的", wait=SLOW * 0.3)
    scene.play(*[a for d, T in zip(nums, (T0, S1, S2)) for a in mark_value(d, T, 3)], run_time=0.9)
    scene.wait(SLOW * 1.2)
    scene.say("第 8 章：同一條關係，只把數字換成向量", wait=SLOW * 0.3)
    scene.play(FadeIn(head_r), *[TransformFromCopy(a, b) for a, b in zip(left, right)], run_time=1.4)
    scene.play(*[a for d, T in zip(vecs, (T0, S1, S2)) for a in mark_value(d, T, 3)], run_time=0.9)
    scene.wait(SLOW * 1.0)
    scene.say("寫成外積：第 1 行兩格 → ", r"$\wedge$", "，第 2 行一格 → ", r"$\otimes$", wait=SLOW * 0.3)
    scene.play(Write(trans), run_time=1.6)
    scene.wait(SLOW * 1.2)
    scene.say("用處和第 7 章一樣：不夠「標準」的表，都能改寫成標準的表的組合", wait=SLOW * 1.2)
    scene.say(r"$m=3$", "：", r"${\textstyle\bigwedge^2}E\otimes E$", " 有 9 維，這條關係只砍掉 1 維", wait=SLOW * 0.3)
    scene.play(FadeIn(dim, shift=0.2 * UP), run_time=0.9)
    scene.wait(SLOW * 1.5)


# ---------------------------------------------------------------- 4. 基底＝半標準表
def part_basis(scene):
    t2 = VGroup(*[tableau_mob(T, cs=0.45) for T in ssyt(LAM, 2)]).arrange(RIGHT, buff=0.7, aligned_edge=UP)
    t3 = VGroup(*[tableau_mob(T, cs=0.45) for T in ssyt(LAM, 3)]).arrange(RIGHT, buff=0.45, aligned_edge=UP)
    lab2 = Tex(r"m=2", font_size=38, fill_color=MUTED_COLOR)
    lab3 = Tex(r"m=3", font_size=38, fill_color=MUTED_COLOR)
    row2 = VGroup(lab2, t2).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(np.array([0, 2.0, 0]))
    row3 = VGroup(lab3, t3).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(np.array([0, 0.25, 0]))
    row2.align_to(row3, LEFT)
    cnt2 = Tex(r"d_{(2,1)}(2)=%d" % len(t2), font_size=36, fill_color=POS_COLOR).next_to(t2, RIGHT, buff=0.9)
    cnt3 = Tex(r"d_{(2,1)}(3)=%d" % len(t3), font_size=36, fill_color=POS_COLOR).next_to(row3, DOWN, buff=0.45)
    formula = Tex(r"d_{(2,1)}(m)=\frac{m(m^2-1)}{3}", font_size=40).move_to(np.array([0, -2.25, 0]))
    assert_in_frame(row2, row3, cnt2, cnt3, formula)
    assert_apart(row2, row3)
    assert_apart(cnt3, formula)

    scene.say("那 ", r"$E^{(2,1)}$", " 的基底是什麼？把 ", "$v_i$", " 取成標準基底 ", "$e_i$", "，格子裡又只剩數字",
              wait=SLOW * 1.2)
    scene.say("表 ", "$T$", " 給出向量 ", "$e_T$", "；取 ", "$T$", " 半標準：列不減、行嚴格增", wait=SLOW * 0.3)
    scene.play(FadeIn(lab2), LaggedStart(*[FadeIn(t) for t in t2], lag_ratio=0.3), run_time=1.2)
    scene.play(Write(cnt2), run_time=0.7)
    scene.say(r"$m=2$", "：數字只能用 1、2，只有兩個半標準表", wait=SLOW * 1.2)
    scene.say(r"$m=3$", "：數字用 1、2、3，共八個", wait=SLOW * 0.3)
    scene.play(FadeIn(lab3), LaggedStart(*[FadeIn(t, shift=0.15 * DOWN) for t in t3], lag_ratio=0.15), run_time=2.0)
    scene.play(Write(cnt3), run_time=0.7)
    scene.say("數字可以重複：", "$11/2$", "、", "$22/3$", " 都算；但同一行（column）不能重複", wait=SLOW * 1.2)
    scene.say("定理：這些 ", "$e_T$", "（", "$T$", " 半標準）恰好是 ", r"$E^\lambda$", " 的一組基底", wait=SLOW * 1.5)
    scene.play(Write(formula), run_time=1.0)
    scene.say("維度 ", r"$d_\lambda(m)$", "：", r"$m=2,3,4$", " 依序是 2、8、20", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 5. 收束：數標準表 vs. 數半標準表
def part_compare(scene):
    std = VGroup(*[tableau_mob(T, cs=0.55) for T in standard_tableaux(LAM)]).arrange(RIGHT, buff=0.6)
    std.move_to(np.array([-3.5, 0.6, 0]))
    head7 = mixed("第 7 章：數標準表", font_size=28, color=MUTED_COLOR).next_to(std, UP, buff=0.6)
    f = Tex(r"f^{(2,1)}=%d" % len(std), font_size=44, fill_color=POS_COLOR).next_to(std, DOWN, buff=0.6)
    note7 = zh("固定，不看 m", font_size=24, color=MUTED_COLOR).next_to(f, DOWN, buff=0.3)
    ms = (1, 2, 3, 4)
    vals = [len(ssyt(LAM, m)) for m in ms]
    tbl = VGroup()
    for k, (m, d) in enumerate(zip(ms, vals)):
        tbl.add(Tex(r"m=%d" % m, font_size=34, fill_color=MUTED_COLOR).move_to(np.array([2.3, 1.0 - 0.7 * k, 0])))
        tbl.add(Tex(r"d_{(2,1)}(%d)=%d" % (m, d), font_size=36, fill_color=POS_COLOR)
                .move_to(np.array([4.4, 1.0 - 0.7 * k, 0])))
    head8 = mixed("第 8 章：數半標準表", font_size=28, color=MUTED_COLOR).move_to(np.array([3.4, head7.get_y(), 0]))
    note8 = zh("隨 m = dim E 改變", font_size=24, color=MUTED_COLOR).next_to(tbl, DOWN, buff=0.35)
    sep = DashedLine(np.array([0, 2.6, 0]), np.array([0, -2.5, 0]), color=MUTED_COLOR)
    assert vals == [0, 2, 8, 20]
    assert_in_frame(std, head7, f, note7, tbl, head8, note8)
    assert_apart(VGroup(std, head7, f, note7), VGroup(tbl, head8, note8), 0.3)

    scene.say("收束：同一張楊圖 (2,1)，兩章數的東西不一樣", wait=SLOW * 0.3)
    scene.play(ShowCreation(sep), FadeIn(head7), FadeIn(std), run_time=1.0)
    scene.play(Write(f), FadeIn(note7), run_time=0.8)
    scene.say("第 7 章數標準表：1 到 n 各用一次，", r"$f^\lambda=2$", " 是固定的", wait=SLOW * 1.2)
    scene.play(FadeIn(head8), LaggedStart(*[FadeIn(t) for t in tbl], lag_ratio=0.12), run_time=1.6)
    scene.play(FadeIn(note8), run_time=0.6)
    scene.say("第 8 章數半標準表：數字可重複，個數 ", r"$d_\lambda(m)$", " 隨 ", r"$\dim E$", " 變大", wait=SLOW * 1.5)
    scene.say(r"$m=1$", " 時是 0：一行兩格放不下兩個不同的數", wait=SLOW * 1.5)


class SceneF42SchurModule(ChuScene):
    def construct(self):
        self.show_header("Schur 模：把數字換成向量")
        check_math()
        part_vectors(self)
        self.clear_stage()
        part_extremes(self)
        self.clear_stage()
        part_relation(self)
        self.clear_stage()
        part_basis(self)
        self.clear_stage()
        part_compare(self)
        self.wait(1.0)
