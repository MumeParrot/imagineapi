#!/usr/bin/env python3
"""
ImagineAPI Client Script
Sends image generation requests to http://localhost:8055 and downloads results.
"""

import os
import time
import random
import requests
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8055"
AUTH_TOKEN = os.environ.get("IMAGINE_API_TOKEN", "your-token-here")
PARROT_DIR = os.environ.get("PARROT_DIR", "parrots")

BACKUP_THRESHOLD = int(os.environ.get("BACKUP_THRESHOLD", 32))
BACKUP_AMOUNT = int(os.environ.get("BACKUP_AMOUNT", 32))

PIGEON_PROB = float(os.environ.get("PIGEON_PROB", 0.01))
CHICKEN_PROB = float(os.environ.get("CHICKEN_PROB", 0.03))
EAGLE_PROB = float(os.environ.get("EAGLE_PROB", 0.03))

# Prompt pool
PROMPTS = [
    "adorable silly parrot character, roughly drawn with happy face, cheering at stock investing graphs, simple background, circular png",
    "illy cheerful parrot character, roughly drawn, surrounded by stock papers and charts, simple background, circular png",
    "cute silly parrot character with big smile, roughly drawn, looking at a laptop showing stock investing graphs, simple background, circular png",
    "funny parrot character, roughly drawn in green, smiling while holding a bag of money and stock chart, simple background, circular png",
    "silly happy parrot character, roughly drawn, wearing tiny glasses and holding a stock chart, simple background, circular png",
    "goofy parrot character, roughly drawn, sitting at a desk with coffee cup and stock investing papers, simple background, circular png",
    "cuty goofy happy and loudly squaking parrot character, roughly drawn, sitting at a desk with coffee cup and stock investing papers, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, wearing a funny hat while looking at stock trading charts, simple background, circular png"
    "cute, loudly squaking silly parrot character, roughly drawn, sitting on a pile of money while cheering at a stock graph, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, juggling money and stock charts, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, looking at a laptop showing stock investing graphs, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn in bright colors, surrounded by stock papers and charts, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn with happy face, cheering at stock investing graphs, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, wearing a funny hat while looking at stock trading charts, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, sitting on a pile of money while cheering at a stock graph, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, juggling money and stock charts, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, sitting at a desk with laptop, coffee cup, and stock papers, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, sitting on a pile of money with stock charts around, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, juggling coins and stock papers, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn in rainbow colors, cheering at floating stock arrows and money bills, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, carrying a briefcase full of money and stock papers, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, surrounded by coins, charts, and a coffee cup, simple background, circular png",
    "cute, loudly squaking goofy parrot character, roughly drawn, juggling a pencil, calculator, and stock charts, simple background, circular png",
    "cute, loudly squawking adorable parrot character, roughly drawn in yellow, waving stock papers and coins, simple background, circular png",
    "cute, loudly squawking silly parrot character, roughly drawn, sitting at a small desk with laptop and stock graphs, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, sitting in a mini office chair with laptop and coffee, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, balancing a pile of coins and stock charts on its wings, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn, wearing a tiny crown while checking stock graphs, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, floating with balloons labeled with stock tickers, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, standing on a globe with stock arrows around, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn, sitting inside a paper airplane with stock charts attached, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, balancing a pile of coins with a stock chart in its claws, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, standing on a pile of colorful papers with stock graphs and arrows, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, perched on a pile of coins with stock charts around, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, sitting next to a laptop showing stock investing graphs, simple background, circular png",
    "cute, loudly squaking goofy parrot character, roughly drawn, surrounded by floating stock arrows and money bills, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, flying over stock charts with green arrows, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn, standing on a stack of gold bars with stock graphs floating nearby, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, perched on a treasure chest with stock papers around, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, sitting on a desk with coins and stock charts floating above, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, flying with balloons labeled with stock tickers, simple background, circular png",
    "cute, loudly squaking goofy parrot character, roughly drawn, standing on a globe with stock arrows circling, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, surrounded by colorful papers with stock charts, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, perched on a rocket with stock graphs floating around, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, next to piles of coins and upward stock arrows, simple background, circular png",
    "cute, loudly squaking goofy parrot character, roughly drawn, sitting beside floating stock graphs and colorful bills, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn, standing on a pile of papers with stock charts floating above, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, flying over floating gold coins and stock arrows, simple background, circular png",
    "cute, loudly squaking happy parrot character, roughly drawn, perched near a small treasure chest with stock graphs around, simple background, circular png",
    "cute, loudly squaking playful parrot character, roughly drawn, sitting on a stack of coins with stock charts floating, simple background, circular png",
    "cute, loudly squaking goofy parrot character, roughly drawn, flying among floating stock arrows and bills, simple background, circular png",
    "cute, loudly squaking adorable parrot character, roughly drawn, standing near a tiny laptop showing rising stocks, simple background, circular png",
    "cute, loudly squaking silly parrot character, roughly drawn, perched on colorful charts with coins and arrows floating, simple background, circular png",
]

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SMTP_USER", "mumeparrot@gmail.com")
SENDER_PASSWORD = os.environ.get("SMTP_PASS", "")
RECIPIENT_EMAIL = os.environ.get("ERROR_REPORT_EMAIL", "mumeparrot@gmail.com")

# Headers
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
}


def create_image_request(prompt: str) -> str:
    """Send POST request to create image generation task."""
    url = f"{BASE_URL}/items/images"
    payload = {"prompt": prompt}

    response = requests.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    image_id = data["data"]["id"]
    print(f"✓ Image generation requested (ID: {image_id})")
    print(f"  Prompt: {prompt}")
    return image_id


def check_image_status(image_id: str) -> dict:
    """Send GET request to check image generation status."""
    url = f"{BASE_URL}/items/images/{image_id}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]


def download_image(url: str, parrot_id: int) -> None:
    """Download image from URL to the parrots directory."""
    os.makedirs(PARROT_DIR, exist_ok=True)

    # Extract file extension from URL or default to .png
    ext = url.split(".")[-1] if "." in url.split("/")[-1] else "png"
    filename = f"parrot-{parrot_id:06d}.{ext}"
    filepath = os.path.join(PARROT_DIR, filename)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  ✓ Downloaded: {filepath}")


def poll_until_complete(
    image_id: str,
    parrot_id_base: int,
    poll_interval: int = 5,
    max_wait: int = 300,
) -> None:
    """Poll the API until image generation is complete or timeout."""
    elapsed = 0

    while elapsed < max_wait:
        data = check_image_status(image_id)

        if not data:
            raise Exception("None received from check_image_status")

        status = data.get("status")
        progress = data.get("progress")

        print(f"  Status: {status}", end="")
        if progress is not None:
            print(f" ({progress}%)", end="")
        print()

        if status == "completed":
            upscaled_urls = data.get("upscaled_urls")
            if upscaled_urls:
                print(
                    f"✓ Generation complete! Downloading {len(upscaled_urls)} image(s)..."
                )
                for idx, url in enumerate(upscaled_urls):
                    download_image(url, parrot_id_base + idx)
            else:
                raise Exception(
                    "✗ No upscaled URLs found in completed response"
                )
            break
        elif status == "failed":
            error = data.get("error", "Unknown error")
            raise Exception(f"✗ Generation failed: {error}")

        time.sleep(poll_interval)
        elapsed += poll_interval

    if elapsed >= max_wait:
        raise Exception(
            f"✗ Timeout: Image generation took longer than {max_wait} seconds"
        )


def send_error_email(error_message: str) -> None:
    """Send error notification email via Gmail SMTP."""
    if not SENDER_PASSWORD:
        print("✗ SMTP_SENDER_PASSWORD not set, skipping email notification")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = (
            f"Parrot Backup Error - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        body = f"""Parrot backup script encountered an error:

{error_message}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✓ Error notification email sent to {RECIPIENT_EMAIL}")
    except Exception as e:
        print(f"✗ Failed to send error email: {e}")


def main():
    print(
        f"=== {datetime.now().strftime('%Y-%m-%d')}: Backing Parrot Images... ===\n"
    )

    try:
        with open(f"{PARROT_DIR}/counter", "r") as fd:
            counter = int(fd.read())
    except FileNotFoundError:
        counter = 0

    n_parrots = len(
        [f for f in os.listdir(PARROT_DIR) if f.startswith("parrot")]
    )

    if counter + BACKUP_THRESHOLD < n_parrots:
        print(f"[*] Enough parrots left ({counter} vs. {n_parrots}) ")
        return

    for i in range(BACKUP_AMOUNT // 4):
        # Select random prompt from pool
        prompt = random.choice(PROMPTS)

        prob = random.random()
        if prob < PIGEON_PROB:
            prompt = prompt.replace("parrot", "pigeon")
        elif prob < PIGEON_PROB + CHICKEN_PROB:
            prompt = prompt.replace("parrot", "chicken")
        elif prob < PIGEON_PROB + CHICKEN_PROB + EAGLE_PROB:
            prompt = prompt.replace("parrot", "eagle")

        # Step 1: Create image generation request
        image_id = create_image_request(prompt)

        # Step 2: Poll until complete and download
        print(f"\n[{i}] Polling for completion...")
        poll_until_complete(image_id, n_parrots + 1 + i * 4)

    print("\n=== Done ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_message = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"\n✗ Error occurred:\n{error_message}")
        send_error_email(error_message)
        raise
