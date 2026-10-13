"""
Scene F44 —— 兩個群共用一個空間：Schur–Weyl（Fulton §8.3，書 p.116–124；原大綱卡 F802）
執行（在 codes/ 內）：manimgl scenes/sceneF44_schur_weyl.py SceneF44SchurWeyl

E^{⊗3}：GL(E) 同時作用三個因子、S_3 交換因子，兩者可交換（g 與 (1 2) 對調順序結果相同）；
E^{⊗n} ≅ ⊕_λ E^λ ⊗ S^λ；維度 8 = 4·1 + 2·2 + 0·1（m=2）、27 = 10·1 + 8·2 + 1·1（m=3）；
E^λ ≅ E^{⊗n} ⊗_{C[S_n]} S^λ；列數 > m 的項為 0。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.mit_draw import YoungDiagramMob
from utils.rep_draw import NEG_COLOR, OP_COLOR, POS_COLOR
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import hook_content_count, partitions, ssyt, standard_tableaux

LAMS = [(3,), (2, 1), (1, 1, 1)]
SIG_COLOR = TEAL
SLOW = 3.6


def lam_str(lam):
    return "(" + ",".join(map(str, lam)) + ")"


def f_of(lam):
    return len(standard_tableaux(lam))


def d_of(lam, m):
    return hook_content_count(lam, m)


def act_g(g, t):
    """g 同時作用在 3 階張量的每個因子。"""
    return np.einsum("ai,bj,ck,ijk->abc", g, g, g, t)


def swap12(t):
    """(1 2)：交換第 1、2 個因子。"""
    return np.transpose(t, (1, 0, 2))


def check_math():
    assert set(partitions(3)) == set(LAMS)
    assert [f_of(l) for l in LAMS] == [1, 2, 1]
    assert [d_of(l, 2) for l in LAMS] == [4, 2, 0]
    assert [d_of(l, 3) for l in LAMS] == [10, 8, 1]
    for lam in LAMS:
        for m in (1, 2, 3, 4):
            assert d_of(lam, m) == len(ssyt(lam, m))
            assert (d_of(lam, m) == 0) == (len(lam) > m)        # 列數 > m 的項為 0
    for n in (3, 4):
        for m in (1, 2, 3, 4):
            assert m ** n == sum(d_of(l, m) * f_of(l) for l in partitions(n))
    assert 2 ** 3 == 4 * 1 + 2 * 2 + 0 * 1 and 3 ** 3 == 10 * 1 + 8 * 2 + 1 * 1
    # 兩個作用可交換：純張量與一般張量都驗
    g = np.array([[1, 2, 0], [0, 1, 1], [1, 0, 1]])
    v1, v2, v3 = np.array([1, 0, 2]), np.array([0, 3, 1]), np.array([2, 1, 0])
    t = np.einsum("i,j,k->ijk", v1, v2, v3)
    assert np.array_equal(swap12(act_g(g, t)), act_g(g, swap12(t)))
    assert np.array_equal(act_g(g, t), np.einsum("i,j,k->ijk", g @ v1, g @ v2, g @ v3))
    r = np.arange(27).reshape(3, 3, 3) % 5 - 2
    assert np.array_equal(swap12(act_g(g, r)), act_g(g, swap12(r)))


# ---------------------------------------------------------------- 1. E⊗E⊗E 上的兩個作用
def part_actions(scene):
    xs = (-2.6, 0.0, 2.6)
    Es = [Tex("E", font_size=80).move_to(np.array([x, 0.7, 0])) for x in xs]
    ots = [Tex(r"\otimes", font_size=64).move_to(np.array([(xs[k] + xs[k + 1]) / 2, 0.7, 0])) for k in range(2)]
    g = Tex("g", font_size=60, fill_color=OP_COLOR).move_to(np.array([0, 2.6, 0]))
    g_arrows = [Arrow(g.get_bottom(), E.get_top(), buff=0.15).set_color(OP_COLOR) for E in Es]
    g_lab = mixed(r"$GL(E)$", "：同時作用在三個因子", font_size=26, color=OP_COLOR).move_to(np.array([3.8, 2.6, 0]))
    sw = Arrow(Es[0].get_bottom() + 0.1 * DOWN, Es[1].get_bottom() + 0.1 * DOWN, path_arc=PI / 2.2, buff=0.1)
    sw.set_color(SIG_COLOR)
    s_lab = mixed(r"$S_3$", "：交換因子的位置", font_size=26, color=SIG_COLOR).move_to(np.array([3.8, -0.4, 0]))
    f1 = Tex(r"g\cdot(v_1\otimes v_2\otimes v_3)=gv_1\otimes gv_2\otimes gv_3", font_size=38, fill_color=OP_COLOR)
    f2 = Tex(r"(v_1\otimes v_2\otimes v_3)\cdot\sigma=v_{\sigma(1)}\otimes v_{\sigma(2)}\otimes v_{\sigma(3)}",
             font_size=38, fill_color=SIG_COLOR)
    f1.move_to(np.array([0, -1.55, 0]))
    f2.move_to(np.array([0, -2.45, 0]))
    assert_in_frame(*Es, g, g_lab, sw, s_lab, f1, f2)
    assert_apart(g_lab, Es[2])
    assert_apart(sw, f1)

    scene.say("第 7 章與第 8 章在同一個空間相遇：", r"$E^{\otimes3}=E\otimes E\otimes E$", wait=SLOW * 0.3)
    scene.play(LaggedStart(*[FadeIn(m) for m in (Es[0], ots[0], Es[1], ots[1], Es[2])], lag_ratio=0.15), run_time=1.2)
    scene.wait(SLOW * 0.8)
    scene.say("矩陣 ", "$g$", " 從左邊來，同時作用在三個因子上", wait=SLOW * 0.3)
    scene.play(FadeIn(g), *[GrowArrow(a) for a in g_arrows], FadeIn(g_lab), run_time=1.2)
    scene.play(Write(f1), run_time=1.2)
    scene.wait(SLOW * 1.0)
    scene.say("置換 ", r"$\sigma\in S_3$", " 從右邊來，只交換因子的位置", wait=SLOW * 0.3)
    scene.play(ShowCreation(sw), FadeIn(s_lab), Swap(Es[0], Es[1]), run_time=1.4)
    scene.play(Write(f2), run_time=1.2)
    scene.wait(SLOW * 1.0)
    scene.say(r"$g$", " 管每個因子「裡面」，", r"$\sigma$", " 只管「位置」：兩件事互不干擾", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 2. 兩個作用可交換
def part_commute(scene):
    fs = 40
    TL = Tex(r"v_1\otimes v_2\otimes v_3", font_size=fs).move_to(np.array([-3.3, 1.7, 0]))
    TR = Tex(r"v_2\otimes v_1\otimes v_3", font_size=fs).move_to(np.array([3.3, 1.7, 0]))
    BL = Tex(r"gv_1\otimes gv_2\otimes gv_3", font_size=fs).move_to(np.array([-3.3, -1.3, 0]))
    BR = Tex(r"gv_2\otimes gv_1\otimes gv_3", font_size=fs).move_to(np.array([3.3, -1.3, 0]))
    top = Arrow(TL.get_right(), TR.get_left(), buff=0.3).set_color(SIG_COLOR)
    bot = Arrow(BL.get_right(), BR.get_left(), buff=0.3).set_color(SIG_COLOR)
    lft = Arrow(TL.get_bottom(), BL.get_top(), buff=0.3).set_color(OP_COLOR)
    rgt = Arrow(TR.get_bottom(), BR.get_top(), buff=0.3).set_color(OP_COLOR)
    l_top = Tex(r"(1\,2)", font_size=34, fill_color=SIG_COLOR).next_to(top, UP, buff=0.15)
    l_bot = Tex(r"(1\,2)", font_size=34, fill_color=SIG_COLOR).next_to(bot, DOWN, buff=0.15)
    l_lft = Tex("g", font_size=40, fill_color=OP_COLOR).next_to(lft, LEFT, buff=0.2)
    l_rgt = Tex("g", font_size=40, fill_color=OP_COLOR).next_to(rgt, RIGHT, buff=0.2)
    eq = Tex(r"g\cdot(x\cdot\sigma)=(g\cdot x)\cdot\sigma", font_size=40, fill_color=POS_COLOR)
    eq.move_to(np.array([0, -2.4, 0]))
    assert_in_frame(TL, TR, BL, BR, l_top, l_bot, l_lft, l_rgt, eq)
    assert_apart(TL, TR, 0.8)
    assert_apart(BR, eq)

    scene.say("用一個例子看：", r"$g$", " 和交換 ", r"$(1\,2)$", "，先做哪個都一樣", wait=SLOW * 0.3)
    scene.play(FadeIn(TL), run_time=0.7)
    scene.say("路線一：先交換前兩個因子，再用 ", "$g$", wait=SLOW * 0.2)
    scene.play(GrowArrow(top), FadeIn(l_top), run_time=0.8)
    scene.play(TransformFromCopy(TL, TR), run_time=1.0)
    scene.play(GrowArrow(rgt), FadeIn(l_rgt), run_time=0.8)
    scene.play(TransformFromCopy(TR, BR), run_time=1.0)
    scene.wait(SLOW * 0.8)
    scene.say("路線二：先用 ", "$g$", "，再交換前兩個因子", wait=SLOW * 0.2)
    scene.play(GrowArrow(lft), FadeIn(l_lft), run_time=0.8)
    scene.play(TransformFromCopy(TL, BL), run_time=1.0)
    scene.play(GrowArrow(bot), FadeIn(l_bot), run_time=0.8)
    BR2 = BR.copy()
    scene.play(TransformFromCopy(BL, BR2), run_time=1.0)
    scene.remove(BR2)
    scene.play(Indicate(BR, color=POS_COLOR), run_time=1.0)
    scene.say("兩條路走到同一個向量：", r"$GL(E)$", " 和 ", "$S_3$", " 的作用可交換", wait=SLOW * 0.3)
    scene.play(Write(eq), run_time=1.0)
    scene.wait(SLOW * 1.5)


# ---------------------------------------------------------------- 3. 分解與維度表
def part_table(scene):
    head = Tex(r"E^{\otimes n}\cong\bigoplus_\lambda E^\lambda\otimes S^\lambda", font_size=44)
    head.move_to(np.array([0, 2.35, 0]))
    cx = (-3.6, -2.2, -0.8)
    ys = {"diag": 1.0, "f": 0.0, 2: -0.85, 3: -1.7}
    row_lab = {
        "f": Tex(r"f^\lambda", font_size=36, fill_color=MUTED_COLOR),
        2: Tex(r"d_\lambda(2)", font_size=36, fill_color=MUTED_COLOR),
        3: Tex(r"d_\lambda(3)", font_size=36, fill_color=MUTED_COLOR),
    }
    for k, t in row_lab.items():
        t.move_to(np.array([-5.4, ys[k], 0]))
    diags = [YoungDiagramMob(l, cell_size=0.26, center=np.array([x, ys["diag"], 0])) for l, x in zip(LAMS, cx)]
    vals = {}
    for l, x in zip(LAMS, cx):
        vals[(l, "f")] = Tex(str(f_of(l)), font_size=38).move_to(np.array([x, ys["f"], 0]))
        for m in (2, 3):
            d = d_of(l, m)
            vals[(l, m)] = Tex(str(d), font_size=38, fill_color=NEG_COLOR if d == 0 else WHITE)\
                .move_to(np.array([x, ys[m], 0]))
    sums = {}
    for m in (2, 3):
        rhs = "+".join(r"%d\cdot%d" % (d_of(l, m), f_of(l)) for l in LAMS)
        total = sum(d_of(l, m) * f_of(l) for l in LAMS)
        assert total == m ** 3
        sums[m] = Tex(r"%d^3=%d=%s" % (m, total, rhs), font_size=36, fill_color=POS_COLOR)
        if sums[m].get_width() > 5.2:
            sums[m].set_width(5.2)
        sums[m].move_to(np.array([3.6, ys[m], 0]))
    zero_box = SurroundingRectangle(VGroup(diags[2], vals[(LAMS[2], 2)]), buff=0.15, color=NEG_COLOR)
    assert_in_frame(head, *row_lab.values(), *diags, *vals.values(), *sums.values(), zero_box)
    assert_apart(head, VGroup(*diags))
    assert_apart(VGroup(*vals.values()), VGroup(*sums.values()), 0.4)

    scene.say("可交換的兩個作用，把空間切成一塊一塊", wait=SLOW * 0.3)
    scene.play(Write(head), run_time=1.4)
    scene.say("每一塊是 ", r"$E^\lambda\otimes S^\lambda$", "：同一個 ", r"$\lambda$", " 同時標記兩邊的不可約表示",
              wait=SLOW * 1.5)
    scene.say(r"$n=3$", "：三個形狀；第 7 章的 ", r"$f^\lambda$", "，第 8 章的 ", r"$d_\lambda(m)$", wait=SLOW * 0.3)
    scene.play(LaggedStart(*[FadeIn(d) for d in diags], lag_ratio=0.2), run_time=1.0)
    scene.play(FadeIn(row_lab["f"]), *[FadeIn(vals[(l, "f")]) for l in LAMS], run_time=0.9)
    scene.wait(SLOW * 0.6)
    for m in (2, 3):
        scene.play(FadeIn(row_lab[m]), LaggedStart(*[FadeIn(vals[(l, m)]) for l in LAMS], lag_ratio=0.2),
                   run_time=1.0)
        scene.say("維度相乘再相加：", r"$\dim E^{\otimes3}=%d^3$" % m, wait=SLOW * 0.2)
        scene.play(Write(sums[m]), run_time=1.3)
        scene.wait(SLOW * 1.0)
    scene.say(r"$(1,1,1)$", " 有 3 列，", r"$m=2$", " 時 ", r"$E^{(1,1,1)}=0$", "：這一塊不出現", wait=SLOW * 0.3)
    scene.play(ShowCreation(zero_box), run_time=0.8)
    scene.wait(SLOW * 1.2)
    scene.say("一般地 ", r"$m^n=\sum_\lambda d_\lambda(m)\,f^\lambda$", "；列數大於 ", "$m$", " 的項都是 0", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 4. 橋：E^λ = E^{⊗n} ⊗_{C[S_n]} S^λ
def part_bridge(scene):
    parts = VGroup(Tex(r"E^\lambda\cong", font_size=52), Tex(r"E^{\otimes n}", font_size=52, fill_color=OP_COLOR),
                   Tex(r"\otimes_{\mathbb C[S_n]}", font_size=52),
                   Tex(r"S^\lambda", font_size=52, fill_color=SIG_COLOR)).arrange(RIGHT, buff=0.12)
    parts.move_to(np.array([0, 1.9, 0]))
    lab_e = mixed("第 8 章這邊", font_size=24, color=OP_COLOR).next_to(parts[1], DOWN, buff=0.6).shift(0.8 * LEFT)
    lab_s = mixed("第 7 章的 Specht 模", font_size=24, color=SIG_COLOR).next_to(parts[3], DOWN, buff=0.6)\
        .shift(0.8 * RIGHT)
    ar_e = Arrow(lab_e.get_top(), parts[1].get_bottom(), buff=0.1).set_color(OP_COLOR)
    ar_s = Arrow(lab_s.get_top(), parts[3].get_bottom(), buff=0.1).set_color(SIG_COLOR)
    ex1 = mixed(r"$\lambda=(3)$", "：", r"$S^\lambda$", " 是平凡表示，得到 ", r"$\operatorname{Sym}^3E$", font_size=28)
    ex2 = mixed(r"$\lambda=(1,1,1)$", "：", r"$S^\lambda$", " 是符號表示，得到 ", r"${\textstyle\bigwedge^3}E$", font_size=28)
    exs = VGroup(ex1, ex2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(np.array([0, -1.5, 0]))
    assert_in_frame(parts, lab_e, lab_s, exs)
    assert_apart(lab_e, lab_s, 0.3)
    assert_apart(VGroup(lab_e, lab_s), exs)

    scene.say("怎麼從第 7 章的 ", r"$S^\lambda$", " 直接造出 ", r"$E^\lambda$", "？", wait=SLOW * 0.3)
    scene.play(Write(parts), run_time=1.6)
    scene.play(FadeIn(lab_e), GrowArrow(ar_e), FadeIn(lab_s), GrowArrow(ar_s), run_time=1.0)
    scene.say("把 ", r"$S^\lambda$", " 接在 ", r"$E^{\otimes n}$", " 的右邊，在群代數 ", r"$\mathbb C[S_n]$", " 上做張量積",
              wait=SLOW * 1.5)
    scene.say("兩個極端最好驗證", wait=SLOW * 0.3)
    scene.play(FadeIn(ex1, shift=0.2 * UP), run_time=0.8)
    scene.wait(SLOW * 0.8)
    scene.play(FadeIn(ex2, shift=0.2 * UP), run_time=0.8)
    scene.say("正好是 F42 的一列與一行", wait=SLOW * 1.2)
    scene.say("收束：同一個 ", r"$\lambda$", " 標記兩個群的不可約表示，在 ", r"$E^{\otimes n}$", " 裡成對出現",
              wait=SLOW * 1.8)


class SceneF44SchurWeyl(ChuScene):
    def construct(self):
        self.show_header("Schur–Weyl：兩個群共用一個空間")
        check_math()
        part_actions(self)
        self.clear_stage()
        part_commute(self)
        self.clear_stage()
        part_table(self)
        self.clear_stage()
        part_bridge(self)
        self.wait(1.0)
