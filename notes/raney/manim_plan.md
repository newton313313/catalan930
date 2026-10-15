# Raney (1960) 導讀 → manim 動畫 N01–N12 的分鏡

依據：`notes/raney1960_導讀.pdf`（本資料夾的 part1..6.tex）。例子與導讀相同，數字由 `codes/utils/raney.py` 算出、
各場景開頭 `check_math()` assert。隨機例子由 `codes/utils/raney_examples.py` 產生（固定 seed，每次渲染相同）。
畫圖：`codes/utils/raney_draw.py`（`word_tiles`、`WordTreeMob`、`forest_mob`、`rank_walk`、`chu_walk`、`IntPathMob`），
圓上分法用 `polygon_groups.make_configuration`。顏色：符號 j ＝ j 點群組的顏色（2 藍、3 黃、4 綠），1 棕、0 灰。
連續播放：`RaneyPaperDemo`；`render_all.py --raney-paper / --raney-paper-demo`。

| 幕 | 類別 | 導讀 | 內容 |
|---|---|---|---|
| N01 | `SceneN01PrefixWords` | §3 | Cayley：abcd 的 5 種乘積＝5 棵二元樹＝5 個字；前序記法 (a+b)+c → ++abc → 22000；F(G(x,H(y,z),t),K(u)) → 230200010；a₀ = 1+Σ(i−1)a_i（節點＝邊＋1） |
| N02 | `SceneN02RankCounter` | §4.2–4.4 | 讀 230200010，「還欠幾個引數」的計數器 = 秩 + 1，同步畫秩路徑；Rosenbloom 判別法；020 不是字（讀到第一個 0 就結束）；字列 3000200 切成 3000 / 200 |
| N03 | `SceneN03ThreeReadings` | §2.3、§4.5、§12.3 | 同一個 2 字列 3000200：Raney 的秩路徑（停在 −2 之上）、倒過來讀＋1−j 的 Chu 路徑（> 0）、森林；高度 = −後綴的秩；Gessel 的後序碼 00201（鏡射） |
| N04 | `SceneN04RaneyProof` | §5 | σ = 0020030 的 7 個循環變形（k = 2、5 好）；第 1 步 α＝秩最大的弧（3）；第 2 步 σ₁ = σg₅ 的秩路徑停在 −2 之上；第 3 步切成 3000 / 200、輪換；第 4 步沒有別的；200200 的 k = 0、3 給出同一字串 |
| N05 | `SceneN05DoubleCounting` | §6.1 | (1;0,1,1)：30 個字串 = 6 × 5；Chu 原文 Fig. 1 的 5 種分法 ↔ 5 個字（固定點 1 的分解：203000）；Cayley L(1;0,k) = C_k |
| N06 | `SceneN06RandomExamples` | 新增（raney_examples.py） | 循環引理＝均勻隨機樹產生器：打亂符號 → 轉到好的起點 → 樹；同一方法產生隨機不交叉分法；例題集指令 |
| N07 | `SceneN07SplitFirst` | §6.2–6.3 | 定理 2.3：2003000 唯一的 1 字列開頭；L(2;0,1,1) = 5+1+1+5 = 12；定理 2.4：12 = 5+3+4，k = 0：5 = 0+2+3（Chu 收尾、場景 06 的 2+3=5）；F_n = F_1ⁿ、F_1 = 1+Σx_iF_1^i |
| N08 | `SceneN08LStar` | §7–8 | A^P＝以 E₁,E₂,… 為變數的冪級數；L* 的前幾項；(4.1) 驗算 E₁E₂ 的係數 3 = 1 + 2；代換：E_i ↦ x^i（依邊數 → C_e）、E_i ↦ x（無限多 → 不行）、E_{v_i} ↦ x_i（Chu 的 (6)(8)(9)(10)） |
| N09 | `SceneN09Lagrange` | §9 | w = xφ(w)；[xⁿ]w = (1/n)[xⁿ⁻¹]φⁿ ＝ n 個節點的平面樹的權重和；φ = 1+x+x²、n = 4 的 4 棵樹（Motzkin）；代換 E_j ↦ a₀^{j−1}a_j x^j、乘 a₀x；五個 φ 的係數表 |
| N10 | `SceneN10Trinomial` | §10 | w = 1 + x wⁿ 的 Fuss–Catalan 表；Problem 4983（每次乘 r+1 個，P₅(2) = 3 種乘積）；六邊形切成兩個四邊形 3 種；模 2：C_n 奇 ⇔ n = 2^j − 1 |
| N11 | `SceneN11Convolution` | §11 | 定理 7.1（森林切兩片）；投票數表、b(2,3) = 14 = 5+2+2+5；Gould 的 G；γ = 1 ⇒ Chu 的 A_t（α = ½ 也成立：2 = 7/8 + 1/4 + 7/8）；γ = 0 ⇒ Abel：50 = 16+9+9+16 |
| N12 | `SceneN12Summary` | §15 | 邏輯流程圖；Raney ↔ Chu 講義的對照 |
