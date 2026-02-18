"""
Google Sheet HTML Export → CSV 轉換工具
把 作業管理表TEST/ 下的 HTML exports 轉成 Web_App/ 下的 CSV 檔案

用法: python import_html_to_csv.py
"""
import csv
import html
import re
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent
HTML_DIR = BASE / "作業管理表TEST"
OUT_DIR = BASE / "Web_App"


class GoogleSheetParser(HTMLParser):
    """解析 Google Sheet HTML export 的 table rows"""

    def __init__(self):
        super().__init__()
        self.rows: list[list[str]] = []
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None  # accumulate text parts
        self._in_td = False
        self._in_th = False
        self._skip_row_header = False

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._current_row = []
        elif tag == "td":
            self._in_td = True
            self._current_cell = []
        elif tag == "th":
            self._in_th = True
        elif tag == "br" and self._in_td:
            # <br> inside a cell → newline
            self._current_cell.append("\n")
        elif tag == "span" and self._in_td:
            pass  # just continue accumulating text

    def handle_endtag(self, tag):
        if tag == "tr":
            if self._current_row is not None and len(self._current_row) > 0:
                self.rows.append(self._current_row)
            self._current_row = None
        elif tag == "td":
            if self._current_cell is not None and self._current_row is not None:
                text = "".join(self._current_cell).strip()
                self._current_row.append(text)
            self._in_td = False
            self._current_cell = None
        elif tag == "th":
            self._in_th = False

    def handle_data(self, data):
        if self._in_td and self._current_cell is not None:
            self._current_cell.append(data)

    def handle_entityref(self, name):
        c = html.unescape(f"&{name};")
        if self._in_td and self._current_cell is not None:
            self._current_cell.append(c)

    def handle_charref(self, name):
        c = html.unescape(f"&#{name};")
        if self._in_td and self._current_cell is not None:
            self._current_cell.append(c)


def parse_html(filepath: Path) -> list[list[str]]:
    """讀取 HTML 檔案，回傳 rows (list of list[str])"""
    raw = filepath.read_text(encoding="utf-8")
    parser = GoogleSheetParser()
    parser.feed(raw)
    return parser.rows


def write_csv(filepath: Path, header: list[str], rows: list[list[str]]):
    """寫出 CSV 檔案 (UTF-8 BOM for Excel, CRLF)"""
    with open(filepath, "w", newline="\r\n", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    print(f"  ✅ 寫入 {filepath.name}: {len(rows)} 筆資料")


def import_status():
    """Status.html → status.csv"""
    print("\n📋 Status.html → status.csv")
    rows = parse_html(HTML_DIR / "Status.html")
    if not rows:
        print("  ❌ 沒有資料")
        return

    # 第一行是 header: Status, BgColor, TextColor, [preview col]
    header = ["Status", "BgColor", "TextColor"]
    data_rows = []
    for row in rows[1:]:  # skip header
        if len(row) >= 3 and row[0]:  # 有 Status 名稱才算
            data_rows.append(row[:3])

    write_csv(OUT_DIR / "status.csv", header, data_rows)


def import_project():
    """Project.html → project.csv"""
    print("\n📋 Project.html → project.csv")
    rows = parse_html(HTML_DIR / "Project.html")
    if not rows:
        print("  ❌ 沒有資料")
        return

    # header: project_code, Status, bu → mapped to Code, Status, BU
    header = ["Code", "Status", "BU"]
    data_rows = []
    for row in rows[1:]:  # skip header
        if len(row) >= 3 and row[0]:  # 有 project_code 才算
            data_rows.append(row[:3])

    write_csv(OUT_DIR / "project.csv", header, data_rows)


def import_data():
    """工作管理表.html → data.csv
    
    注意：Google Sheet 可能有篩選，匯出的不一定是全部資料。
    此函數會完整替換 data.csv。
    如果 HTML 只有部分資料（篩選後），會提示使用者。
    """
    print("\n📋 工作管理表.html → data.csv")
    rows = parse_html(HTML_DIR / "工作管理表.html")
    if not rows:
        print("  ❌ 沒有資料")
        return

    # header 在第一行: status, project_code, client, bu, task_name, start_date, due_date, complete_date, remark, [J=countdown]
    # 我們只取前 9 欄
    header = ["status", "project_code", "client", "bu", "task_name",
              "start_date", "due_date", "complete_date", "remark"]
    data_rows = []
    for row in rows[1:]:
        # 確保有足夠欄位，pad to 9
        padded = row[:9] + [""] * max(0, 9 - len(row))
        # 空行跳過 (全部空白)
        if not any(cell.strip() for cell in padded):
            continue
        data_rows.append(padded[:9])

    # 顯示資料量比較
    existing = OUT_DIR / "data.csv"
    if existing.exists():
        with open(existing, "r", encoding="utf-8") as f:
            old_count = sum(1 for _ in f) - 1  # minus header
        print(f"  📊 舊 data.csv: {old_count} 筆, HTML 匯出: {len(data_rows)} 筆")
        if len(data_rows) < old_count * 0.5:
            print(f"  ⚠️  HTML 資料量偏少，可能是篩選後匯出。")
            print(f"      仍然會寫入，請確認是否為完整資料。")

    write_csv(OUT_DIR / "data.csv", header, data_rows)


def main():
    print("=" * 50)
    print("Google Sheet HTML → CSV 轉換工具")
    print("=" * 50)
    print(f"HTML 來源: {HTML_DIR}")
    print(f"CSV 輸出: {OUT_DIR}")

    import_status()
    import_project()
    import_data()

    print("\n" + "=" * 50)
    print("✅ 全部完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
