"""
Scene F09 —— 字與 Knuth 等價（Fulton《Young Tableaux》§2.1，書 p.17–20）

    (1) 表 ↔ 字：CH2_WORD = 5 6 4 4 6 2 3 5 5 1 2 2 3 在「後一個數變小」處切成 56｜446｜2355｜1223，
        由下往上疊回 T = FULTON_INSERT_T；3 4 1 4 疊起來第 2 行是 4 在 4 上面 → 不是表的字；
        任何字都是某個斜表的字：skew_from_word(CH3_WORD) 的階梯
    (2) 列插入的字語言：(u x' v)·x ↦ x'·(u x v)（u ≤ x < x' ≤ v）；例：T ← 2 的四行（書 p.18）
    (3) Knuth 的原子步驟（書 p.19）：K'  y z x ↦ y x z（x < y ≤ z）＝列 [y z] 插入 x
                                    K'' x z y ↦ z x y（x ≤ y < z）＝列 [x z] 插入 y
    (4) Knuth 等價 ≡；命題 1：w(T ← x) ≡ w(T)·x —— insertion_knuth_chain(T, 2) 共 8 步
        （K''×3、K'、K''×4），結尾是 w(T ← 2)；推論：w(T·U) ≡ w(T)·w(U)

數字全部由 utils/tableaux.py 算出並 assert（格子 (i,j) 0 起算；字幕裡的「第 k 列」1 起算）。

執行（在 codes/ 資料夾內；要平行渲染請用 combkit/tools/render_check.py）：
    manimgl scenes/sceneF09_words_knuth.py SceneF09WordsKnuth
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import RULE_COLORS, SkewMob, WordMob, assert_apart, assert_in_frame, tableau_mob
from utils.mit_draw import YoungDiagramMob
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH2_WORD,
    CH3_WORD,
    FULTON_INSERT_T,
    bump_steps,
    insertion_knuth_chain,
    is_tableau,
    knuth_moves,
    row_insert,
    skew_from_word,
    tableau_word,
    word_runs,
    word_to_tableau,
)

T0 = FULTON_INSERT_T
X_INS = 2
T_INS = ((1, 2, 2, 2), (2, 3, 3, 5), (4, 4, 5), (5, 6, 6))          # T ← 2
RUNS = ((5, 6), (4, 4, 6), (2, 3, 5, 5), (1, 2, 2, 3))
BAD_WORD = (3, 4, 1, 4)
BAD_STACK = ((1, 4), (3, 4))                                         # 由下往上疊（第 1 段在下）
BAD_COL = 1                                                          # 出問題的行（0 起算）
CHAIN_RULES = ("K''",) * 3 + ("K'",) + ("K''",) * 4
EX_K1 = ((2, 3, 1), (2, 1, 3))                                       # K' 的數字例
EX_K2 = ((1, 3, 2), (3, 1, 2))                                       # K'' 的數字例
RUN_COLORS = [TEAL, GOLD, PINK, BLUE_B]                              # 第 1、2、3、4 段（讀的順序）
MOVER_COLOR = YELLOW
CHANGED_COLOR = TEAL


def run_starts(w):
    """各弱遞增片段在字裡的起點（0 起算）。"""
    out, k = [], 0
    for r in word_runs(w):
        out.append(k)
        k += len(r)
    return out


def row_moves(T, x):
    """插入 x 時每一列的 (列號, 進來的數 a, 擠出的數 b 或 None, u, v)：a 用 K' 越過 v，b 用 K'' 越過 u。"""
    out = []
    for (r, c), a, b in bump_steps(T, x):
        row = T[r] if r < len(T) else ()
        out.append((r, a, b, row[:c], row[c + 1:]))
    return out


def insertion_lines(T, x):
    """列插入的字語言（書 p.18）：每行是 [("row", 列, 改過?) 或 ("mover", 數)]，依讀的順序。"""
    rows = [tuple(r) for r in T]
    lines = [[("row", r, False) for r in reversed(rows)] + [("mover", x)]]
    for (r, c), a, b in bump_steps(T, x):
        if r == len(rows):
            rows.append((a,))
        else:
            rows[r] = rows[r][:c] + (a,) + rows[r][c + 1:]
        line = [("row", rows[k], k <= r) for k in reversed(range(len(rows)))]
        if b is not None:
            line.insert(len(rows) - 1 - r, ("mover", b))          # 在改過的第 r 列前面
        lines.append(line)
    assert tuple(rows) == row_insert(T, x)[0]
    return lines


def flat(line):
    return tuple(a for kind, *d in line for a in (d[0] if kind == "row" else (d[0],)))


def check_math():
    assert is_tableau(T0) and tableau_word(T0) == CH2_WORD
    assert tuple(word_runs(CH2_WORD)) == RUNS and tuple(reversed(RUNS)) == T0
    assert word_to_tableau(CH2_WORD) == T0 and run_starts(CH2_WORD) == [0, 2, 5, 9]
    # 3 4 1 4 不是表的字：第 2 行上下相等
    assert tuple(reversed(word_runs(BAD_WORD))) == BAD_STACK and word_to_tableau(BAD_WORD) is None
    assert BAD_STACK[0][BAD_COL] >= BAD_STACK[1][BAD_COL]
    assert all(BAD_STACK[0][j] < BAD_STACK[1][j] for j in range(BAD_COL))
    # 任何字都是某個斜表的字
    S = skew_from_word(CH3_WORD)
    assert tableau_word(S) == CH3_WORD and len(S) == len(word_runs(CH3_WORD)) == 4
    assert word_to_tableau(CH3_WORD) is None
    # 列插入的字語言
    lines = insertion_lines(T0, X_INS)
    assert len(lines) == len(bump_steps(T0, X_INS)) + 1 == 5
    assert flat(lines[0]) == CH2_WORD + (X_INS,) and flat(lines[-1]) == tableau_word(T_INS)
    assert row_insert(T0, X_INS)[0] == T_INS
    # K'、K'' 就是兩個小插入（含等號的情形）
    for x in range(1, 5):
        for y in range(1, 5):
            for z in range(1, 5):
                if x < y <= z:
                    Tk = row_insert(((y, z),), x)[0]
                    assert Tk == ((x, z), (y,)) and tableau_word(Tk) == (y, x, z)
                    assert (0, "K'", (y, x, z)) in knuth_moves((y, z, x))
                if x <= y < z:
                    Tk = row_insert(((x, z),), y)[0]
                    assert Tk == ((x, y), (z,)) and tableau_word(Tk) == (z, x, y)
                    assert (0, "K''", (z, x, y)) in knuth_moves((x, z, y))
    assert (0, "K'", EX_K1[1]) in knuth_moves(EX_K1[0]) and (0, "K''", EX_K2[1]) in knuth_moves(EX_K2[0])
    # 命題 1：8 步，每步都是合法的基本變換
    chain = insertion_knuth_chain(T0, X_INS)
    assert tuple(r for _, r, _ in chain) == CHAIN_RULES and chain[-1][2] == tableau_word(T_INS)
    prev = CH2_WORD + (X_INS,)
    for i, rule, w in chain:
        assert (i, rule, w) in knuth_moves(prev)
        prev = w
    expect = []
    for r, a, b, u, v in row_moves(T0, X_INS):
        if b is not None:
            expect += ["K'"] * len(v) + ["K''"] * len(u)
    assert tuple(expect) == CHAIN_RULES
    assert [m[:3] for m in row_moves(T0, X_INS)] == [(0, 2, 3), (1, 3, 5), (2, 5, 6), (3, 6, None)]


def nums(seq, sep=" "):
    return sep.join(str(a) for a in seq)


def ntex(seq):
    """數字串的 Tex（字母之間留空）。"""
    return r"\ ".join(str(a) for a in seq)


def cut_marks(wm, cuts, color=YELLOW):
    """在位置 k-1 與 k 之間畫切線（k 在 cuts 裡）。"""
    h = wm.size + 0.34
    marks = VGroup()
    for k in cuts:
        x = (wm.slot(k - 1) + wm.slot(k)) / 2
        marks.add(Line(x + h / 2 * UP, x + h / 2 * DOWN, stroke_color=color, stroke_width=4))
    return marks


def fly_runs(scene, wm, w, target, run_time=0.55):
    """各片段的方塊複製後依序飛到 target(第 t 段, 段內第 j 個) 的位置；回傳複製品。"""
    copies = VGroup()
    for t, (s, r) in enumerate(zip(run_starts(w), word_runs(w))):
        grp = VGroup(*[wm.tiles[s + j].copy() for j in range(len(r))])
        copies.add(grp)
        scene.play(*[g.animate.move_to(target(t, j)) for j, g in enumerate(grp)], run_time=run_time)
    return copies


# =============================================================================
# 第 1 段：表 ↔ 字
# =============================================================================
def part_tableau_word(scene):
    starts, runs = run_starts(CH2_WORD), word_runs(CH2_WORD)
    colors = {s + j: RUN_COLORS[t] for t, (s, r) in enumerate(zip(starts, runs)) for j in range(len(r))}
    wm = WordMob(CH2_WORD, size=0.55, center=np.array([0.7, 2.4, 0.0]))
    cuts = cut_marks(wm, starts[1:])
    w_lab = Tex("w(T)=", font_size=40).next_to(wm, LEFT, buff=0.3)
    n = len(T0)
    tab = tableau_mob(T0, cs=0.6, center=np.array([0.7, -0.45, 0.0]))
    for i in range(n):
        for j in range(len(T0[i])):
            tab.cell(i, j).set_fill(RUN_COLORS[n - 1 - i], opacity=0.3)
    t_lab = Tex("T=", font_size=44).next_to(tab, LEFT, buff=0.3)
    tags = VGroup(*[zh(f"第 {t + 1} 段", font_size=22, color=RUN_COLORS[t]) for t in range(n)])
    for t, tag in enumerate(tags):
        tag.move_to(np.array([tab.get_right()[0] + 0.3, tab.cell_center(n - 1 - t, 0)[1], 0.0]), aligned_edge=LEFT)
    assert_in_frame(wm, cuts, w_lab, tab, t_lab, tags)
    assert_apart(VGroup(wm, cuts), VGroup(tab, tags), gap=0.4)
    assert_apart(t_lab, tab, gap=0.1)

    scene.say(f"「字」就是一串正整數，例如這 {len(CH2_WORD)} 個數")
    scene.play(FadeIn(wm), run_time=0.8)
    scene.wait(0.6)
    scene.say(f"在「後一個數比前一個小」的地方切開，得到 {len(runs)} 段弱遞增的片段")
    scene.play(ShowCreation(cuts), *wm.color_slots(colors), run_time=0.9)
    scene.wait(1.0)
    scene.say("把片段由下往上疊：第 1 段放最下面，最後一段放最上面")
    copies = fly_runs(scene, wm, CH2_WORD, lambda t, j: tab.cell_center(n - 1 - t, j))
    scene.play(FadeIn(tab), FadeOut(copies), FadeIn(tags), FadeIn(t_lab), run_time=0.7)
    scene.say("疊出來正是第 1 章的表 ", "$T$", "；反過來，由下往上逐列讀 ", "$T$", "，就讀回它的字 ", "$w(T)$")
    scene.play(FadeIn(w_lab, shift=0.15 * RIGHT), run_time=0.6)
    scene.wait(2.0)


def part_any_word(scene):
    # 左：不是表的字
    bw = WordMob(BAD_WORD, size=0.55, center=np.array([-4.5, 1.95, 0.0]))
    bcut = cut_marks(bw, run_starts(BAD_WORD)[1:])
    bt = tableau_mob(BAD_STACK, cs=0.62, center=np.array([-4.5, 0.1, 0.0]))
    bad = SurroundingRectangle(VGroup(bt.cell(0, BAD_COL), bt.cell(1, BAD_COL)), buff=0.06,
                               color=RED, stroke_width=4)
    bad_lab = zh("不是表的字", font_size=26, color=RED).next_to(bt, DOWN, buff=0.35)
    # 右：任何字都是某個斜表的字
    S = skew_from_word(CH3_WORD)
    cs = 0.42
    width = max(len(r) for r in S)
    cw = WordMob(CH3_WORD, size=cs, buff=0.06, center=np.array([2.9, 1.95, 0.0]))
    ccut = cut_marks(cw, run_starts(CH3_WORD)[1:])
    sk = SkewMob(S, cs=cs, show_mu=False, top_left=np.array([2.9 - width * cs / 2, 0.85, 0.0]))
    sk_lab = zh("斜表", font_size=26, color=OK_COLOR).next_to(sk, DOWN, buff=0.35)
    sk_lab.align_to(sk, LEFT)
    assert_in_frame(bw, bcut, bt, bad, bad_lab, cw, ccut, sk, sk_lab)
    assert_apart(VGroup(bw, bcut, bt, bad_lab), VGroup(cw, ccut, sk), gap=0.5)
    assert_apart(VGroup(cw, ccut), sk, gap=0.2)
    assert_apart(VGroup(bw, bcut), bt, gap=0.3)
    nb = len(BAD_STACK)

    scene.say("不是每個字都來自表：", f"${ntex(BAD_WORD)}$", " 切成兩段疊起來看看")
    scene.play(FadeIn(bw), run_time=0.5)
    scene.play(ShowCreation(bcut), run_time=0.4)
    copies = fly_runs(scene, bw, BAD_WORD, lambda t, j: bt.cell_center(nb - 1 - t, j), run_time=0.5)
    scene.play(FadeIn(bt), FadeOut(copies), run_time=0.5)
    top, bottom = BAD_STACK[0][BAD_COL], BAD_STACK[1][BAD_COL]
    scene.say(f"第 {BAD_COL + 1} 行是 {top} 疊在 {bottom} 上面，行沒有嚴格遞增：所以不是任何表的字")
    scene.play(ShowCreation(bad), FadeIn(bad_lab), run_time=0.7)
    scene.wait(1.4)
    scene.say("但每個字都是某個斜表的字：每段自成一列，一列比一列更往右上")
    scene.play(FadeIn(cw), run_time=0.5)
    scene.play(ShowCreation(ccut), run_time=0.4)
    nr = len(S)
    copies = fly_runs(scene, cw, CH3_WORD,
                      lambda t, j: sk.cell_center(nr - 1 - t, run_starts(CH3_WORD)[t] + j), run_time=0.45)
    scene.play(FadeIn(sk), FadeOut(copies), FadeIn(sk_lab), run_time=0.6)
    scene.wait(1.6)


# =============================================================================
# 第 2 段：用字寫列插入
# =============================================================================
def line_tex(line, font_size=34):
    """一行字語言的 Tex：每個符號一個字形；改過的列 TEAL、往下一列走的數 YELLOW。"""
    chunks, cols = [], []
    for t, (kind, *d) in enumerate(line):
        if kind == "row":
            chunks.append("(" + r"\ ".join(str(a) for a in d[0]) + ")")
            cols += [CHANGED_COLOR if d[1] else WHITE] * (len(d[0]) + 2)
        else:
            last = t == len(line) - 1
            chunks.append(r"\cdot\," + str(d[0]) + ("" if last else r"\,\cdot"))
            cols += [WHITE, MOVER_COLOR] + ([] if last else [WHITE])
    tex = Tex(r"\,".join(chunks), font_size=font_size)
    assert len(tex) == len(cols), (len(tex), len(cols))
    for g, c in zip(tex, cols):
        g.set_fill(c)
    return tex


def part_insert_words(scene):
    rule = Tex(r"(u\,x'\,v)\cdot x\ \mapsto\ x'\cdot(u\,x\,v)", font_size=44)
    cond = Tex(r"u\le x<x'\le v", font_size=34, fill_color=MUTED_COLOR)
    head = VGroup(rule, cond).arrange(RIGHT, buff=0.8).move_to(np.array([0.0, 2.55, 0.0]))
    lines = insertion_lines(T0, X_INS)
    texs = VGroup(*[line_tex(l) for l in lines])
    for k, t in enumerate(texs):
        t.move_to(np.array([-5.4, 1.45 - 0.68 * k, 0.0]), aligned_edge=LEFT)
    arrows = VGroup(*[Tex(r"\mapsto", font_size=34).next_to(t, LEFT, buff=0.2) for t in texs[1:]])
    notes = VGroup()
    for k, (r, a, b, u, v) in enumerate(row_moves(T0, X_INS)):
        txt = f"第 {r + 1} 列：{a} 擠出 {b}" if b is not None else f"第 {r + 1} 列：{a} 接在列尾"
        notes.add(zh(txt, font_size=24, color=MUTED_COLOR).move_to(
            np.array([1.9, texs[k + 1].get_center()[1], 0.0]), aligned_edge=LEFT))
    end = mixed("最後一行就是 ", f"$w(T\\leftarrow {X_INS})$", font_size=28, color=OK_COLOR)
    end.move_to(np.array([0.0, -2.35, 0.0]))
    assert_in_frame(head, texs, arrows, notes, end)
    assert_apart(head, VGroup(texs, arrows), gap=0.3)
    assert_apart(VGroup(texs, arrows), notes, gap=0.4)
    assert_apart(VGroup(texs, notes), end, gap=0.3)
    for a, b in zip(texs[:-1], texs[1:]):
        assert_apart(a, b, gap=0.1)

    scene.say("用字來寫列插入：", "$x$", " 取代 ", "$x'$", "，被擠出的 ", "$x'$", " 跑到這一列的前面")
    scene.play(Write(rule), run_time=1.0)
    scene.play(FadeIn(cond), run_time=0.5)
    scene.wait(1.4)
    scene.say("（", "$u$", " 的字母都 ", "$\\le x$", "，", "$x'$", " 是列中第一個比 ", "$x$", " 大的數）例：把 ",
              f"${X_INS}$", " 插入 ", "$T$")
    scene.play(FadeIn(texs[0]), run_time=0.6)
    scene.wait(0.8)
    for k in range(1, len(texs)):
        scene.play(FadeIn(arrows[k - 1]), FadeIn(texs[k], shift=0.1 * DOWN), FadeIn(notes[k - 1]), run_time=0.6)
        scene.wait(0.7)
    scene.say("黃色是正要往下一列走的數；綠色是已經改好的列")
    scene.play(FadeIn(end, shift=0.1 * UP), run_time=0.5)
    scene.wait(1.8)


# =============================================================================
# 第 3 段：Knuth 的兩條基本規則
# =============================================================================
def rule_panel(title, cond, row, ins, result, word, ex, color):
    t = Tex(title, font_size=42, fill_color=color)
    c = Tex(cond, font_size=32, fill_color=MUTED_COLOR)
    row_m = YoungDiagramMob((2,), cell_size=0.62, entries=[row], font_size=36)
    ins_m = Tex(r"\leftarrow " + ins, font_size=38)
    left = VGroup(row_m, ins_m).arrange(RIGHT, buff=0.2)
    res_m = YoungDiagramMob((2, 1), cell_size=0.62, entries=result, font_size=36)
    w_m = Tex(word, font_size=30, fill_color=MUTED_COLOR)
    right = VGroup(res_m, w_m).arrange(DOWN, buff=0.2)
    arr = Arrow(LEFT, RIGHT, buff=0.0, thickness=2.5, fill_color=GREY_B).set_width(0.9)
    pic = VGroup(left, arr, right).arrange(RIGHT, buff=0.3)
    ex_m = mixed("例：", ex, font_size=26, color=MUTED_COLOR)
    return VGroup(t, c, pic, ex_m).arrange(DOWN, buff=0.32)


def part_knuth_rules(scene):
    k1 = rule_panel(r"K':\ y\,z\,x\ \mapsto\ y\,x\,z", r"(x<y\le z)", ["y", "z"], "x", [["x", "z"], ["y"]],
                    r"w=y\,x\,z", f"${ntex(EX_K1[0])}\\ \\mapsto\\ {ntex(EX_K1[1])}$", RULE_COLORS["K'"])
    k2 = rule_panel(r"K'':\ x\,z\,y\ \mapsto\ z\,x\,y", r"(x\le y<z)", ["x", "z"], "y", [["x", "y"], ["z"]],
                    r"w=z\,x\,y", f"${ntex(EX_K2[0])}\\ \\mapsto\\ {ntex(EX_K2[1])}$", RULE_COLORS["K''"])
    k1.move_to(np.array([-3.4, 0.35, 0.0]))
    k2.move_to(np.array([3.4, 0.35, 0.0]))
    inv = mixed("兩條都可以倒過來用：", "$K'^{-1}$", "、", "$K''^{-1}$", font_size=26)
    inv.move_to(np.array([0.0, -2.45, 0.0]))
    assert_in_frame(k1, k2, inv)
    assert_apart(k1, k2, gap=0.6)
    assert_apart(VGroup(k1, k2), inv, gap=0.2)

    scene.say("Knuth 把插入拆成最小的動作：每次只動相鄰的三個字母，交換其中兩個")
    scene.wait(1.4)
    scene.say("$K'$", "：列 ", "$y\\,z$", " 插入較小的 ", "$x$", "，擠出 ", "$y$", "；字 ", "$y\\,z\\,x$", " 變成 ",
              "$y\\,x\\,z$")
    scene.play(FadeIn(k1[0]), FadeIn(k1[1]), run_time=0.6)
    scene.play(FadeIn(k1[2], shift=0.2 * RIGHT), run_time=0.8)
    scene.play(FadeIn(k1[3]), run_time=0.4)
    scene.wait(1.6)
    scene.say("$K''$", "：列 ", "$x\\,z$", " 插入中間的 ", "$y$", "，擠出 ", "$z$", "；字 ", "$x\\,z\\,y$", " 變成 ",
              "$z\\,x\\,y$")
    scene.play(FadeIn(k2[0]), FadeIn(k2[1]), run_time=0.6)
    scene.play(FadeIn(k2[2], shift=0.2 * RIGHT), run_time=0.8)
    scene.play(FadeIn(k2[3]), run_time=0.4)
    scene.wait(1.6)
    scene.say("換句話說：", "$y$", " 一邊的兩個鄰居一大一小時，可以交換它們")
    scene.play(FadeIn(inv, shift=0.1 * UP), run_time=0.5)
    scene.wait(1.6)


# =============================================================================
# 第 4 段：Knuth 等價與命題 1
# =============================================================================
def row_caption(r, a, b, u, v):
    if b is None:
        return [f"第 {r + 1} 列：{a} 接在列尾，不用再動"]
    parts = [f"第 {r + 1} 列：{a} 擠出 {b}"]
    if v:
        parts += [f"；{a} 先用 ", "$K'$", f" 越過 {nums(v)}"]
    if u:
        parts += [f"；{b} 再用 ", "$K''$", f" 往左越過 {nums(u)}"]
    return parts


def part_prop1(scene):
    defn = mixed("能用基本變換（", "$K',K'',K'^{-1},K''^{-1}$", "）一步步互相變到的字：Knuth 等價，記作 ",
                 "$w\\equiv w'$", font_size=24)
    defn.move_to(np.array([0.0, 2.8, 0.0]))
    prop = mixed("命題 1：", "$w(T\\leftarrow x)\\equiv w(T)\\cdot x$", font_size=30)
    prop_box = SurroundingRectangle(prop, buff=0.15, color=YELLOW, stroke_width=3)
    prop_g = VGroup(prop, prop_box).move_to(np.array([0.0, 2.0, 0.0]))
    w0 = CH2_WORD + (X_INS,)
    wm = WordMob(w0, size=0.55, colors={len(w0) - 1: MOVER_COLOR})
    lab0 = Tex(f"w(T)\\cdot {X_INS}=", font_size=36)
    VGroup(lab0, wm).arrange(RIGHT, buff=0.3).move_to(np.array([0.0, 0.95, 0.0]))
    lab1 = Tex(f"w(T\\leftarrow {X_INS})=", font_size=36).move_to(lab0, aligned_edge=RIGHT)
    probe = wm.bracket(0, 3, r"K''^{-1}")                         # 括號與規則名稱佔的空間
    cs = 0.42
    t_small = tableau_mob(T0, cs=cs, top_left=np.array([-5.6, -0.9, 0.0]))
    t_ins = tableau_mob(T_INS, cs=cs, top_left=np.array([-1.9, -0.9, 0.0]))
    t_name = Tex("T", font_size=34).next_to(t_small, UP, buff=0.15)
    ins_name = Tex(f"T\\leftarrow {X_INS}", font_size=34).next_to(t_ins, UP, buff=0.15)
    arr = Arrow(t_small.get_right() + 0.2 * RIGHT, t_ins.get_left() + 0.2 * LEFT, buff=0.0, thickness=2.5,
                fill_color=GREY_B)
    cor = mixed("推論：", "$w(T\\cdot U)\\equiv w(T)\\cdot w(U)$", font_size=28)
    cor_box = SurroundingRectangle(cor, buff=0.18, color=OK_COLOR, stroke_width=3)
    cor_g = VGroup(cor, cor_box).move_to(np.array([3.7, -1.7, 0.0]))
    assert_in_frame(defn, prop_g, lab0, lab1, wm, probe, t_small, t_ins, t_name, ins_name, arr, cor_g)
    assert_apart(defn, prop_g, gap=0.15)
    assert_apart(prop_g, VGroup(wm, probe), gap=0.15)
    assert_apart(VGroup(wm, probe), VGroup(t_name, ins_name, t_small, t_ins), gap=0.2)
    assert_apart(VGroup(t_small, t_ins, arr), cor_g, gap=0.3)
    assert_apart(arr, t_small, gap=0.1)
    assert_apart(arr, t_ins, gap=0.1)

    scene.say("對字做一連串基本變換能互相變到的兩個字，叫做 Knuth 等價")
    scene.play(FadeIn(defn), run_time=0.7)
    scene.wait(1.4)
    scene.say("命題 1：列插入不改變字的等價類。看 ", f"$T\\leftarrow {X_INS}$", " 怎麼拆成基本變換")
    scene.play(FadeIn(prop_g), run_time=0.6)
    scene.play(FadeIn(lab0), FadeIn(wm), FadeIn(t_small), FadeIn(t_name), run_time=0.8)
    scene.wait(0.8)

    chain = insertion_knuth_chain(T0, X_INS)
    k = 0
    for r, a, b, u, v in row_moves(T0, X_INS):
        scene.say(*row_caption(r, a, b, u, v))
        if b is None:
            scene.wait(1.0)
            continue
        scene.wait(0.4)
        for _ in range(len(v) + len(u)):
            i, rule, w = chain[k]
            assert wm.apply_move(scene, i, rule, run_time=0.45, hold=0.1) == w
            k += 1
        scene.wait(0.5)
    assert k == len(chain) == 8 and wm.letters == tableau_word(T_INS)

    cuts = cut_marks(wm, run_starts(wm.letters)[1:])
    scene.play(FadeOut(lab0), FadeIn(lab1), ShowCreation(cuts), GrowArrow(arr), FadeIn(t_ins), FadeIn(ins_name),
               run_time=0.9)
    scene.say(f"{len(chain)} 步之後，切開來正是 ", f"$T\\leftarrow {X_INS}$", " 的字：",
              f"$w(T\\leftarrow {X_INS})\\equiv w(T)\\cdot {X_INS}$")
    scene.wait(2.0)
    scene.say("推論：", "$T\\cdot U$", " 是把 ", "$w(U)$", " 的數逐一插入 ", "$T$", "，所以 ",
              "$w(T\\cdot U)\\equiv w(T)\\cdot w(U)$")
    scene.play(FadeIn(cor_g, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.2)


class SceneF09WordsKnuth(ChuScene):
    def construct(self):
        self.show_header("字與 Knuth 等價")
        check_math()
        part_tableau_word(self)
        self.clear_stage()
        part_any_word(self)
        self.clear_stage()
        part_insert_words(self)
        self.clear_stage()
        part_knuth_rules(self)
        self.clear_stage()
        part_prop1(self)
        self.wait(1.0)
