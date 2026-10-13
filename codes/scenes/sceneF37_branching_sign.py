"""
Scene F37 —— 分支律與轉置（Fulton §7.3 Corollary 3、Proposition 3、Exercises 5、8；原大綱卡 F718、F719）
執行（在 codes/ 內）：manimgl scenes/sceneF37_branching_sign.py SceneF37BranchingSign

最大標號在角格 → f^λ = Σ f^{λ⁻}；Res S^(2,1) = S^(2) ⊕ S^(1,1)（特徵向量 2v_a − v_b、v_b，特徵值 +1、−1）；
Young 格 0–4 格；Ind 到 S_4：8 = 3 + 2 + 3；S^λ ⊗ U_n ≅ S^λ̃（特徵標乘 sign、ω(s_λ) = s_λ̃）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.rep_data import load, rep_matrix21
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, MatrixMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import conjugate, contains, corners, partitions, standard_tableaux

BR = load("branching")
S21 = load("shape21")
S32 = load("shape32")
CHAR = load("character_S3")
MAT = load("matrices21")
HOOKS = load("hooks")
P_CHANGE = [[1, 2], [-2, -1]]          # P ρ(σ) P⁻¹ = sgn(σ) ρ(σ)（下面 check_math 驗證）
SLOW = 1.8                             # 旁白停頓倍率


def tup(T):
    return tuple(tuple(r) for r in T)


def max_box(T):
    n = max(max(r) for r in T)
    return next((i, j) for i, r in enumerate(T) for j, v in enumerate(r) if v == n)


def remove_max(T):
    n = max(max(r) for r in T)
    return tuple(r2 for r2 in (tuple(x for x in r if x != n) for r in T) if r2)


def lam_of(T):
    return tuple(len(r) for r in T)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def neg(A):
    return [[-x for x in r] for r in A]


def lattice_edges(nodes):
    return [(a, b) for a in nodes for b in nodes if sum(b) == sum(a) + 1 and contains(b, a)]


def f_of(lam):
    return len(standard_tableaux(tuple(lam))) if lam else 1


def check_math():
    # 最大標號在角格；刪掉後仍標準
    for T, lam in zip((S21["Ta"], S21["Tb"]), BR["remove21"]):
        assert max_box(T) in corners((2, 1)) and list(lam_of(remove_max(T))) == lam
    std32 = [tup(T) for T in standard_tableaux((3, 2))]
    assert std32 == [tup(T) for T in S32["standard"]] and len(std32) == S32["f"] == 5
    for T in std32:
        assert max_box(T) in corners((3, 2)) and remove_max(T) in [tup(U) for U in standard_tableaux(lam_of(remove_max(T)))]
    assert [lam_of(remove_max(T)) for T in std32] == [(3, 1), (3, 1), (2, 2), (3, 1), (2, 2)]
    assert f_of((3, 1)) == 3 and f_of((2, 2)) == 2 and BR["f_remove"] == [f_of((2,)), f_of((1, 1))] == [1, 1]
    # 限制到 S_2 = {e, (12)}
    A = [list(r) for r in rep_matrix21((2, 1, 3))]
    assert A == MAT["rho12"]
    assert matmul(A, [[2], [-1]]) == [[2], [-1]] and matmul(A, [[0], [1]]) == [[0], [-1]]
    assert BR["restriction_eigenvalues"] == [1, -1]
    assert BR["restriction_basis"] == {"shape2": "2*va-vb", "shape11": "vb"}
    # Young 格與誘導
    nodes = [tuple(p) for p in BR["young_lattice_0_to_4"]]
    assert sorted(nodes) == sorted(tuple(p) for n in range(5) for p in partitions(n))
    add = [b for a, b in lattice_edges(nodes) if a == (2, 1)]
    assert [list(b) for b in add] == BR["add21"] == [[3, 1], [2, 2], [2, 1, 1]]
    assert [f_of(b) for b in add] == BR["f_add"] == [3, 2, 3]
    assert 4 * 2 == sum(BR["f_add"]) == BR["induced_dim"] == 8
    paths = [p for p in ([(), (1,), mid, (2, 1)] for mid in [(2,), (1, 1)])]
    assert all((p[k], p[k + 1]) in lattice_edges(nodes) for p in paths for k in range(3)) and len(paths) == f_of((2, 1))
    # 乘 sign：平凡 ↔ sign，(2,1) 不變
    sgn_row = CHAR["specht"]["111"]
    assert sgn_row == [(-1) ** (3 - len(mu)) for mu in CHAR["types"]] == [1, -1, 1]
    tw = lambda key: [a * b for a, b in zip(CHAR["specht"][key], sgn_row)]
    assert tw("3") == CHAR["specht"]["111"] and tw("111") == CHAR["specht"]["3"] and tw("21") == CHAR["specht"]["21"]
    # 轉置 (3,2) ↔ (2,2,1)
    assert list(conjugate((3, 2))) == S32["transpose"] == [2, 2, 1] and f_of((2, 2, 1)) == f_of((3, 2)) == 5
    assert HOOKS["32"]["scale"] == 24 and load("symmetric_functions")["omega_p_r"] == "(-1)^(r-1)*p_r"
    # 換基底：P A = −A P、P B = −B P、det P = 3
    B = [list(r) for r in rep_matrix21((1, 3, 2))]
    assert B == MAT["rho23"]
    P = P_CHANGE
    assert matmul(P, A) == neg(matmul(A, P)) and matmul(P, B) == neg(matmul(B, P))
    assert P[0][0] * P[1][1] - P[0][1] * P[1][0] == 3
    assert A != neg(A) and A[0][0] + A[1][1] == 0


def lam_tex(lam):
    if not lam:
        return r"\varnothing"
    if len(lam) > 1 and len(set(lam)) == 1 and lam[0] == 1:
        return "(1^" + str(len(lam)) + ")"
    return "(" + ",".join(map(str, lam)) + ")"


# ---------------------------------------------------------------- 1. 最大標號在角格
def part_corner(scene):
    t21 = [tableau_mob(S21["Ta"], cs=0.5), tableau_mob(S21["Tb"], cs=0.5)]
    for d, x in zip(t21, (-5.2, -3.4)):
        d.move_to(np.array([x, 1.75, 0]))
    t32 = [tableau_mob(T, cs=0.42) for T in S32["standard"]]
    for d, x in zip(t32, (-5.0, -2.5, 0.0, 2.5, 5.0)):
        d.move_to(np.array([x, -0.35, 0]))
    lab21 = [Tex(lam_tex(lam_of(remove_max(tup(T)))), font_size=30, fill_color=GREY_A).next_to(d, DOWN, buff=0.25)
             for T, d in zip((S21["Ta"], S21["Tb"]), t21)]
    lab32 = []
    for T, d in zip(S32["standard"], t32):
        lam = lam_of(remove_max(tup(T)))
        lab32.append(Tex(lam_tex(lam), font_size=30, fill_color=ROW_COLOR if lam == (3, 1) else COL_COLOR)
                     .next_to(d, DOWN, buff=0.25))
    f21 = Tex(r"f^{(2,1)}=f^{(2)}+f^{(1,1)}=1+1", font_size=36).move_to(np.array([2.4, 1.7, 0]))
    f32 = Tex(r"f^{(3,2)}=f^{(3,1)}+f^{(2,2)}=3+2", font_size=36).move_to(np.array([0, -2.45, 0]))
    assert_in_frame(*t21, *t32, *lab21, *lab32, f21, f32)
    assert_apart(VGroup(*t21, *lab21), f21)
    assert_apart(VGroup(*lab32), f32)
    assert_apart(VGroup(*lab21), VGroup(*t32))

    scene.say("從 ", "$S_n$", " 換到 ", "$S_{n-1}$", "，為什麼就是刪一格？", wait=SLOW * 1.0)
    scene.play(*[FadeIn(d) for d in t21], run_time=0.8)
    hl = []
    for d, T in zip(t21, (S21["Ta"], S21["Tb"])):
        i, j = max_box(T)
        hl.append(d.cell(i, j).animate.set_fill(OP_COLOR, opacity=0.4))
        hl.append(d.entry(i, j).animate.set_fill(OP_COLOR))
    scene.play(*hl, run_time=0.8)
    scene.say("標準表裡最大的數一定坐在角格：右邊、下面都沒有更大的數", wait=SLOW * 1.5)
    dim = []
    for d, T in zip(t21, (S21["Ta"], S21["Tb"])):
        i, j = max_box(T)
        dim += [d.cell(i, j).animate.set_stroke(opacity=0.2).set_fill(opacity=0.08), d.entry(i, j).animate.set_opacity(0.2)]
    scene.play(*dim, *[FadeIn(l, shift=0.15 * DOWN) for l in lab21], run_time=1.0)
    scene.say("拿掉它，剩下的仍是標準表，形狀少一個角", wait=SLOW * 1.0)
    scene.play(Write(f21), run_time=1.0)
    scene.wait(SLOW * 1.0)

    scene.play(LaggedStart(*[FadeIn(d) for d in t32], lag_ratio=0.15), run_time=1.2)
    hl, dim = [], []
    for d, T in zip(t32, S32["standard"]):
        i, j = max_box(T)
        hl += [d.cell(i, j).animate.set_fill(OP_COLOR, opacity=0.4), d.entry(i, j).animate.set_fill(OP_COLOR)]
        dim += [d.cell(i, j).animate.set_stroke(opacity=0.2).set_fill(opacity=0.08), d.entry(i, j).animate.set_opacity(0.2)]
    scene.play(*hl, run_time=0.8)
    scene.say("$(3,2)$", " 的 5 張標準表：5 坐在第一列尾或第二列尾", wait=SLOW * 1.5)
    scene.play(*dim, *[FadeIn(l, shift=0.15 * DOWN) for l in lab32], run_time=1.0)
    scene.play(Write(f32), run_time=1.0)
    scene.say("刪掉 5 後，3 張是 ", "$(3,1)$", "、2 張是 ", "$(2,2)$", "：", "$5=3+2$", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 2. 限制到 S_2
def part_restrict(scene):
    top = Tex(r"\operatorname{Res}^{S_3}_{S_2}S^{(2,1)}=S^{(2)}\oplus S^{(1,1)}", font_size=42).move_to(2.5 * UP)
    sub = mixed("$S_2=\\{e,(1\\,2)\\}$", "：只重排 1、2，忘掉 3", font_size=26).move_to(1.65 * UP)
    A = MAT["rho12"]
    eqs = []
    for vec, img, x, ev, lam, name, word in (
            ([[2], [-1]], [[2], [-1]], -3.4, 1, (2,), r"2v_a-v_b", "平凡"),
            ([[0], [1]], [[0], [-1]], 3.2, -1, (1, 1), r"v_b", "sign")):
        assert matmul(A, vec) == img
        g = VGroup(Tex(r"\rho(1\,2)", font_size=32), MatrixMob(A, font_size=32, h_buff=0.65),
                   MatrixMob(vec, font_size=32, colors={(0, 0): OP_COLOR, (1, 0): OP_COLOR}),
                   Tex("=", font_size=34), MatrixMob(img, font_size=32)).arrange(RIGHT, buff=0.18)
        g.move_to(np.array([x, 0.3, 0]))
        lbl = Tex(name, font_size=32, fill_color=OP_COLOR).next_to(g[2], UP, buff=0.25)
        evc = POS_COLOR if ev > 0 else NEG_COLOR
        evt = Tex(("+1" if ev > 0 else "-1"), font_size=40, fill_color=evc)
        evw = mixed("特徵值 ", evt, font_size=26)
        diag = YoungDiagramMob(lam, cell_size=0.4, stroke_width=2)
        tag = VGroup(diag, mixed("$S^{" + lam_tex(lam) + "}$", "（" + word + "）", font_size=26)).arrange(RIGHT, buff=0.25)
        VGroup(evw, tag).arrange(DOWN, buff=0.3).next_to(g, DOWN, buff=0.4)
        eqs.append((g, lbl, evw, tag))
    dimq = Tex(r"\dim:\ 2=1+1", font_size=34).move_to(2.55 * DOWN)
    assert_in_frame(top, sub, dimq, *[m for e in eqs for m in e])
    assert_apart(VGroup(*eqs[0]), VGroup(*eqs[1]), 0.3)
    assert_apart(sub, VGroup(eqs[0][1], eqs[1][1]))
    assert_apart(VGroup(eqs[0][3], eqs[1][3]), dimq)

    scene.play(Write(top), run_time=1.2)
    scene.play(FadeIn(sub), run_time=0.6)
    scene.say("用 F33 的矩陣 ", "$\\rho(1\\,2)$", " 直接看這個分解", wait=SLOW * 1.0)
    for g, lbl, evw, tag in eqs:
        scene.play(FadeIn(g[:3]), FadeIn(lbl), run_time=0.8)
        scene.play(FadeIn(g[3:]), run_time=0.6)
        scene.play(FadeIn(evw), FadeIn(tag), run_time=0.8)
        scene.wait(SLOW * 1.2)
    scene.play(Write(dimq), run_time=0.8)
    scene.say("$2v_a-v_b$", " 被固定（平凡），", "$v_b$", " 變號（sign）：", "$2=1+1$", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 3. Young 格
def part_lattice(scene):
    nodes = [tuple(p) for p in BR["young_lattice_0_to_4"]]
    xs = [-6.1, -4.0, -1.9, 0.2, 2.4]
    mobs = {}
    for n in range(5):
        level = [p for p in nodes if sum(p) == n]
        for k, lam in enumerate(level):
            y = 0.15 + 1.15 * ((len(level) - 1) / 2 - k)
            pos = np.array([xs[n], y, 0])
            m = Tex(r"\varnothing", font_size=34).move_to(pos) if not lam else \
                YoungDiagramMob(lam, cell_size=0.2, center=pos, stroke_width=2)
            mobs[lam] = m
    edges = {}
    for a, b in lattice_edges(nodes):
        edges[(a, b)] = Line(mobs[a].get_right() + 0.1 * RIGHT, mobs[b].get_left() + 0.1 * LEFT,
                             stroke_color=GREY_D, stroke_width=2)
    add = [tuple(b) for b in BR["add21"]]
    dims = VGroup(*[Tex(str(f), font_size=30, fill_color=POS_COLOR).next_to(mobs[b], RIGHT, buff=0.2)
                    for b, f in zip(add, BR["f_add"])])
    paths = [[(), (1,), (2,), (2, 1)], [(), (1,), (1, 1), (2, 1)]]
    tabs = VGroup(tableau_mob(S21["Ta"], cs=0.4), tableau_mob(S21["Tb"], cs=0.4)).arrange(RIGHT, buff=0.6)
    tabs.move_to(np.array([5.3, 2.2, 0]))
    chk = VGroup(Tex(r"[S_4:S_3]\cdot 2", font_size=32), Tex(r"=4\cdot 2=8", font_size=32),
                 Tex(r"=3+2+3", font_size=32, fill_color=POS_COLOR)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    chk.move_to(np.array([5.3, -0.6, 0]))
    allm = VGroup(*mobs.values(), *edges.values(), dims)
    assert_in_frame(allm, tabs, chk)
    assert_apart(allm, tabs, 0.3)
    assert_apart(allm, chk, 0.3)
    assert_apart(tabs, chk, 0.3)
    win = VGroup(zh("小窗：刪格只給出計數", font_size=20, color=MUTED_COLOR),
                 zh("證明要 Sagan 的穩定濾鏈", font_size=20, color=MUTED_COLOR)).arrange(DOWN, buff=0.12)
    if win.get_width() > 2.8:
        win.set_width(2.8)
    wbox = SurroundingRectangle(win, buff=0.12, color=GREY_D)
    wg = VGroup(wbox, win)
    wg.set_x(6.6 - wg.get_width() / 2).set_y(-2.9 + wg.get_height() / 2)
    assert_in_frame(wbox)
    assert_apart(allm, wbox, 0.1)
    assert_apart(chk, wbox, 0.1)

    scene.say("Young 格：從空圖出發，每一步加一個可加的角格", wait=SLOW * 0.3)
    for n in range(5):
        new = [mobs[p] for p in nodes if sum(p) == n]
        es = [e for (a, b), e in edges.items() if sum(b) == n]
        scene.play(*[ShowCreation(e) for e in es], *[FadeIn(m) for m in new], run_time=0.8)
    scene.wait(SLOW * 1.0)
    for path, t in zip(paths, tabs):
        es = [edges[(path[k], path[k + 1])] for k in range(3)]
        scene.play(*[e.animate.set_stroke(OP_COLOR, width=5) for e in es], FadeIn(t), run_time=0.9)
        scene.wait(SLOW * 0.6)
        scene.play(*[e.animate.set_stroke(GREY_D, width=2) for e in es], run_time=0.5)
    scene.say("一條從 ", "$\\varnothing$", " 走到 ", "$\\lambda$", " 的路＝一張標準表：路的條數就是 ", "$f^\\lambda$", wait=SLOW * 2.0)

    scene.play(mobs[(2, 1)].animate.set_fill(OP_COLOR, opacity=0.5), run_time=0.6)
    down = [edges[(a, (2, 1))] for a in [(2,), (1, 1)]]
    scene.play(*[e.animate.set_stroke(ROW_COLOR, width=5) for e in down], run_time=0.8)
    scene.say("往左刪角＝限制：", "$\\operatorname{Res}S^{(2,1)}=S^{(2)}\\oplus S^{(1,1)}$", wait=SLOW * 1.8)
    up = [edges[((2, 1), b)] for b in add]
    scene.play(*[e.animate.set_stroke(POS_COLOR, width=5) for e in up], run_time=0.8)
    scene.play(LaggedStart(*[FadeIn(d, shift=0.1 * LEFT) for d in dims], lag_ratio=0.3), run_time=1.0)
    scene.say("往右加角＝誘導：", "$\\operatorname{Ind}_{S_3}^{S_4}S^{(2,1)}=S^{(3,1)}\\oplus S^{(2,2)}\\oplus S^{(2,1,1)}$",
              wait=SLOW * 2.0)
    scene.play(FadeIn(chk[0]), run_time=0.6)
    scene.play(FadeIn(chk[1]), run_time=0.6)
    scene.play(TransformFromCopy(dims, chk[2]), run_time=0.9)
    scene.say("維度核對：", "$[S_4:S_3]\\cdot 2=8=3+2+3$", "（這裡用的是 ", "$f^\\lambda$", "）", wait=SLOW * 2.5)
    scene.play(FadeIn(win), ShowCreation(wbox), run_time=0.8)
    scene.say("數格子只說明維度對得上；真正的證明要一條穩定的子模組濾鏈", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 4. 乘 sign ＝ 轉置
def part_transpose(scene):
    keys, lams = ["3", "21", "111"], [(3,), (2, 1), (1, 1, 1)]
    sgn_row = CHAR["specht"]["111"]
    Lx, Rx, ys = [-4.1, -3.0, -1.9], [3.1, 4.2, 5.3], [1.3, 0.45, -0.4]
    heads = VGroup(*[Tex(lam_tex(tuple(mu)), font_size=26, fill_color=GREY_A).move_to(np.array([x, 2.1, 0]))
                     for mu, x in zip(CHAR["types"], Lx)])
    heads_r = heads.copy().shift((Rx[0] - Lx[0]) * RIGHT)
    left_lbl, left_vals, right_lbl, right_vals = VGroup(), [], VGroup(), []
    for key, lam, y in zip(keys, lams, ys):
        left_lbl.add(Tex(lam_tex(lam), font_size=30).move_to(np.array([-5.6, y, 0])))
        left_vals.append(VGroup(*[Tex(str(v), font_size=32).move_to(np.array([x, y, 0]))
                                  for v, x in zip(CHAR["specht"][key], Lx)]))
        prod = [v * s for v, s in zip(CHAR["specht"][key], sgn_row)]
        tl = lams[[CHAR["specht"][k] for k in keys].index(prod)]
        assert tl == tuple(conjugate(lam))
        right_vals.append(VGroup(*[Tex(str(v), font_size=32).move_to(np.array([x, y, 0])) for v, x in zip(prod, Rx)]))
        right_lbl.add(Tex(lam_tex(tl), font_size=30, fill_color=OP_COLOR if tl != lam else WHITE)
                      .move_to(np.array([6.3, y, 0])))
    srow = VGroup(Tex(r"\operatorname{sgn}", font_size=30, fill_color=GREY_A).move_to(np.array([-5.6, -1.45, 0])),
                  *[Tex(str(s), font_size=32, fill_color=POS_COLOR if s > 0 else NEG_COLOR).move_to(np.array([x, -1.45, 0]))
                    for s, x in zip(sgn_row, Lx)])
    srow_box = SurroundingRectangle(srow, buff=0.12, color=GREY_C)
    arrow = Arrow(np.array([-1.1, 0.45, 0]), np.array([2.2, 0.45, 0]), stroke_color=OP_COLOR)
    alab = Tex(r"\times\operatorname{sgn}", font_size=30, fill_color=OP_COLOR).next_to(arrow, UP, buff=0.1)
    tbl = VGroup(heads, heads_r, left_lbl, *left_vals, *right_vals, right_lbl, srow, srow_box, arrow, alab)
    assert_in_frame(tbl)
    assert_apart(VGroup(*left_vals, srow_box), arrow)
    assert_apart(arrow, VGroup(*right_vals))

    scene.say("另一個小符號：每個奇置換都乘上 ", "$-1$", wait=SLOW * 0.5)
    scene.play(FadeIn(heads), FadeIn(left_lbl), *[FadeIn(v) for v in left_vals], run_time=1.0)
    scene.play(FadeIn(srow), ShowCreation(srow_box), run_time=0.8)
    scene.say("$S_3$", " 的特徵標表每一列，逐項乘上 sign 列 ", "$1,-1,1$", wait=SLOW * 1.0)
    scene.play(GrowArrow(arrow), FadeIn(alab), FadeIn(heads_r), run_time=0.8)
    for lv, rv, rl in zip(left_vals, right_vals, right_lbl):
        scene.play(TransformFromCopy(VGroup(lv, srow[1:]), rv), run_time=0.9)
        scene.play(FadeIn(rl, shift=0.1 * LEFT), run_time=0.4)
    scene.say("平凡和 sign 互換；", "$(2,1)$", " 是自共軛，特徵標不變", wait=SLOW * 2.5)
    scene.clear_stage()

    d1 = YoungDiagramMob((3, 2), cell_size=0.55, center=np.array([-3.6, 1.2, 0]))
    d2 = YoungDiagramMob((2, 2, 1), cell_size=0.55, center=np.array([0.6, 1.2, 0]))
    d1.fill_cells([(0, 0), (0, 1), (0, 2)], ROW_COLOR, 0.45)
    d2.fill_cells([(0, 0), (1, 0), (2, 0)], COL_COLOR, 0.45)
    tr = Tex(r"\longleftrightarrow", font_size=40).move_to(np.array([-1.5, 1.2, 0]))
    f1 = Tex(r"f^{(3,2)}=5", font_size=32).next_to(d1, DOWN, buff=0.3)
    f2 = Tex(r"f^{(2,2,1)}=5", font_size=32).next_to(d2, DOWN, buff=0.3)
    iso = Tex(r"S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}", font_size=40).move_to(np.array([4.6, 1.2, 0]))
    om = Tex(r"\omega(h_r)=e_r,\quad \omega(p_r)=(-1)^{r-1}p_r,\quad \omega(s_\lambda)=s_{\tilde\lambda}",
             font_size=34).move_to(np.array([0, -1.2, 0]))
    om2 = Tex(r"\omega(p_\mu)=(-1)^{n-\ell(\mu)}p_\mu=\operatorname{sgn}(\sigma)\,p_\mu", font_size=34).move_to(om)
    assert_in_frame(d1, d2, f1, f2, iso, om, om2)
    assert_apart(VGroup(d1, f1), tr)
    assert_apart(tr, VGroup(d2, f2))
    assert_apart(VGroup(d2, f2), iso)
    assert_apart(VGroup(f1, f2), om)

    scene.play(FadeIn(d1), run_time=0.7)
    scene.play(Write(tr), TransformFromCopy(d1, d2), run_time=1.2)
    scene.say("一般地，乘 sign 把形狀轉置：", "$(3,2)$", " 的橫行變成 ", "$(2,2,1)$", " 的直欄", wait=SLOW * 1.5)
    scene.play(FadeIn(f1), FadeIn(f2), Write(iso), run_time=1.0)
    scene.wait(SLOW * 1.0)
    scene.play(Write(om), run_time=1.5)
    scene.say("對稱函數這邊就是對合 ", "$\\omega$", "：", "$h_r\\leftrightarrow e_r$", "、", "$s_\\lambda\\mapsto s_{\\tilde\\lambda}$",
              wait=SLOW * 2.0)
    scene.play(ReplacementTransform(om, om2), run_time=1.0)
    scene.say("循環型 ", "$\\mu$", " 的符號 ", "$(-1)^{n-\\ell(\\mu)}$", " 正好是 ", "$p_\\mu$", " 前的符號", wait=SLOW * 2.5)
    scene.clear_stage()

    A = MAT["rho12"]
    g1 = VGroup(Tex(r"\rho(1\,2)=", font_size=34), MatrixMob(A, font_size=32),
                Tex(r"\ne", font_size=36, fill_color=NEG_COLOR),
                Tex(r"\operatorname{sgn}(1\,2)\,\rho(1\,2)=", font_size=34), MatrixMob(neg(A), font_size=32))
    g1.arrange(RIGHT, buff=0.2).move_to(1.2 * UP)
    g2 = VGroup(Tex(r"P\rho(\sigma)P^{-1}=\operatorname{sgn}(\sigma)\rho(\sigma),", font_size=34),
                Tex("P=", font_size=34), MatrixMob(P_CHANGE, font_size=32, colors={(i, j): OP_COLOR for i in (0, 1) for j in (0, 1)}))
    g2.arrange(RIGHT, buff=0.2).move_to(0.9 * DOWN)
    assert_in_frame(g1, g2)
    assert_apart(g1, g2, 0.3)
    scene.play(FadeIn(g1), run_time=1.0)
    scene.say("注意：", "$S^{(2,1)}\\otimes\\mathbb U_3\\cong S^{(2,1)}$", " 不是說 ", "$A=-A$", wait=SLOW * 2.0)
    scene.play(FadeIn(g2, shift=0.2 * UP), run_time=1.0)
    scene.say("同構要換一組基底 ", "$P$", "；兩個矩陣的跡都是 0，但逐項不同", wait=SLOW * 2.5)


# ---------------------------------------------------------------- 5. 收束
def part_summary(scene):
    lines = VGroup(
        mixed("刪角＝限制：", r"$\operatorname{Res}S^\lambda=\bigoplus S^{\lambda^-}$", font_size=30),
        mixed("加角＝誘導：", r"$\operatorname{Ind}S^\lambda=\bigoplus S^{\lambda^+}$", font_size=30),
        mixed("乘 sign＝轉置：", r"$S^\lambda\otimes\mathbb U_n\cong S^{\tilde\lambda}$", font_size=30),
    ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(0.3 * UP)
    marks = VGroup(*[Dot(radius=0.07, fill_color=OP_COLOR).next_to(l, LEFT, buff=0.3) for l in lines])
    assert_in_frame(lines, marks)
    scene.say("收束：三個操作，都只看角格和轉置", wait=SLOW * 0.5)
    for l, m in zip(lines, marks):
        scene.play(FadeIn(m), FadeIn(l, shift=0.2 * RIGHT), run_time=0.9)
        scene.wait(SLOW * 1.2)
    scene.say("維度核對：", "$2=1+1$", "、", "$8=3+2+3$", "、", "$f^{(3,2)}=f^{(2,2,1)}=5$", wait=SLOW * 1.5)


class SceneF37BranchingSign(ChuScene):
    def construct(self):
        self.show_header("分支律與轉置")
        check_math()
        part_corner(self)
        self.clear_stage()
        part_restrict(self)
        self.clear_stage()
        part_lattice(self)
        self.clear_stage()
        part_transpose(self)
        self.clear_stage()
        part_summary(self)
        self.wait(1.0)
