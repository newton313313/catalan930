"""
Scene 00e —— 括號與滿二元樹的一一對應（來源論文 2.3 節）

    完全括號化  <->  滿二元樹（n 個內部節點、n+1 片葉子）
    每一次乘法 -> 一個內部節點；每一個因子 -> 一片葉子；最後一次乘法 -> 樹根

執行（在 codes/ 資料夾內）：
    manimgl scenes/scene00e_binary_trees.py Scene00eBinaryTrees
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manimlib import *

from utils.catalan_draw import (
    CATALAN_COLOR,
    LEFT_COLOR,
    RIGHT_COLOR,
    BinaryTreeMob,
    non_paren_glyphs,
    paren_mob,
)
from utils.counting import binary_trees, tree_size
from utils.scene_base import ChuScene
from utils.styles import MUTED_COLOR, ROOT_COLOR, YELLOW, mixed, zh

FACTORS = "abcd"


def tree_for(t, root_pos, leaf_gap, level_height, leaf_font, node_radius=0.09, colored=False):
    return BinaryTreeMob(t, root_pos=root_pos, leaf_gap=leaf_gap, level_height=level_height,
                         node_radius=node_radius, leaf_labels=list(FACTORS[: tree_size(t) + 1]),
                         leaf_font=leaf_font, edge_width=3, root_color=ROOT_COLOR, colored=colored)


def bijection_animations(formula: Tex, tree: BinaryTreeMob):
    """乘號 -> 內部節點（中序對中序）、因子 -> 葉子（由左到右）。"""
    ops = [g for g, tok in zip(formula.glyphs, formula.tokens) if tok == "·"]
    letters = [g for g, tok in zip(formula.glyphs, formula.tokens) if tok not in "()·"]
    assert len(ops) == len(tree.nodes) and len(letters) == len(tree.leaves)
    first = [TransformFromCopy(o, n) for o, n in zip(ops, tree.nodes)]
    second = [TransformFromCopy(l, f) for l, f in zip(letters, tree.leaves)]
    return first, second


class Scene00eBinaryTrees(ChuScene):
    def construct(self):
        self.show_header("括號與二元樹")
        trees = binary_trees(3)

        # ------------------------------------------------------------ 定義
        definition = VGroup(
            mixed("滿二元樹（full binary tree）：每個內部節點恰好有左、右兩個小孩，左右有分別", font_size=26),
            mixed("有 ", "$n$", " 個內部節點的滿二元樹，恰有 ", "$n+1$", " 片葉子", font_size=26,
                  color=MUTED_COLOR),
        ).arrange(DOWN, buff=0.15)
        definition.move_to(2.75 * UP)
        self.play(FadeIn(definition, shift=0.2 * DOWN), run_time=0.9)
        self.say("把括號寫成一棵樹")
        self.wait(1.0)

        # ------------------------------------------------------------ (a·b)·(c·d) 變成樹
        t_ab_cd = trees[2]
        formula = paren_mob(t_ab_cd, FACTORS, font_size=56).move_to(1.55 * UP)
        self.play(Write(formula), run_time=1.0)
        tree = tree_for(t_ab_cd, root_pos=np.array([0, 0.45, 0]), leaf_gap=1.25,
                        level_height=1.0, leaf_font=46, node_radius=0.11)
        first, second = bijection_animations(formula, tree)
        self.say("每一次乘法（", "$\\cdot$", "）變成一個內部節點")
        self.play(*first, run_time=1.2)
        self.say("每一個因子變成一片葉子；括號告訴我們誰和誰先乘")
        self.play(*second, run_time=1.2)
        self.play(LaggedStart(*[ShowCreation(e) for e in tree.edges], lag_ratio=0.15), run_time=1.2)
        root_op = [g for g, tok, part in zip(formula.glyphs, formula.tokens, formula.parts)
                   if tok == "·" and part == "root"][0]
        root_node = tree.nodes[tree.node_parts.index("root")]
        self.say("最後一次乘法（橘色）就是樹根")
        self.play(root_op.animate.set_fill(ROOT_COLOR), Indicate(root_node, scale_factor=1.6,
                                                                   color=ROOT_COLOR), run_time=1.0)
        self.wait(1.0)

        # ------------------------------------------------------------ 再一個：a·(b·(c·d))
        t_right = trees[0]
        formula2 = paren_mob(t_right, FACTORS, font_size=56).move_to(1.55 * UP)
        tree2 = tree_for(t_right, root_pos=np.array([0, 0.45, 0]), leaf_gap=1.25,
                         level_height=0.85, leaf_font=46, node_radius=0.11)
        self.say("換一種括法 ", "$a\\cdot(b\\cdot(c\\cdot d))$", "，樹的形狀就不同")
        self.play(FadeOut(VGroup(formula, tree)), run_time=0.6)
        self.play(Write(formula2), run_time=0.9)
        first, second = bijection_animations(formula2, tree2)
        self.play(*first, *second, run_time=1.3)
        self.play(LaggedStart(*[ShowCreation(e) for e in tree2.edges], lag_ratio=0.15), run_time=1.0)
        root_op2 = [g for g, tok, part in zip(formula2.glyphs, formula2.tokens, formula2.parts)
                    if tok == "·" and part == "root"][0]
        self.play(root_op2.animate.set_fill(ROOT_COLOR), run_time=0.5)
        self.wait(1.2)

        # ------------------------------------------------------------ 五種括法、五棵樹
        self.play(FadeOut(VGroup(formula2, tree2, definition)), run_time=0.7)
        xs = np.linspace(-5.2, 5.2, 5)
        formulas, small_trees = VGroup(), VGroup()
        for x, t in zip(xs, trees):
            f = paren_mob(t, FACTORS, font_size=30).move_to(np.array([x, 2.35, 0]))
            tr = tree_for(t, root_pos=np.array([x, 1.55, 0]), leaf_gap=0.42, level_height=0.48,
                          leaf_font=28, node_radius=0.06)
            formulas.add(f)
            small_trees.add(tr)
        self.say("4 個因子的 5 種括法，對應 5 棵不同的滿二元樹")
        for f, tr in zip(formulas, small_trees):
            first, second = bijection_animations(f, tr)
            self.play(FadeIn(f), run_time=0.3)
            self.play(*first, *second, *[ShowCreation(e) for e in tr.edges], run_time=0.7)
        self.wait(0.8)

        # 樹根把樹切成左、右兩棵子樹：又是同一個遞迴
        colored = VGroup(*[tree_for(t, root_pos=np.array([x, 1.55, 0]), leaf_gap=0.42, level_height=0.48,
                                    leaf_font=28, node_radius=0.06, colored=True)
                           for x, t in zip(xs, trees)])
        colored_f = VGroup(*[paren_mob(t, FACTORS, font_size=30, colored=True).move_to(f)
                             for t, f in zip(trees, formulas)])
        self.say("樹根下面是左子樹（青）和右子樹（粉紅），各自獨立：又是 ",
                 "$C_kC_{n-1-k}$", " 的結構")
        self.play(*[Transform(a, b) for a, b in zip(small_trees, colored)],
                  *[Transform(a, b) for a, b in zip(formulas, colored_f)], run_time=1.2)
        self.wait(1.8)

        # 注意：Tex 字串的開頭、結尾不要放 \; 之類的間距指令（見交接說明「已知問題」）
        box_text = mixed("完全括號化", "$\\longleftrightarrow$", "滿二元樹", font_size=32, buff=0.25)
        detail = mixed("$n+1$", " 個因子 ", "$\\leftrightarrow$", " ", "$n+1$", " 片葉子；",
                       "$n$", " 次乘法 ", "$\\leftrightarrow$", " ", "$n$", " 個內部節點", font_size=26,
                       color=MUTED_COLOR)
        count = mixed("數目都是 ", "$C_n$", font_size=28, t2c={"C_n": CATALAN_COLOR})
        block = VGroup(box_text, detail, count).arrange(DOWN, buff=0.18)
        box = SurroundingRectangle(block, buff=0.22, color=YELLOW, stroke_width=3)
        VGroup(block, box).move_to(1.35 * DOWN)
        self.play(FadeIn(block, shift=0.2 * UP), ShowCreation(box), run_time=1.0)
        self.wait(1.8)

        # ------------------------------------------------------------ 另一種常見說法：拿掉葉子
        self.say("拿掉所有葉子，剩下 ", "$n$", " 個節點的二元樹（每個節點的左、右小孩可有可無）")
        leaf_stuff = []
        for tr in small_trees:
            leaf_stuff.append(tr.leaves)
            leaf_stuff += [e for e, kind in zip(tr.edges, tr.edge_kinds) if kind == "leaf"]
        self.play(*[FadeOut(m) for m in leaf_stuff], run_time=1.0)
        note = mixed("來源論文說的「", "$n$", " 個頂點的二元樹」就是這一種；兩種說法一一對應，數目都是 ",
                     "$C_n$", font_size=24, color=MUTED_COLOR)
        note.next_to(box, DOWN, buff=0.25)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(3.0)
