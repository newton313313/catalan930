"""
Scene F34 —— 置換模組的特徵標與 Young's rule（Fulton §7.2–7.3；原大綱卡 F712、F714、X705 精簡）
執行（在 codes/ 內）：manimgl scenes/sceneF34_young_rule.py SceneF34YoungRule

1. σ = (12)(34)(5) 作用在 (3,2) 的 tabloid：整隊放進一列才固定 → 125/34、345/12 → ξ = [x^λ]p_μ = 2；
   回 S_3：ξ^(2,1)_(2,1) = 1 但 χ^(2,1)_(2,1) = 0。
2. Young's rule：M^(2,1) = S^(3) ⊕ S^(2,1)（112、11/2）；μ = (2,2,1) 的 7 張半標準表 → 重數 1,2,2,1,1，維數 30。
3. 半標準表 ＝ Hom(S^λ, M^μ) 的基底：θ_T 一例（T = 112 給 t_1+t_2+t_3）。
"""
import math
import sys
from itertools import combinations, permutations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.rep_data import act, cycles, load, tabloid_key
from utils.rep_draw import COL_COLOR, NEG_COLOR, OP_COLOR, POS_COLOR, ROW_COLOR, TabloidMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, mixed, zh
from utils.tableaux import kostka, p_lambda, partitions, ssyt, standard_tableaux

TEAM_COLORS = [TEAL_C, PURPLE_B, LIGHT_BROWN]        # 三支隊伍：(12)、(34)、(5)
BAD = [[1, 3, 5], [2, 4]]                            # 拆散隊伍的例子


# ----------------------------------------------------------------------------- 資料
def team_of(pc):
    """標號 → 隊伍編號（依 permutation_char32 的 cycles）。"""
    return {v: k for k, c in enumerate(pc["cycles"]) for v in c}


def choice_count(pc):
    """每支隊伍整隊選一列：λ 的列容量剛好填滿的選法數（= [x^λ] p_μ）。"""
    lens = [len(c) for c in pc["cycles"]]
    lam = pc["lambda"]
    good = []
    for rows in product(range(len(lam)), repeat=len(lens)):
        if all(sum(l for l, r in zip(lens, rows) if r == i) == lam[i] for i in range(len(lam))):
            good.append(rows)
    return good


def theta_fillings():
    """λ=(3)、μ=(2,1)、T=112：同列重排的 filling → 對應的 μ-tabloid（U = 123）。"""
    out = []
    for F in sorted(set(permutations((1, 1, 2)))):
        rows = [[u for u, f in zip((1, 2, 3), F) if f == r] for r in (1, 2)]
        out.append((F, tabloid_key(rows)))
    return out


def check_math():
    pc = load("permutation_char32")
    sigma = tuple(pc["permutation"])
    assert [list(c) for c in cycles(sigma)] == pc["cycles"]
    lam = tuple(pc["lambda"])
    fixed = []
    for top in combinations(range(1, 6), lam[0]):
        rows = [list(top), [i for i in range(1, 6) if i not in top]]
        if tabloid_key(act(sigma, rows)) == tabloid_key(rows):
            fixed.append(tabloid_key(rows))
    assert sorted(fixed) == sorted(tabloid_key(t) for t in pc["fixed_tabloids"])
    assert tabloid_key(act(sigma, BAD)) != tabloid_key(BAD)
    assert len(choice_count(pc)) == pc["character"] == 2
    assert p_lambda(tuple(pc["mu"]), 2)[tuple(pc["coefficient_target"])] == 2
    cs = load("character_S3")
    assert cs["permutation"]["21"][1] == 1 and cs["specht"]["21"][1] == 0
    assert ssyt((3,), content=(2, 1)) == [((1, 1, 2),)] and ssyt((2, 1), content=(2, 1)) == [((1, 1), (2,))]
    assert kostka((1, 1, 1), (2, 1)) == 0
    y = load("young221")
    mu = tuple(y["mu"])
    tot = 0
    for comp in y["components"]:
        lm = tuple(comp["lambda"])
        assert [list(map(list, T)) for T in ssyt(lm, content=mu)] == comp["semistandard"]
        assert kostka(lm, mu) == comp["K"] and len(standard_tableaux(lm)) == comp["f"]
        tot += comp["K"] * comp["f"]
    assert tot == y["dim_M"] == 30 == math.factorial(5) // (2 * 2)
    shown = {tuple(c["lambda"]) for c in y["components"]}
    assert all(kostka(l, mu) == 0 for l in partitions(5) if tuple(l) not in shown)
    tabs = load("shape21")["tabloids"]
    assert [k for _, k in theta_fillings()] == [tabloid_key(tabs[t]) for t in ("t3", "t2", "t1")]


# ----------------------------------------------------------------------------- 小工具
def team_badge(nums, color):
    cells = VGroup(*[Square(side_length=0.48).set_stroke(color, 3).set_fill(color, 0.25) for _ in nums])
    cells.arrange(RIGHT, buff=0)
    labs = VGroup(*[Tex(str(n), font_size=30).move_to(c) for n, c in zip(nums, cells)])
    return VGroup(cells, labs)


def colored_tabloid(rows, teams, cs=0.5):
    t = TabloidMob(rows, cs=cs)
    for i, r in enumerate(t.key):
        for j, v in enumerate(r):
            t.entry(i, j).set_fill(TEAM_COLORS[teams[v]])
    return t


def ssyt_mob(T, cs=0.4):
    return tableau_mob([list(r) for r in T], cs=cs)


# ----------------------------------------------------------------------------- 1. 置換特徵標
def part_fixed(scene):
    pc = load("permutation_char32")
    teams = team_of(pc)
    sig = VGroup(*[Tex("(" + "\\,".join(map(str, c)) + ")", font_size=40, fill_color=TEAM_COLORS[k])
                 for k, c in enumerate(pc["cycles"])]).arrange(RIGHT, buff=0.08)
    sig_full = VGroup(Tex("\\sigma=", font_size=40), sig).arrange(RIGHT, buff=0.15).move_to(np.array([-3.6, 2.6, 0]))
    badges = VGroup(*[team_badge(c, TEAM_COLORS[k]) for k, c in enumerate(pc["cycles"])]).arrange(RIGHT, buff=0.5)
    badges.next_to(sig_full, DOWN, buff=0.3)
    scene.say("$\\sigma=(12)(34)(5)$", " 是三支隊伍：兩支雙人隊、一支單人隊")
    scene.play(Write(sig_full), run_time=1.0)
    scene.play(LaggedStartMap(FadeIn, badges, shift=0.1 * DOWN, lag_ratio=0.3), run_time=1.0)
    scene.wait(6.5)

    lam = pc["lambda"]
    cap = mixed("$\\lambda=(3,2)$", "：兩列，容量 3 與 2", font_size=26).next_to(badges, DOWN, buff=0.3)
    bad = colored_tabloid(BAD, teams, cs=0.42)
    bad_img = colored_tabloid([list(r) for r in act(tuple(pc["permutation"]), BAD)], teams, cs=0.42)
    arr = Tex("\\xrightarrow{\\ \\sigma\\ }", font_size=40)
    neq = Tex("\\neq", font_size=40, fill_color=NEG_COLOR)
    bad_copy = colored_tabloid(BAD, teams, cs=0.42)
    bad_row = VGroup(bad, arr, bad_img, neq, bad_copy).arrange(RIGHT, buff=0.25).next_to(cap, DOWN, buff=0.35)
    bad_row.set_x(-3.6)
    scene.say("把隊伍拆開放：", "$\\sigma$", " 一作用就有人跨到另一列，tabloid 變了")
    scene.play(FadeIn(cap), FadeIn(bad), run_time=0.8)
    scene.play(Write(arr), TransformFromCopy(bad, bad_img), run_time=1.2)
    scene.play(FadeIn(neq), FadeIn(bad_copy), run_time=0.7)
    scene.wait(6.5)

    goods = VGroup()
    for rows in pc["fixed_tabloids"]:
        g = colored_tabloid(rows, teams)
        ok = Tex("\\sigma\\{T\\}=\\{T\\}", font_size=32, fill_color=POS_COLOR).next_to(g, RIGHT, buff=0.3)
        goods.add(VGroup(g, ok))
    goods.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(np.array([3.6, 1.1, 0]))
    head = zh("整隊放進同一列：只有兩種", font_size=26, color=POS_COLOR).next_to(goods, UP, buff=0.35)
    scene.say("固定的 tabloid 必須讓每支隊伍整隊坐在同一列：只剩 ", "$125/34$", "、", "$345/12$")
    scene.play(FadeIn(head), LaggedStartMap(FadeIn, goods, lag_ratio=0.4), run_time=1.4)
    assert_in_frame(sig_full, badges, cap, bad_row, goods, head)
    assert_apart(VGroup(sig_full, badges, cap, bad_row), VGroup(goods, head))
    scene.wait(7.5)

    fac = VGroup(Tex("(x_1^2+x_2^2)", font_size=34, fill_color=TEAM_COLORS[0]),
                 Tex("(x_1^2+x_2^2)", font_size=34, fill_color=TEAM_COLORS[1]),
                 Tex("(x_1+x_2)", font_size=34, fill_color=TEAM_COLORS[2])).arrange(RIGHT, buff=0.1)
    pmu = VGroup(Tex("p_{(2,2,1)}=", font_size=34), fac).arrange(RIGHT, buff=0.15).move_to(np.array([2.4, -1.0, 0]))
    picks = choice_count(pc)
    pick_tex = VGroup()
    for rows in picks:
        parts = []
        for k, r in enumerate(rows):
            e = len(pc["cycles"][k])
            parts.append(f"x_{r + 1}" + (f"^{e}" if e > 1 else ""))
        pick_tex.add(Tex("\\cdot ".join(parts), font_size=32))
    pick_tex.arrange(RIGHT, buff=0.8).next_to(pmu, DOWN, buff=0.25)
    coef = Tex(f"\\xi^{{(3,2)}}_{{(2,2,1)}}=[x_1^3x_2^2]\\,p_{{(2,2,1)}}={pc['character']}", font_size=34,
               fill_color=OP_COLOR).next_to(pick_tex, DOWN, buff=0.25)
    scene.say("每支雙人隊選第 1 列或第 2 列：", "$x_1^2+x_2^2$", "；單人隊：", "$x_1+x_2$")
    scene.play(FadeIn(pmu, shift=0.1 * UP), run_time=1.0)
    scene.wait(5.5)
    scene.say("要湊出列長 ", "$(3,2)$", "，只看 ", "$x_1^3x_2^2$", " 的係數：兩種選法")
    scene.play(LaggedStartMap(FadeIn, pick_tex, lag_ratio=0.4), run_time=1.0)
    scene.play(Write(coef), run_time=1.0)
    assert_in_frame(pmu, pick_tex, coef)
    assert_apart(VGroup(pmu, pick_tex, coef), VGroup(bad_row, goods))
    scene.wait(5.5)
    scene.say("兩支雙人隊身分不同，不能除以 2!：固定的 tabloid 恰好兩個", wait=6.5)
    scene.play(FadeOut(VGroup(sig_full, badges, cap, bad_row, goods, head, pmu, pick_tex)),
               coef.animate.move_to(np.array([0, 2.3, 0])), run_time=0.8)

    cs = load("character_S3")
    xi = Tex(f"\\xi^{{(2,1)}}_{{(2,1)}}={cs['permutation']['21'][1]}", font_size=44, fill_color=ROW_COLOR)
    ch = Tex(f"\\chi^{{(2,1)}}_{{(2,1)}}={cs['specht']['21'][1]}", font_size=44, fill_color=POS_COLOR)
    pair = VGroup(xi, ch).arrange(RIGHT, buff=1.6).move_to(np.array([0, 0.6, 0]))
    notes = VGroup(zh("M 的跡：數固定的 tabloid", font_size=24, color=ROW_COLOR).next_to(xi, DOWN, buff=0.3),
                   zh("Specht 的跡：不能這樣數", font_size=24, color=POS_COLOR).next_to(ch, DOWN, buff=0.3))
    scene.say("回到 ", "$S_3$", "：同一個 ", "$(12)$", "，兩種特徵標不一樣")
    scene.play(FadeIn(pair, shift=0.1 * UP), run_time=1.0)
    scene.play(FadeIn(notes), run_time=0.8)
    assert_in_frame(coef, pair, notes)
    scene.wait(7.5)


# ----------------------------------------------------------------------------- 2. Young's rule
def part_young(scene):
    t3 = ssyt_mob(ssyt((3,), content=(2, 1))[0], cs=0.5)
    t21 = ssyt_mob(ssyt((2, 1), content=(2, 1))[0], cs=0.5)
    l3 = Tex("S^{(3)}", font_size=34).next_to(t3, DOWN, buff=0.25)
    l21 = Tex("S^{(2,1)}", font_size=34).next_to(t21, DOWN, buff=0.25)
    small = VGroup(VGroup(t3, l3), VGroup(t21, l21)).arrange(RIGHT, buff=1.5, aligned_edge=DOWN)
    small.move_to(np.array([-2.0, 1.2, 0]))
    eq = Tex("M^{(2,1)}=S^{(3)}\\oplus S^{(2,1)},\\quad 3=1+2", font_size=40).next_to(small, DOWN, buff=0.5)
    eq.set_x(0)
    scene.say("Young's rule：內容 ", "$\\mu=(2,1)$", "（兩個 1、一個 2）的半標準表")
    scene.play(FadeIn(small[0]), run_time=0.8)
    scene.play(FadeIn(small[1]), run_time=0.8)
    scene.wait(3.5)
    scene.say("每張表給一個副本：", "$M^{(2,1)}=S^{(3)}\\oplus S^{(2,1)}$", "，正是 F31 的平均線＋零和平面")
    scene.play(Write(eq), run_time=1.2)
    assert_in_frame(small, eq)
    scene.wait(7.5)
    scene.play(FadeOut(VGroup(small, eq)), run_time=0.6)

    y = load("young221")
    cols = VGroup()
    for comp in y["components"]:
        head = Tex(tuple_str(comp["lambda"]), font_size=30, fill_color=MUTED_COLOR)
        tabs = VGroup(*[ssyt_mob(T, cs=0.4) for T in comp["semistandard"]]).arrange(DOWN, buff=0.3)
        kl = Tex(f"K={comp['K']}", font_size=30, fill_color=OP_COLOR)
        cols.add(VGroup(head, tabs, kl).arrange(DOWN, buff=0.3))
    cols.arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to(np.array([0, 1.0, 0]))
    for c in cols:
        c[2].set_y(cols.get_bottom()[1] + 0.15)
    scene.say("換成 ", "$\\mu=(2,2,1)$", "：兩個 1、兩個 2、一個 3，列弱增、行嚴增")
    scene.play(LaggedStartMap(FadeIn, VGroup(*[VGroup(c[0], c[1]) for c in cols]), lag_ratio=0.25), run_time=2.0)
    scene.wait(3.5)

    ex = cols[2][1][0]                               # (3,2) 的第一張
    lam_ex = y["components"][2]["lambda"]
    rows_hl = VGroup(*[ex.cell_group([(i, j) for j in range(r)]).copy().set_stroke(ROW_COLOR, 5).set_fill(opacity=0)
                       for i, r in enumerate(lam_ex)])
    cols_hl = VGroup(*[ex.cell_group([(i, j) for i in range(len(lam_ex)) if lam_ex[i] > j]).copy()
                       .set_stroke(COL_COLOR, 5).set_fill(opacity=0) for j in range(lam_ex[0])])
    scene.say("檢查一張：每列（藍）可以相等，每行（橙）必須嚴格變大")
    scene.play(ShowCreation(rows_hl), run_time=0.8)
    scene.wait(2.0)
    scene.play(FadeOut(rows_hl), ShowCreation(cols_hl), run_time=0.8)
    scene.wait(2.5)
    scene.play(FadeOut(cols_hl), LaggedStartMap(FadeIn, VGroup(*[c[2] for c in cols]), lag_ratio=0.2), run_time=1.0)
    scene.say("同形狀的兩張表＝同一個不可約模組的兩個副本，不是同一個向量", wait=6.5)

    comps = y["components"]

    def term(c):
        k = "" if c["K"] == 1 else str(c["K"])
        return f"{k}S^{{{tuple_str(c['lambda'])}}}"

    dec = Tex("M^{(2,2,1)}=" + "\\oplus ".join(term(c) for c in comps), font_size=36)
    dims = Tex("+".join((f"{c['K']}\\cdot{c['f']}" if c["K"] > 1 else str(c["f"])) for c in comps)
               + f"={y['dim_M']}=\\frac{{5!}}{{2!\\,2!\\,1!}}", font_size=36)
    rule = Tex("M^\\mu\\cong\\bigoplus_\\lambda (S^\\lambda)^{\\oplus K_{\\lambda\\mu}}", font_size=36,
               fill_color=OP_COLOR)
    VGroup(dec, dims).arrange(DOWN, buff=0.3).next_to(cols, DOWN, buff=0.45)
    scene.say("讀出分解：重數就是 Kostka 數 ", "$K_{\\lambda\\mu}$")
    scene.play(Write(dec), run_time=1.5)
    scene.wait(4.5)
    scene.say("維數驗算：", "$f^\\lambda$", " 依序是 1、4、5、6、5")
    scene.play(Write(dims), run_time=1.5)
    assert_in_frame(cols, dec, dims)
    assert_apart(cols, dec)
    scene.wait(6.5)
    scene.play(FadeOut(VGroup(dec, dims)), run_time=0.5)
    rule.next_to(cols, DOWN, buff=0.6)
    scene.play(Write(rule), run_time=1.2)
    assert_in_frame(rule)
    scene.say("這就是 Young's rule：", "$M^\\mu\\cong\\bigoplus_\\lambda(S^\\lambda)^{\\oplus K_{\\lambda\\mu}}$", wait=6.5)


# ----------------------------------------------------------------------------- 3. Hom 的基底
def part_hom(scene):
    U = tableau_mob([[1, 2, 3]], cs=0.45)
    U_lab = Tex("U", font_size=32, fill_color=MUTED_COLOR).next_to(U, LEFT, buff=0.25)
    T = tableau_mob([[1, 1, 2]], cs=0.45)
    T.cells.set_stroke(OP_COLOR, width=3)
    T_lab = Tex("T", font_size=32, fill_color=OP_COLOR).next_to(T, LEFT, buff=0.25)
    top = VGroup(VGroup(U_lab, U), VGroup(T_lab, T)).arrange(RIGHT, buff=1.0).move_to(np.array([-3.4, 2.4, 0]))
    scene.say("為什麼表數的是副本？固定編號 ", "$U$", "，另放一張填數 ", "$T$")
    scene.play(FadeIn(top), run_time=1.0)
    scene.wait(2.5)
    scene.say("$T$", " 的格子寫 ", "$i$", "：", "$U$", " 在那格的標號就去 tabloid 的第 ", "$i$", " 列")
    scene.wait(5.5)

    rows = VGroup()
    names = {tabloid_key(v): k for k, v in load("shape21")["tabloids"].items()}
    for F, key in theta_fillings():
        f = tableau_mob([list(F)], cs=0.4)
        arr = Tex("\\mapsto", font_size=34)
        tb = TabloidMob([list(r) for r in key], cs=0.42)
        nm = Tex("=" + names[key][0] + "_" + names[key][1], font_size=32)
        rows.add(VGroup(f, arr, tb, nm).arrange(RIGHT, buff=0.3))
    rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(top, DOWN, buff=0.5).set_x(-3.6)
    total = Tex("\\theta_T=t_1+t_2+t_3", font_size=38, fill_color=ROW_COLOR).next_to(rows, DOWN, buff=0.35)
    scene.say("$T=112$", "：對同一列重排出 112、121、211，三張各送到一個 tabloid 再相加")
    scene.play(LaggedStartMap(FadeIn, rows, shift=0.1 * RIGHT, lag_ratio=0.4), run_time=1.8)
    scene.play(Write(total), run_time=1.0)
    scene.wait(4.5)

    T2 = tableau_mob([[1, 1], [2]], cs=0.45)
    T2.cells.set_stroke(OP_COLOR, width=3)
    T2_lab = Tex("T=11/2", font_size=32, fill_color=OP_COLOR).next_to(T2, UP, buff=0.25)
    id_tex = Tex("\\bar\\theta_T=\\mathrm{id}", font_size=36).next_to(T2, DOWN, buff=0.3)
    right = VGroup(T2_lab, T2, id_tex).move_to(np.array([3.2, 1.3, 0]))
    match = VGroup(mixed("$S^{(3)}$", " → 平均方向", font_size=26, color=ROW_COLOR),
                   mixed("$S^{(2,1)}$", " → 零和平面", font_size=26, color=POS_COLOR),
                   Tex("3=1+2", font_size=36)).arrange(DOWN, buff=0.22).next_to(right, DOWN, buff=0.45)
    scene.say("把 ", "$S^{(3)}$", " 嵌進平均方向；而 ", "$\\lambda=\\mu=(2,1)$", "、", "$T=11/2$", " 給的就是恆等")
    scene.play(FadeIn(right), run_time=1.0)
    scene.play(FadeIn(match, shift=0.1 * UP), run_time=1.0)
    assert_in_frame(top, rows, total, right, match)
    assert_apart(VGroup(top, rows, total), VGroup(right, match))
    scene.wait(6.5)
    scene.say("一般做法：對 ", "$T$", " 的同列重排求和得 ", "$\\theta_T$", "，再限制到 ", "$S^\\lambda$", " 得 ", "$\\bar\\theta_T$", wait=6.5)

    scene.play(FadeOut(VGroup(top, rows, total, right, match)), run_time=0.6)
    comp = load("young221")["components"][2]
    mcards = VGroup()
    for k, Tt in enumerate(comp["semistandard"]):
        tb = ssyt_mob(Tt, cs=0.45)
        nm = Tex(f"\\bar\\theta_{{T_{k + 1}}}:S^{{(3,2)}}\\to M^{{(2,2,1)}}", font_size=30).next_to(tb, DOWN, buff=0.25)
        box = SurroundingRectangle(VGroup(tb, nm), buff=0.2).set_stroke(GREY_B, 2)
        mcards.add(VGroup(box, tb, nm))
    mcards.arrange(RIGHT, buff=0.8).move_to(np.array([0, 1.2, 0]))
    homdim = Tex("\\dim\\operatorname{Hom}_{S_n}(S^\\lambda,M^\\mu)=K_{\\lambda\\mu}", font_size=40, fill_color=OP_COLOR)
    homdim.next_to(mcards, DOWN, buff=0.6)
    scene.say("$(3,2)$", " 在 ", "$M^{(2,2,1)}$", " 裡的兩張半標準表＝兩張不同的映射卡")
    scene.play(LaggedStartMap(FadeIn, mcards, lag_ratio=0.4), run_time=1.4)
    scene.wait(4.5)
    scene.play(Write(homdim), run_time=1.2)
    assert_in_frame(mcards, homdim)
    scene.say("獨立靠首項、張成靠 Garnir；半標準表正好是 ", "$\\operatorname{Hom}(S^\\lambda,M^\\mu)$", " 的基底", wait=7.5)


class SceneF34YoungRule(ChuScene):
    def construct(self):
        self.show_header("置換模組與 Young's rule")
        check_math()
        part_fixed(self)
        self.clear_stage()
        part_young(self)
        self.clear_stage()
        part_hom(self)
        self.wait(1.0)
