#!/usr/bin/env python3
# written by claude 3.7 sonnet, code was not reviewed or verified by me :3 (i didnt feel like it)

import sys
import os
import json
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pykakasi
from collections import defaultdict

def load_spotify_data(data_dir):
    """Load and parse Spotify streaming history JSON files."""
    streaming_data = []
    
    # Initialize kakasi for Japanese to romaji conversion
    kks = pykakasi.kakasi()
    
    # Find all Streaming_History_Audio files
    try:
        files = [f for f in os.listdir(data_dir) 
                if f.startswith("Streaming_History_Audio_") and f.endswith(".json")]
    except FileNotFoundError:
        print(f"Directory not found: {data_dir}")
        return []
    
    if not files:
        print(f"No Spotify streaming history files found in {data_dir}")
        return []
    
    # Load and combine all files
    for filename in files:
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                streaming_data.extend(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading {filename}: {e}")
    
    # Process the streaming data
    processed_data = []
    for item in streaming_data:
        artist = item.get("master_metadata_album_artist_name")
        ms_played = item.get("ms_played")
        timestamp = item.get("ts")
        
        if artist and ms_played and timestamp:
            # Convert Japanese characters to romaji
            if artist and any(ord(c) > 127 for c in artist):
                result = kks.convert(artist)
                romaji_parts = [item['hepburn'] for item in result]
                artist = ''.join(romaji_parts)
            
            # Convert timestamp to Unix timestamp
            try:
                ts_unix = int(dt.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").timestamp())
                processed_data.append((artist, ms_played, ts_unix))
            except ValueError:
                continue
    
    return processed_data

def plot_listening_history(listening_data):
    """Plot cumulative listening time for artists over time."""
    # Group data by artist
    artist_data = defaultdict(list)
    for artist, ms_played, timestamp in listening_data:
        artist_data[artist].append((int(timestamp), int(ms_played)))
    
    # Sort by timestamp for each artist
    for artist in artist_data:
        artist_data[artist].sort(key=lambda x: x[0])
    
    # Configure the plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.xaxis.set_major_formatter(md.DateFormatter("%Y-%m-%d"))
    plt.gcf().autofmt_xdate()
    
    # Color mapping for specific artists
    colors = {
        'NIKI': 'plum',
        'keshi': 'darkviolet',
        'beabadoobee': 'deepskyblue',
        'yorushika': 'crimson',
    }
    
    # Plot data for each artist
    for artist, data_points in artist_data.items():
        if not data_points:
            continue
        
        # Calculate cumulative listening time
        timestamps = [dt.datetime.fromtimestamp(ts) for ts, _ in data_points]
        ms_played = [ms for _, ms in data_points]
        
        # Calculate cumulative hours
        cumulative_hours = []
        total_ms = 0
        for ms in ms_played:
            total_ms += ms
            cumulative_hours.append(total_ms / (1000 * 60 * 60))  # Convert to hours
        
        # Skip artists with very little listening time
        if cumulative_hours[-1] < 0.5:  # Less than 30 minutes total
            continue
        
        # Plot the data
        color = colors.get(artist, 'black')
        plt.plot(timestamps, cumulative_hours, color=color, label=artist)
        
        # Add artist label at the end of each line
        if timestamps and cumulative_hours:
            hours = int(cumulative_hours[-1])
            minutes = int((cumulative_hours[-1] - hours) * 60)
            time_str = f"{hours}h {minutes}m"
            plt.text(timestamps[-1], cumulative_hours[-1], f"{artist}\n{time_str}")
    
    plt.title('Spotify Listening History Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Listening Time (hours)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return plt

def main():
    if len(sys.argv) < 2:
        print("Usage: python spotify_plot.py path/to/spotify_data_directory/")
        return
    
    data_dir = sys.argv[1]
    listening_data = load_spotify_data(data_dir)
    
    if not listening_data:
        print("No valid listening data found")
        return
    
    print(f"Processing {len(listening_data)} listening entries...")
    plot = plot_listening_history(listening_data)
    
    print("Plot ready! Showing visualization...")
    plot.show()

if __name__ == "__main__":
    main()
