import os
import json
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://impds.nic.in/sale/"

# District mappings for Goa
DISTRICT_MAP = {
    "585": "north_goa",
    "586": "south_goa"
}

MONTHS = [
    {"code": "Mar", "year": "2026", "folder": "2026-03"},
    {"code": "Apr", "year": "2026", "folder": "2026-04"}
]

def get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": BASE_URL
    })
    return session

def parse_html_tables(html_str, meta):
    soup = BeautifulSoup(html_str, "html.parser")

    # 1. Summary Cards Extraction
    summary_cards = {
        "total_etransaction": 0,
        "aadhaar_authenticated": 0,
        "other_mode_authenticated": 0,
        "non_authenticated": 0
    }

    cards = soup.find_all("div", class_=["card", "box", "small-box"])
    for card in cards:
        text = card.get_text(separator=" ", strip=True).lower()
        digits = "".join([c for c in text if c.isdigit()])
        val = int(digits) if digits else 0

        if "total e-transaction" in text or "total transaction" in text:
            summary_cards["total_etransaction"] = val
        elif "aadhaar authenticated" in text:
            summary_cards["aadhaar_authenticated"] = val
        elif "other mode" in text:
            summary_cards["other_mode_authenticated"] = val
        elif "non-authenticated" in text or "non authenticated" in text:
            summary_cards["non_authenticated"] = val

    # 2. Extract All Tables
    tables = soup.find_all("table")

    def parse_single_table(table_elem):
        if not table_elem:
            return {"headers": [], "rows": []}

        headers = [th.text.strip() for th in table_elem.find_all("th")]
        rows = []
        for tr in table_elem.find_all("tr"):
            tds = tr.find_all("td")
            if tds:
                # Retain all commodity rows (including expanded Coarse Grains sub-commodities)
                row_data = [td.text.strip() for td in tds]
                rows.append(row_data)
        return {"headers": headers, "rows": rows}

    num_tx = parse_single_table(tables[0]) if len(tables) > 0 else {}
    ration_cards = parse_single_table(tables[1]) if len(tables) > 1 else {}
    dist_qty = parse_single_table(tables[2]) if len(tables) > 2 else {}

    return {
        "metadata": meta,
        "summary_cards": summary_cards,
        "tables": {
            "number_of_transactions": num_tx,
            "number_of_transacted_ration_cards": ration_cards,
            "distributed_quantity_kg": dist_qty
        }
    }

def run_scraper():
    session = get_session()

    # Initial handshake
    try:
        session.get(BASE_URL, timeout=15)
    except Exception as e:
        print(f"❌ Portal connect error: {e}")
        return

    for m in MONTHS:
        print(f"\n==========================================")
        print(f"🚀 SCRAPING MONTH: {m['code']} {m['year']}")
        print(f"==========================================")

        # Set Month State in Session
        try:
            session.post(f"{BASE_URL}stateUnautmated", data={"month": m['code'], "year": m['year']}, timeout=15)
        except Exception as e:
            print(f"Warning setting month: {e}")

        for dist_code, dist_name in DISTRICT_MAP.items():
            out_dir = os.path.join("data", "raw", m['folder'], dist_name)
            os.makedirs(out_dir, exist_ok=True)

            print(f"\n📍 Fetching FPS list for District: {dist_name.upper()}...")

            # Maintain portal state chain
            session.get(f"{BASE_URL}stateByCountryAjax?stateCode=30", timeout=15)
            session.get(f"{BASE_URL}districtByCountryAjax?stateCode={dist_code}", timeout=15)

            # Retrieve FPS List
            fps_url = f"{BASE_URL}fpsByCountryAjax2?stateCode=30&districtCode={dist_code}"
            res = session.get(fps_url, timeout=15)

            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.find_all("a") or soup.find_all("li")

            fps_list = []
            for it in items:
                txt = it.text.strip()
                f_id = it.get("data-id") or it.get("id") or (txt.split(":")[0].strip() if ":" in txt else None)
                f_name = txt.split(":")[1].strip() if ":" in txt else txt
                if f_id and f_id.isdigit():
                    fps_list.append({"fps_id": f_id, "fps_name": f_name, "raw_label": txt})

            print(f"Found {len(fps_list)} FPS entries for {dist_name}.")

            for idx, fps in enumerate(fps_list, 1):
                f_id = fps["fps_id"]
                f_name = fps["fps_name"]
                safe_name = "".join([c if c.isalnum() else "_" for c in f_name]).lower()
                filepath = os.path.join(out_dir, f"{f_id}_{safe_name}.json")

                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    print(f"[{idx}/{len(fps_list)}] Skipping existing: {f_id}")
                    continue

                # Detail AJAX Endpoint
                detail_url = f"{BASE_URL}fpsByCountryAjax?stateCode={f_id}"
                try:
                    r = session.get(detail_url, timeout=15)

                    meta = {
                        "year": m['year'],
                        "month": m['code'],
                        "state": "GOA",
                        "district": dist_name,
                        "fps_id": f_id,
                        "fps_name": f_name
                    }

                    parsed_record = parse_html_tables(r.text, meta)

                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(parsed_record, f, indent=2, ensure_ascii=False)

                    print(f"[{idx}/{len(fps_list)}] Saved: {f_id} - {f_name}")
                except Exception as e:
                    print(f"[{idx}/{len(fps_list)}] Error fetching {f_id}: {e}")

                time.sleep(0.1)

if __name__ == "__main__":
    run_scraper()