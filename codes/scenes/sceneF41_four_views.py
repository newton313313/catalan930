"""
Scene F41 —— 四個視角拼成一件事（Fulton 第 7 章統整；第 8 章 §8.1、§8.3 只作預告；原大綱卡 F725）
執行（在 codes/ 內）：manimgl scenes/sceneF41_four_views.py SceneF41FourViews

λ = (2,1) 居中，四角：列 tabloid 子模 span(v_T)、群代數 A·c_T、行 tabloid 商 M̃/Q、標準基底。
三個快問 dim M = 3、dim S = 2、c² 的尺度 3；整個 S_3：6 = 1 + 2·2 + 1；操作鏈；
第 8 章預告：E^(2,1) 在 m = 3 是 8 維，S^(2,1) 仍是 2 維（兩章的維度分開標）。
"""
import sys
from math import factorial, prod
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import gr_mul, load, rep_matrix21, symmetrizers
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import hook_content_count, ssyt, standard_tableaux

SHAPES = [(3,), (2, 1), (1, 1, 1)]
CHAIN = ["編號", "tabloid", "交錯", "標準化", "矩陣", "特徵標", "分解"]


def check_math():
    s21 = load("shape21")
    lam = tuple(s21["lambda"])
    dim_m = factorial(3) // prod(factorial(x) for x in lam)
    assert dim_m == 3 == len(s21["tabloids"]) == load("character_S3")["permutation"]["21"][0]
    f = load("hooks")["21"]["f"]
    assert f == 2 == len(standard_tableaux(lam)) == load("character_S3")["specht"]["21"][0]
    _, _, c = symmetrizers(tuple(map(tuple, s21["Ta"])))
    assert dict(gr_mul(c, c)) == {p: 3 * v for p, v in c.items()}
    assert load("young_symmetrizer21")["n_lambda"] == 3 == load("hooks")["21"]["scale"]
    ch = load("character_S3")
    dims = [len(standard_tableaux(s)) for s in SHAPES]
    assert dims == ch["regular_dimensions"] == ch["regular_multiplicities"] == [1, 2, 1]
    assert sum(m * d for m, d in zip(ch["regular_multiplicities"], dims)) == 6 == ch["squared_dimension_sum"]
    assert len(ssyt(lam, 3)) == 8 == hook_content_count(lam, 3)          # 第 8 章：E^(2,1)，m = 3
    assert rep_matrix21((2, 1, 3)) == load("matrices21")["rho12"]
    chi = ch["specht"]["21"]
    assert chi == [2, 0, -1] and sum(z * x * x for z, x in zip(ch["sizes"], chi)) == 6   # 內積 (4+0+2)/6 = 1
    assert load("shape32")["f"] == 5 and load("hooks")["32"]["scale"] == 24


def tx(s, fs=36, color=WHITE):
    return Tex(s, font_size=fs).set_color(color)


def corner_box(title, formula, center, color):
    t = zh(title, font_size=24, color=color)
    f = tx(formula, 30)
    g = VGroup(t, f).arrange(DOWN, buff=0.22)
    r = RoundedRectangle(width=max(4.1, g.get_width() + 0.4), height=g.get_height() + 0.5, corner_radius=0.15, stroke_color=color,
                         stroke_width=2.5)
    return VGroup(r, g.move_to(r)).move_to(center)


# =============================================================================
# 第一段：四個視角
# =============================================================================
def part_views(scene):
    center = tableau_mob(tuple(map(tuple, load("shape21")["Ta"])), cs=0.6, center=np.array([0, 0.2, 0]))
    lam = tx(r"\lambda=(2,1)", 34, OP_COLOR).next_to(center, DOWN, buff=0.25)
    ul = corner_box("列 tabloid 子模", r"S^\lambda=\operatorname{span}(v_T)\subseteq M^\lambda",
                    np.array([-4.3, 1.9, 0]), ROW_COLOR)
    ur = corner_box("群代數的左理想", r"\mathbb C[S_3]\,c_T", np.array([4.3, 1.9, 0]), OP_COLOR)
    dl = corner_box("行 tabloid 商", r"\widetilde M^\lambda/Q^\lambda", np.array([-4.3, -1.6, 0]), COL_COLOR)
    dr = corner_box("標準基底", r"v_{T_a},\ v_{T_b}", np.array([4.3, -1.6, 0]), POS_COLOR)
    boxes = VGroup(ul, ur, dl, dr)
    assert_in_frame(center, lam, boxes)
    scene.play(FadeIn(center), FadeIn(lam))
    scene.say("中間是 ", "$\\lambda=(2,1)$", "：這一章的每個構造都從它出發", wait=2.6)
    scene.play(LaggedStart(*[FadeIn(b, scale=0.95) for b in boxes], lag_ratio=0.3), run_time=2.0)
    scene.say("四個角是同一個表示的四種實現", wait=3.1)
    beats = [(ul, ("左上：", "$v_T$", " 是列 tabloid 的交錯和，張成子模（F31）")),
             (ur, ("右上：群代數乘上 ", "$c_T=b_Ta_T$", "（F40）")),
             (dl, ("左下：行 tabloid 模掉交換關係（F38、F39）",)),
             (dr, ("右下：標準表給的 ", "$v_T$", " 是基底（F32）"))]
    for box, words in beats:
        scene.play(Indicate(box[0], color=OP_COLOR, scale_factor=1.03))
        scene.say(*words, wait=2.6)

    top = Arrow(ur.get_left(), ul.get_right(), buff=0.12, thickness=2.5, fill_color=GREY_B)
    top_l = tx(r"x\mapsto x\cdot\{T\}", 28).next_to(top, UP, buff=0.08)
    left = Arrow(dl.get_top(), ul.get_bottom(), buff=0.12, thickness=2.5, fill_color=GREY_B)
    left_l = VGroup(tx(r"\alpha", 32), mixed("核恰是 ", r"$Q^\lambda$", font_size=20)
                    ).arrange(DOWN, buff=0.08).next_to(left, RIGHT, buff=0.15)
    bot = Arrow(dl.get_right(), dr.get_left(), buff=0.12, thickness=2.5, fill_color=GREY_B)
    bot_l = zh("拉直：標準表給基底", font_size=20).next_to(bot, DOWN, buff=0.12)
    arrows = VGroup(top, top_l, left, left_l, bot, bot_l)
    assert_in_frame(arrows)
    assert_apart(left_l, center)
    assert_apart(bot_l, lam)
    assert_apart(top_l, center)
    scene.play(GrowArrow(top), FadeIn(top_l))
    scene.say("左理想 ", "$\\mathbb C[S_3]c_T$", " 作用在 ", "$\\{T\\}$", " 上，落到列 tabloid 子模", wait=3.1)
    scene.play(GrowArrow(left), FadeIn(left_l))
    scene.say("行 tabloid 商經 ", "$\\alpha$", " 送過去，核恰好是 ", "$Q^\\lambda$", "（F39）", wait=3.1)
    scene.play(GrowArrow(bot), FadeIn(bot_l))
    scene.say("拉直保證標準表就夠：基底有 ", "$f^\\lambda=2$", " 個", wait=3.1)
    iso = mixed("四者同構，但住在不同空間：不是逐元素相等", font_size=22, color=MUTED_COLOR)
    iso.move_to(np.array([0, -2.75, 0]))
    assert_in_frame(iso)
    assert_apart(iso, dr)
    scene.play(FadeIn(iso))
    scene.wait(2.5)


# =============================================================================
# 第二段：三個快問
# =============================================================================
def part_quiz(scene):
    qs = [(r"\dim M^{(2,1)}=", "3"), (r"\dim S^{(2,1)}=", "2"), (r"c_T^2=", "3")]
    rows = VGroup()
    for k, (q, a) in enumerate(qs):
        lhs = tx(q, 44)
        mark = tx("?", 44, OP_COLOR)
        ans = tx(a, 44, POS_COLOR)
        row = VGroup(lhs, mark)
        if k == 2:
            row.add(tx(r"\cdot c_T", 44))
        row.arrange(RIGHT, buff=0.15)
        ans.move_to(mark)
        row.ans = ans
        rows.add(row)
    rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(np.array([-0.6, 0.3, 0]))
    for r in rows:
        r.ans.move_to(r[1])
    hints = [zh("三張 tabloid", font_size=22, color=MUTED_COLOR), zh("兩個標準表", font_size=22, color=MUTED_COLOR),
             zh("鉤長 3·1·1", font_size=22, color=MUTED_COLOR)]
    for h, r in zip(hints, rows):
        h.next_to(r, RIGHT, buff=0.6).set_x(3.6)
    assert_in_frame(rows, *hints)
    scene.say("三個快問：先自己想兩秒", wait=1.1)
    for r, h in zip(rows, hints):
        scene.play(FadeIn(r))
        scene.wait(2.0)
        scene.play(Transform(r[1], r.ans), FadeIn(h))
        scene.wait(1.8)
    scene.say("$3$", "、", "$2$", "、", "$3$", "：模組、子模、對稱化子的尺度", wait=2.6)


# =============================================================================
# 第三段：整個 S_3 與操作鏈
# =============================================================================
def part_s3(scene):
    ch = load("character_S3")
    dims = ch["regular_dimensions"]
    ds = VGroup()
    for lam, d, x in zip(SHAPES, dims, (-4.0, -1.6, 0.8)):
        yd = YoungDiagramMob(lam, cell_size=0.45, center=np.array([x, 1.6, 0]))
        lab = mixed("$\\dim=" + str(d) + "$", font_size=22, color=POS_COLOR).next_to(yd, DOWN, buff=0.2)
        ds.add(VGroup(yd, lab))
    for g in ds:
        g[1].set_y(ds[2][1].get_y())
    reg = VGroup(tx("6", 48), tx("=", 48), tx("1", 48), tx("+", 48), tx(r"2\cdot2", 48, OP_COLOR), tx("+", 48),
                 tx("1", 48)).arrange(RIGHT, buff=0.18).move_to(np.array([4.3, 1.4, 0]))
    note = zh("出現次數 × 維度", font_size=20, color=OP_COLOR).next_to(reg[4], DOWN, buff=0.25)
    assert_in_frame(ds, reg, note)
    assert_apart(ds, reg)
    scene.play(LaggedStart(*[FadeIn(g) for g in ds], lag_ratio=0.3))
    scene.say("整個 ", "$S_3$", "：三個形狀，維度 1、2、1", wait=2.6)
    scene.play(Write(reg), FadeIn(note))
    scene.say("正則表示 ", "$6=1+2\\cdot2+1$", "：每個不可約出現的次數就是它的維度", wait=3.6)

    nodes = VGroup(*[zh(s, font_size=24) for s in CHAIN])
    chain = VGroup()
    for k, n in enumerate(nodes):
        chain.add(n)
        if k < len(nodes) - 1:
            chain.add(tx(r"\to", 32, MUTED_COLOR))
    chain.arrange(RIGHT, buff=0.22)
    frames = VGroup(*[SurroundingRectangle(n, buff=0.12, color=GREY_B, stroke_width=1.5) for n in nodes])
    cg = VGroup(chain, frames).move_to(np.array([0, -1.3, 0]))
    if cg.get_width() > 13.0:
        cg.set_width(13.0)
    assert_in_frame(cg)
    assert_apart(cg, VGroup(ds, note))
    scene.play(LaggedStart(*[FadeIn(m) for m in chain], lag_ratio=0.15), FadeIn(frames), run_time=2.5)
    scene.say("整章的操作鏈：從編號一路走到分解", wait=3.1)
    chi = ch["specht"]["21"]
    norm = sum(z * x * x for z, x in zip(ch["sizes"], chi)) // 6
    ex = VGroup(VGroup(tx(r"\rho(1\,2)=", 30), MatrixMob(rep_matrix21((2, 1, 3)), 28, 0.6, 0.42)).arrange(RIGHT, buff=0.1),
                tx(r"\chi^{(2,1)}=(%d,%d,%d)" % tuple(chi), 32),
                tx(r"\langle\chi,\chi\rangle=\frac{4+0+2}{6}=%d" % norm, 32)).arrange(RIGHT, buff=0.7)
    ex.next_to(cg, DOWN, buff=0.4)
    assert_in_frame(ex)
    scene.play(FadeIn(ex, lag_ratio=0.3), run_time=1.5)
    scene.say("實際算一次：矩陣、特徵標 ", "$2,0,-1$", "、內積 1，回到同一個不可約", wait=3.6)
    scene.play(LaggedStart(*[Indicate(n, color=OP_COLOR) for n in nodes], lag_ratio=0.2), run_time=2.5)
    scene.say("也能倒著走：從分解回到形狀", wait=2.6)


# =============================================================================
# 第四段：第 8 章預告
# =============================================================================
def part_preview(scene):
    steps = VGroup(
        mixed("編號 1、2、3 ", r"$\to$", " 向量空間 ", "$E$", " 裡的向量", font_size=24),
        mixed("一行 ", r"$\to$", " 楔積 ", r"$\wedge$", font_size=24),
        mixed("同一種交換關係 ", r"$\to$", " Schur 模 ", r"$E^\lambda$", font_size=24),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([0, 1.7, 0]))
    tag = zh("下一章預告", font_size=22, color=OP_COLOR).next_to(steps, UP, buff=0.25)
    e_box = VGroup(mixed(r"$E^{(2,1)}$", "（", "$m=3$", "）", font_size=24), tx(r"\dim=8", 40, OP_COLOR)
                   ).arrange(DOWN, buff=0.2)
    s_box = VGroup(mixed(r"$S^{(2,1)}$", "（本章）", font_size=24), tx(r"\dim=2", 40, POS_COLOR)).arrange(DOWN, buff=0.2)
    eg = VGroup(SurroundingRectangle(e_box, buff=0.25, color=OP_COLOR), e_box)
    sg = VGroup(SurroundingRectangle(s_box, buff=0.25, color=POS_COLOR), s_box)
    pair = VGroup(sg, eg).arrange(RIGHT, buff=2.2).move_to(np.array([0, -1.4, 0]))
    neq = zh("不要混在一起", font_size=22, color=NEG_COLOR).move_to(pair.get_center())
    assert_in_frame(steps, tag, pair, neq)
    assert_apart(steps, pair)
    assert_apart(neq, sg)
    assert_apart(neq, eg)
    scene.play(FadeIn(tag), FadeIn(steps[0]))
    scene.say("第 8 章：把編號換成 ", "$E$", " 裡的向量", wait=3.1)
    scene.play(FadeIn(steps[1:], lag_ratio=0.4))
    scene.say("行變成楔積，同樣的交換關係定義 Schur 模", wait=3.6)
    scene.play(FadeIn(sg), FadeIn(eg))
    scene.say("$m=3$", " 時 ", "$E^{(2,1)}$", " 是 8 維；", "$S^{(2,1)}$", " 仍是 2 維", wait=3.1)
    scene.play(FadeIn(neq))
    scene.say("兩章的維度分開記：一個看 ", "$m$", "，一個只看 ", "$n$", wait=3.6)
    scene.say("這一章的問題都有了答案：從形狀到矩陣，再回到形狀", wait=3.6)


class SceneF41FourViews(ChuScene):
    def construct(self):
        self.show_header("F41　四個視角拼成一件事")
        check_math()
        part_views(self)
        self.clear_stage()
        part_quiz(self)
        self.clear_stage()
        part_s3(self)
        self.clear_stage()
        part_preview(self)
        self.wait(1.0)
