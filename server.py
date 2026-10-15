"""
Lightweight Zero-Dependency Web & API Server for YouTube Shorts Analytics.
Subject: Social Media | Parul University | Author: Thota Abhiram
"""

import http.server
import json
import os
import socketserver
import urllib.parse
from typing import Dict, Any

from core.dataset_generator import load_dataset
from core.analyzer import ShortsPerformanceAnalyzer, analyze_single_short
from core.youtube_api import YouTubeShortsClient

PORT = int(os.environ.get("PORT", 8000))
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

# In-memory cached dataset & analyzer
RAW_DATASET = load_dataset()
ANALYZER = ShortsPerformanceAnalyzer(RAW_DATASET)


class ShortsRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler serving static dashboard and JSON API routes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def log_message(self, format, *args):
        # Clean terminal logging
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} - {args[1] if len(args) > 1 else ''}")

    def do_GET(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        if path == "/api/data":
            self.send_json_response(ANALYZER.get_full_analysis())
        elif path == "/api/health":
            self.send_json_response({"status": "healthy", "service": "YouTube Shorts Analytics"})
        else:
            # Fallback to static files in web/
            super().do_GET()

    def do_POST(self):
        url_parts = urllib.parse.urlparse(self.path)
        path = url_parts.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path == "/api/fetch-live":
            self.handle_fetch_live(payload)
        elif path == "/api/predict-virality":
            self.handle_predict_virality(payload)
        else:
            self.send_error(404, "Endpoint Not Found")

    def handle_fetch_live(self, payload: Dict[str, Any]):
        global RAW_DATASET, ANALYZER
        query = payload.get("query", "shorts")
        max_results = int(payload.get("max_results", 15))

        try:
            client = YouTubeShortsClient()
            live_shorts = client.fetch_shorts(query=query, max_results=max_results)
            if live_shorts:
                RAW_DATASET = live_shorts
                ANALYZER = ShortsPerformanceAnalyzer(RAW_DATASET)
            self.send_json_response(ANALYZER.get_full_analysis())
        except Exception as e:
            self.send_json_response({"error": str(e)}, status=500)

    def handle_predict_virality(self, payload: Dict[str, Any]):
        title = payload.get("title", "Untitled Short")
        duration = int(payload.get("duration_seconds", 30))
        category = payload.get("category", "General & Trending")
        views = int(payload.get("views", 250000))

        dummy = {
            "title": title,
            "views": views,
            "likes": int(views * 0.055),
            "comments": int(views * 0.0035),
            "duration_seconds": duration,
            "category": category,
            "tags": ["shorts"]
        }
        result = analyze_single_short(dummy)
        self.send_json_response(result)

    def send_json_response(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)


def run_server(port: int = PORT):
    for p in [port, 8080, 8081, 5000]:
        try:
            with socketserver.TCPServer(("", p), ShortsRequestHandler) as httpd:
                print("=" * 70)
                print(f"🚀 YOUTUBE SHORTS ANALYTICS DASHBOARD RUNNING")
                print(f"🎓 Subject: Social Media | Parul University | Student: Thota Abhiram")
                print(f"🌐 Access Dashboard in your browser: http://localhost:{p}")
                print(f"💡 Press Ctrl+C in terminal to stop server")
                print("=" * 70)
                httpd.serve_forever()
                break
        except OSError:
            print(f"Port {p} already in use, trying next port...")
            continue


if __name__ == "__main__":
    run_server()
