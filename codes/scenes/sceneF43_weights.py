"""
Scene F43 —— 對角矩陣數格子：權重（Fulton §8.2–8.3，書 p.112–120；原大綱卡 F801）
執行（在 codes/ 內）：manimgl scenes/sceneF43_weights.py SceneF43Weights

diag(x_1,x_2,x_3)：e_T ↦ x^T e_T；F42 的 8 個半標準表按權重（content）分 7 堆，x_1x_2x_3 那堆 2 個；
最高權重向量 e_{U(λ)} = 11/2，權重 (2,1,0)；多項式不可約表示 ↔ 至多 m 列的 λ；Char E^λ = s_λ。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import content, partitions, schur_poly, ssyt

LAM = (2, 1)
M = 3
SS = ssyt(LAM, M)
SLOW = 3.6
HEX_C = np.array([-3.2, 0.15, 0])
HEX_S = 1.2
U_DIR = [np.array([np.cos(a), np.sin(a), 0.0]) for a in (PI / 6, 5 * PI / 6, 3 * PI / 2)]


def groups_by_weight():
    g = {}
    for T in SS:
        g.setdefault(content(T, M), []).append(T)
    return g


def mono_tex(w):
    out = ""
    for k, e in enumerate(w, start=1):
        if e == 1:
            out += "x_%d" % k
        elif e > 1:
            out += "x_%d^%d" % (k, e)
    return out or "1"


def weight_pos(w):
    return HEX_C + HEX_S * sum((w[k] - 1) * U_DIR[k] for k in range(3))


def fit(mob, width):
    if mob.get_width() > width:
        mob.set_width(width)
    return mob


def check_math():
    g = groups_by_weight()
    assert len(SS) == 8 and len(g) == 7
    assert g[(1, 1, 1)] == [((1, 2), (3,)), ((1, 3), (2,))]
    assert {w: len(v) for w, v in g.items()} == schur_poly(LAM, M)
    assert max(g) == (2, 1, 0) == LAM + (0,) and g[(2, 1, 0)] == [((1, 1), (2,))]
    assert sum(schur_poly(LAM, M).values()) == 8 and schur_poly(LAM, M)[(1, 1, 1)] == 2
    assert content(((1, 2), (3,)), M) == (1, 1, 1) and content(((1, 1), (2,)), M) == (2, 1, 0)
    assert schur_poly((1, 1, 1), 2) == {}
    assert [sum(schur_poly(l, 3).values()) for l in ((3,), (2, 1), (1, 1, 1))] == [10, 8, 1]
    assert sum(schur_poly((3,), 2).values()) == 4 and sum(schur_poly((2, 1), 2).values()) == 2
    for lam in partitions(3):
        assert (len(lam) <= 3) == bool(schur_poly(lam, 3))
    for w in g:                                   # 7 個權重都在 a+b+c=3 的平面上，六角形＋中心
        assert sum(w) == 3


# ---------------------------------------------------------------- 1. 只看對角矩陣
def part_diagonal(scene):
    mat = MatrixMob([["x_1", "0", "0"], ["0", "x_2", "0"], ["0", "0", "x_3"]], font_size=36)
    gl = Tex(r"g=", font_size=40)
    gmat = VGroup(gl, mat).arrange(RIGHT, buff=0.2).move_to(np.array([-4.3, 1.4, 0]))
    for k in range(3):
        mat.entry(k, k).set_fill(OP_COLOR)
    rule = Tex(r"e_i\mapsto x_i\,e_i", font_size=44).move_to(np.array([2.6, 1.9, 0]))
    rule2 = Tex(r"e_T\mapsto x^T e_T", font_size=44, fill_color=OP_COLOR).move_to(np.array([2.6, 1.0, 0]))
    Ta, Tb = ((1, 2), (3,)), ((1, 1), (2,))
    da = tableau_mob(Ta, cs=0.75, center=np.array([-3.6, -1.3, 0]))
    db = tableau_mob(Tb, cs=0.75, center=np.array([1.2, -1.3, 0]))
    assert_in_frame(gmat, rule, rule2, da, db)
    assert_apart(gmat, rule)

    scene.say(r"$GL(E)$", " 太大了；先只看對角矩陣", wait=SLOW * 0.3)
    scene.play(FadeIn(gmat), run_time=1.0)
    scene.say("對角矩陣把每個基底向量 ", "$e_i$", " 乘上 ", "$x_i$", wait=SLOW * 0.3)
    scene.play(Write(rule), run_time=0.9)
    scene.wait(SLOW * 0.8)
    scene.say("表 ", "$T$", " 的每一格都乘一次：格子裡是 ", "$i$", " 就乘 ", "$x_i$", wait=SLOW * 0.3)
    scene.play(FadeIn(da), run_time=0.7)
    cells = [(0, 0), (0, 1), (1, 0)]
    facs = VGroup(*[Tex("x_%d" % Ta[i][j], font_size=44, fill_color=OP_COLOR) for i, j in cells])
    resa = VGroup(Tex(r"\mapsto", font_size=44), *facs, Tex("e_T", font_size=44)).arrange(RIGHT, buff=0.1)
    resa.next_to(da, RIGHT, buff=0.35)
    scene.play(FadeIn(resa[0]), *[TransformFromCopy(da.entry(i, j), f) for (i, j), f in zip(cells, facs)],
               run_time=1.3)
    scene.play(FadeIn(resa[-1]), run_time=0.5)
    scene.wait(SLOW * 0.8)
    scene.play(FadeIn(db), run_time=0.7)
    facs_b = VGroup(*[Tex("x_%d" % Tb[i][j], font_size=44, fill_color=OP_COLOR) for i, j in cells])
    resb = VGroup(Tex(r"\mapsto", font_size=44), *facs_b, Tex("e_T", font_size=44)).arrange(RIGHT, buff=0.1)
    resb.next_to(db, RIGHT, buff=0.35)
    scene.play(FadeIn(resb[0]), *[TransformFromCopy(db.entry(i, j), f) for (i, j), f in zip(cells, facs_b)],
               run_time=1.3)
    scene.play(FadeIn(resb[-1]), run_time=0.5)
    mono_b = Tex(mono_tex(content(Tb, M)), font_size=44, fill_color=OP_COLOR).move_to(VGroup(*facs_b))
    scene.play(ReplacementTransform(VGroup(*facs_b), mono_b), run_time=0.8)
    assert_in_frame(resa, resb)
    assert_apart(resa, db)
    scene.say("每個 ", "$e_T$", " 都是特徵向量，特徵值 ", "$x^T$", " 只看每個數出現幾次", wait=SLOW * 0.3)
    scene.play(Write(rule2), run_time=0.9)
    scene.say("出現次數 ", "$(1,1,1)$", "、", "$(2,1,0)$", "：這就是表的 content，叫做權重", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 2. 8 個表按權重分堆
def part_piles(scene):
    g = groups_by_weight()
    tabs = [tableau_mob(T, cs=0.45) for T in SS]
    row = VGroup(*tabs).arrange(RIGHT, buff=0.75).move_to(np.array([0, 0.8, 0]))
    labs = [Tex(mono_tex(content(T, M)), font_size=28, fill_color=OP_COLOR).next_to(t, DOWN, buff=0.4)
            for T, t in zip(SS, tabs)]
    assert_in_frame(row, *labs)

    scene.say("把 F42 的 8 個半標準表都算出 ", "$x^T$", wait=SLOW * 0.3)
    scene.play(LaggedStart(*[FadeIn(t) for t in tabs], lag_ratio=0.1), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(l, shift=0.15 * DOWN) for l in labs], lag_ratio=0.1), run_time=1.4)
    scene.wait(SLOW * 0.8)

    # 目標位置：六角形的頂點＋中心
    hexagon = Polygon(*[weight_pos(w) for w in ((2, 1, 0), (1, 2, 0), (0, 2, 1), (0, 1, 2), (1, 0, 2), (2, 0, 1))],
                      stroke_color=MUTED_COLOR, stroke_width=2, stroke_opacity=0.5)
    anims, new_labs, targets = [], [], {}
    sc = 0.32 / 0.45
    for T, t, lab in zip(SS, tabs, labs):
        w = content(T, M)
        pile = g[w]
        p = weight_pos(w)
        if len(pile) == 2:
            p = p + (pile.index(T) - 0.5) * 0.9 * RIGHT
        targets[T] = p
        anims.append(t.animate.scale(sc).move_to(p))
    for w, pile in g.items():
        txt = ("2" if len(pile) == 2 else "") + mono_tex(w)
        nl = Tex(txt, font_size=24, fill_color=OP_COLOR).move_to(weight_pos(w) + 0.5 * DOWN)
        new_labs.append((w, nl))
    assert_in_frame(hexagon, *[nl for _, nl in new_labs])

    scene.say("相同權重的放在一起：8 個表分成 7 堆", wait=SLOW * 0.3)
    scene.play(*anims, FadeOut(VGroup(*labs)), run_time=1.8)
    scene.play(ShowCreation(hexagon), *[FadeIn(nl) for _, nl in new_labs], run_time=1.2)
    centre = VGroup(*[t for T, t in zip(SS, tabs) if content(T, M) == (1, 1, 1)])
    box = SurroundingRectangle(centre, buff=0.12, color=OP_COLOR)
    scene.say("中間那堆有 2 個：", "$12/3$", " 和 ", "$13/2$", " 的權重都是 ", "$(1,1,1)$", wait=SLOW * 0.3)
    scene.play(ShowCreation(box), run_time=0.8)
    scene.wait(SLOW * 1.5)
    scene.play(FadeOut(box), run_time=0.4)
    scene.say("其他 6 堆各 1 個，排成一個六角形", wait=SLOW * 1.2)
    scene.say("權重 ", "$(a,b,c)$", "：1 出現 ", "$a$", " 次、2 出現 ", "$b$", " 次、3 出現 ", "$c$", " 次，",
              "$a+b+c=3$", wait=SLOW * 1.2)
    return tabs, hexagon, new_labs


# ---------------------------------------------------------------- 3. 最高權重
def part_highest(scene, tabs):
    top = tabs[SS.index(((1, 1), (2,)))]
    box = SurroundingRectangle(top, buff=0.12, color=OP_COLOR)
    U = YoungDiagramMob(LAM, cell_size=0.85, center=np.array([3.4, 1.4, 0]), entries=[[1, 1], [2]], font_size=40)
    U.cell(0, 0).set_fill(ROW_COLOR, opacity=0.45)
    U.cell(0, 1).set_fill(ROW_COLOR, opacity=0.45)
    U.cell(1, 0).set_fill(ROW_COLOR, opacity=0.2)
    name = Tex(r"e_{U(\lambda)}", font_size=44, fill_color=OP_COLOR).next_to(U, LEFT, buff=0.5)
    wt = Tex(r"\text{weight}=(2,1,0)=\lambda", font_size=40).move_to(np.array([3.3, -0.55, 0]))
    note = zh("第 i 列全填 i", font_size=26, color=ROW_COLOR).next_to(U, DOWN, buff=0.3)
    lex = zh("字典序：先比 1 出現幾次，再比 2……", font_size=24, color=MUTED_COLOR).move_to(np.array([3.3, -1.5, 0]))
    assert_in_frame(U, name, wt, note, lex)
    assert_apart(name, top)
    assert_apart(wt, note)

    scene.say("哪一堆最「高」？比權重的字典序：", "$x_1$", " 的次數越多越高", wait=SLOW * 0.3)
    scene.play(ShowCreation(box), run_time=0.8)
    scene.play(FadeIn(lex), run_time=0.6)
    scene.wait(SLOW * 1.0)
    scene.say("最高的是 ", "$11/2$", "，權重 ", "$(2,1,0)$", "：正好就是 ", r"$\lambda$", wait=SLOW * 0.3)
    scene.play(TransformFromCopy(top, U), FadeIn(name), run_time=1.2)
    scene.play(FadeIn(note), Write(wt), run_time=1.0)
    scene.say("例如 ", "$(2,0,1)$", "：1 一樣是 2 次，再比 2 的次數 ", "$0<1$", "，所以比 ", "$(2,1,0)$", " 低",
              wait=SLOW * 1.2)
    scene.say("最高權重向量 ", r"$e_{U(\lambda)}$", "：每一列都填自己的列號", wait=SLOW * 1.5)
    scene.play(FadeOut(VGroup(U, name, wt, note, lex, box)), run_time=0.7)


# ---------------------------------------------------------------- 4. 特徵標 = Schur 多項式
def part_character(scene):
    poly = schur_poly(LAM, M)
    keys = sorted(poly, reverse=True)
    l1 = Tex(r"\operatorname{Char}E^{(2,1)}=\sum_T x^T", font_size=38)
    terms = []
    for k, w in enumerate(keys):
        c = poly[w]
        terms.append(Tex(("+" if k else "=") + (str(c) if c > 1 else "") + mono_tex(w), font_size=36,
                         fill_color=OP_COLOR if c > 1 else WHITE))
    l2 = VGroup(*terms[:4]).arrange(RIGHT, buff=0.1)
    l3 = VGroup(*terms[4:]).arrange(RIGHT, buff=0.1)
    l4 = Tex(r"=s_{(2,1)}(x_1,x_2,x_3)", font_size=40, fill_color=POS_COLOR)
    block = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    fit(block, 5.6).move_to(np.array([3.5, 0.3, 0]))
    assert len(terms) == 7 and sum(poly.values()) == 8
    assert_in_frame(block)

    scene.say("把 8 個 ", "$x^T$", " 全部加起來，就是這個表示的特徵標", wait=SLOW * 0.3)
    scene.play(Write(l1), run_time=1.0)
    scene.play(LaggedStart(*[FadeIn(t) for t in terms], lag_ratio=0.12), run_time=2.0)
    scene.say("7 種單項式；", "$x_1x_2x_3$", " 的係數是 2，對應中間那堆", wait=SLOW * 0.3)
    scene.play(Indicate(terms[keys.index((1, 1, 1))], color=OP_COLOR), run_time=1.0)
    scene.wait(SLOW * 1.0)
    scene.say("這正是第 6 章的 Schur 多項式 ", r"$s_\lambda$", wait=SLOW * 0.3)
    scene.play(Write(l4), run_time=1.0)
    scene.say("令所有 ", "$x_i=1$", "：係數加起來 ", r"$=8=\dim E^{(2,1)}$", wait=SLOW * 1.2)
    scene.say(r"$\operatorname{Char}E^\lambda=s_\lambda(x_1,\dots,x_m)$", "：同一個物件換了身分", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 5. 分類：至多 m 列
def part_classify(scene):
    head = mixed("多項式不可約表示 ", r"$\leftrightarrow$", " 至多 ", "$m$", " 列的 ", r"$\lambda$", font_size=32)
    head.move_to(np.array([0, 2.5, 0]))
    lams = [(3,), (2, 1), (1, 1, 1)]
    xs = (-4.0, 0.0, 4.0)
    diags, labs = [], []
    for lam, x in zip(lams, xs):
        d = YoungDiagramMob(lam, cell_size=0.5, center=np.array([x, 1.0, 0]))
        diags.append(d)
        n = sum(schur_poly(lam, 2).values())
        txt = r"\dim E^{%s}=%d" % ("(" + ",".join(map(str, lam)) + ")", n)
        labs.append(Tex(txt, font_size=34, fill_color=NEG_COLOR if n == 0 else POS_COLOR)
                    .move_to(np.array([x, -0.5, 0])))
    sub = Tex(r"m=2,\ n=3", font_size=36, fill_color=MUTED_COLOR).move_to(np.array([0, -1.45, 0]))
    cross = Cross(diags[2], stroke_color=NEG_COLOR, stroke_width=5)
    assert_in_frame(head, *diags, *labs, sub)
    assert_apart(labs[1], labs[2], 0.2)

    scene.say("哪些 ", r"$\lambda$", " 真的出現？", wait=SLOW * 0.3)
    scene.play(FadeIn(head), run_time=1.0)
    scene.play(FadeIn(sub), *[FadeIn(d) for d in diags], run_time=1.0)
    scene.say(r"$m=2$", "：數字只有 1、2", wait=SLOW * 0.3)
    scene.play(LaggedStart(*[Write(l) for l in labs], lag_ratio=0.3), run_time=1.8)
    scene.say(r"$(1,1,1)$", " 的一行要放 3 個不同的數，", r"$m=2$", " 不夠：沒有半標準表", wait=SLOW * 0.3)
    scene.play(ShowCreation(cross), run_time=0.8)
    scene.wait(SLOW * 1.2)
    scene.say(r"$m=3$", " 時三個形狀都在，維度依序是 10、8、1", wait=SLOW * 1.0)
    scene.say("所以 ",r"$E^\lambda\neq0$", " 恰好當 ", r"$\lambda$", " 至多 ", "$m$", " 列；這些就是全部的多項式不可約表示",
              wait=SLOW * 1.5)
    scene.say("收束：權重就是 content，特徵標就是 Schur 多項式", wait=SLOW * 1.5)


class SceneF43Weights(ChuScene):
    def construct(self):
        self.show_header("權重：用對角矩陣數格子")
        check_math()
        part_diagonal(self)
        self.clear_stage()
        tabs, hexagon, labs = part_piles(self)
        part_highest(self, tabs)
        part_character(self)
        self.clear_stage()
        part_classify(self)
        self.wait(1.0)
