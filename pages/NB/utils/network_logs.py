"""
network_logger.py
------------------
Captures network RESPONSES (like DevTools Network tab) for specific API calls
made during a Playwright test run.

Only captures these target services (edit TARGET_SERVICES to add/remove):
    - bp
    - ncdRequestV2
    - quote
    - issuePolicy

Saves files as:
    NetworkLogs/bp_<vehicle_reg>.json
    NetworkLogs/ncdRequestV2_<vehicle_reg>.json
    NetworkLogs/create_quote_<quote_number>.json
    NetworkLogs/issuePolicy_<policy_number>.json

Duration:
----------
response.request.timing()["responseEnd"] often returns null because the
server doesn't send a Timing-Allow-Origin header for cross-origin calls.
So duration is measured manually instead: note the wall-clock time when
each request STARTS (via the "request" event), then subtract that from
the wall-clock time when its matching response ARRIVES (via the
"response" event). This works regardless of any server headers.

Usage (sync Playwright + pytest):
----------------------------------
Attach once in conftest.py's page fixture:

    page.net_logger = NetworkLogger(page)

Then in each test, once known:

    page.net_logger.set_vehicle_reg(vehicle_data["vehicle_reg_no"])   # early in the test
    page.net_logger.set_quote_number(quote_number)                    # once quote ref # is read
    page.net_logger.set_policy_number(policy_number)                  # once policy # is read after issuance

    page.net_logger.summary()   # optional, prints what got captured/missing
"""

import os
import json
import re
from datetime import datetime
from urllib.parse import urlparse


class NetworkLogger:
    # Service names to capture - matched against the last URL path segment (query params ignored)
    TARGET_SERVICES = ["bp", "ncdRequestV2", "quote", "issuePolicy", "issueSapPolicy"]

    # The policy-issuance call shows up under different names depending on env/build -
    # treat any of these as "the policy issuance call".
    POLICY_SERVICE_NAMES = {"issuePolicy", "issueSapPolicy"}

    def __init__(self, page, vehicle_reg=None, log_dir="NetworkLogs", target_services=None):
        self.page = page
        self.vehicle_reg = self._sanitize(vehicle_reg) if vehicle_reg else None
        self.quote_number = None
        self.policy_number = None
        self.log_dir = log_dir
        self.target_services = target_services or self.TARGET_SERVICES
        self.captured = {}  # service_name -> filepath, for summary()
        self._pending = []        # bp / ncdRequestV2 captures before vehicle_reg is known
        self._quote_pending = []  # quote captures before quote_number is known
        self._policy_pending = [] # issuePolicy captures before policy_number is known
        self._request_start_times = {}  # id(request) -> datetime, for manual duration tracking

        os.makedirs(self.log_dir, exist_ok=True)
        self.page.on("request", self._handle_request)
        self.page.on("response", self._handle_response)

    def set_vehicle_reg(self, vehicle_reg):
        """Call once vehicle reg is known. Flushes buffered bp/ncdRequestV2 captures."""
        self.vehicle_reg = self._sanitize(vehicle_reg)
        for record in self._pending:
            self._write_record(record)
        self._pending = []

    def set_quote_number(self, quote_number):
        """Call once the quote number is known (e.g. from 'Quote Reference #' on screen).
        Flushes buffered quote captures, saved as create_quote_<quote_number>.json"""
        self.quote_number = self._sanitize(quote_number)
        for record in self._quote_pending:
            self._write_quote_record(record)
        self._quote_pending = []

    def set_policy_number(self, policy_number):
        """Call once the policy number is known (e.g. from 'Policy Number' shown after Issue Policy).
        Flushes buffered issuePolicy captures, saved as issuePolicy_<policy_number>.json"""
        self.policy_number = self._sanitize(policy_number)
        for record in self._policy_pending:
            self._write_policy_record(record)
        self._policy_pending = []

    def _sanitize(self, value):
        """Make a string safe to use in a filename."""
        return re.sub(r'[\\/*?:"<>|]', "_", str(value))

    def _extract_service_name(self, url):
        path = urlparse(url).path
        segments = [s for s in path.split("/") if s]
        return segments[-1] if segments else url

    def _handle_request(self, request):
        """Records the wall-clock start time of every request, keyed by the
        request object's identity (safe even if the same URL fires twice)."""
        self._request_start_times[id(request)] = datetime.now()

    def _handle_response(self, response):
        try:
            service_name = self._extract_service_name(response.url)

            if service_name not in self.target_services:
                return

            try:
                body = response.json()
            except Exception:
                try:
                    body = response.text()
                except Exception:
                    body = None

            # Manual duration: start time (from the request event) -> now (response arrived)
            start_time = self._request_start_times.pop(id(response.request), None)
            if start_time:
                duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            else:
                duration_ms = None

            record = {
                "service": service_name,
                "url": response.url,
                "status": response.status,
                "duration_ms": duration_ms,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response": body,
            }

            if service_name == "quote":
                if self.quote_number is None:
                    self._quote_pending.append(record)
                else:
                    self._write_quote_record(record)
            elif service_name in self.POLICY_SERVICE_NAMES:
                if self.policy_number is None:
                    self._policy_pending.append(record)
                else:
                    self._write_policy_record(record)
            else:
                if self.vehicle_reg is None:
                    self._pending.append(record)
                else:
                    self._write_record(record)

        except Exception as e:
            print(f"[NetworkLogger] Failed to capture response for {getattr(response, 'url', '?')}: {e}")

    def _write_record(self, record):
        service_name = record["service"]
        record["vehicle_reg"] = self.vehicle_reg
        filename = f"{service_name}_{self.vehicle_reg}.json"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        self.captured[service_name] = filepath

    def _write_quote_record(self, record):
        record["quote_number"] = self.quote_number
        filename = f"create_quote_{self.quote_number}.json"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        self.captured["quote"] = filepath

    def _write_policy_record(self, record):
        service_name = record["service"]  # whichever name actually matched: issuePolicy / issueSapPolicy
        record["policy_number"] = self.policy_number
        filename = f"{service_name}_{self.policy_number}.json"
        filepath = os.path.join(self.log_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        self.captured[service_name] = filepath

        # Print duration to the terminal as soon as it's written, labeled with the real service name
        duration = record.get("duration_ms")
        if duration is not None:
            print(f"{service_name} duration: {duration} ms ({duration / 1000:.1f}s)")
        else:
            print(f"{service_name} duration: not available")

    def summary(self):
        """Prints/returns which target services were captured vs missing for this run."""
        missing = [s for s in self.target_services if s not in self.captured]
        print(f"[NetworkLogger] Captured: {list(self.captured.keys())}")
        if missing:
            print(f"[NetworkLogger] MISSING (not called or not detected): {missing}")
        return {"captured": self.captured, "missing": missing}