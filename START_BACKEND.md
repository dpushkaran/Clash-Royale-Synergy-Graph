# 🚀 Quick Start Guide - Backend Server

## To Start the Backend:

1. **Open a new terminal window** (keep it open - don't close it!)

2. **Navigate to the backend directory:**
   ```bash
   cd "/Users/devadarshanpushkaran/Documents/Personal Projects/Clash Royale Synergy Graph/backend"
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Start the server:**
   ```bash
   python3 app.py
   ```

5. **You should see:**
   ```
   Initialized: 120 cards loaded
   * Running on http://127.0.0.1:5001
   * Debug mode: on
   ```

6. **Keep this terminal window open!** The server needs to keep running.

7. **Verify it's working:**
   - Open your browser and go to: `http://localhost:5001/health`
   - You should see: `{"status":"healthy","cards_loaded":120}`

8. **Now refresh your frontend** - the error should be gone!

## Alternative: Use the run script

```bash
cd "/Users/devadarshanpushkaran/Documents/Personal Projects/Clash Royale Synergy Graph/backend"
./run.sh
```

## Troubleshooting

- If you see "Module not found" errors, run: `pip3 install -r requirements.txt`
- If port 5001 is already in use, you may need to kill the process using it first
- Note: Port 5000 is often used by macOS AirPlay Receiver, so we use port 5001
- Make sure you're in the backend directory when running the command

