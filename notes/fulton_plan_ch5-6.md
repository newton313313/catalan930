# Fulton《Young Tableaux》第 5–6 章 → Manim 演示：計畫表（2026-10-10）

**路徑的寫法：** 本檔的相對路徑相對於 `C:\mypython\manim\projects\catalan930`。

## 0. 範圍、來源、原則
- 原文：`C:\mypython\manim\projects\ref\fulton\md\05_the-littlewoodrichardson-rule.md`（書 p.58–71）、`06_symmetric-polynomials.md`（p.72–78），
  PDF 在上一層。OCR 的數學式常有錯，計畫裡的數字都已用程式重算（`codes/utils/tableaux.py` 第 8 節）。
- 新的一組，獨立播放（不接 F01–F19），連續播放叫 `FultonDemo3`；舊影片都不動。
- **生動**：每幕開頭一個「鉤子」（問題、比喻或小遊戲），中間用動畫「做出來」，結尾一句話收束；配色與 F09–F19 相同。
- **省 token**：數學與檢查已完成；場景由 3 個代理人平行做（每人 2–3 幕），只讀本檔第 2–4 節、`utils/fulton_draw.py`、一個範本場景。

## 1. 步驟
| 步驟 | 做法 | 狀態 |
|---|---|---|
| 1 讀原文 | 只讀第 5、6 章的 md | 完成 |
| 2 數學 | `tableaux.py` 第 8 節＋自我檢查（書上的例子全部重算） | 完成 |
| 3 計畫 | 本檔 | 完成 |
| 4 場景 | 3 個代理人：A = F20–F22、B = F23–F24、C = F25–F27；`combkit/tools/render_check.py` 自查 | 完成（8 幕都 STATUS OK） |
| 5 審查、整合 | 看總覽圖；`main.py` 加 `FULTON3_SCENES`、`FultonDemo3`；`render_all.py` 加 `--fulton3`、`--fulton3-demo`；1080p；文件；combkit 1.2.0 | 完成：9 支 1080p 影片，`FultonDemo3` 10 分 0 秒 |
| 6 講義 | `notes/young_tableaux_導讀.tex` 第 5–6 節（`fulton/part3.tex`、`part4.tex`；圖 `fulton/make_figs.py`），17 頁 | 完成（2026-10-11） |

## 2. 數學 API（`codes/utils/tableaux.py` 第 8 節，已驗證）
- LR：`factorizations(V, λ, μ)` → 所有 `(T, U)` 使 T·U = V；`rectifying_skews(ν, λ, U0)` → ν/λ 上 rectify 成 U0 的斜表；
  `is_reverse_lattice(w)`；`lattice_tableau(μ)`（第 i 列全是 i）；`lr_tableaux(ν, λ, μ=None)`；`lr_coefficient(λ, μ, ν)`；
  `lr_product(λ, μ)` → `{ν: c}`；`skew_decomposition(ν, λ)` → `{μ: c}`；`reverse_numbering(ν, λ)` → `{格子: 號碼}`；`remmel_whitney(ν, λ, μ)`。
- 對稱多項式（m 個變數，多項式 = `{指數 tuple: 係數}`）：`monomial_sym`、`power_sum`、`h_lambda`、`e_lambda`、`p_lambda`、`z_lambda`、
  `schur_expand(f, m)` → `{λ: 係數}`、`poly_det`、`jacobi_trudi(λ, m, dual=False)`、`alternant(exps, m)`、`principal_specialization(λ, m)` → `{q 的次數: 係數}`、
  `character_table(n)`、`schur_inner(f, g, m)`、`omega(f, m)`、`poly_scale`、`poly_prod`；已有的 `schur_poly`、`complete_h`、`elementary_e`、`kostka`、`hook_content_count`。
- 常數：`CH5_RL_GOOD`、`CH5_RL_BAD`、`CH5_NU`、`CH5_LAM`、`CH5_DECOMP`、`CH5_S21_SQUARED`、`CH5_ZERO`。
- 已算好的事實：
  - `factorizations(((1,2,3),(4,5),(6,)), (2,1), (2,1))` = 2 個：[14/6 , 23/5]、[16/4 , 23/5]；`((1,1,2),(2,3),(3,))` 也是 2 個 → c = 2。
  - `rectifying_skews((3,2,1), (2,1), ((1,1),(2,)))` = 2 個（也正是兩個 LR 斜表）。
  - (5,4,3,2)/(3,3,1)：15 個 LR 斜表；s_ν/λ = s(5,2)+s(5,1,1)+s(4,1,1,1)+s(2,2,2,1)+2[s(4,3)+s(3,2,1,1)+s(3,3,1)+s(3,2,2)]+3s(4,2,1)。
  - s(2,1)² = s(4,2)+s(4,1,1)+s(3,3)+2s(3,2,1)+s(3,1,1,1)+s(2,2,2)+s(2,2,1,1)；c^{(3,3,3)}_{(2,2),(3,2)} = 0。
  - 反格字 n 個 1、n 個 2 的個數 = 卡塔蘭數 C_n（練習 8）。
  - χ（n=3，順序 (3),(2,1),(1,1,1)）：χ^(3) = 1,1,1；χ^(2,1) = −1,0,2；χ^(1,1,1) = 1,−1,1。
  - s(2,1)(1,q,q²) = q+2q²+2q³+2q⁴+q⁵（q=1 時 8 = d_(2,1)(3)）。

## 3. 場景規格（F20–F27；書頁碼 p.N；長度是目標）
| 代號 | 檔名 / 類別 | 鉤子 → 內容 | 長度 |
|---|---|---|---|
| F20 | `sceneF20_factor_tableaux.py` / `SceneF20FactorTableaux` | **「表也能因數分解嗎？」** 像 12 = 3×4 一樣，問 V = T·U 有幾種寫法（T 形 λ、U 形 μ）。以 V = 123/45/6 示範：試出 2 種分解並逐一驗算乘積；換成 V = 112/23/3 也是 2 種 → 「只看形狀、不看數字」。另一面：ν/λ 上 rectify 成 U0 = 11/2 的斜表也恰好 2 個（滑動動畫）。命題 2：兩邊一一對應 → 定義 LR 數 c^ν_{λμ}（p.60–62） | ~75s |
| F21 | `sceneF21_lr_symmetry.py` / `SceneF21LRSymmetry` | **「同一個數字的三張臉」**：c^ν_{λμ} = c^ν_{μλ} = c^{ν̃}_{λ̃μ̃}（推論 2，舉一個數值例子並轉置畫面）；**「卡住的拼圖」**：λ=(2,2)、μ=(3,2)、ν=(3,3,3)，ν 穿出 λ*μ 的框 → c = 0（p.62–63）；推論 3：S_λ·S_μ = Σ c S_ν（表的乘法表），推論 4：S_{ν/λ} = Σ c S_μ；在多項式裡用 m 個變數驗算一個係數 | ~70s |
| F22 | `sceneF22_yamanouchi.py` / `SceneF22Yamanouchi` | **「倒著開票的選舉」**：反格字＝從字尾往前開票，1 號候選人永遠不落後 2 號、2 號不落後 3 號……；2132121 ✓（長條圖計票動畫）、1232121 ✗（在哪一票翻盤）（p.63）。LR 斜表＝字是反格字的斜表；Lemma 1：它們 rectify 後一定是 U(μ)（第 i 列全是 i）；Lemma 2：基本 Knuth 變換不改變「是不是反格字」（看關鍵的那一票）→ 命題 3：c^ν_{λμ} = ν/λ 上內容 μ 的 LR 斜表數（p.64–66） | ~75s |
| F23 | `sceneF23_lr_rule.py` / `SceneF23LRRule` | **「計數機器」**：ν/λ = (5,4,3,2)/(3,3,1) 的 15 個 LR 斜表依內容 μ 分堆（1、2、3 個）→ s_{ν/λ} 的展開（p.63–65）；s(2,1)·s(2,1)：在每個 ν/(2,1) 上數內容 (2,1) 的 LR 斜表 → 展開式，係數 2 的 (3,2,1) 特別標出兩個表（p.66–67）；練習 2：ν = λ+μ 時 c = 1 | ~80s |
| F24 | `sceneF24_lr_other.py` / `SceneF24LROther` | **「換一副眼鏡看同一批東西」**：反向編號（每列由右往左，p.68）；Remmel–Whitney：μ 上的標準表要滿足兩條規則（動畫逐步放入 1, 2, 3, …，p.68–70），對 (5,4,3,2)/(3,3,1) 數出同樣的 15 個；反格字 ↔ 標準表 U(w)（p.68 的 1123121）；Zelevinsky 的 picture 一句；**彩蛋**：n 個 1、n 個 2 的反格字個數是卡塔蘭數 C_n（練習 8，n=3：5 個，連回卡塔蘭系列） | ~70s |
| F25 | `sceneF25_bases.py` / `SceneF25Bases` | **「五種語言說同一件事」**：3 個變數、次數 3 的對稱多項式，五組基底 m_λ、s_λ、e_λ、h_λ、p_λ 並排（命題 1）；首項單項式說明為何是基底；e 與 h 的關係 Σ(−1)^i e_i h_{k−i} = 0（生成函數 E(−t)H(t) = 1）；Newton 恆等式（k=1..3 逐步驗算）；z(λ) 與 h_n = Σ p_λ/z(λ)，n!/z(λ) 恰是循環型 λ 的排列數（S_3：1、3、2，p.72–74） | ~75s |
| F26 | `sceneF26_jacobi_trudi.py` / `SceneF26JacobiTrudi` | **「三條路通羅馬」**：s_λ 的三個公式殊途同歸——(5) Jacobi–Trudi det(h_{λi+j−i})（例 s(2,1) = h2h1 − h3，矩陣下標沿對角線動畫）、(6) 對偶 det(e_{λ̃i+j−i})、(7) 雙交錯式 a_{λ+δ}/a_δ（m=2 或 3 驗算）（p.75）；**「代入 1, q, q², …」**：s(2,1)(1,q,q²) = q+2q²+2q³+2q⁴+q⁵、乘積公式（練習 5），q=1 得表數 8＝鉤–內容公式（練習 6） | ~75s |
| F27 | `sceneF27_symmetric_functions.py` / `SceneF27SymFunctions` | **「讓變數無限多」**：對稱函數環 Λ（代入 0 會相容，p.77）；Cauchy 核的三種展開 Σh_λ m_λ = Σp_λ p_λ/z(λ) = Σs_λ s_λ（命題 2）→ 內積：s_λ 正交規範、⟨h_λ,m_μ⟩ = δ、⟨p_λ,p_μ⟩ = z(λ)δ（命題 3）；ω：s_λ ↦ s_λ̃、h ↔ e、ω(p_μ) = ±p_μ（推論 1，用 Young 圖翻轉動畫）；**預告**：p_μ = Σ χ^λ_μ s_λ 的 χ（n=3 的 3×3 表）就是第 7 章 S_n 的特徵值 | ~75s |

連續播放：`FultonDemo3` = F20–F27（獨立）。

## 4. 實作規則（同 `fulton_plan_ch2-4.md` 第 5 節）
- ManimGL；繼承 `ChuScene`；`construct` 只用 ChuScene 的方法與模組層級函式（`play_sequence` 會用別的場景物件呼叫）；開頭 `show_header` 與 `check_math()`，結尾 `self.wait(1.0)`。
- 畫面上的每個數字都由 `utils.tableaux` 算出並 assert；版面用 `utils/fulton_draw.py` 的 `assert_in_frame`、`assert_apart`；表用 `tableau_mob`、斜表用 `SkewMob`、字用 `WordMob`。
- 字幕繁體中文、用自己的話；Tex 不放中文；Tex 開頭結尾不要 `\;`、`\,`；t2c 時不要 `\left(…\right)`。
- 只建立自己的場景檔，不改共用檔；每幕約 250–400 行。
- 自查：在 `C:\mypython\manim\projects\combkit` 執行
  `python tools/render_check.py ../catalan930/codes/scenes/<檔名> <類別> --config ../catalan930/codes/custom_config.yml`，看 `runs/<類別>/sheet.png`。
