# Fulton《Young Tableaux》第 2–4 章（到 R-S-K）→ Manim 演示：計畫表（2026-10-10）

**路徑的寫法：** 本檔的相對路徑相對於 `C:\mypython\manim\projects\catalan930`。

## 0. 範圍與來源
- 原文（僅供個人研讀，不可散布）：`C:\mypython\manim\projects\ref\fulton\` 的各章 PDF（掃描頁＋OCR 文字層），
  機械轉出的 Markdown 在同一資料夾的 `md\`（`02_…`、`03_…`、`04_…`；數學式的 OCR 常有錯，要精確內容時看 PDF 頁面）。
  全書 PDF（`London_Mathematical_Society…Young_Tableaux….pdf`）只有影像、沒有文字層，只當參考，不轉檔。
- 前 4 章：第 1 章 Bumping and sliding（書 p.7–16）、第 2 章 Words; the plactic monoid（p.17–29）、
  第 3 章 Increasing sequences; proofs of the claims（p.30–35）、第 4 章 The R-S-K correspondence（p.36–57）。
- **已做過、不重做**：Notation 與第 1 章（F01–F08，見 `notes/fulton_plan.md`）；鉤長公式與鉤上漫步（MIT 場景 M13、M14，只在 F19 回顧一句）。
- 影片獨立（不接卡塔蘭／Chu／MIT），也不接 F01–F08 的 `FultonDemo`（那支影片不重做、不覆寫）；新的連續播放叫 `FultonDemo2`。
- 畫面上的說明用自己的話，不逐字抄書；例子用書上的資料。

## 1. 步驟（省 token）
| 步驟 | 做法 | 狀態 |
|---|---|---|
| 0 轉檔 | `ref/fulton/md/convert_to_md.py` 機械轉出各章（不讀進對話） | 完成 |
| 1 計畫 | 只讀第 2–4 章的 md（不看頁面影像），寫本檔 | 完成 |
| 2 數學 | `codes/utils/tableaux.py` 第 7 節（下面第 2 節），附暴力驗證；書上的例子都 assert | 完成（`python -m utils.tableaux`） |
| 3 畫圖工具 | `codes/utils/fulton_draw.py`（第 3 節），已試渲染 | 完成 |
| 4 場景 | 4 個代理人平行，各做 2–3 幕；每幕用 `combkit/tools/render_check.py` 看總覽圖自查 | 完成（11 幕都 STATUS OK） |
| 5 審查 | 主對話只看總覽圖與代理人的簡短回報，必要時修 | 完成（數字與版面逐幕檢查） |
| 6 整合 | `main.py` 加 `FULTON2_SCENES`、`FultonDemo2`；`render_all.py` 加 `--fulton2`、`--fulton2-demo`；輸出 1080p；更新 README、交接說明；combkit 同步、升版 1.1.0、重新打包 | 完成：12 支 1080p 影片，`FultonDemo2` 13 分 18 秒 |
| 7 講義 | 附錄 B（`notes/fulton/part1.tex`、`part2.tex`；圖 `fulton/make_figs.py` → `figs.tex`），講義變成 51 頁 | 完成（2026-10-10）；2026-10-11 移到獨立的 `notes/young_tableaux_導讀.tex` |

## 2. 數學資料：`codes/utils/tableaux.py` 第 7 節（純 Python，已驗證）
- 字：`word_runs(w)`（在「下一個變小」處切開）、`word_to_tableau(w)`（不是表的字傳回 None）、`skew_from_word(w)`、`column_word(S)`。
- Knuth：`knuth_moves(w)` → `[(i, 規則, 新字)]`（規則 `"K'"`、`"K'⁻¹"`、`"K''"`、`"K''⁻¹"`；i = 三個字母的起點）、
  `knuth_class(w)`、`knuth_path(w1, w2)`（最短變換序列）、`insertion_knuth_chain(T, x)`（Knuth 對列插入的拆解，書 p.18–19）。
- 遞增子序列：`max_increasing(w, k, decreasing=False)` → `(L(w,k), 一組子序列的位置)`、`greene_numbers(w)`（= P(w) 的列長）、
  `remove_largest(w, p)`、`tableau_from_greene(w)`（第 3 章唯一性證明當演算法）。
- R-S-K：`rsk_steps(top, bottom=None)` → `[(u, v, P_k, Q_k, 新格子)]`（bottom 省略＝字）、`rsk`、`inverse_rsk(P, Q)`、`is_lex_array`、
  `matrix_to_array`、`array_to_matrix`、`rsk_matrix(A)`、`transpose_matrix`。
- 矩陣球：`ball_numbering(A)` → `{(i,j): [號碼]}`（0 起算）、`derived_matrix(A)`、`matrix_ball(A)` → `(P, Q, 各輪 {"A","balls","P_row","Q_row"})`。
- 其他：`pieri_shapes(λ, p, vertical)`、`poly_mul`、`poly_sum`、`lex_greater`、`dominates`（已有）、`kostka_matrix(n)`（字典序由小到大，下三角）、
  `hook_content_count(λ, m)`、`count_involutions(n)`；已有的 `insert_word`、`row_insert`、`reverse_bump`、`rectify`、`star`、`jdt_steps`、`ssyt`、`kostka`、`schur_poly`…
- 書上的例子常數：`CH2_WORD`、`CH2_SLIDE_BEFORE/AFTER/CHAIN`、`CH3_WORD`、`CH3_WORD2`、`CH3_TABLEAU`、`CH4_WORD`、`CH4_ARRAY`、`CH4_MATRIX`、`CH4_P`、`CH4_Q`、`CH4_HOOK_SHAPE`。
- 已算好的事實：`insertion_knuth_chain(FULTON_INSERT_T, 2)` 共 8 步（K''×3、K'、K''×4）；`rsk(CH4_WORD)` 的
  P = ((1,1,3,5),(2,3),(4,4),(5,7),(8,))、Q = ((1,3,6,8),(2,5),(4,9),(7,10),(11,))；L(CH3_WORD, k) = 6, 9, 12；
  `matrix_ball(CH4_MATRIX)` 兩輪：A♭ = ((0,0),(0,1),(0,2))；Erdős–Szekeres 例 (4,9,2,10,6,1,8,3,7,5) 的 P 形狀 (3,3,3,1)。

## 3. 畫圖工具：`codes/utils/fulton_draw.py`
`assert_in_frame`、`assert_apart`、`X_MIN…Y_MAX`、`tuple_str`、`labeled(tex, mob)`；`tableau_mob(T, cs, fs, top_left/center)`（YoungDiagramMob，
`.entry(i,j).tab_value`）；`SkewMob(S, cs, …, show_mu)`（列首 None＝μ 灰格、中間 None＝洞的黃色虛線框；`.cell`、`.entry`、`.cell_center`）；
`WordMob(w, size, colors, center)`（`.tiles`、`.letters`、`.slot(k)`、`.bracket(i, n, label, color)`、`.apply_move(scene, i, rule)`、`.color_slots`）；
`word_tex(w, colors)`（一位數字母的 Tex，`tex[k]` = 第 k 個字母）；`TwoRowArray(top, bottom)`（`.col(k)`）；
`BallMatrixMob(A, numbering)`（`.ball(i,j,t)`、`.cell_center(i,j)`、`.cell_square(i,j)`，號碼在 `.number`）。
其他可沿用：`utils/mit_draw.py` 的 `YoungDiagramMob`、`box_row`；F07 的滑動板子工具（`scenes/sceneF07_jeu_de_taquin.py` 的 `make_board`、`anims_*`）。

## 4. 場景規格（書頁碼 p.N；長度是目標）
| 代號 | 檔名 / 類別 | 內容 | 長度 |
|---|---|---|---|
| F09 | `sceneF09_words_knuth.py` / `SceneF09WordsKnuth` | (1) 表↔字：`CH2_WORD` 在變小處切成 56｜446｜2355｜1223，由下往上疊回 `FULTON_INSERT_T`；3 4 1 4 疊起來行不嚴格遞增→不是表的字；任何字都是某個斜表的字（`skew_from_word(CH3_WORD)` 的階梯）（p.17）。(2) 字的語言寫列插入：(u x′ v)·x ↦ x′·(u x v)（u ≤ x < x′ ≤ v），例：插入 2 的四行（p.18）。(3) Knuth 的原子步驟：K′ y z x→y x z（x<y≤z）＝列 [y z] 插入 x；K″ x z y→z x y（x≤y<z）＝列 [x z] 插入 y，用兩個小插入圖記（p.19）。(4) 基本變換、Knuth 等價 ≡；Proposition 1：w(T←x) ≡ w(T)·x，在 `WordMob` 上播放 `insertion_knuth_chain(FULTON_INSERT_T, 2)` 的 8 步，結尾等於 w(T←2)；推論 w(T·U) ≡ w(T)·w(U) | ~80s |
| F10 | `sceneF10_slides_theorem.py` / `SceneF10SlidesTheorem` | (1) 滑動也保持 ≡（p.20–22）：水平滑動字不變；垂直滑動 `CH2_SLIDE_BEFORE`→`AFTER`（u,v,x,y,z = 1..5），字 23514 → 25134，用 `CH2_SLIDE_CHAIN` 四步（規則用 `knuth_moves` 查）；一般情形一句帶過 → Proposition 2。(2) 主定理：每個字恰與一個表的字等價；存在＝正則程序 P(w)=(…(x₁←x₂)…)←x_r（例 `CH3_WORD`→`CH3_TABLEAU`，快速播放），唯一性第 3 章證（p.22）。(3) 推論 1：Rect(S)＝唯一與 w(S) 等價的表（`FULTON_SKEW`：`rectify` 與 `insert_word(w(S))` 相同）。(4) 推論 2：T·U 的三種做法（列插入、Rect(T∗U)、P(w(T)w(U))）相同，三個箭頭指向同一個表（`FULTON_INSERT_T`、`FULTON_PRODUCT_U`）（p.23）。(5) Plactic monoid：字的連接 ↔ 表的乘積；tableau ring R[m] → ℤ[x]，T ↦ x^T（p.23–24） | ~80s |
| F11 | `sceneF11_pieri.py` / `SceneF11Pieri` | S_λ＝所有 λ 形表的和；Pieri (4)(5)：S_λ·S_(p)＝Σ S_μ（μ/λ 水平帶）、S_λ·S_(1^p)（垂直帶）；例 λ=(2,1)、p=2：`pieri_shapes` 得 (4,1),(3,2),(3,1,1),(2,2,1) 與 (3,2),(3,1,1),(2,2,1),(2,1,1,1)，新格子上色；理由＝§1.1 的命題（F05：插入弱遞增序列→水平帶，且分解唯一）；(6)(7) s_λh_p、s_λe_p，用 m=3 的 `poly_mul`/`schur_poly` 驗算幾個係數（p.24–25） | ~60s |
| F12 | `sceneF12_kostka.py` / `SceneF12Kostka` | 內容 μ、Kostka 數 K_λμ＝水平帶鏈的個數；例 λ=(3,2)、μ=(2,2,1)：列出 `ssyt(λ, content=μ)` 的表並依數字上色看出鏈；(8) h_μ = Σ K_λμ s_λ（例 μ=(2,1,1)）、(9) e_μ 一句；兩種序：(2,2)⊴(3,1) 但不包含；(4,1,1) 字典序大於 (3,3) 但不支配；(2,2,2) 與 (3,1,1,1) 不可比；`kostka_matrix(4)` 下三角、對角線 1；Exercise 2：K_λμ≠0 ⟺ μ⊴λ；→ Schur 多項式對稱、K_λμ 與 μ 的順序無關（第 4 章證）（p.25–26） | ~70s |
| F13 | `sceneF13_column_words.py` / `SceneF13ColumnWords` | 行字（每行由下往上、由左到右）：`column_word(FULTON_INSERT_T)` = 5 4 2 1 6 4 3 2 6 5 2 5 3，插入後回到同一個 T → (10) w_col ≡ w_row；Lemma 1：直線切成 T′、T″，T′ 移到 T″ 的左下（`star(T′,T″)`），從 T′ 正上方的內角由右到左滑回 T（例：切在第 2 行之後）；逐行剝下得 (10)；K′-等價（Lemma 2）一句（p.27–29） | ~55s |
| F14 | `sceneF14_increasing.py` / `SceneF14Increasing` | L(w,k)：`CH3_WORD`，`max_increasing` 找 1、2、3 個不相交弱遞增子序列（6、9、12），上色；長度分配不唯一；w′ = `CH3_WORD2` = w(P(w))，可以一列一列從右邊讀出；Lemma 1：表的字裡的遞增子序列在圖上由左往右、不往下→每行至多一個→L = λ₁+…+λ_k；Lemma 2：基本變換不改變 L（交換兩條子序列的示意）；所以形狀由 w 決定（p.30–33） | ~70s |
| F15 | `sceneF15_uniqueness.py` / `SceneF15Uniqueness` | 唯一性的證明＝演算法 `tableau_from_greene(CH3_WORD)`：由 L(w,k) 得形狀、去掉最右邊的最大字母（`remove_largest`）看少哪一格→那個字母放那格，倒過來一格一格長出 `CH3_TABLEAU`；Lemma 3；→主定理成立，第 1 章三個 Claim 全部證完；Exercise 1–2：嚴格遞減↔行；Erdős–Szekeres：(4,9,2,10,6,1,8,3,7,5) 長度 10>3²，P 形狀 (3,3,3,1)：最長遞增 3、最長嚴格遞減 4（p.33–35） | ~65s |
| F16 | `sceneF16_rs_correspondence.py` / `SceneF16RS` | 記錄表 Q：`rsk_steps(CH4_WORD)` 逐步（P_k 列插入、Q_k 的新格子寫 k；前幾步慢、後面快）；反過來從 Q 最大的數那格反向擠出還原字（`inverse_rsk`，示範 2–3 步後快轉）；Robinson–Schensted：長 r 的字 ↔ (P,Q) 且 Q 標準；排列 ↔ 兩個標準表：S₃ 的 6 個排列 ↔ 6 對，n! = Σ (f^λ)²（n=4：1+9+4+9+1=24）；Exercise 17 一句（p.36–38、52、57） | ~75s |
| F17 | `sceneF17_rsk_arrays.py` / `SceneF17RSKArrays` | 雙列陣列與字典序 (1)(2)；`CH4_ARRAY` 逐步：下列插入 P、上列放進 Q → (`CH4_P`, `CH4_Q`)（Exercise 1）；Q 是表的原因＝Row Bumping Lemma（一句）；R-S-K 定理 (i)–(iii)；矩陣 `CH4_MATRIX`（列和↔Q 的內容、行和↔P 的內容）；對稱定理：陣列上下翻＝轉置 ↔ (Q,P)（Exercise 2）；推論 P(w⁻¹)=Q(w)（S₄ 的一個排列）；對稱矩陣 ↔ P=Q；對合 ↔ 標準表（S₄ 有 10 個對合）（p.38–41） | ~75s |
| F18 | `sceneF18_matrix_ball.py` / `SceneF18MatrixBall` | 矩陣球：`CH4_MATRIX` 放球、依「西北方最大號碼＋1」逐一編號（`ball_numbering`）；P 第一列＝各號碼最左的行 (1,1,1,1,1,2)、Q 第一列＝最上的列 (1,1,1,2,3,3)；導出矩陣：同號球由西南到東北，在每個球右邊、下一個球正下方放新球 → A♭，再編號讀出 (2,2,2)、(2,3,3)；沒有同號球就停 → 與 F17 相同；構造對列與行對稱 → 對稱定理一目了然；Exercise 4（對稱矩陣：trace A + trace A♭ = P 第一列長；trace = 奇數長的行數）小例子；排列矩陣時＝Viennot 影子線（一句）（p.42–47） | ~80s |
| F19 | `sceneF19_rsk_applications.py` / `SceneF19RSKApplications` | Proposition 2：K_λμ 與 μ 的順序無關（兩個字母的情形：λ=(r+s+t, r)，交換 s、t；例 r=2,s=3,t=1）→ Schur 多項式對稱；Cauchy–Littlewood (3)：矩陣 A ↔ (P,Q)，x^P y^Q；小驗算：2×2、總和 3 的矩陣 20 個 = Σ d_λ(2)²（16+4+0）；(4) n!=Σ(f^λ)²、(5) mⁿ=Σ d_λ(m) f^λ（n=3, m=2：8=4·1+2·2+0·1）、(6) Σ f^λ = 對合數（n=4：10）；鉤長公式回顧（M13 做過）：(6,5,5,3) 的 f = 6,651,216；Stanley 鉤–內容公式 d_λ(5)=3,360（格子寫 m+內容、除以鉤長）；Exercise 12 一句（p.50–57） | ~80s |

連續播放：`FultonDemo2` = F09–F19（獨立）。

## 5. 實作規則（同 `fulton_plan.md` 第 4 節，再加幾條）
- ManimGL；繼承 `ChuScene`（`show_header`、`say`、`clear_stage`）；字幕繁體中文、`say` 的數學段以 `$` 開頭；輔助函式寫在模組層級（`play_sequence` 會呼叫）。
- 畫面上的每個數字都由 `tableaux.py` 算出並 assert；版面用 `assert_in_frame`／`assert_apart` 檢查（字幕在底部 y≈−3.45，畫面內容放在 y∈[−3.0, 3.2]）。
- Tex 不放中文；Tex 字串開頭／結尾不要有 `\;`、`\,`；用 t2c 時不要用 `\left(…\right)`。
- **只建立自己的場景檔**；不要改 `utils/` 的共用檔、`main.py`、`render_all.py`（缺工具就在場景檔裡寫模組層級的小函式）。
- 每幕約 250–400 行；字幕每句停留夠讀（約 1.5–3 秒）。
- 自查（在 `C:\mypython\manim\projects\combkit` 執行；各自的資料夾與快取，可以平行）：
  `python tools/render_check.py ../catalan930/codes/scenes/<檔名> <類別> --config ../catalan930/codes/custom_config.yml`，看 `runs/<類別>/sheet.png`，必要時加 `--frames 秒數`。
