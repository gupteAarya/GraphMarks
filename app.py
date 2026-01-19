import asyncio
import threading
import os
from flask import Flask, render_template, request
from telethon import TelegramClient
from dotenv import load_dotenv
import sqlite3
import df_manager
import analysis_manager

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

app = Flask(__name__)
load_dotenv()

#TELEGRAM:
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

loop = asyncio.new_event_loop()

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS marks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    test_type TEXT,
    physics INTEGER,
    chemistry INTEGER,
    maths INTEGER,
    total INTEGER
    )
    """
)
conn.commit()
conn.close()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

# 🔹 Bind client to THAT loop
client = TelegramClient("session", api_id, api_hash, loop=loop)

async def start_client():
    print("Starting Telegram client...")
    await client.start()
    print("Client started!")

asyncio.run_coroutine_threadsafe(start_client(), loop)

async def send_msg(msg):
    print(f"Sending message: {msg}")
    result = await client.send_message("me", msg)
    print("Message sent result:", result)

async def send_graph_to_telegram(path, test_type):
    test_name = {
    "PAT": "📘 Part Test",
    "ADV": "⏱️ 6 Hour Advanced",
    "JEM": "🎯 JEE Main"
    }.get(test_type, "📝 Test")
    await client.send_file("me", path, caption=f"📈 {test_name} Progress")


@app.route("/send", methods=["POST"])
def send():
    date = request.form.get("date")  # YYYY-MM-DD
    pmarks = int(request.form.get("pmarks"))
    cmarks = int(request.form.get("cmarks"))
    mmarks = int(request.form.get("mmarks"))
    test_type = str(request.form.get("test_type"))

    if not all([date, pmarks, cmarks, mmarks]):
        return "Missing form data", 400

    # Insert into database
    df_manager.insert_marks(d=date, p=pmarks, c=cmarks, m=mmarks, test_type=test_type)

    # Generate graph
    path = analysis_manager.generate_line_graph(test_type=test_type)

    # Calculate improvements
    latest, total = analysis_manager.calculate_latest_and_total_improvement(test_type)

    # Build a fancy Telegram message with MarkdownV2
    test_name = {
    "PAT": "📘 Part Test",
    "ADV": "⏱️ 6 Hour Advanced",
    "JEM": "🎯 JEE Main"
    }.get(test_type, "📝 Test")

    improvement_msg = f"{test_name} Entry\n"
    improvement_msg += f"📅 Date: {date}\n\n"
    improvement_msg += f"📊 **Marks Entry**: `{date}`\n\n"
    improvement_msg += f"**Latest Marks:**\n"
    improvement_msg += f"• Physics: {pmarks}\n"
    improvement_msg += f"• Chemistry: {cmarks}\n"
    improvement_msg += f"• Maths: {mmarks}\n"
    improvement_msg += f"• Total: {pmarks + cmarks + mmarks}\n\n"

    improvement_msg += "📈 **Improvements**\n"
    improvement_msg += "**Since Last Entry:**\n"
    for k, v in latest.items():
        improvement_msg += f"• {k.capitalize()}: **{v}%**\n"

    improvement_msg += "\n**Since First Entry:**\n"
    for k, v in total.items():
        improvement_msg += f"• {k.capitalize()}: **{v}%**\n"

    # Send messages to Telegram using MarkdownV2
    asyncio.run_coroutine_threadsafe(
        send_msg(improvement_msg), loop
    )

    # Send graph
    if path:
        asyncio.run_coroutine_threadsafe(
            send_graph_to_telegram(path, test_type), loop
        )

    msg = f"P-{pmarks} C-{cmarks} M-{mmarks}, Date:{date}"
    return render_template("sent.html", msg=msg)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/view", methods=['GET'])
def view():
    # Get months from query string
    months = request.args.get("months", default="1")
    test_type = request.args.get("test_type", default="PAT")

    try:
        months = int(months)
    except ValueError:
        months = 1

    # Get filtered DataFrame for display
    df = df_manager.get_marks_df(test_type)
    print(df.head(5))
    table = df.to_html(index=False)

    # Generate graph and calculate improvement
    path = analysis_manager.generate_line_graph(months=months, test_type=test_type)
    improvements = analysis_manager.calculate_improvement(months=months, test_type=test_type)
    print("Improvements:", improvements)  # debug

    if path is None:
        return "No data yet"

    return render_template(
    "view.html",
    table=table,
    image=f"marks_{test_type}.png",
    improvements=improvements,
    selected_months=months,
    selected_test=test_type
)   



if __name__ == "__main__":
    # ❗ disable reloader
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 4000)))
