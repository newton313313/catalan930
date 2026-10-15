"""
Scene N01 —— 前序記法與字（Raney 導讀第 3 節；原文 p. 441）
執行（在 codes/ 內）：manimgl scenes/sceneN01_prefix_words.py SceneN01PrefixWords

1. Cayley (1859)：abcd 在非結合乘法下有 5 種乘積 ↔ 5 棵二元樹 ↔ 5 個字（只記每個符號的元數）。
2. 前序記法：(a+b)+c → ++abc → 型 22000；a+(b+c) → +a+bc → 20200。
3. F(G(x,H(y,z),t),K(u)) → 230200010。
4. Raney 的問題：規定各元數的個數，有幾個字？引數個數 a₀ = 1 + Σ(i−1)a_i（節點數 = 邊數 + 1）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.fulton_draw import assert_apart, assert_in_frame
from utils.raney import a0_of, is_word, lists_with, word_to_tree
from utils.raney_draw import WordTreeMob, word_tiles
from utils.scene_base import ChuScene
from utils.styles import boxed, mixed, zh

CAYLEY = lists_with(1, (0, 3))
EX1 = (2, 2, 0, 0, 0)
EX2 = (2, 0, 2, 0, 0)
EXF = (2, 3, 0, 2, 0, 0, 0, 1, 0)
EXF_LABELS = ["F", "G", "x", "H", "y", "z", "t", "K", "u"]


def paren(word, letters="abcd") -> str:
    it = iter(letters)

    def rec(t):
        k, kids = t
        if k == 0:
            return next(it)
        return "(" + "".join(rec(c) for c in kids) + ")"

    return rec(word_to_tree(word))[1:-1]


def check_math():
    assert [paren(w) for w in CAYLEY] == ["a(b(cd))", "a((bc)d)", "(ab)(cd)", "(a(bc))d", "((ab)c)d"]
    assert all(is_word(w) for w in (EX1, EX2, EXF))
    assert a0_of(1, (1, 2, 1)) == 5 and len(EXF) == 9


class SceneN01PrefixWords(ChuScene):
    def construct(self):
        check_math()
        self.show_header("N01　前序記法與字")

        # 1. Cayley 的問題
        self.say("Cayley (1859)：四個因子 ", "$abcd$", "，乘法不滿足結合律，有幾種乘積？")
        cols = VGroup()
        for w in CAYLEY:
            p = Tex(paren(w), font_size=30)
            t = WordTreeMob(w, x_gap=0.32, y_gap=0.42)
            tiles = word_tiles(w, size=0.26, font_size=18, buff=0.03)
            cols.add(VGroup(p, t, tiles).arrange(DOWN, buff=0.35))
        cols.arrange(RIGHT, buff=0.5).move_to(0.35 * UP)
        assert_in_frame(cols)
        self.play(LaggedStartMap(FadeIn, VGroup(*[c[0] for c in cols]), lag_ratio=0.2), run_time=1.8)
        self.wait(1)
        self.say("每一種乘積是一棵二元樹：乘號是有兩個小孩的節點，因子是葉子")
        self.play(LaggedStartMap(FadeIn, VGroup(*[c[1] for c in cols]), lag_ratio=0.2), run_time=2)
        self.wait(1.5)
        self.say("從根開始、先左後右讀出每個節點有幾個小孩：這串數字叫做「字」")
        self.play(LaggedStartMap(FadeIn, VGroup(*[c[2] for c in cols]), lag_ratio=0.2), run_time=2)
        c3 = Tex(r"C_3=5", font_size=44).next_to(cols, DOWN, buff=0.45)
        assert_in_frame(c3)
        self.play(Write(c3))
        self.wait(2)
        self.play(FadeOut(VGroup(cols, c3)))

        # 2. 前序記法與「型」
        rows = VGroup()
        for w, inf, pre, labs in [(EX1, "(a+b)+c", "{+}{+}abc", ["+", "+", "a", "b", "c"]),
                                  (EX2, "a+(b+c)", "{+}a{+}bc", ["+", "a", "+", "b", "c"])]:
            a = Tex(inf, font_size=40)
            b = Tex(pre, font_size=40)
            tree = WordTreeMob(w, x_gap=0.55, y_gap=0.6, labels=labs, font_size=26)
            tiles = word_tiles(w, size=0.48, font_size=28)
            arr1, arr2 = Tex(r"\to", font_size=40), Tex(r"\to", font_size=40)
            rows.add(VGroup(a, arr1, b, arr2, tiles).arrange(RIGHT, buff=0.35))
            rows[-1].tree = tree
        rows.arrange(DOWN, buff=1.4, aligned_edge=LEFT).move_to(np.array([-1.6, 0.4, 0]))
        trees = VGroup()
        for r in rows:
            r.tree.next_to(r, RIGHT, buff=0.9)
            trees.add(r.tree)
        assert_in_frame(rows, trees)
        self.say("Raney 用前序記法：運算子寫在引數前面，不需要括號")
        for r in rows:
            self.play(FadeIn(r[0]), run_time=0.6)
            self.play(FadeIn(r[1]), FadeIn(r[2]), run_time=0.8)
            self.play(FadeIn(r.tree), run_time=0.8)
            self.play(FadeIn(r[3]), FadeIn(r[4]), run_time=0.8)
            self.wait(0.8)
        self.say("把每個符號換成它要幾個引數（引數是 0）：得到運算式的「型」")
        self.wait(2.5)
        self.play(FadeOut(VGroup(rows, trees)))

        # 3. 大例子
        expr = Tex(r"F(G(x,H(y,z),t),K(u))", font_size=44).move_to(2.4 * UP)
        tree = WordTreeMob(EXF, x_gap=0.75, y_gap=0.75, labels=EXF_LABELS, font_size=26, root_pos=np.array([-1.6, 1.4, 0]))
        tiles = word_tiles(EXF, size=0.5, font_size=28).move_to(np.array([3.6, 0.2, 0]))
        names = VGroup(*[Tex(lab, font_size=24, fill_color=GREY_A).next_to(t, UP, buff=0.1)
                         for lab, t in zip(EXF_LABELS, tiles)])
        assert_in_frame(expr, tree, tiles, names)
        assert_apart(tree, VGroup(tiles, names))
        self.say("原文的例子：", "$F,H$", " 是二元、", "$G$", " 是三元、", "$K$", " 是一元")
        self.play(Write(expr))
        self.play(FadeIn(tree), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(VGroup(n, t)) for n, t in zip(names, tiles)], lag_ratio=0.15), run_time=2.2)
        self.say("型是 ", "$230200010$", "；Raney 把這種數字串叫做「字」（word）")
        self.wait(2.5)

        # 4. Raney 的問題
        self.play(FadeOut(VGroup(expr, tree, names)), tiles.animate.move_to(2.3 * UP))
        q = VGroup(
            zh("Raney 的問題", font_size=34, color=YELLOW),
            mixed("規定 1 出現 ", "$a_1$", " 次、2 出現 ", "$a_2$", " 次、……，有幾個字？", font_size=30),
            mixed("0（引數）的個數不用規定：", "$a_0=1+\\sum_{i\\ge1}(i-1)a_i$", font_size=30),
        ).arrange(DOWN, buff=0.32)
        box = boxed(q, color=YELLOW).move_to(0.3 * UP)
        why = mixed("理由：節點數 ", "$=$", " 邊數 ", "$+1$", "，", "$a_0+\\sum a_i=1+\\sum i\\,a_i$", font_size=28, color=GREY_A)
        ex = mixed("例：", "$a_0=1+0\\cdot1+1\\cdot2+2\\cdot1=5$", "（", "$x,y,z,t,u$", "）", font_size=28)
        VGroup(why, ex).arrange(DOWN, buff=0.25).next_to(box, DOWN, buff=0.4)
        assert_in_frame(tiles, box, why, ex)
        self.play(FadeIn(box, shift=0.2 * UP), run_time=1.2)
        self.say("推廣 Cayley 的問題：運算子可以是任意元數")
        self.wait(1.5)
        self.play(FadeIn(why))
        self.play(FadeIn(ex))
        self.wait(3)
