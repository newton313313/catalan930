"""
Scene F35 —— 誘導積與 Fulton 的字典（Fulton §7.3；原大綱卡 F715、F716、F713 回顧、X704 精簡）
執行（在 codes/ 內）：manimgl scenes/sceneF35_induction_dictionary.py SceneF35InductionDictionary

1. 兩桌標號 → 合併洗牌 → V∘W = Ind(V⊗W)；I_1∘I_1 = S^(2) ⊕ S^(1,1) 對 h_1² = s_2 + s_11；與同一 S_n 的張量積區分。
2. h, e, p, s 回顧一句；φ(h_λ) = [M^λ]、ψ；三角形展開＋等距 ⇒ φ(s_λ) = [S^λ]。
3. LR：S^21∘S^21 含 2 S^321（兩個 LR 斜表）；Hopf 一句。
"""
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import X_MAX, SkewMob, assert_apart, assert_in_frame, tuple_str
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import load
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import (h_lambda, is_reverse_lattice, kostka, lr_tableaux, p_lambda, poly_scale, poly_sum,
                            schur_expand, standard_tableaux, z_lambda)

V_COLOR, W_COLOR = TEAL_C, PURPLE_B
INVALID_LR = ((None, None, 2), (None, 1), (1,))


# ----------------------------------------------------------------------------- 資料
def nz(f):
    return {k: v for k, v in f.items() if v != 0}


def reading_word(S):
    """由上往下、每列由右往左。"""
    return [v for row in S for v in reversed(row) if v is not None]


def is_lattice(w) -> bool:
    cnt = {}
    for v in w:
        cnt[v] = cnt.get(v, 0) + 1
        if v > 1 and cnt[v] > cnt.get(v - 1, 0):
            return False
    return True


def psi_M21():
    """ψ([M^(2,1)]) = Σ χ_M(μ)/z(μ) p_μ，回傳 [(係數, μ)]。"""
    cs = load("character_S3")
    return [(Fraction(c, z), tuple(t)) for c, z, t in zip(cs["permutation"]["21"], cs["z"], cs["types"])]


def check_math():
    assert math.comb(5, 3) == 10
    assert nz(schur_expand(h_lambda((1, 1), 2), 2)) == {(2,): 1, (1, 1): 1}
    assert len(standard_tableaux((2,))) + len(standard_tableaux((1, 1))) == 2 == math.comb(2, 1)
    sf = load("symmetric_functions")
    assert sf["h21"] == "s3+s21" and sf["schur21"] == "h2*h1-h3"
    assert nz(schur_expand(h_lambda((2, 1), 3), 3)) == {(3,): 1, (2, 1): 1}
    assert [kostka(l, (2, 1)) for l in ((3,), (2, 1), (1, 1, 1))] == [1, 1, 0]
    cs = load("character_S3")
    assert [z_lambda(tuple(t)) for t in cs["types"]] == cs["z"] == [6, 2, 3]
    psi = poly_sum([poly_scale(p_lambda(mu, 3), c) for c, mu in psi_M21()])
    assert nz(psi) == nz(h_lambda((2, 1), 3))
    assert [c for c, _ in psi_M21()] == [Fraction(1, 2), Fraction(1, 2), 0]
    lr = load("LR_example")
    L = lr_tableaux(tuple(lr["nu"]), tuple(lr["lambda"]), tuple(lr["mu"]))
    assert len(L) == lr["multiplicity"] == 2
    assert [reading_word(S) for S in L] == lr["valid_reading_words"]
    assert all(is_lattice(reading_word(S)) and is_reverse_lattice(tuple(reversed(reading_word(S)))) for S in L)
    assert reading_word(INVALID_LR) == lr["invalid_reading_word"] and not is_lattice(lr["invalid_reading_word"])
    cells = sorted([i + 1, j + 1] for i, row in enumerate(L[0]) for j, v in enumerate(row) if v is not None)
    assert cells == sorted(lr["skew_cells"])
    assert sum(lr["nu"]) == sum(lr["lambda"]) + sum(lr["mu"]) == 6


# ----------------------------------------------------------------------------- 小工具
def table(labels, color, seat=0.5):
    seats = VGroup(*[Circle(radius=seat / 2).set_stroke(color, 3).set_fill(color, 0.2) for _ in labels])
    seats.arrange(RIGHT, buff=0.18)
    nums = VGroup(*[Tex(str(v), font_size=30).move_to(s) for v, s in zip(labels, seats)])
    box = RoundedRectangle(width=seats.get_width() + 0.5, height=seat + 0.45, corner_radius=0.2)
    box.set_stroke(GREY_B, 2).move_to(seats)
    return VGroup(box, seats, nums)


def wall(title, items, color, center):
    cards = VGroup(*[Tex(t, font_size=36) for t in items]).arrange(DOWN, buff=0.35)
    head = Tex(title, font_size=40, fill_color=color)
    body = VGroup(head, cards).arrange(DOWN, buff=0.3)
    box = SurroundingRectangle(body, buff=0.25).set_stroke(color, 2.5)
    return VGroup(box, head, cards).move_to(center)


# ----------------------------------------------------------------------------- 1. 誘導積
def part_induction(scene):
    A = table([1, 2, 3], V_COLOR)
    B = table([4, 5], W_COLOR)
    tables = VGroup(A, B).arrange(RIGHT, buff=0.7).move_to(np.array([-3.5, 1.7, 0]))
    la = Tex("S_3\\curvearrowright V", font_size=32, fill_color=V_COLOR).next_to(A, UP, buff=0.2)
    lb = Tex("S_2\\curvearrowright W", font_size=32, fill_color=W_COLOR).next_to(B, UP, buff=0.2)
    ext = Tex("V\\otimes W", font_size=36).next_to(tables, DOWN, buff=0.3)
    scene.say("兩桌標號互不重疊：", "$S_n\\times S_m$", " 各管各的桌，得到 ", "$V\\otimes W$")
    scene.play(FadeIn(tables), FadeIn(la), FadeIn(lb), run_time=1.0)
    scene.play(FadeIn(ext), run_time=0.6)
    scene.wait(6.5)

    order = [1, 4, 2, 5, 3]
    row = table(order, GREY_B).move_to(np.array([-3.5, -1.2, 0]))
    src = {v: m for v, m in zip([1, 2, 3], A[2])}
    src.update({v: m for v, m in zip([4, 5], B[2])})
    for v, s in zip(order, row[1]):
        s.set_stroke(V_COLOR if v <= 3 else W_COLOR, 3).set_fill(V_COLOR if v <= 3 else W_COLOR, 0.2)
    shuffle = zh("合併成一桌：新的洗牌讓兩桌交錯", font_size=24, color=OP_COLOR).next_to(row, UP, buff=0.25)
    scene.say("合併成 5 個座位，", "$S_{n+m}$", " 的洗牌可以把兩桌的人交錯排")
    scene.play(FadeIn(row[0]), FadeIn(row[1]), FadeIn(shuffle), run_time=0.8)
    scene.play(*[TransformFromCopy(src[v], m) for v, m in zip(order, row[2])], run_time=1.6)
    scene.wait(4.5)

    f1 = Tex("V\\circ W=\\operatorname{Ind}_{S_n\\times S_m}^{S_{n+m}}(V\\otimes W)", font_size=36)
    f2 = Tex("\\dim(V\\circ W)=\\binom{n+m}{n}\\dim V\\,\\dim W", font_size=34)
    f3 = Tex("\\binom{5}{3}=" + str(math.comb(5, 3)), font_size=32, fill_color=MUTED_COLOR)
    forms = VGroup(f1, f2, f3).arrange(DOWN, buff=0.35).move_to(np.array([3.4, 0.3, 0]))
    scene.say("這就是誘導：", "$V\\circ W=\\operatorname{Ind}(V\\otimes W)$", "，每個座位分法一份")
    scene.play(Write(f1), run_time=1.2)
    scene.play(FadeIn(f2), run_time=0.8)
    scene.play(FadeIn(f3), run_time=0.6)
    assert_in_frame(tables, la, lb, ext, row, shuffle, forms)
    assert_apart(VGroup(tables, la, lb, ext, row, shuffle), forms)
    scene.wait(6.5)
    scene.play(FadeOut(VGroup(tables, la, lb, ext, row, shuffle, forms)), run_time=0.6)

    # n = m = 1
    one = VGroup(table([1], V_COLOR), table([2], W_COLOR)).arrange(RIGHT, buff=0.5).move_to(np.array([-4.6, 1.9, 0]))
    arr = Tex("\\longrightarrow", font_size=40).next_to(one, RIGHT, buff=0.3)
    u12, u21 = table([1, 2], GREY_B), table([2, 1], GREY_B)
    for t, labs in ((u12, (1, 2)), (u21, (2, 1))):
        for v, s in zip(labs, t[1]):
            s.set_stroke(V_COLOR if v == 1 else W_COLOR, 3).set_fill(V_COLOR if v == 1 else W_COLOR, 0.2)
    cosets = VGroup(u12, u21).arrange(RIGHT, buff=0.4).next_to(arr, RIGHT, buff=0.3)
    names = VGroup(Tex("u_{12}", font_size=30).next_to(u12, DOWN, buff=0.15),
                   Tex("u_{21}", font_size=30).next_to(u21, DOWN, buff=0.15))
    scene.say("最小的例子 ", "$n=m=1$", "：兩個單人桌合併，只有兩種坐法")
    scene.play(FadeIn(one), run_time=0.7)
    scene.play(Write(arr), FadeIn(cosets), FadeIn(names), run_time=1.0)
    scene.wait(5.5)

    plus = Tex("u_{12}+u_{21}", font_size=36, fill_color=POS_COLOR)
    minus = Tex("u_{12}-u_{21}", font_size=36, fill_color=NEG_COLOR)
    pl = mixed("$(12)$", "：乘 ", "$+1$", font_size=24)
    ml = mixed("$(12)$", "：乘 ", "$-1$", font_size=24)
    vecs = VGroup(VGroup(plus, pl).arrange(RIGHT, buff=0.3), VGroup(minus, ml).arrange(RIGHT, buff=0.3))
    vecs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(np.array([-3.3, 0.0, 0]))
    shapes = VGroup(YoungDiagramMob((2,), cell_size=0.4), YoungDiagramMob((1, 1), cell_size=0.4))
    for sh, v in zip(shapes, vecs):
        sh.next_to(v, RIGHT, buff=0.5)
    shapes.set_x(0.4)
    scene.say("這是 ", "$S_2$", " 的正則表示：拆成平凡線與 sign 線")
    scene.play(FadeIn(vecs[0]), FadeIn(shapes[0]), run_time=0.8)
    scene.play(FadeIn(vecs[1]), FadeIn(shapes[1]), run_time=0.8)
    eqR = Tex("\\mathbb{I}_1\\circ\\mathbb{I}_1=S^{(2)}\\oplus S^{(1,1)}", font_size=38)
    eqL = Tex("h_1^2=s_{(2)}+s_{(1,1)}", font_size=38, fill_color=OP_COLOR)
    eqs = VGroup(eqR, eqL).arrange(DOWN, buff=0.3).move_to(np.array([-2.6, -1.9, 0]))
    scene.say("表示這邊的分解，正好對上對稱函數的 ", "$h_1^2=s_2+s_{11}$")
    scene.play(Write(eqR), run_time=1.0)
    scene.play(Write(eqL), run_time=1.0)
    scene.wait(5.5)

    side = VGroup(mixed("同一個 ", "$S_n$", " 裡的張量積 ", "$V\\otimes W$", "：", font_size=22),
                  zh("群不變、格數不相加、係數是 Kronecker 數", font_size=22),
                  mixed("本章的 ", "$\\circ$", " 換群、格數相加、係數是 LR", font_size=22, color=OP_COLOR))
    side.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    sbox = SurroundingRectangle(side, buff=0.2).set_stroke(MUTED_COLOR, 2)
    sidebox = VGroup(sbox, side)
    if sidebox.get_width() > 5.6:
        sidebox.set_width(5.6)
    sidebox.next_to(np.array([X_MAX - 0.1, -1.5, 0]), LEFT, buff=0)
    scene.say("別和同一個 ", "$S_n$", " 裡的張量積搞混：那是另一種乘法")
    scene.play(FadeIn(sidebox), run_time=0.8)
    assert_in_frame(one, arr, cosets, names, vecs, shapes, eqs, sidebox)
    assert_apart(VGroup(vecs, shapes, eqs), sidebox)
    assert_apart(VGroup(one, cosets, names), vecs)
    scene.wait(6.5)
    scene.say("$R=\\bigoplus_nR_n$", "：直和是加法，", "$\\circ$", " 是乘法，次數 ", "$n+m$", wait=8.0)


# ----------------------------------------------------------------------------- 2. 字典
def part_dictionary(scene):
    recap = VGroup(Tex("h_2=\\sum_{i\\le j}x_ix_j", font_size=28), Tex("e_2=\\sum_{i<j}x_ix_j", font_size=28),
                   Tex("p_2=\\sum_i x_i^2", font_size=28), Tex("s_{(2,1)}=h_2h_1-h_3", font_size=28))
    recap.arrange(RIGHT, buff=0.6).move_to(np.array([0, 2.6, 0])).set_color(MUTED_COLOR)
    scene.say("回顧 F25–F27：", "$h$", "、", "$e$", "、", "$p$", "、", "$s$", " 四族對稱函數")
    scene.play(LaggedStartMap(FadeIn, recap, lag_ratio=0.25), run_time=1.2)
    scene.wait(5.5)

    L = wall("\\Lambda", ["h_\\lambda", "s_\\lambda"], OP_COLOR, np.array([-4.8, 0.8, 0]))
    R = wall("R", ["[M^\\lambda]", "[S^\\lambda]"], ROW_COLOR, np.array([4.8, 0.8, 0]))
    phi = Arrow(np.array([-3.4, 1.35, 0]), np.array([3.4, 1.35, 0]), buff=0).set_color(GREY_A)
    phl = Tex("\\varphi", font_size=36).next_to(phi, UP, buff=0.08)
    psi = Arrow(np.array([3.4, 0.25, 0]), np.array([-3.4, 0.25, 0]), buff=0).set_color(GREY_A)
    psl = Tex("\\psi", font_size=36).next_to(psi, DOWN, buff=0.08)
    hm = Tex("\\varphi(h_\\lambda)=[M^\\lambda]", font_size=36, fill_color=ROW_COLOR).move_to(np.array([0, 0.8, 0]))
    scene.say("Fulton 的字典 ", "$\\varphi:\\Lambda\\to R$", "：先把 ", "$h_\\lambda$", " 送到置換模組 ", "$[M^\\lambda]$")
    scene.play(FadeIn(L), FadeIn(R), run_time=1.0)
    scene.play(GrowArrow(phi), FadeIn(phl), run_time=0.8)
    scene.play(FadeIn(hm), run_time=0.7)
    scene.wait(5.5)

    e1 = Tex("h_{(2,1)}=s_{(3)}+s_{(2,1)}", font_size=38, fill_color=OP_COLOR)
    e2 = Tex("M^{(2,1)}=S^{(3)}\\oplus S^{(2,1)}", font_size=38, fill_color=ROW_COLOR)
    tri = VGroup(e1, e2).arrange(DOWN, buff=0.3).move_to(np.array([0, -1.5, 0]))
    scene.say("兩邊是同一個三角形展開：係數都是 Kostka 數（F34 的 Young's rule）")
    scene.play(Write(e1), run_time=1.0)
    scene.play(Write(e2), run_time=1.0)
    assert_in_frame(recap, L, R, phl, psl, hm, tri)
    assert_apart(VGroup(L, R, phi, hm), tri)
    scene.wait(6.5)

    scene.play(FadeOut(tri), run_time=0.5)
    pf = Tex("\\psi([V])=\\sum_{\\mu\\vdash n}\\frac{\\chi_V(C(\\mu))}{z(\\mu)}\\,p_\\mu", font_size=36)
    terms = "+".join(f"\\frac{{{c.numerator}}}{{{c.denominator}}}p_{{{tuple_str(mu)}}}" for c, mu in psi_M21() if c)
    ex = Tex("\\psi([M^{(2,1)}])=" + terms + "=h_2h_1", font_size=34)
    VGroup(pf, ex).arrange(DOWN, buff=0.35).move_to(np.array([0, -1.5, 0]))
    scene.say("反方向 ", "$\\psi$", "：把特徵標按 ", "$z(\\mu)$", " 加權，組回對稱函數")
    scene.play(GrowArrow(psi), FadeIn(psl), run_time=0.8)
    scene.play(Write(pf), run_time=1.2)
    scene.wait(4.5)
    scene.say("例：", "$M^{(2,1)}$", " 的特徵標 3、1、0 除以 ", "$z=6,2,3$", "，得回 ", "$h_2h_1$")
    scene.play(Write(ex), run_time=1.2)
    assert_in_frame(pf, ex)
    scene.wait(6.5)

    scene.play(FadeOut(VGroup(pf, ex)), run_time=0.5)
    ip = VGroup(Tex("\\langle p_\\mu,p_\\nu\\rangle=\\delta_{\\mu\\nu}\\,z(\\mu)", font_size=34),
                Tex("\\langle s_\\lambda,s_\\nu\\rangle=\\delta_{\\lambda\\nu}", font_size=34),
                mixed("$\\varphi$", " 是等距", font_size=26, color=OP_COLOR)).arrange(RIGHT, buff=0.7)
    ip.move_to(np.array([0, -1.0, 0]))
    scene.say("兩邊的內積對得上：", "$\\varphi$", " 保持內積（等距）")
    scene.play(FadeIn(ip), run_time=0.9)
    scene.wait(5.5)
    a1 = Tex("\\varphi(s_\\lambda)=[S^\\lambda]+\\sum_{\\nu\\ne\\lambda}a_\\nu[S^\\nu]", font_size=34)
    a2 = Tex("1=\\langle s_\\lambda,s_\\lambda\\rangle=1+\\sum_{\\nu\\ne\\lambda}a_\\nu^2\\ \\Rightarrow\\ a_\\nu=0", font_size=34)
    args = VGroup(a1, a2).arrange(DOWN, buff=0.3).move_to(np.array([0, -1.5, 0]))
    scene.say("三角形展開給出首項係數 1（", "$a_\\nu$", " 是整數）")
    scene.play(FadeOut(ip), run_time=0.5)
    scene.play(Write(a1), run_time=1.2)
    scene.wait(4.5)
    scene.say("等距性逼其他係數全為 0——配對同形狀不是巧合")
    scene.play(Write(a2), run_time=1.2)
    assert_in_frame(ip, args)
    scene.wait(5.5)
    final = Tex("\\varphi(s_\\lambda)=[S^\\lambda]", font_size=44, fill_color=POS_COLOR)
    tag = zh("環同構＋等距", font_size=24, color=POS_COLOR)
    fin = VGroup(final, tag).arrange(RIGHT, buff=0.5).move_to(hm)
    scene.play(FadeOut(hm), FadeIn(fin, scale=1.1), run_time=0.9)
    assert_in_frame(fin)
    scene.say("結論：", "$\\varphi(s_\\lambda)=[S^\\lambda]$", "；", "$\\varphi$", " 是環同構，也是等距", wait=8.0)


# ----------------------------------------------------------------------------- 3. LR
def part_lr(scene):
    lr = load("LR_example")
    L = lr_tableaux(tuple(lr["nu"]), tuple(lr["lambda"]), tuple(lr["mu"]))
    items = [(S, True) for S in L] + [(INVALID_LR, False)]
    cards = VGroup()
    for S, ok in items:
        sk = SkewMob(S, cs=0.5)
        w = Tex("\\,".join(map(str, reading_word(S))), font_size=34).next_to(sk, DOWN, buff=0.3)
        mark = Tex("\\checkmark" if ok else "\\times", font_size=36,
                   fill_color=POS_COLOR if ok else NEG_COLOR).next_to(w, RIGHT, buff=0.25)
        cards.add(VGroup(sk, w, mark))
    cards.arrange(RIGHT, buff=1.4).move_to(np.array([0.6, 1.65, 0]))
    shape_lab = Tex("(3,2,1)/(2,1)", font_size=32, fill_color=MUTED_COLOR).next_to(cards, LEFT, buff=0.5)
    scene.say("LR 係數（見 F23）：", "$(3,2,1)/(2,1)$", " 的三格，填內容 ", "$(2,1)$")
    scene.play(FadeIn(shape_lab), LaggedStartMap(FadeIn, VGroup(*[c[0] for c in cards]), lag_ratio=0.3), run_time=1.4)
    scene.wait(4.5)
    scene.say("由上往下、每列由右往左讀：112、121 合格，211 一開頭就是 2")
    scene.play(LaggedStartMap(FadeIn, VGroup(*[VGroup(c[1], c[2]) for c in cards]), lag_ratio=0.3), run_time=1.4)
    scene.play(cards[2].animate.set_opacity(0.4), run_time=0.6)
    scene.wait(5.5)

    c_tex = Tex(f"c^{{(3,2,1)}}_{{(2,1),(2,1)}}={lr['multiplicity']}", font_size=40, fill_color=OP_COLOR)
    prod = Tex("S^{(2,1)}\\circ S^{(2,1)}=2\\,S^{(3,2,1)}\\oplus\\cdots", font_size=40)
    res = VGroup(c_tex, prod).arrange(DOWN, buff=0.3).next_to(cards, DOWN, buff=0.4)
    scene.say("兩張 LR 表，所以 ", "$S^{(3,2,1)}$", " 在 ", "$S^{(2,1)}\\circ S^{(2,1)}$", " 裡出現兩次")
    scene.play(Write(c_tex), run_time=1.0)
    scene.play(Write(prod), run_time=1.0)
    assert_in_frame(shape_lab, cards, res)
    assert_apart(cards, res)
    scene.wait(5.5)
    scene.say("這裡只展示這一項；格數 ", "$6=3+3$", "，完整分解還有別的形狀", wait=6.5)

    hopf = Tex("\\Delta(s_\\nu)=\\sum_{\\lambda,\\mu}c^\\nu_{\\lambda\\mu}\\,s_\\lambda\\otimes s_\\mu", font_size=36)
    hopf.next_to(res, DOWN, buff=0.3)
    hbox = SurroundingRectangle(hopf, buff=0.12).set_stroke(MUTED_COLOR, 2)
    scene.say("Hopf 觀點：同一組 ", "$c$", " 也是限制到 ", "$S_p\\times S_q$", " 的重數（含 ", "$p=0$", " 或 ", "$q=0$", "）")
    scene.play(FadeIn(hopf), ShowCreation(hbox), run_time=1.0)
    assert_in_frame(hopf, hbox)
    scene.wait(6.0)


class SceneF35InductionDictionary(ChuScene):
    def construct(self):
        self.show_header("誘導積與 Fulton 的字典")
        check_math()
        part_induction(self)
        self.clear_stage()
        part_dictionary(self)
        self.clear_stage()
        part_lr(self)
        self.wait(1.0)
