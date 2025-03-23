#!/usr/bin/env python3
# written by claude 3.7 sonnet, code was not reviewed or verified by me :3 (i didnt feel like it)

import datetime as dt
import json
import sys

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np


def process_name(name, user_id):
    """Apply name normalization rules."""
    # Name exceptions for consistent tracking
    name_mapping = {
        "iloveyanna": "17xr",
        "agaa13": "17xr",
        "celestialexe_": "celestialexe",
    }

    id_mapping = {"456226577798135808": "undrscre"}

    if name in name_mapping:
        return name_mapping[name]
    if user_id in id_mapping:
        return id_mapping[user_id]
    return name


def load_discord_data(filepath):
    """Load and parse Discord JSON data."""
    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

        # Extract relevant information from each message
        messages = []
        for msg in data.get("messages", []):
            if isinstance(msg, dict) and "author" in msg and "timestamp" in msg:
                # Handle different message structures
                if isinstance(msg.get("content"), dict):
                    name = msg.get("content", {}).get("name", "")
                else:
                    name = msg.get("author", {}).get("name", "")
                user_id = msg.get("author", {}).get("id", "")
                timestamp = msg.get("timestamp")

                if name and timestamp:
                    name = process_name(name, user_id)
                    messages.append((name, user_id, timestamp))

        return messages
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading Discord data: {e}")
        return []


def plot_messages(messages):
    """Plot messages over time for each user."""
    # Group messages by user
    user_messages = {}
    for name, _, timestamp in messages:
        if name not in user_messages:
            user_messages[name] = []
        try:
            # Parse timestamp to datetime
            msg_time = dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            user_messages[name].append(msg_time)
        except (ValueError, AttributeError):
            continue

    # Sort timestamps for each user
    for user in user_messages:
        user_messages[user].sort()

    # Configure plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.xaxis.set_major_formatter(md.DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate()

    # User color mapping
    colors = {
        "celestialexe": "plum",
        "pdbaroni": "royalblue",
        "normalcat_": "red",
        "undrscre": "darkorange",
        "17xr": "limegreen",
        "itscattybro": "darkviolet",
        "morilis": "sienna",
        "mcsaucynuggets": "darkviolet",
        "frozenremnant": "lightcoral",
        "baccon.": "navy",
        "clyde": "crimson",
        "brixk": "yellowgreen",
    }

    # Plot messages for each user
    for user, timestamps in user_messages.items():
        if not timestamps:
            continue

        # Create cumulative message count
        counts = np.arange(1, len(timestamps) + 1)

        # Plot the data
        color = colors.get(user, "black")
        plt.plot(timestamps, counts, color=color, label=user)

        # Add user label at the end of each line
        if timestamps and counts.size > 0:
            plt.text(timestamps[-1], counts[-1], user)

    plt.title("Discord Messages Over Time")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Messages")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    return plt


def main():
    if len(sys.argv) < 2:
        print("Usage: python discord_plot.py path/to/discord_export.json")
        return

    filepath = sys.argv[1]
    messages = load_discord_data(filepath)

    if not messages:
        print("No valid messages found in the data")
        return

    print(f"Processing {len(messages)} messages...")
    plot = plot_messages(messages)

    print("Plot ready! Showing visualization...")
    plot.show()


if __name__ == "__main__":
    main()
