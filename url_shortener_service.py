import http.server
import socketserver
import sqlite3
import urllib.parse
import json
import re

PORT = 8080
DB_FILE = "urls.db"
BASE_URL = f"http://localhost:{PORT}"

# Base62 mapping characters
BASE62_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def encode_base62(num):
    """Encodes an integer into a base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    arr = []
    while num:
        num, rem = divmod(num, 62)
        arr.append(BASE62_ALPHABET[rem])
    return "".join(reversed(arr))

def init_db():
    """Initializes the SQLite database schema."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url TEXT UNIQUE,
                short_code TEXT UNIQUE,
                clicks INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

class ShortenerHTTPHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent logger to keep console output clean
        pass

    def send_html_response(self, html_content, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        url_path = self.path.strip("/")
        
        # Serves root page - shorten URL form UI
        if url_path == "" or url_path == "index.html":
            self.serve_home_page()
            return
            
        # Serves statistics page
        if url_path == "stats":
            self.serve_stats_page()
            return

        # Redirect short codes
        if re.match(r"^[a-zA-Z0-9]+$", url_path):
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (url_path,))
                row = cursor.fetchone()
                if row:
                    long_url, clicks = row
                    # Update click stats
                    cursor.execute("UPDATE urls SET clicks = ? WHERE short_code = ?", (clicks + 1, url_path))
                    conn.commit()
                    
                    # Permanent redirect
                    self.send_response(302)
                    self.send_header("Location", long_url)
                    self.end_headers()
                    return
        
        # Fallback 404
        self.serve_error_page("404 - Page Not Found", "The requested link or short code could not be located in our telemetry systems.")

    def do_POST(self):
        if self.path == "/shorten":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            
            # Parse form fields
            params = urllib.parse.parse_qs(post_data)
            long_url = params.get("url", [""])[0].strip()
            
            # Simple URL regex validation
            if not long_url or not re.match(r"^https?://[^\s/$.?#].[^\s]*$", long_url):
                self.serve_error_page("Invalid URL", "Please provide a valid destination URL starting with http:// or https://")
                return

            short_code = self.shorten_url(long_url)
            self.serve_success_page(long_url, f"{BASE_URL}/{short_code}")
            return
            
        self.serve_error_page("400 - Bad Request", "The action requested is invalid.")

    def shorten_url(self, long_url):
        """Shortens a URL, returns the short code."""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # Check if already shortened
            cursor.execute("SELECT short_code FROM urls WHERE long_url = ?", (long_url,))
            row = cursor.fetchone()
            if row:
                return row[0]
            
            # Insert and get ID
            cursor.execute("INSERT INTO urls (long_url) VALUES (?)", (long_url,))
            last_id = cursor.lastrowid
            
            # Generate code and update
            short_code = encode_base62(last_id)
            cursor.execute("UPDATE urls SET short_code = ? WHERE id = ?", (short_code, last_id))
            conn.commit()
            
            return short_code

    def serve_home_page(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyShort — Sleek URL Shortener</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg: #03030c;
                    --text: #ffffff;
                    --primary: #00e5ff;
                    --accent: #ff1744;
                    --glass: rgba(15, 15, 27, 0.6);
                    --border: rgba(255, 255, 255, 0.08);
                }
                * { box-sizing: border-box; margin: 0; padding: 0; }
                body {
                    background: var(--bg);
                    color: var(--text);
                    font-family: 'Outfit', sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    overflow: hidden;
                    position: relative;
                }
                .ambient {
                    position: absolute;
                    width: 300px;
                    height: 300px;
                    background: radial-gradient(circle, rgba(0,229,255,0.15) 0%, transparent 70%);
                    top: -100px;
                    left: -100px;
                    border-radius: 50%;
                    animation: pulse 10s infinite alternate;
                }
                .ambient-2 {
                    position: absolute;
                    width: 400px;
                    height: 400px;
                    background: radial-gradient(circle, rgba(255,23,68,0.1) 0%, transparent 70%);
                    bottom: -150px;
                    right: -150px;
                    border-radius: 50%;
                    animation: pulse 12s infinite alternate-reverse;
                }
                @keyframes pulse {
                    0% { transform: scale(1) translate(0, 0); }
                    100% { transform: scale(1.2) translate(30px, 30px); }
                }
                .container {
                    background: var(--glass);
                    backdrop-filter: blur(20px);
                    -webkit-backdrop-filter: blur(20px);
                    border: 1px solid var(--border);
                    border-radius: 24px;
                    padding: 3rem;
                    width: 90%;
                    max-width: 520px;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                    z-index: 10;
                    text-align: center;
                }
                h1 {
                    font-size: 2.5rem;
                    font-weight: 800;
                    letter-spacing: -0.03em;
                    margin-bottom: 0.5rem;
                    background: linear-gradient(135deg, #fff 30%, var(--primary));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }
                p.subtitle {
                    color: rgba(255,255,255,0.6);
                    font-size: 0.9rem;
                    margin-bottom: 2rem;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                input[type="url"] {
                    background: rgba(255,255,255,0.03);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 1rem 1.25rem;
                    color: white;
                    font-size: 1rem;
                    transition: all 0.3s;
                    font-family: inherit;
                }
                input[type="url"]:focus {
                    outline: none;
                    border-color: var(--primary);
                    background: rgba(255,255,255,0.08);
                    box-shadow: 0 0 15px rgba(0,229,255,0.2);
                }
                button {
                    background: var(--text);
                    color: var(--bg);
                    border: none;
                    border-radius: 12px;
                    padding: 1rem;
                    font-size: 1rem;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.3s;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                button:hover {
                    background: var(--primary);
                    color: var(--bg);
                    box-shadow: 0 0 20px rgba(0,229,255,0.4);
                }
                .footer-links {
                    margin-top: 2rem;
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                    font-size: 0.8rem;
                }
                a {
                    color: rgba(255,255,255,0.4);
                    text-decoration: none;
                    transition: color 0.3s;
                }
                a:hover { color: var(--primary); }
            </style>
        </head>
        <body>
            <div class="ambient"></div>
            <div class="ambient-2"></div>
            <div class="container">
                <h1>PyShort</h1>
                <p class="subtitle">Enter a long destination link to generate a shortened URL</p>
                <form action="/shorten" method="POST">
                    <input type="url" name="url" placeholder="https://example.com/very/long/destination/link" required>
                    <button type="submit">Shorten Link</button>
                </form>
                <div class="footer-links">
                    <a href="/stats">View Shortener Database & Clicks</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_html_response(html)

    def serve_success_page(self, original_url, shortened_url):
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Link Created! — PyShort</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --bg: #03030c;
                    --text: #ffffff;
                    --primary: #00e676;
                    --glass: rgba(15, 15, 27, 0.6);
                    --border: rgba(255, 255, 255, 0.08);
                }}
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    background: var(--bg);
                    color: var(--text);
                    font-family: 'Outfit', sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }}
                .container {{
                    background: var(--glass);
                    backdrop-filter: blur(20px);
                    border: 1px solid var(--border);
                    border-radius: 24px;
                    padding: 3rem;
                    width: 90%;
                    max-width: 520px;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                    text-align: center;
                }}
                h1 {{
                    font-size: 2.2rem;
                    font-weight: 800;
                    margin-bottom: 0.5rem;
                    color: var(--primary);
                }}
                p.success-msg {{
                    color: rgba(255,255,255,0.6);
                    font-size: 0.95rem;
                    margin-bottom: 2rem;
                }}
                .result-box {{
                    background: rgba(255,255,255,0.03);
                    border: 1px solid var(--border);
                    border-radius: 12px;
                    padding: 1rem;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 1.1rem;
                    color: #00e5ff;
                    margin-bottom: 1.5rem;
                    word-break: break-all;
                    cursor: pointer;
                    user-select: all;
                }}
                .orig-url {{
                    font-size: 0.75rem;
                    color: rgba(255,255,255,0.4);
                    word-break: break-all;
                    margin-bottom: 2rem;
                    max-height: 50px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }}
                .btn-group {{
                    display: flex;
                    gap: 1rem;
                }}
                .btn {{
                    flex: 1;
                    padding: 0.85rem;
                    border-radius: 10px;
                    font-weight: 700;
                    font-size: 0.85rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    cursor: pointer;
                    transition: all 0.3s;
                    text-decoration: none;
                    display: inline-block;
                }}
                .btn.primary {{
                    background: white;
                    color: var(--bg);
                    border: none;
                }}
                .btn.primary:hover {{
                    background: #00e5ff;
                    box-shadow: 0 0 15px rgba(0,229,255,0.3);
                }}
                .btn.secondary {{
                    background: rgba(255,255,255,0.05);
                    color: white;
                    border: 1px solid var(--border);
                }}
                .btn.secondary:hover {{
                    background: rgba(255,255,255,0.1);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Short URL Ready!</h1>
                <p class="success-msg">Your link has been compiled and compressed successfully.</p>
                <div class="result-box" onclick="navigator.clipboard.writeText(this.innerText)">{shortened_url}</div>
                <div class="orig-url">Destination: {original_url}</div>
                <div class="btn-group">
                    <a href="/" class="btn primary">Shorten Another</a>
                    <a href="/stats" class="btn secondary">View Database</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_html_response(html)

    def serve_stats_page(self):
        rows_html = ""
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, long_url, short_code, clicks FROM urls ORDER BY id DESC")
            rows = cursor.fetchall()
            
            for row in rows:
                db_id, long_url, short_code, clicks = row
                short_link = f"{BASE_URL}/{short_code}"
                rows_html += f"""
                <tr>
                    <td>{db_id}</td>
                    <td class="long-link-cell" title="{long_url}">{long_url}</td>
                    <td><a href="{short_link}" target="_blank">{short_code}</a></td>
                    <td class="clicks-cell">{clicks}</td>
                </tr>
                """

        if not rows_html:
            rows_html = "<tr><td colspan='4' style='text-align:center; color:rgba(255,255,255,0.4); padding: 2rem;'>No URLs shortened yet. Database is empty.</td></tr>"

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PyShort Analytics & Database</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --bg: #03030c;
                    --text: #ffffff;
                    --primary: #00e5ff;
                    --glass: rgba(15, 15, 27, 0.6);
                    --border: rgba(255, 255, 255, 0.08);
                }}
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    background: var(--bg);
                    color: var(--text);
                    font-family: 'Outfit', sans-serif;
                    padding: 2rem;
                    display: flex;
                    justify-content: center;
                    min-height: 100vh;
                }}
                .container {{
                    background: var(--glass);
                    backdrop-filter: blur(20px);
                    border: 1px solid var(--border);
                    border-radius: 24px;
                    padding: 2rem;
                    width: 100%;
                    max-width: 800px;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                    display: flex;
                    flex-direction: column;
                }}
                header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 2rem;
                    border-bottom: 1px solid var(--border);
                    padding-bottom: 1rem;
                }}
                h1 {{
                    font-size: 1.8rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                }}
                .back-btn {{
                    background: rgba(255,255,255,0.05);
                    border: 1px solid var(--border);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    font-size: 0.8rem;
                    font-weight: 600;
                    text-decoration: none;
                    transition: all 0.3s;
                }}
                .back-btn:hover {{
                    background: var(--primary);
                    color: var(--bg);
                    border-color: var(--primary);
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    text-align: left;
                    font-family: 'Outfit', sans-serif;
                }}
                th {{
                    color: rgba(255,255,255,0.4);
                    font-size: 0.75rem;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    padding: 0.75rem 1rem;
                    border-bottom: 1px solid var(--border);
                }}
                td {{
                    padding: 1rem;
                    border-bottom: 1px solid rgba(255,255,255,0.04);
                    font-size: 0.9rem;
                }}
                .long-link-cell {{
                    max-width: 320px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }}
                .clicks-cell {{
                    font-family: 'JetBrains Mono', monospace;
                    color: #00e676;
                    font-weight: 700;
                }}
                a {{
                    color: var(--primary);
                    text-decoration: none;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: 700;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Shortened Database</h1>
                    <a href="/" class="back-btn">← Back to Shortener</a>
                </header>
                <div style="overflow-x: auto; flex: 1;">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 80px;">ID</th>
                                <th>Long Destination URL</th>
                                <th style="width: 150px;">Short Code</th>
                                <th style="width: 100px;">Clicks</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_html_response(html)

    def serve_error_page(self, title, message):
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error — PyShort</title>
            <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --bg: #03030c;
                    --text: #ffffff;
                    --primary: #ff1744;
                    --glass: rgba(15, 15, 27, 0.6);
                    --border: rgba(255, 255, 255, 0.08);
                }}
                * {{ box-sizing: border-box; margin: 0; padding: 0; }}
                body {{
                    background: var(--bg);
                    color: var(--text);
                    font-family: 'Outfit', sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                }}
                .container {{
                    background: var(--glass);
                    backdrop-filter: blur(20px);
                    border: 1px solid var(--border);
                    border-radius: 24px;
                    padding: 3rem;
                    width: 90%;
                    max-width: 500px;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
                    text-align: center;
                }}
                h1 {{
                    font-size: 2rem;
                    font-weight: 800;
                    margin-bottom: 1rem;
                    color: var(--primary);
                }}
                p {{
                    color: rgba(255,255,255,0.7);
                    font-size: 0.95rem;
                    line-height: 1.5;
                    margin-bottom: 2rem;
                }}
                .back-btn {{
                    display: inline-block;
                    background: white;
                    color: var(--bg);
                    border: none;
                    border-radius: 12px;
                    padding: 1rem 2rem;
                    font-size: 0.9rem;
                    font-weight: 700;
                    text-decoration: none;
                    text-transform: uppercase;
                    transition: all 0.3s;
                }}
                .back-btn:hover {{
                    background: var(--primary);
                    color: white;
                    box-shadow: 0 0 20px rgba(255,23,68,0.4);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{title}</h1>
                <p>{message}</p>
                <a href="/" class="back-btn">Go Back</a>
            </div>
        </body>
        </html>
        """
        self.send_html_response(html, status=400)

def main():
    init_db()
    
    # Allow address reuse to avoid "port already in use" errors during testing/restart
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), ShortenerHTTPHandler) as httpd:
        print(f"[*] PyShort URL Shortener Service running on port {PORT}")
        print(f"[*] Admin Panel: {BASE_URL}/stats")
        print("[*] Press Ctrl+C to terminate...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Shutting down URL Shortener Service...")

if __name__ == "__main__":
    main()
