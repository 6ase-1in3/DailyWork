import os
import json
from bs4 import BeautifulSoup
import re

def parse_html_to_json(html_path, output_path):
    if not os.path.exists(html_path):
        print(f"Error: File not found at {html_path}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    if not table:
        print("Error: No table found in HTML")
        return

    rows = table.find_all('tr')
    data = []
    
    # Iterate through rows, skipping header/metadata rows as needed
    # Based on the HTML view:
    # Row 1 (index 0): Header "工作項目", "2026-02-12 更新"...
    # Row 2 (index 1): Headers "狀態", "專案代號", "事項"...
    # Row 3 (index 2): Filter row / Data starts
    
    headers = []
    
    # Let's find the header row explicitly. It looks like Row 2 (index 1 based on previous view)
    # The view_file output showed: <tr style="height: 20px"><th id="72545322R2"...><td...>狀態</td>...
    
    header_row_index = -1
    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        text_content = [c.get_text(strip=True) for c in cells]
        if "專案代號" in text_content and "事項" in text_content:
            header_row_index = i
            # Create a map of column index to key name
            # We want to map these Chinese headers to our English keys from spec
            # Expected headers: 狀態, 專案代號, 事項, 開始時間, 預定完成, 完成時間, 倒數, 備註
            headers = text_content
            print(f"Found header row at index {i}: {headers}")
            break
            
    if header_row_index == -1:
        print("Error: Could not find header row")
        return

    # Define column mapping based on the headers found
    # We need to robustly map indices
    col_map = {}
    
    # We need to check the exact cell indices because there might be a row header (th) at the start
    header_cells = rows[header_row_index].find_all(['td', 'th'])
    
    for idx, cell in enumerate(header_cells):
        text = cell.get_text(strip=True)
        if "狀態" in text: col_map['status'] = idx
        elif "專案代號" in text: col_map['project_code'] = idx
        elif "事項" in text: col_map['task_name'] = idx
        elif "開始時間" in text: col_map['start_date'] = idx
        elif "預定完成" in text: col_map['due_date'] = idx
        elif "完成時間" in text: col_map['complete_date'] = idx
        elif "備註" in text: col_map['remark'] = idx

    print(f"Column mapping: {col_map}")

    # Process data rows
    for i in range(header_row_index + 1, len(rows)):
        row = rows[i]
        cells = row.find_all(['td', 'th'])
        
        # Skip rows that act as separators or empty rows
        # Check if project code or task name exists
        if len(cells) <= max(col_map.values(), default=0):
            continue
            
        # Helper to safely get cell content
        def get_cell_content(idx, is_date=False):
            if idx >= len(cells): return ""
            cell = cells[idx]
            
            if is_date:
                # Special handling for dates with <br> and strikethrough
                # We need to process the inner HTML logic
                # Find all text nodes separated by <br>
                # Using separator for get_text might be enough if we just want the last line
                text = cell.get_text(separator='|', strip=True) # Use pipe as temp separator
                if not text: return ""
                
                parts = text.split('|')
                # The user says "the bottom one is the final date"
                # So we take the last part
                final_date = parts[-1].strip()
                return final_date
            else:
                return cell.get_text(strip=True)

        item = {
            "id": i, # Simple ID for now
            "status": get_cell_content(col_map.get('status')),
            "project_code": get_cell_content(col_map.get('project_code')),
            "task_name": get_cell_content(col_map.get('task_name')),
            "start_date": get_cell_content(col_map.get('start_date'), is_date=True),
            "due_date": get_cell_content(col_map.get('due_date'), is_date=True),
            "complete_date": get_cell_content(col_map.get('complete_date'), is_date=True),
            "remark": get_cell_content(col_map.get('remark'))
        }
        
        # Filter out rows that are purely categorical/separators if they don't have task names or look like tasks
        # The HTML has "類別：" rows which act as section headers.
        # If "事項" (task_name) matches "2025年度" or is empty, it might be a header or separator.
        if not item['task_name'] and not item['project_code']:
            continue
            
        # Clean up statuses (remove emoji or unicode chars if needed, but keeping for now is fine)
        # The user's example showed "✖︎ 完成", "Done", "台北展" (as project code maybe?)
        
        data.append(item)

    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully extracted {len(data)} items to {output_path}")

if __name__ == "__main__":
    html_file = r"d:\OneDrive\Python_File\網頁_作業管理表\工作管理表.html"
    json_file = r"d:\OneDrive\Python_File\網頁_作業管理表\Web_App\data.json"
    parse_html_to_json(html_file, json_file)
