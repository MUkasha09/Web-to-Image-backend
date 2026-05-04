from flask import Flask, jsonify
import base64
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/scrape")
def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://mepco-it.com.pk/missing_batches_report.asp")
        page.wait_for_load_state('networkidle')

        title = page.title()

        screenshot_path = "screenshot.png"
        page.screenshot(path=screenshot_path, full_page=True)

        browser.close()

    with open(screenshot_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()

    return jsonify({
        "title": title,
        "image": image_base64
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)