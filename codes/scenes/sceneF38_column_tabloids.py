"""
Scene F38 —— 帶方向的行 tabloid 與交換關係（Fulton §7.4 起首、Lemma 5、Exercises 12–13；原大綱卡 F720、F721）
執行（在 codes/ 內）：manimgl scenes/sceneF38_column_tabloids.py SceneF38ColumnTabloids

列 tabloid {T} 無號、行 tabloid [qT] = sgn(q)[T]；ṽ_T = a_T[T]、α([T]) = v_T、β({T}) = ṽ_T。
商空間裡的交換關係：[21/3] = [12/3] + [23/1] = [12/3] − [13/2]（第二項排行出現 −1）；作用 α 得 v_a − v_b。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.rep_data import act, col_group, columns, load, polytabloid, row_group, sign, specht21, tabloid_key
from utils.rep_draw import (COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, ColumnTabloidMob, MatrixMob,
                            TabloidMob, signed_sum)
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh

S21 = load("shape21")
ST = load("straightening21")
YS = load("young_symmetrizer21")
MAT = load("matrices21")
TA, TB = ((1, 2), (3,)), ((1, 3), (2,))
T21 = ((2, 1), (3,))
SLOW = 2.0                                         # 旁白停頓倍率


def tup(T):
    return tuple(tuple(r) for r in T)


def from_columns(cols):
    return tuple(tuple(c[i] for c in cols if len(c) > i) for i in range(max(len(c) for c in cols)))


def sort_columns(rows):
    """每一行由小到大排好；回傳 (係數, rows)，係數 = 各行排序置換的符號乘積。"""
    coef = 1
    for c in columns(rows):
        coef *= (-1) ** sum(c[a] > c[b] for a in range(len(c)) for b in range(a + 1, len(c)))
    return coef, from_columns([sorted(c) for c in columns(rows)])


def exchanges(rows):
    """Fulton 的 π_{1,1}：右欄頂端的數和左欄的每一個數交換（其餘順序不動）。"""
    c0, c1 = columns(rows)[:2]
    out = []
    for i in range(len(c0)):
        n0, n1 = list(c0), list(c1)
        n0[i], n1[0] = c1[0], c0[i]
        out.append(from_columns([n0, n1]))
    return out


def vec_sub(u, v):
    out = dict(u)
    for k, c in v.items():
        out[k] = out.get(k, 0) - c
    return {k: c for k, c in out.items() if c}


def check_math():
    assert tup(S21["Ta"]) == TA and tup(S21["Tb"]) == TB
    assert tabloid_key(TA) == tabloid_key(T21)                       # {12/3} = {21/3}
    q = (3, 2, 1)                                                    # (13) ∈ C(T_a)
    assert q in col_group(TA) and sign(q) == -1 and act(q, TA) == ((3, 2), (1,))
    assert sort_columns(((3, 2), (1,))) == (-1, TA)                  # [32/1] = −[12/3]
    assert [list(p) for p in row_group(TA)] == S21["row_group_Ta"] and YS["row_perm"] == [2, 1, 3]
    assert act((2, 1, 3), TA) == T21 and sort_columns(T21) == (1, T21) and T21 != TA   # ṽ_T = [12/3] + [21/3]
    assert polytabloid(TA) == {TA: 1, ((2, 3), (1,)): -1} and specht21(polytabloid(TA)) == (1, 0)
    for qq in col_group(TA):                                         # α([qT]) = v_{qT} = sgn(q) v_T
        assert polytabloid(act(qq, TA)) == {k: sign(qq) * c for k, c in polytabloid(TA).items()}
    # 交換關係
    assert tup(ST["input"]) == T21 and T21[0][0] > T21[0][1]
    assert all(c == sorted(c) for c in columns(T21))
    raw = exchanges(T21)
    assert raw == [tup(r) for r in ST["raw_terms"]] == [TA, ((2, 3), (1,))]
    srt = [sort_columns(r) for r in raw]
    assert srt == [(t["coefficient"], tup(t["rows"])) for t in ST["sorted_terms"]] == [(1, TA), (-1, TB)]
    assert ST["basis_coordinates"] == [1, -1]
    # 作用 α：v_{21/3} = v_a − v_b ＝ ρ(12) 的第一欄
    assert polytabloid(T21) == vec_sub(polytabloid(TA), polytabloid(TB))
    assert list(specht21(polytabloid(T21))) == ST["basis_coordinates"] == MAT["rho12_va"]
    assert [MAT["rho12"][0][0], MAT["rho12"][1][0]] == MAT["rho12_va"]
    # 繞一圈：α∘β(v_T) = n_λ v_T，(2,1) 時 n_λ = 3
    ab_vT = {}
    for q in col_group(TA):
        S = act(q, TA)
        for p in row_group(S):
            for k, c in polytabloid(act(p, S)).items():
                ab_vT[k] = ab_vT.get(k, 0) + sign(q) * c
    ab_vT = {k: c for k, c in ab_vT.items() if c}
    assert ab_vT == {k: YS["n_lambda"] * c for k, c in polytabloid(TA).items()} and YS["n_lambda"] == 3


def row_tabloid_raw(rows, cs=0.55, color=WHITE):
    """列 tabloid，但照給定順序畫數字（用來顯示 {21/3} 和 {12/3} 是同一個）。"""
    g, fs = VGroup(), 60 * cs
    for i, r in enumerate(rows):
        y = -i * cs
        for j, v in enumerate(r):
            g.add(Tex(str(v), font_size=fs, fill_color=color).move_to(np.array([(j + 0.5) * cs, y, 0])))
        g.add(Line(np.array([0, y + cs / 2, 0]), np.array([len(r) * cs, y + cs / 2, 0]), stroke_color=GREY_B, stroke_width=2))
    yb = -(len(rows) - 0.5) * cs
    g.add(Line(np.array([0, yb, 0]), np.array([len(rows[-1]) * cs, yb, 0]), stroke_color=GREY_B, stroke_width=2))
    return g


def col_entries(mob):
    """ColumnTabloidMob 的數字：{(i, j): Tex}（依 rep_draw 的建立順序：每行先數字、再兩條直線）。"""
    out, k = {}, 0
    for j, c in enumerate(columns(mob.rows)):
        for i in range(len(c)):
            out[(i, j)] = mob.body[k]
            k += 1
        k += 2
    return out


def orient_arrow(mob, color):
    """第一行旁邊的定向箭頭：從較小的數指向較大的數。"""
    e = col_entries(mob)
    a, b = e[(0, 0)].get_center(), e[(1, 0)].get_center()
    if mob.rows[0][0] > mob.rows[1][0]:
        a, b = b, a
    x = mob.body.get_left()[0] - 0.22
    return Arrow(np.array([x, a[1], 0]), np.array([x, b[1], 0]), buff=0.0, stroke_color=color,
                 stroke_width=4, max_tip_length_to_length_ratio=0.35)


# ---------------------------------------------------------------- 1. 無號與帶號
def part_two_kinds(scene):
    divider = DashedLine(np.array([0, 2.8, 0]), np.array([0, -2.6, 0]), stroke_color=GREY_D)
    lt = zh("列 tabloid：無號", font_size=30, color=ROW_COLOR).move_to(np.array([-3.4, 2.45, 0]))
    rt = zh("行 tabloid：帶方向", font_size=30, color=COL_COLOR).move_to(np.array([3.4, 2.45, 0]))
    l1, l2 = row_tabloid_raw(TA), row_tabloid_raw(T21)
    leq = VGroup(l1, Tex("=", font_size=44), l2).arrange(RIGHT, buff=0.4).move_to(np.array([-3.4, 0.9, 0]))
    lf = Tex(r"\{pT\}=\{T\},\quad p\in R(T)", font_size=34).move_to(np.array([-3.4, -0.7, 0]))
    c1 = ColumnTabloidMob(TA, cs=0.55)
    c2 = ColumnTabloidMob(((3, 2), (1,)), cs=0.55)
    req = VGroup(c2, Tex("=", font_size=44), Tex("-", font_size=44, fill_color=NEG_COLOR), c1.copy())
    req.arrange(RIGHT, buff=0.3).move_to(np.array([3.6, 0.9, 0]))
    c1.move_to(req[3])
    req.remove(req[3])
    a1, a2 = orient_arrow(c1, POS_COLOR), orient_arrow(c2, NEG_COLOR)
    t1 = Tex("+1", font_size=30, fill_color=POS_COLOR).next_to(c1, DOWN, buff=0.3)
    t2 = Tex("-1", font_size=30, fill_color=NEG_COLOR).next_to(c2, DOWN, buff=0.3)
    swap = Tex(r"(1\,3)", font_size=30, fill_color=OP_COLOR)
    rf = Tex(r"[qT]=\operatorname{sgn}(q)[T],\quad q\in C(T)", font_size=34).move_to(np.array([3.4, -0.7, 0]))
    note = mixed("不是 Sagan 拿來比大小的無號 column class", font_size=24, color=MUTED_COLOR).move_to(np.array([3.4, -1.7, 0]))
    swap.next_to(VGroup(c2, req[1], req[2], c1), UP, buff=0.2)
    assert_in_frame(lt, rt, leq, lf, req, c1, a1, a2, t1, t2, swap, rf, note)
    assert_apart(VGroup(lt, leq, lf), divider, 0.2)
    assert_apart(divider, VGroup(rt, req, c1, a1, a2, rf, note), 0.2)
    assert_apart(VGroup(t1, t2), rf)
    assert_apart(rt, swap)

    scene.say("row tabloid 不記順序；column tabloid 為什麼要記方向？", wait=SLOW * 1.0)
    scene.play(ShowCreation(divider), FadeIn(lt), FadeIn(rt), run_time=0.8)
    scene.play(FadeIn(l1), run_time=0.6)
    scene.play(TransformFromCopy(l1, l2), FadeIn(leq[1]), run_time=1.0)
    scene.play(Write(lf), run_time=0.8)
    scene.say("列裡的數換順序，", "$\\{T\\}$", " 完全不變：只記每列是哪些數", wait=SLOW * 1.5)
    scene.play(FadeIn(c1), GrowArrow(a1), FadeIn(t1), run_time=0.9)
    scene.wait(SLOW * 0.8)
    scene.play(FadeIn(swap), TransformFromCopy(c1, c2), TransformFromCopy(a1, a2), FadeIn(t2), run_time=1.2)
    scene.say("行 tabloid 在第一行交換 1、3：箭頭翻過來，帶一個 ", "$-1$", wait=SLOW * 1.5)
    scene.play(FadeIn(req[1]), FadeIn(req[2]), run_time=0.6)
    scene.play(Write(rf), run_time=0.9)
    scene.say("$[qT]=\\operatorname{sgn}(q)[T]$", "：負號屬於向量，", "$[-T]$", " 不是新的編號", wait=SLOW * 2.0)
    scene.play(FadeIn(note), run_time=0.6)
    scene.say("這和 Sagan 用來排序的無號 column class 是不同的東西", wait=SLOW * 1.5)


# ---------------------------------------------------------------- 2. ṽ_T、α、β
def part_maps(scene):
    xl, xr = -3.4, 3.4
    lt = Tex(r"M^\lambda", font_size=40, fill_color=ROW_COLOR).move_to(np.array([xl, 2.5, 0]))
    rt = Tex(r"\widetilde M^\lambda", font_size=40, fill_color=COL_COLOR).move_to(np.array([xr, 2.5, 0]))
    ldef = VGroup(Tex("v_T=", font_size=36), Tex("b_T", font_size=36, fill_color=COL_COLOR),
                  Tex(r"\{T\}", font_size=36)).arrange(RIGHT, buff=0.1).move_to(np.array([xl, 1.7, 0]))
    rdef = VGroup(Tex(r"\widetilde v_T=", font_size=36), Tex("a_T", font_size=36, fill_color=ROW_COLOR),
                  Tex("[T]", font_size=36)).arrange(RIGHT, buff=0.1).move_to(np.array([xr, 1.7, 0]))
    lex = VGroup(Tex(r"v_{12/3}=", font_size=32),
                 signed_sum([(1, TabloidMob(TA, cs=0.42)), (-1, TabloidMob(((3, 2), (1,)), cs=0.42))], font_size=34))
    rex = VGroup(Tex(r"\widetilde v_{12/3}=", font_size=32),
                 signed_sum([(1, ColumnTabloidMob(TA, cs=0.42)), (1, ColumnTabloidMob(T21, cs=0.42))], font_size=34))
    for g, x in ((lex, xl), (rex, xr)):
        g.arrange(RIGHT, buff=0.2).move_to(np.array([x, 0.55, 0]))
    mL = Tex(r"M^\lambda", font_size=38, fill_color=ROW_COLOR).move_to(np.array([-2.3, -1.55, 0]))
    mR = Tex(r"\widetilde M^\lambda", font_size=38, fill_color=COL_COLOR).move_to(np.array([2.3, -1.55, 0]))
    beta = Arrow(mL.get_right() + 0.2 * UP + 0.15 * RIGHT, mR.get_left() + 0.2 * UP + 0.15 * LEFT, buff=0, stroke_color=GREY_A)
    alpha = Arrow(mR.get_left() + 0.2 * DOWN + 0.15 * LEFT, mL.get_right() + 0.2 * DOWN + 0.15 * RIGHT, buff=0, stroke_color=GREY_A)
    bl = Tex(r"\beta:\{T\}\mapsto\widetilde v_T", font_size=30).next_to(beta, UP, buff=0.12)
    al = Tex(r"\alpha:[T]\mapsto v_T", font_size=30).next_to(alpha, DOWN, buff=0.12)
    w1 = Tex(r"\alpha([qT])=v_{qT}=\operatorname{sgn}(q)\,v_T", font_size=34).move_to(np.array([0, 1.4, 0]))
    w2 = Tex(r"\alpha(\sigma[T])=v_{\sigma T}=\sigma\,v_T", font_size=34).move_to(np.array([0, 0.5, 0]))
    tops = VGroup(lt, rt, ldef, rdef, lex, rex)
    bottom = VGroup(mL, mR, beta, alpha, bl, al)
    assert_in_frame(tops, bottom, w1, w2)
    assert_apart(VGroup(lt, ldef, lex), VGroup(rt, rdef, rex), 0.3)
    assert_apart(VGroup(lex, rex), bl, 0.2)
    assert_apart(w2, bl, 0.2)

    scene.say("兩個空間並排：左邊用列 tabloid，右邊用行 tabloid", wait=SLOW * 1.0)
    scene.play(FadeIn(lt), FadeIn(rt), run_time=0.6)
    scene.play(FadeIn(ldef), run_time=0.8)
    scene.play(FadeIn(lex), run_time=0.9)
    scene.say("$v_T=b_T\\{T\\}$", "：在行群上帶號求和", wait=SLOW * 1.2)
    scene.play(FadeIn(rdef), run_time=0.8)
    scene.play(FadeIn(rex), run_time=0.9)
    scene.say("對稱地，", "$\\widetilde v_T=a_T[T]$", "：在列群上不帶號求和", wait=SLOW * 1.5)
    scene.play(FadeIn(mL), FadeIn(mR), run_time=0.6)
    scene.play(GrowArrow(beta), FadeIn(bl), run_time=0.9)
    scene.play(GrowArrow(alpha), FadeIn(al), run_time=0.9)
    scene.say("$\\alpha:[T]\\mapsto v_T$", "，", "$\\beta:\\{T\\}\\mapsto\\widetilde v_T$", "：方向相反的兩座橋", wait=SLOW * 2.0)
    scene.play(FadeOut(VGroup(ldef, rdef, lex, rex)), run_time=0.6)
    scene.play(Write(w1), run_time=1.0)
    scene.say("$[T]$", " 帶號，", "$\\alpha$", " 才定義得好：", "$v_{qT}$", " 本來就帶 ", "$\\operatorname{sgn}(q)$", wait=SLOW * 2.0)
    scene.play(Write(w2), run_time=1.0)
    scene.say("兩座橋都和 ", "$S_n$", " 的作用交換（等變）", wait=SLOW * 1.5)
    w3 = Tex(r"\alpha\beta(v_T)=n_\lambda\,v_T,\qquad n_{(2,1)}=" + str(YS["n_lambda"]), font_size=36)
    w3.move_to(np.array([0, 0.9, 0]))
    w3box = SurroundingRectangle(w3, buff=0.15, color=OP_COLOR)
    assert_in_frame(w3box)
    assert_apart(w3box, bl, 0.2)
    scene.play(FadeOut(VGroup(w1, w2)), run_time=0.5)
    scene.play(Write(w3), ShowCreation(w3box), run_time=1.0)
    scene.say("繞一圈回來是乘上 ", "$n_\\lambda$", "；", "$(2,1)$", " 時是 3，先不除（F40 再談）", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 3. 交換關係
def part_exchange(scene):
    note = zh("以下等式在商空間中", font_size=26, color=OP_COLOR)
    nbox = SurroundingRectangle(note, buff=0.15, color=OP_COLOR)
    banner = VGroup(nbox, note).move_to(np.array([4.6, 2.55, 0]))
    T = ColumnTabloidMob(T21, cs=0.65).move_to(np.array([-5.0, 0.35, 0]))
    eT = col_entries(T)
    rbox = SurroundingRectangle(VGroup(eT[(0, 0)], eT[(0, 1)]), buff=0.1, color=RED)
    bad = Tex("2>1", font_size=30, fill_color=RED).next_to(rbox, UP, buff=0.15)
    raw = [ColumnTabloidMob(r, cs=0.5) for r in exchanges(T21)]
    ys = [1.45, -0.85]
    for m, y in zip(raw, ys):
        m.move_to(np.array([-1.6, y, 0]))
    arrows = [Arrow(T.get_right() + 0.1 * RIGHT, m.get_left() + 0.25 * LEFT, buff=0.05, stroke_color=OP_COLOR) for m in raw]
    swaps = [Tex(r"1\leftrightarrow 2", font_size=28, fill_color=OP_COLOR), Tex(r"1\leftrightarrow 3", font_size=28, fill_color=OP_COLOR)]
    for s, a, d in zip(swaps, arrows, (UP, DOWN)):
        s.next_to(a.get_center(), d + 0.6 * LEFT, buff=0.25)
    srt = [sort_columns(r) for r in exchanges(T21)]
    ok = mixed("已是標準表 ", "$+1$", font_size=26, color=POS_COLOR).next_to(raw[0], RIGHT, buff=0.5)
    e2 = col_entries(raw[1])
    cbox = SurroundingRectangle(VGroup(e2[(0, 0)], e2[(1, 0)]), buff=0.1, color=OP_COLOR)
    eq2 = Tex("=", font_size=40).next_to(raw[1], RIGHT, buff=0.4)
    tok = Tex(str(srt[1][0]), font_size=40, fill_color=NEG_COLOR)
    tokbox = SurroundingRectangle(tok, buff=0.1, color=NEG_COLOR)
    sorted2 = ColumnTabloidMob(srt[1][1], cs=0.5)
    VGroup(VGroup(tokbox, tok), sorted2).arrange(RIGHT, buff=0.15).next_to(eq2, RIGHT, buff=0.3)
    tokbox.move_to(tok)
    why = zh("第一行 2、1 排好：一次對換", font_size=24, color=MUTED_COLOR).next_to(sorted2, RIGHT, buff=0.4)
    final = VGroup(ColumnTabloidMob(T21, cs=0.42), Tex("=", font_size=40),
                   signed_sum([(c, ColumnTabloidMob(r, cs=0.42)) for c, r in srt], font_size=40)).arrange(RIGHT, buff=0.3)
    final.move_to(np.array([2.6, -2.35, 0]))
    fbox = SurroundingRectangle(final, buff=0.15, color=POS_COLOR)
    assert_in_frame(banner, T, rbox, bad, *raw, *arrows, *swaps, ok, eq2, tokbox, sorted2, why, fbox)
    assert_apart(VGroup(raw[0], ok), banner, 0.1)
    assert_apart(VGroup(raw[1], eq2, tokbox, sorted2, why), fbox, 0.1)
    assert_apart(VGroup(T, bad), VGroup(*raw), 0.3)

    scene.play(FadeIn(banner), run_time=0.6)
    scene.say("先說好：以下的等式都在商空間 ", "$\\widetilde M^\\lambda/Q^\\lambda$", " 裡", wait=SLOW * 1.2)
    scene.play(FadeIn(T), run_time=0.6)
    scene.play(ShowCreation(rbox), FadeIn(bad), run_time=0.8)
    scene.say("$T=21/3$", "：兩行都遞增，但第一列 2>1，不是標準表", wait=SLOW * 1.5)
    scene.say("交換：固定右行頂端的 1，和左行的 2 或 3 對調，其餘順序不動", wait=SLOW * 1.2)
    for a, s, m in zip(arrows, swaps, raw):
        scene.play(GrowArrow(a), FadeIn(s), run_time=0.7)
        scene.play(TransformFromCopy(T, m), run_time=1.0)
        scene.wait(SLOW * 0.6)
    scene.play(FadeIn(ok), run_time=0.7)
    scene.say("第一支：", "$1\\leftrightarrow 2$", " 得 ", "$[12/3]$", "，直接是標準表", wait=SLOW * 1.2)
    scene.play(ShowCreation(cbox), run_time=0.6)
    scene.say("第二支：", "$1\\leftrightarrow 3$", " 得 ", "$[23/1]$", "，但第一行是 2 在 1 上面", wait=SLOW * 1.2)
    scene.play(FadeIn(eq2), FadeIn(tok), ShowCreation(tokbox), TransformFromCopy(raw[1], sorted2), run_time=1.2)
    scene.play(FadeIn(why), run_time=0.6)
    scene.say("把這一行排好要一次對換：明確的 ", "$-1$", "，不是靠顏色暗示", wait=SLOW * 2.0)
    scene.play(FadeIn(final), ShowCreation(fbox), run_time=1.2)
    scene.say("$[21/3]=[12/3]-[13/2]$", "：只用一次交換、一次排行", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 4. 作用 α，回到 F33
def part_alpha(scene):
    srt = [sort_columns(r) for r in exchanges(T21)]
    rel = VGroup(ColumnTabloidMob(T21, cs=0.45), Tex("=", font_size=40),
                 signed_sum([(c, ColumnTabloidMob(r, cs=0.45)) for c, r in srt], font_size=40)).arrange(RIGHT, buff=0.3)
    rel.move_to(np.array([-2.6, 2.1, 0]))
    arr = Arrow(np.array([-2.6, 1.4, 0]), np.array([-2.6, 0.55, 0]), buff=0, stroke_color=GREY_A)
    alab = Tex(r"\alpha", font_size=36).next_to(arr, RIGHT, buff=0.15)
    coords = ST["basis_coordinates"]
    img = VGroup(Tex(r"v_{21/3}=", font_size=38),
                 signed_sum([(coords[0], Tex("v_a", font_size=38, fill_color=POS_COLOR)),
                             (coords[1], Tex("v_b", font_size=38, fill_color=POS_COLOR))], font_size=38))
    img.arrange(RIGHT, buff=0.15).move_to(np.array([-2.6, 0.0, 0]))
    A = MatrixMob(MAT["rho12"], font_size=36, colors={(0, 0): OP_COLOR, (1, 0): OP_COLOR})
    rho = VGroup(Tex(r"\rho(1\,2)=", font_size=36), A).arrange(RIGHT, buff=0.15).move_to(np.array([3.6, 1.6, 0]))
    cbox = SurroundingRectangle(A.col(0), buff=0.12, color=OP_COLOR)
    link = Tex(r"(1\,2)\,T_a=21/3,\quad v_{21/3}=(1\,2)\,v_a", font_size=32).move_to(np.array([3.3, 0.0, 0]))
    gar = mixed("Sagan 旁窗：", "$g\\,v_T=0$", "（Garnir 元素）", font_size=26, color=MUTED_COLOR)
    gar.move_to(np.array([0, -1.8, 0]))
    assert_in_frame(rel, arr, alab, img, rho, cbox, link, gar)
    assert_apart(VGroup(rel, arr, img), VGroup(rho, cbox, link), 0.2)
    assert_apart(VGroup(img, link), gar, 0.3)

    scene.play(FadeIn(rel), run_time=0.8)
    scene.say("現在把 ", "$\\alpha$", " 作用上去：", "$[T]\\mapsto v_T$", wait=SLOW * 0.8)
    scene.play(GrowArrow(arr), FadeIn(alab), run_time=0.7)
    scene.play(TransformFromCopy(rel, img), run_time=1.2)
    scene.say("得到 ", "$v_{21/3}=v_a-v_b$", "：標準基底的組合", wait=SLOW * 1.5)
    scene.play(FadeIn(rho), run_time=0.8)
    scene.play(ShowCreation(cbox), run_time=0.6)
    scene.play(Write(link), run_time=1.0)
    scene.say("這正是 F33 裡 ", "$\\rho(1\\,2)$", " 的第一欄 ", "$(1,-1)$", "：不是新規則，是同一個計算", wait=SLOW * 2.5)
    scene.play(FadeIn(gar), run_time=0.6)
    scene.say("Sagan 用 Garnir 元素 ", "$g\\,v_T=0$", " 組織同一個局部改寫；兩種求和不要逐項混用", wait=SLOW * 2.0)


# ---------------------------------------------------------------- 5. 收束
def part_summary(scene):
    lines = VGroup(
        mixed("列 tabloid 無號：", r"$\{pT\}=\{T\}$", font_size=30),
        mixed("行 tabloid 帶號：", r"$[qT]=\operatorname{sgn}(q)[T]$", font_size=30),
        mixed("商空間裡：", r"$[21/3]=[12/3]-[13/2]$", "，負號來自排行", font_size=30),
    ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(0.3 * UP)
    marks = VGroup(*[Dot(radius=0.07, fill_color=OP_COLOR).next_to(l, LEFT, buff=0.3) for l in lines])
    assert_in_frame(lines, marks)
    scene.say("收束：左邊無號、右邊有方向；負號屬於向量", wait=SLOW * 0.5)
    for l, m in zip(lines, marks):
        scene.play(FadeIn(m), FadeIn(l, shift=0.2 * RIGHT), run_time=0.9)
        scene.wait(SLOW * 1.2)
    scene.say("下一步：形狀大一點時，一輪改寫可能弄壞別處，要做兩輪", wait=SLOW * 1.5)


class SceneF38ColumnTabloids(ChuScene):
    def construct(self):
        self.show_header("帶方向的行 tabloid")
        check_math()
        part_two_kinds(self)
        self.clear_stage()
        part_maps(self)
        self.clear_stage()
        part_exchange(self)
        self.clear_stage()
        part_alpha(self)
        self.clear_stage()
        part_summary(self)
        self.wait(1.0)
