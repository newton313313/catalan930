"""
Scene F14 —— 字裡的遞增子序列與 L(w,k)（Fulton《Young Tableaux》§3.1，書 p.30–33）

    w = 1 3 4 2 3 4 1 2 2 3 3 2（CH3_WORD）
    L(w,k) = k 條互不相交的弱遞增子序列，長度總和的最大值：L(w,1)=6、L(w,2)=9、L(w,3)=12
        同樣是 9，可以 5+4 也可以 6+3（分配不唯一）；但找不到長度 6、3、3 的三條
    w′ = 3 4 4 2 3 3 1 1 2 2 2 3（CH3_WORD2）= w(P(w))：從右邊一段一段取（＝ P(w) 的各列）就是最好的選法
    Lemma 1：表的字的遞增子序列在圖上只往右、不往下 → 每行至多一格 → L(w,k) = λ1+…+λk
    Lemma 2：基本變換不改變 L(w,k)。knuth_path(w, w′) 共 20 步；第 2 步 K″（1 3 → 3 1）是關鍵情形：
        A = 1 3 3 3 3、B = 2 2 2 2 → A′ = 1 2 2 2 2、B′ = 3 3 3 3（交換兩條的後段，總長仍是 9）
    → 與 w 等價的表，形狀 λk = L(w,k) − L(w,k−1) 只由 w 決定

數字全部由 utils/tableaux.py 算出並 assert（位置 0 起算）。

執行（在 codes/ 資料夾內）：
    manimgl scenes/sceneF14_increasing.py SceneF14Increasing
"""
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import WordMob, assert_apart, assert_in_frame, tableau_mob, tuple_str
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, OK_COLOR, mixed, zh
from utils.tableaux import (
    CH3_TABLEAU,
    CH3_WORD,
    CH3_WORD2,
    greene_numbers,
    insert_word,
    knuth_path,
    max_increasing,
    shape,
    tableau_word,
    word_runs,
)

W = CH3_WORD                                       # 1 3 4 2 3 4 1 2 2 3 3 2（書 p.30）
W2 = CH3_WORD2                                     # 3 4 4 2 3 3 1 1 2 2 2 3（書 p.31）
T = CH3_TABLEAU                                    # P(w)
LAM = (6, 3, 3)
L_VALUES = (6, 9, 12)
SEQ = {1: [[0, 6, 7, 8, 9, 10]],                   # max_increasing(W, k) 給的一組
       2: [[6, 7, 8, 9, 10], [0, 1, 4, 5]],
       3: [[0, 1, 2, 5], [3, 4, 9, 10], [6, 7, 8, 11]]}
ALT2 = [[0, 6, 7, 8, 9, 10], [3, 4, 5]]           # 6 + 3：也是 9
BLOCKS2 = [[6, 7, 8, 9, 10, 11], [3, 4, 5], [0, 1, 2]]   # w′ 從右邊一段一段取 = P(w) 的第 1、2、3 列
PATH_SEQ = [3, 4, 5, 11]                           # w′ 的一條遞增子序列 2 3 3 3
WA = (1, 3, 2, 4, 3, 4, 1, 2, 2, 3, 3, 2)           # knuth_path(w, w′) 第 1 步（K′）之後
WB = (3, 1, 2, 4, 3, 4, 1, 2, 2, 3, 3, 2)           # 第 2 步（K″）之後
A_SEQ, B_SEQ = [0, 1, 4, 9, 10], [2, 7, 8, 11]      # 在 WA 裡：1 3 3 3 3、2 2 2 2
A_NEW, B_NEW = [1, 2, 7, 8, 11], [0, 4, 9, 10]      # 在 WB 裡：1 2 2 2 2、3 3 3 3
N_PATH = 20

SEQ_COLORS = [TEAL, GOLD, PINK]
BASE = GREY_A
WORD_CENTER = np.array([0.6, 1.85, 0.0])
LINE_X = -4.0
GLYPHS = {"cdots": 3, "ldots": 3, "longleftrightarrow": 2, "longrightarrow": 2}


# =============================================================================
# 數學
# =============================================================================
def is_inc(w, seq):
    seq = list(seq)
    return seq == sorted(seq) and all(w[a] <= w[b] for a, b in zip(seq, seq[1:]))


def disjoint(*seqs):
    flat = [p for s in seqs for p in s]
    return len(flat) == len(set(flat))


def can_split(w, lengths):
    """w 的全部位置能否分成長度依序為 lengths 的互不相交弱遞增子序列（暴力）。"""
    def rec(rest, lens):
        if not lens:
            return not rest
        return any(is_inc(w, c) and rec([p for p in rest if p not in c], lens[1:])
                   for c in combinations(rest, lens[0]))
    return rec(list(range(len(w))), list(lengths))


def word_cell(T, p):
    """表 T 的字裡第 p 個字母（0 起算）在表上的格子；字由最下面一列讀起。"""
    for i in reversed(range(len(T))):
        if p < len(T[i]):
            return (i, p)
        p -= len(T[i])
    raise IndexError(p)


def check_math():
    assert insert_word(W) == T and tableau_word(T) == W2 and shape(T) == LAM
    assert sorted(W) == sorted(W2) and W != W2
    for k in (1, 2, 3):
        L, seqs = max_increasing(W, k)
        assert L == L_VALUES[k - 1] == sum(LAM[:k]) and seqs == SEQ[k]
        assert all(is_inc(W, s) for s in seqs) and disjoint(*seqs) and sum(map(len, seqs)) == L
        assert max_increasing(W2, k)[0] == L
    assert max_increasing(W, 4)[0] == L_VALUES[2] == len(W)
    assert greene_numbers(W) == LAM == greene_numbers(W2)
    assert [len(s) for s in SEQ[2]] == [5, 4] and [len(s) for s in ALT2] == [6, 3]
    assert all(is_inc(W, s) for s in ALT2) and disjoint(*ALT2) and sum(map(len, ALT2)) == L_VALUES[1]
    assert can_split(W, (4, 4, 4)) and not can_split(W, LAM)          # 沒有 6、3、3 的三條
    # w′：從右邊一段一段取 = P(w) 的各列
    assert [tuple(W2[p] for p in b) for b in BLOCKS2] == word_runs(W2)[::-1] == list(T)
    assert all(is_inc(W2, b) for b in BLOCKS2)
    assert all(sum(len(b) for b in BLOCKS2[:k]) == L_VALUES[k - 1] for k in (1, 2, 3))
    # Lemma 1 的例子：每行至多一格、由左往右、不往下
    cells = [word_cell(T, p) for p in PATH_SEQ]
    assert is_inc(W2, PATH_SEQ) and all(T[i][j] == W2[p] for p, (i, j) in zip(PATH_SEQ, cells))
    cols = [j for _, j in cells]
    assert cols == sorted(set(cols)) and all(a[0] >= b[0] for a, b in zip(cells, cells[1:]))
    # Lemma 2 的例子
    path = knuth_path(W, W2)
    assert len(path) == N_PATH and path[0] == (1, "K'", WA) and path[1] == (0, "K''", WB)
    assert path[-1][2] == W2
    assert is_inc(WA, A_SEQ) and is_inc(WA, B_SEQ) and disjoint(A_SEQ, B_SEQ)
    assert len(A_SEQ) + len(B_SEQ) == max_increasing(WA, 2)[0] == L_VALUES[1]
    moved = sorted({0: 1, 1: 0}.get(p, p) for p in A_SEQ)               # K″ 交換位置 0、1
    assert [WB[p] for p in moved] == [WA[p] for p in A_SEQ][1::-1] + [WA[p] for p in A_SEQ][2:]
    assert not is_inc(WB, moved) and WB[0] > WB[1]
    assert is_inc(WB, A_NEW) and is_inc(WB, B_NEW) and disjoint(A_NEW, B_NEW)
    assert sorted(WB[p] for p in A_NEW + B_NEW) == sorted(WA[p] for p in A_SEQ + B_SEQ)
    assert (len(A_NEW), len(B_NEW)) == (len(A_SEQ), len(B_SEQ)) == (5, 4)


# =============================================================================
# 畫圖小工具
# =============================================================================
def glyphs(s):
    """Tex 字串 s 會畫出幾個字形（空白、括號、上下標符號不算；\\cdots 算 3 個）。"""
    n, i = 0, 0
    while i < len(s):
        if s[i] == "\\":
            j = i + 1
            while j < len(s) and s[j].isalpha():
                j += 1
            if j == i + 1:                      # \  \, \; 之類：不佔字形
                j += 1
            else:
                n += GLYPHS.get(s[i + 1:j], 1)
            i = j
            continue
        if s[i] not in " {}^_":
            n += 1
        i += 1
    return n


def ctex(pieces, font_size=40):
    """pieces = [(tex, 顏色或 None), ...]：接成一個 Tex，依字形個數替各段上色。"""
    t = Tex("".join(p for p, _ in pieces), font_size=font_size)
    k = 0
    for p, col in pieces:
        n = glyphs(p)
        if col is not None:
            t[k:k + n].set_fill(col)
        k += n
    assert k == len(t), (pieces, k, len(t))
    return t


def sum_pieces(lengths, colors):
    out = []
    for t, (n, c) in enumerate(zip(lengths, colors)):
        if t:
            out.append(("+", None))
        out.append((str(n), c))
    return out


def color_seqs(word, seqs, colors=SEQ_COLORS):
    """word 的方塊依 seqs 上色，其餘回到灰色；回傳動畫。"""
    cmap = {k: BASE for k in range(len(word.tiles))}
    for s, col in zip(seqs, colors):
        for p in s:
            cmap[p] = col
    anims = []
    for k, col in cmap.items():
        anims += word.color_slots({k: col}, opacity=0.15 if col == BASE else 0.5)
    return anims


def seq_line(name, w, seq, color, font_size=40):
    return ctex([(name + "=", None), (r"\ ".join(str(w[p]) for p in seq), color)], font_size)


# =============================================================================
# 第 1 段：L(w,k)
# =============================================================================
def part_definition(scene):
    word = WordMob(W, size=0.7, center=WORD_CENTER)
    wlab = Tex("w=", font_size=44).next_to(word, LEFT, buff=0.3)
    lines = []
    for k in (1, 2, 3):
        L, seqs = max_increasing(W, k)
        if k == 1:
            pieces = [(f"L(w,1)=", None), (str(L), SEQ_COLORS[0])]
        else:
            pieces = [(f"L(w,{k})={L}=", None)] + sum_pieces([len(s) for s in seqs], SEQ_COLORS)
        lines.append(ctex(pieces))
    for line, y in zip(lines, (0.6, -0.3, -1.2)):
        line.move_to(np.array([LINE_X, y, 0.0]), aligned_edge=LEFT)
    alt = ctex([("=", None)] + sum_pieces([len(s) for s in ALT2], SEQ_COLORS))
    alt.next_to(lines[1], RIGHT, buff=0.15).align_to(lines[1][-1], DOWN)
    note = mixed("可是找不到長度 ", f"${','.join(map(str, LAM))}$", " 的三條", font_size=28, color=RED_B)
    note.move_to(np.array([LINE_X, -2.1, 0.0]), aligned_edge=LEFT)
    assert_in_frame(word, wlab, *lines, alt, note)
    for a, b in [(word, lines[0]), (lines[0], lines[1]), (lines[1], lines[2]), (lines[2], note), (alt, lines[2])]:
        assert_apart(a, b, gap=0.2)

    scene.say("從字裡挑幾個字母（不必相鄰），由左到右不減：一條遞增子序列")
    scene.play(FadeIn(wlab), FadeIn(word), run_time=0.8)
    scene.wait(0.6)
    scene.say("$L(w,1)$", f"：最長的一條有幾個字母？這裡是 {L_VALUES[0]}")
    scene.play(*color_seqs(word, SEQ[1]), run_time=0.8)
    scene.play(FadeIn(lines[0], shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(1.0)
    scene.say("$L(w,k)$", "：取 ", "$k$", " 條互不相交的遞增子序列，長度總和的最大值")
    scene.play(*color_seqs(word, SEQ[2]), run_time=0.8)
    scene.play(FadeIn(lines[1], shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(1.2)
    a, b = (len(s) for s in ALT2)
    scene.say(f"同樣是 {L_VALUES[1]}，也可以 {a}+{b}：最大值固定，長度怎麼分卻不唯一")
    scene.play(*color_seqs(word, ALT2), run_time=0.8)
    scene.play(FadeIn(alt, shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(1.2)
    scene.say("$k=3$", f"：三條用完全部 {len(W)} 個字母，所以 ", "$k\\ge 3$", f" 時都是 {L_VALUES[2]}")
    scene.play(*color_seqs(word, SEQ[3]), run_time=0.8)
    scene.play(FadeIn(lines[2], shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(1.2)
    scene.say("但是沒有 ", f"${'+'.join(map(str, LAM))}$", " 的三條：", "$k=1$", " 的最長那條不一定能留下來")
    scene.play(FadeIn(note, shift=0.1 * UP), run_time=0.6)
    scene.wait(1.8)


# =============================================================================
# 第 2 段：w′ = w(P(w))
# =============================================================================
def part_tableau_word(scene):
    word = WordMob(W2, size=0.7, center=WORD_CENTER)
    wlab = Tex("w'=", font_size=44).next_to(word, LEFT, buff=0.3)
    tab = tableau_mob(T, cs=0.62, top_left=(LINE_X, 0.55, 0))
    tlab = Tex("P(w)=", font_size=40).next_to(tab, LEFT, buff=0.25)
    lines = VGroup()
    for k in (1, 2, 3):
        L = max_increasing(W2, k)[0]
        pieces = [(f"L(w',{k})=", None)] + sum_pieces([len(b) for b in BLOCKS2[:k]], SEQ_COLORS)
        if k > 1:
            pieces.append((f"={L}", None))
        lines.add(ctex(pieces))
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(np.array([1.0, -0.4, 0.0]), aligned_edge=LEFT)
    assert_in_frame(word, wlab, tab, tlab, lines)
    assert_apart(word, VGroup(tab, tlab, lines), gap=0.3)
    assert_apart(tab, lines, gap=0.5)

    scene.say("另一個字 ", "$w'$", "：用的字母完全相同，只是順序不同")
    scene.play(FadeIn(wlab), FadeIn(word), run_time=0.8)
    scene.wait(0.6)
    scene.say("$w'$", " 其實是 ", "$P(w)$", " 的字：", "$w$", " 列插入得到的表，由下往上讀")
    scene.play(FadeIn(tlab), FadeIn(tab), run_time=0.8)
    scene.wait(1.2)
    scene.say("在 ", "$w'$", " 裡，從右邊一段一段取，就是最好的選法")
    for k, (b, col) in enumerate(zip(BLOCKS2, SEQ_COLORS)):
        row = [tab.cell(k, j).animate.set_fill(col, opacity=0.45) for j in range(len(T[k]))]
        scene.play(*word.color_slots({p: col for p in b}, opacity=0.5), *row, run_time=0.6)
        scene.play(FadeIn(lines[k], shift=0.1 * RIGHT), run_time=0.4)
        scene.wait(0.4)
    scene.say("得到的還是 ", f"${L_VALUES[0]},\\ {L_VALUES[1]},\\ {L_VALUES[2]}$", "，和 ", "$w$",
              " 的 ", "$L(w,k)$", " 完全相同")
    scene.wait(2.0)


# =============================================================================
# 第 3 段：Lemma 1
# =============================================================================
def part_lemma1(scene):
    word = WordMob(W2, size=0.55, center=np.array([0.3, 2.55, 0.0]))
    wlab = Tex("w'=", font_size=36).next_to(word, LEFT, buff=0.25)
    tab = tableau_mob(T, cs=0.8, top_left=(-6.3, 1.5, 0))
    lam = Tex(f"\\lambda={tuple_str(LAM)}", font_size=36).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
    cells = [word_cell(T, p) for p in PATH_SEQ]
    arrows = VGroup(*[Arrow(tab.cell_center(*a), tab.cell_center(*b), buff=0.2, thickness=3.5, fill_color=YELLOW)
                      for a, b in zip(cells, cells[1:])])
    p1 = zh("① 遞增子序列在表上只往右走，不會往下", font_size=26)
    p2 = zh("② 所以每一行最多用到一格", font_size=26)
    p3 = mixed("③ ", "$k$", " 條的總長 ", "$\\le$", " 前 ", "$k$", " 列的格數", font_size=26)
    panel = VGroup(p1, p2, p3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    panel.move_to(np.array([-0.4, 0.75, 0.0]), aligned_edge=LEFT)
    formula = Tex(r"L(w,k)=\lambda_1+\cdots+\lambda_k", font_size=46)
    box = SurroundingRectangle(formula, buff=0.2, color=YELLOW, stroke_width=3)
    VGroup(formula, box).move_to(np.array([2.6, -1.75, 0.0]))
    assert_in_frame(word, wlab, tab, lam, panel, formula, box)
    assert_apart(word, VGroup(tab, panel), gap=0.25)
    assert_apart(VGroup(tab, lam), panel, gap=0.3)
    assert_apart(VGroup(tab, lam), box, gap=0.3)
    assert_apart(panel, box, gap=0.25)

    scene.say("Lemma 1：如果 ", "$w$", " 是一個表的字，", "$L(w,k)$", " 直接看形狀就知道")
    scene.play(FadeIn(wlab), FadeIn(word), FadeIn(tab), FadeIn(lam), run_time=0.8)
    scene.wait(0.5)
    vals = "\\ ".join(str(W2[p]) for p in PATH_SEQ)
    scene.say("例如 ", "$w'$", " 裡的 ", f"${vals}$", "：在表上一路往右，沒有往下")
    scene.play(*word.color_slots({p: YELLOW for p in PATH_SEQ}, opacity=0.5),
               *[tab.cell(i, j).animate.set_fill(YELLOW, opacity=0.4) for i, j in cells], run_time=0.7)
    scene.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.5), run_time=1.2)
    scene.play(FadeIn(p1, shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(0.8)
    scene.say("字由最下列讀起；往上一列時一定要往右，因為左上方的數都比較小")
    scene.wait(1.9)
    scene.say("所以每一行最多用一格：", "$k$", " 條加起來不超過前 ", "$k$", " 列的格數")
    scene.play(FadeIn(p2, shift=0.1 * RIGHT), run_time=0.5)
    scene.play(FadeIn(p3, shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(1.2)
    scene.say("而前 ", "$k$", " 列本身就是 ", "$k$", " 條遞增子序列，所以剛好相等")
    scene.play(Write(formula), ShowCreation(box), run_time=1.0)
    scene.wait(1.8)


# =============================================================================
# 第 4 段：Lemma 2
# =============================================================================
def part_lemma2(scene):
    word = WordMob(W, size=0.7, center=WORD_CENTER)
    wlab = Tex("w=", font_size=44).next_to(word, LEFT, buff=0.3)
    w2lab = Tex("w'=", font_size=44).next_to(word, LEFT, buff=0.3)
    a_line = seq_line("A", WA, A_SEQ, SEQ_COLORS[0])
    b_line = seq_line("B", WA, B_SEQ, SEQ_COLORS[1])
    a_new = seq_line("A'", WB, A_NEW, SEQ_COLORS[0])
    b_new = seq_line("B'", WB, B_NEW, SEQ_COLORS[1])
    for m, y in ((a_line, 0.25), (b_line, -0.55), (a_new, 0.25), (b_new, -0.55)):
        m.move_to(np.array([LINE_X, y, 0.0]), aligned_edge=LEFT)
    sums = []
    for name, (p, q) in (("|A|+|B|=", (A_SEQ, B_SEQ)), ("|A'|+|B'|=", (A_NEW, B_NEW))):
        s = ctex([(name, None)] + sum_pieces([len(p), len(q)], SEQ_COLORS) + [(f"={len(p) + len(q)}", None)])
        s.move_to(np.array([0.6, -0.15, 0.0]), aligned_edge=LEFT)
        sums.append(s)
    concl1 = mixed("$L(w,k)=L(w',k)$", "：", f"${L_VALUES[0]},\\ {L_VALUES[1]},\\ {L_VALUES[2]}$", font_size=30)
    l1, l2, l3 = L_VALUES
    concl2 = Tex(f"\\lambda=({l1},\\ {l2}-{l1},\\ {l3}-{l2})={tuple_str(LAM)}", font_size=40)
    concl = VGroup(concl1, concl2).arrange(DOWN, buff=0.35).move_to(np.array([0.0, -1.85, 0.0]))
    assert (l1, l2 - l1, l3 - l2) == LAM
    assert_in_frame(word, wlab, a_line, b_line, a_new, b_new, *sums, concl)
    for m in (a_line, b_line, a_new, b_new):
        for s in sums:
            assert_apart(m, s, gap=0.3)
    assert_apart(word, VGroup(a_line, a_new), gap=0.75)                 # 留位置給 K′ 的標籤
    assert_apart(VGroup(b_line, b_new, *sums), concl, gap=0.3)

    scene.say("Lemma 2：做一次基本變換，", "$L(w,k)$", " 不會改變")
    scene.play(FadeIn(wlab), FadeIn(word), run_time=0.8)
    scene.wait(0.4)
    scene.say("第 1 步 ", "$K'$", "：4 2 換成 2 4；沒有遞增子序列同時用到 4 和 2，舊的照樣能用")
    scene.play(FadeOut(wlab), run_time=0.3)
    word.apply_move(scene, 1, "K'", run_time=0.6, hold=0.6)
    assert word.letters == WA
    scene.wait(0.6)
    scene.say("第 2 步 ", "$K''$", " 要把 1 3 換成 3 1；先取兩條 ", "$A$", "、", "$B$", f"，共 {L_VALUES[1]} 個字母")
    scene.play(*color_seqs(word, [A_SEQ, B_SEQ]), FadeIn(a_line), FadeIn(b_line), run_time=0.8)
    scene.play(FadeIn(sums[0]), run_time=0.5)
    scene.wait(1.0)
    word.apply_move(scene, 0, "K''", run_time=0.6, hold=0.3)
    assert word.letters == WB
    bad = word.bracket(0, 2, f"{WB[0]}>{WB[1]}", color=RED, font_size=32)
    scene.say("換位之後 ", "$A$", " 變成先 3 後 1，不再遞增了")
    scene.play(FadeIn(bad), run_time=0.4)
    scene.wait(1.2)
    scene.say("修補：", "$A$", " 改接 ", "$B$", " 的 2 2 2 2，", "$B$", " 改成 3 接上 ", "$A$", " 剩下的 3 3 3")
    scene.play(FadeOut(bad), *color_seqs(word, [A_NEW, B_NEW]), ReplacementTransform(a_line, a_new),
               ReplacementTransform(b_line, b_new), ReplacementTransform(sums[0], sums[1]), run_time=1.0)
    scene.wait(1.8)
    scene.say("一般情形也是這樣交換兩條的後段：總長不變，所以 ", "$L$", " 不會變小")
    scene.wait(1.7)

    rest = knuth_path(W, W2)[2:]
    scene.say(f"從 ", "$w$", f" 到 ", "$w'$", f" 一共 {N_PATH} 步基本變換，每一步都保持 ", "$L(w,k)$")
    scene.play(FadeOut(a_new), FadeOut(b_new), FadeOut(sums[1]), *color_seqs(word, []), run_time=0.6)
    for i, rule, new in rest:
        a = i + 1 if rule.startswith("K'") and not rule.startswith("K''") else i
        scene.play(*word.swap_anims(a, a + 1), run_time=0.22)
        assert word.letters == new
    assert word.letters == W2
    scene.play(FadeIn(w2lab), run_time=0.4)
    scene.play(FadeIn(concl1, shift=0.1 * UP), run_time=0.6)
    scene.wait(0.6)
    scene.say("所以與 ", "$w$", " 等價的表，形狀 ", "$\\lambda_k=L(w,k)-L(w,k-1)$", " 只由 ", "$w$", " 決定")
    scene.play(FadeIn(concl2, shift=0.1 * UP), run_time=0.6)
    scene.wait(2.1)


class SceneF14Increasing(ChuScene):
    def construct(self):
        self.show_header("遞增子序列與 L(w,k)")
        check_math()
        part_definition(self)
        self.clear_stage()
        part_tableau_word(self)
        self.clear_stage()
        part_lemma1(self)
        self.clear_stage()
        part_lemma2(self)
        self.wait(1.0)
