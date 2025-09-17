#!/usr/bin/env python3
"""
Digital Diary Web Application
A simple, elegant digital diary with auto-save functionality.
"""

from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import json

app = Flask(__name__)

# Create directories for storing diary entries
DIARY_DIR = "diary_entries"
if not os.path.exists(DIARY_DIR):
    os.makedirs(DIARY_DIR)

def get_today_date():
    """Get today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

def get_entry_filename(date_str):
    """Get the filename for a diary entry."""
    return os.path.join(DIARY_DIR, f"{date_str}.txt")

def get_all_entries():
    """Get all diary entry dates."""
    entries = []
    if os.path.exists(DIARY_DIR):
        for filename in os.listdir(DIARY_DIR):
            if filename.endswith('.txt'):
                date_str = filename[:-4]  # Remove .txt extension
                entries.append(date_str)
    return sorted(entries, reverse=True)

@app.route('/')
def index():
    """Main page - today's diary entry."""
    return render_template('index.html')

@app.route('/api/today')
def get_today():
    """Get today's date and entry content."""
    today = get_today_date()
    filename = get_entry_filename(today)
    
    content = ""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    
    return jsonify({
        'date': today,
        'content': content
    })

@app.route('/api/save', methods=['POST'])
def save_entry():
    """Save diary entry content."""
    data = request.get_json()
    date_str = data.get('date')
    content = data.get('content', '')
    
    if not date_str:
        return jsonify({'error': 'Date is required'}), 400
    
    filename = get_entry_filename(date_str)
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True, 'message': 'Entry saved successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/entries')
def list_entries():
    """Get list of all diary entries."""
    entries = get_all_entries()
    return jsonify({'entries': entries})

@app.route('/api/entry/<date>')
def get_entry(date):
    """Get a specific diary entry by date."""
    filename = get_entry_filename(date)
    
    if not os.path.exists(filename):
        return jsonify({'error': 'Entry not found'}), 404
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({
            'date': date,
            'content': content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)