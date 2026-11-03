# catalan930：卡塔蘭數與 Chu (1987) 廣義卡塔蘭數 —— 中文講義與 ManimGL 動畫

（本文的相對路徑都以本 repo 的根目錄為基準，開發機上是 `C:\mypython\manim\projects\catalan930`。）

起點是把 Wenchang Chu, *A new combinatorial interpretation for generalized Catalan number*
（Discrete Mathematics 65 (1987) 91–94）做成容易懂的繁體中文講義與 ManimGL 動畫，
之後陸續加上卡塔蘭基礎模組、MIT 18.212 第 1–4 講、Raney (1960) 論文導讀與 Raney 引理、
Fulton《Young Tableaux》各章的演示。

| 位置 | 內容 |
|---|---|
| `codes/` | ManimGL 場景與數學模組；用法見 `codes/README.md`，一鍵輸出全部影片用 `codes/render_all.bat` |
| `notes/` | 講義（`chu1987_導讀`、`raney1960_導讀`、`young_tableaux_導讀`、`ran_note015_改寫` 的 `.tex`／`.pdf`）、各部分的計畫與畫圖程式 |
| `交接說明_HANDOFF.md` | 現況、檔案說明與交接（權威說明） |

- 環境：3Blue1Brown 的 **ManimGL 1.7.2**（3b1b/manim commit fafa083），不是 Manim Community。
- 參考文獻的 PDF 與抄錄（本機的 `ref/`）受著作權保護，**不在這個 repo 裡**，請自行取得原文。
- 影片（`codes/renders/`）不進 git，可用 `codes/render_all.bat` 重新產生。
