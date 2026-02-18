# 專案計畫書: 工作管理表 Web App v2.2

## 1. 專案概述
將 Google Sheets 的「作業管理表」轉換為互動式 Web App，支援即時 CRUD、進階篩選、BU 分組顯示、設定管理，並透過 GAS 或本地 Python Server 進行資料同步。

## 2. 技術架構

| 層級 | 技術 | 說明 |
|:---|:---|:---|
| Frontend | Vue 3 (CDN) + TailwindCSS + RemixIcon | 單檔 SPA (`index.html`) |
| Backend (GAS) | Google Apps Script | `doGet`/`doPost` JSON API |
| Backend (Local) | Python `http.server` (server.py) | 開發用本地伺服器，Port 8998 |
| Database | Google Sheets / CSV files | 4 sheets: data, bu, project, status |

## 3. 資料來源 (CSV Sheets)

| 檔案 | 說明 | 欄位 |
|:---|:---|:---|
| `data.csv` | 工作項目主表 | uuid, status, project_code, bu, task_name, start_date, due_date, complete_date, remark, re |
| `bu.csv` | 事業部設定 | BU, Order |
| `project.csv` | 專案設定 | Code, Status(W/O/X), BU |
| `status.csv` | 狀態顏色設定 | Status, BgColor, TextColor, Order |

## 4. 已完成功能

### Phase 1: 基礎 CRUD ✅
- [x] 讀取/新增/編輯/刪除工作項目
- [x] GAS 與 Local Server 雙模式支援
- [x] 自動偵測環境 (GAS vs Local)

### Phase 2: 進階顯示 ✅
- [x] BU 分組顯示 (可摺疊)
- [x] 狀態顏色 Badge (BgColor/TextColor)
- [x] 倒數天數自動計算 (含逾期警示)
- [x] 預定完成日期版本歷史追蹤
- [x] Sticky 狀態欄位

### Phase 3: 設定管理 ✅
- [x] Settings Modal (Status/Project/BU 三頁簽)
- [x] BU 拖拉排序
- [x] Project 拖拉排序 (群組內)
- [x] Project Status 自動 Order (O=98, X=99)
- [x] Save Config 存回 Google Sheets

### Phase 4: 進階篩選 ✅
- [x] 多欄位多選篩選器 (Filter Bar)
- [x] 群組內篩選聯動
- [x] 清除全部/單一篩選
- [x] 排除篩選功能

### Phase 5: 資料修復 ✅
- [x] CSV header casing 標準化 (BU/Bu/bu)
- [x] Project BU 反查修復 (repair_data.py)
- [x] Template 嵌套結構修復

### Phase 6: Commercial UI/UX Upgrade (In Progress) 🔄
> Goal: Apply `UI_Design.md` to achieve a professional, commercial-grade look and feel.
- [ ] **Global Theme**: Implement Indigo/Slate palette & Inter font.
- [ ] **Layout Polish**: Increase whitespace, rounded corners, drop shadows.
- [ ] **Component Upgrade**:
    - [ ] **Table**: Sticky header, hover rows, clean borders.
    - [ ] **Badges**: Pill shape with defined semantic colors.
    - [ ] **Modals**: Backdrop blur, clean transitions, centered layout.
    - [ ] **Buttons**: Primary/Secondary styles with focus rings.
- [ ] **Micro-interactions**: Hover effects, smooth transitions.

## 5. 檔案結構
```
Web_App/
├── index.html          # 主應用程式 (Vue 3 SPA)
├── server.py           # 本地開發伺服器
├── start.bat           # 啟動腳本
├── kill_server.bat     # 關閉伺服器
├── GAS_Backend.gs      # Google Apps Script 後端
├── data.csv            # 工作資料
├── bu.csv              # BU 設定
├── project.csv         # 專案設定
├── status.csv          # 狀態顏色設定
├── Project_Plan.md     # 本文件
├── Engineering_Spec.md # 工程規格書
└── UI_Design.md        # UI 設計規範
```

## 6. 部署方式
1. **本地開發**: `start.bat` → Python Server (port 8998)
2. **正式環境**: GAS Web App 部署 → 設定 `GAS_URL` 常數
