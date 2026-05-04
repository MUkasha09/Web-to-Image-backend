from flask import Flask, jsonify
import base64
!playwright install
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://mepco-it.com.pk/missing_batches_report.asp")
        page.wait_for_load_state("networkidle")

        title = page.title()

        path = "/tmp/screenshot.png"
        page.screenshot(path=path, full_page=True)

        browser.close()

    with open(path, "rb") as f:
        image = base64.b64encode(f.read()).decode()

    return {
        "status": "success",
        "title": title,
        "image": image
    }

@app.route("/run", methods=["GET"])
def run():
    try:
        return jsonify(run_scraper())
    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500


@app.route("/")
def health():
    return {"status": "live"}