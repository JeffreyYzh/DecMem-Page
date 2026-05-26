#!/usr/bin/env python3
"""Tiny static server with HTTP Range support so browsers can stream MP4 videos.

Usage:
    python3 serve.py [port]   # default port: 8080

Why not `python3 -m http.server`?
    The stock SimpleHTTPRequestHandler does not implement Range / 206 Partial
    Content. Browsers expect Range for <video> playback (especially when the
    MP4 moov atom is at the end of the file). Without it many videos either
    fail to play or get cut off by ConnectionResetError when the user scrolls.
"""

import os
import re
import sys
import traceback
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


_QUIET_EXC = (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)


_RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


class RangeRequestHandler(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler + RFC 7233 single-range support."""

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except _QUIET_EXC:
            pass

    def handle_one_request(self):
        try:
            super().handle_one_request()
        except _QUIET_EXC:
            self.close_connection = True

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - [%s] %s\n" % (
            self.address_string(), self.log_date_time_string(), fmt % args,
        ))

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        if not os.path.isfile(path):
            self.send_error(404, "File not found")
            return None

        ctype = self.guess_type(path)
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        size = fs.st_size

        range_header = self.headers.get("Range")
        if range_header:
            m = _RANGE_RE.fullmatch(range_header.strip())
            if not m:
                f.close()
                self.send_error(400, "Invalid Range header")
                return None
            start_s, end_s = m.group(1), m.group(2)
            if start_s == "" and end_s == "":
                f.close()
                self.send_error(400, "Invalid Range header")
                return None
            if start_s == "":
                length = int(end_s)
                if length <= 0:
                    f.close()
                    self.send_error(416, "Requested Range Not Satisfiable")
                    return None
                start = max(size - length, 0)
                end = size - 1
            else:
                start = int(start_s)
                end = int(end_s) if end_s else size - 1
            if start >= size or end >= size or start > end:
                f.close()
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return None

            length = end - start + 1
            self.send_response(206)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            f.seek(start)
            return _LimitedReader(f, length)

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(size))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        return f


class _LimitedReader:
    """Wraps a file object so copyfileobj reads at most `length` bytes."""

    def __init__(self, fp, length):
        self._fp = fp
        self._remaining = length

    def read(self, n=-1):
        if self._remaining <= 0:
            return b""
        if n is None or n < 0 or n > self._remaining:
            n = self._remaining
        data = self._fp.read(n)
        self._remaining -= len(data)
        return data

    def close(self):
        self._fp.close()


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, _QUIET_EXC):
            return
        traceback.print_exc()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    addr = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(addr, RangeRequestHandler)
    print(f"Serving HTTP with Range support on http://0.0.0.0:{port}/ (Ctrl+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
        httpd.server_close()


if __name__ == "__main__":
    main()
