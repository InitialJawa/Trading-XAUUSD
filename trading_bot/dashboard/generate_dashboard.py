import json
import os

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data"
)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def generate():
    composite = load_json(os.path.join(DATA_DIR, "signals", "latest_composite.json"))
    price = load_json(os.path.join(DATA_DIR, "current", "latest_price.json"))
    indicators = load_json(os.path.join(DATA_DIR, "current", "latest_indicators.json"))

    decision = composite.get("decision", "N/A") if composite else "N/A"
    final_score = composite.get("final_score", "N/A") if composite else "N/A"
    close_price = price.get("close", "N/A") if price else "N/A"
    rsi = indicators.get("rsi", "N/A") if indicators else "N/A"
    atr = indicators.get("atr", "N/A") if indicators else "N/A"

    decision_color = {
        "strong_buy": "#00ff00",
        "buy": "#88ff88",
        "hold": "#ffff88",
        "sell": "#ff8888",
        "strong_sell": "#ff0000",
    }.get(decision, "#ffffff")

    signals_rows = ""
    if composite and "signals" in composite:
        for name, sig in composite["signals"].items():
            val = sig.get("signal", "N/A")
            stype = sig.get("type", "")
            signals_rows += f"""
            <tr>
                <td>{name}</td>
                <td>{val}</td>
                <td>{stype}</td>
            </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="60">
<title>XAUUSD Trading Bot</title>
<style>
    body {{ font-family: 'Courier New', monospace; margin: 20px; background: #1a1a2e; color: #e0e0e0; }}
    h1 {{ color: #f0c040; border-bottom: 2px solid #f0c040; padding-bottom: 10px; }}
    .decision {{ font-size: 48px; font-weight: bold; text-align: center; padding: 20px; border-radius: 10px; margin: 20px 0; }}
    .score {{ font-size: 72px; text-align: center; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
    th, td {{ border: 1px solid #444; padding: 10px; text-align: left; }}
    th {{ background: #16213e; color: #f0c040; }}
    td {{ background: #0f3460; }}
    .container {{ display: flex; gap: 20px; flex-wrap: wrap; }}
    .panel {{ flex: 1; min-width: 300px; }}
    .label {{ color: #888; }}
    .value {{ color: #fff; font-weight: bold; }}
    .green {{ color: #00ff00; }}
    .red {{ color: #ff4444; }}
    .yellow {{ color: #ffff00; }}
</style>
</head>
<body>
<h1>XAUUSD Trading Bot</h1>

<div class="decision" style="background: {decision_color}22; border: 2px solid {decision_color};">
    <div class="score">{final_score}</div>
    <div>{decision.upper()}</div>
</div>

<div class="container">
    <div class="panel">
        <h2>Market Data</h2>
        <table>
            <tr><th>Field</th><th>Value</th></tr>
            <tr><td>Price</td><td class="value">{close_price}</td></tr>
            <tr><td>RSI (14)</td><td class="value">{rsi}</td></tr>
            <tr><td>ATR (14)</td><td class="value">{atr}</td></tr>
        </table>
    </div>

    <div class="panel">
        <h2>Signal Breakdown</h2>
        <table>
            <tr><th>Signal</th><th>Score</th><th>Type</th></tr>
            {signals_rows}
        </table>
    </div>
</div>

<p style="color: #666; margin-top: 40px;">
    Auto-refresh every 60s | Last generated: <span id="timestamp"></span>
</p>

<script>
    document.getElementById('timestamp').textContent = new Date().toLocaleString();
</script>
</body>
</html>"""

    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard generated -> {output_path}")


if __name__ == "__main__":
    generate()
