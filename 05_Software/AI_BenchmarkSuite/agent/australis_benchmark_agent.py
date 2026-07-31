#!/usr/bin/env python3
"""AUSTRALIS AI Benchmark Suite node agent.

This is a public, dependency-light benchmark proxy for PC and CM5 nodes. It
serves the browser console, streams local telemetry via SSE, proxies inference
requests to Ollama/llama.cpp/OpenAI-compatible endpoints, and packages export
bundles. It does not store secrets and treats power data as unavailable unless
a real sensor reports it.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
import zipfile
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    psutil = None  # type: ignore


AGENT_VERSION = "0.2.0"
DEFAULT_PORT = 8765
SENSITIVE_KEYS = (
    "secret",
    "password",
    "authorization",
    "api_key",
    "apikey",
    "access_token",
    "auth_token",
    "agent_token",
    "bearer_token",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json_body(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        sanitized: Dict[str, Any] = {}
        for key, item in value.items():
            if any(s in key.lower() for s in SENSITIVE_KEYS):
                sanitized[key] = "<redacted>"
            else:
                sanitized[key] = sanitize(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    return value


def json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, ensure_ascii=True, indent=2).encode("utf-8")


def compact_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def run_command(args: Iterable[str], timeout_s: float = 2.0) -> Tuple[bool, str]:
    try:
        proc = subprocess.run(
            list(args),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        text = (proc.stdout or proc.stderr or "").strip()
        return proc.returncode == 0, text
    except Exception as exc:
        return False, str(exc)


def parse_vcgencmd_temp(text: str) -> Optional[float]:
    # Example: temp=54.8'C
    if "temp=" not in text:
        return None
    try:
        return float(text.split("temp=", 1)[1].split("'")[0])
    except Exception:
        return None


def parse_pmic_adc(text: str) -> Dict[str, Any]:
    # Raspberry Pi 5 example is line-based and firmware-dependent. Keep it
    # best-effort and never infer watts from voltage-only readings.
    out: Dict[str, Any] = {}
    for line in text.splitlines():
        line = line.strip()
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        raw = raw.strip()
        out[key.strip()] = raw
    return out


class TelemetryCollector:
    def __init__(self, runtime_process_hint: str = "") -> None:
        self.runtime_process_hint = runtime_process_hint.lower()

    def collect(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "schema_version": "benchmark_telemetry.v1",
            "timestamp_utc": utc_now(),
            "host": platform.node(),
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": platform.python_version(),
            },
            "cpu": self._cpu(),
            "memory": self._memory(),
            "disk": self._disk(),
            "gpu": self._nvidia_smi(),
            "sensors": self._sensors(),
            "raspberry_pi": self._raspberry_pi(),
            "inference_process": self._runtime_process(),
            "power": {"state": "unavailable", "watts": None, "source": None},
        }
        return payload

    def _cpu(self) -> Dict[str, Any]:
        if psutil:
            return {
                "load_pct": psutil.cpu_percent(interval=0.0),
                "logical_count": psutil.cpu_count(logical=True),
                "physical_count": psutil.cpu_count(logical=False),
                "load_avg": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            }
        return {
            "load_pct": None,
            "logical_count": os.cpu_count(),
            "physical_count": None,
            "load_avg": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
        }

    def _memory(self) -> Dict[str, Any]:
        if psutil:
            vm = psutil.virtual_memory()
            sm = psutil.swap_memory()
            return {
                "used_bytes": vm.used,
                "available_bytes": vm.available,
                "total_bytes": vm.total,
                "used_pct": vm.percent,
                "swap_used_bytes": sm.used,
                "swap_total_bytes": sm.total,
                "swap_used_pct": sm.percent,
            }
        return {
            "used_bytes": None,
            "available_bytes": None,
            "total_bytes": None,
            "used_pct": None,
            "swap_used_bytes": None,
            "swap_total_bytes": None,
            "swap_used_pct": None,
        }

    def _disk(self) -> Dict[str, Any]:
        usage = shutil.disk_usage(Path.cwd())
        return {
            "path": str(Path.cwd()),
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "total_bytes": usage.total,
            "used_pct": round((usage.used / usage.total) * 100.0, 2) if usage.total else None,
        }

    def _nvidia_smi(self) -> Dict[str, Any]:
        exe = shutil.which("nvidia-smi")
        if not exe:
            return {"available": False, "devices": []}
        ok, text = run_command(
            [
                exe,
                "--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw",
                "--format=csv,noheader,nounits",
            ],
            timeout_s=3.0,
        )
        if not ok:
            return {"available": False, "error": text, "devices": []}
        devices = []
        for line in text.splitlines():
            parts = [part.strip() for part in line.split(",")]
            if len(parts) < 6:
                continue
            devices.append(
                {
                    "name": parts[0],
                    "utilization_pct": _to_float(parts[1]),
                    "memory_used_mib": _to_float(parts[2]),
                    "memory_total_mib": _to_float(parts[3]),
                    "temperature_c": _to_float(parts[4]),
                    "power_draw_w": _to_float(parts[5]),
                }
            )
        return {"available": True, "devices": devices}

    def _sensors(self) -> Dict[str, Any]:
        exe = shutil.which("sensors")
        if not exe:
            return {"available": False}
        ok, text = run_command([exe, "-j"], timeout_s=2.0)
        if ok:
            try:
                return {"available": True, "raw": json.loads(text)}
            except Exception:
                pass
        return {"available": ok, "raw_text": text}

    def _raspberry_pi(self) -> Dict[str, Any]:
        exe = shutil.which("vcgencmd")
        if not exe:
            return {"available": False}
        ok_temp, temp_text = run_command([exe, "measure_temp"], timeout_s=2.0)
        ok_throttle, throttle_text = run_command([exe, "get_throttled"], timeout_s=2.0)
        ok_adc, adc_text = run_command([exe, "pmic_read_adc"], timeout_s=2.0)
        return {
            "available": True,
            "temp_c": parse_vcgencmd_temp(temp_text) if ok_temp else None,
            "get_throttled": throttle_text if ok_throttle else None,
            "pmic_adc": parse_pmic_adc(adc_text) if ok_adc else {"state": "unavailable"},
        }

    def _runtime_process(self) -> Dict[str, Any]:
        if not psutil:
            return {"available": False, "reason": "psutil unavailable"}
        hints = [self.runtime_process_hint, "llama-server", "llama.cpp", "ollama"]
        hints = [hint for hint in hints if hint]
        candidates = []
        for proc in psutil.process_iter(["pid", "name", "cmdline", "memory_info", "cpu_percent"]):
            try:
                name = (proc.info.get("name") or "").lower()
                cmd = " ".join(proc.info.get("cmdline") or []).lower()
                if not any(hint in name or hint in cmd for hint in hints):
                    continue
                mem = proc.info.get("memory_info")
                candidates.append(
                    {
                        "pid": proc.info.get("pid"),
                        "name": proc.info.get("name"),
                        "rss_bytes": getattr(mem, "rss", None),
                        "cpu_pct": proc.info.get("cpu_percent"),
                        "cmdline": " ".join(proc.info.get("cmdline") or [])[:500],
                    }
                )
            except Exception:
                continue
        return {"available": True, "matches": candidates[:8]}


def _to_float(value: Any) -> Optional[float]:
    try:
        return float(str(value).strip())
    except Exception:
        return None


class InferenceProxy:
    def infer(self, request: Dict[str, Any]) -> Dict[str, Any]:
        started = time.perf_counter()
        runtime = str(request.get("runtime") or "").lower()
        endpoint = str(request.get("endpoint") or "").strip()
        if not endpoint:
            return self._error("endpoint_missing", started, "Inference endpoint is required.")

        body = self._build_body(runtime, request)
        url = self._build_url(runtime, endpoint)
        timeout_s = float(request.get("timeout_s") or 120.0)
        headers = {"Content-Type": "application/json"}
        bearer_value = request.get("api_key")
        if bearer_value:
            headers["Authorization"] = f"Bearer {bearer_value}"

        try:
            http_request = urllib.request.Request(
                url,
                data=compact_json_bytes(body),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(http_request, timeout=timeout_s) as response:
                raw_bytes = response.read()
                status = response.status
                raw_text = raw_bytes.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            raw_text = exc.read().decode("utf-8", errors="replace")
            return self._error("http_error", started, raw_text, http_status=exc.code)
        except TimeoutError as exc:
            return self._error("timeout", started, str(exc))
        except Exception as exc:
            return self._error("proxy_error", started, str(exc))

        latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
        parsed: Any
        try:
            parsed = json.loads(raw_text)
        except Exception:
            parsed = {"raw_text": raw_text}

        normalized = self._normalize(runtime, parsed, latency_ms)
        return {
            "ok": True,
            "timestamp_utc": utc_now(),
            "runtime": runtime,
            "endpoint": url,
            "http_status": status,
            "latency_ms": latency_ms,
            "request_body_sanitized": sanitize(body),
            "metrics": normalized["metrics"],
            "text": normalized["text"],
            "raw": parsed,
        }

    def _build_url(self, runtime: str, endpoint: str) -> str:
        endpoint = endpoint.rstrip("/")
        if runtime == "ollama":
            if endpoint.endswith("/api/generate") or endpoint.endswith("/api/chat"):
                return endpoint
            return endpoint + "/api/generate"
        if runtime in ("llama.cpp", "llamacpp"):
            if endpoint.endswith("/completion") or endpoint.endswith("/v1/chat/completions"):
                return endpoint
            return endpoint + "/completion"
        if runtime == "openai-compatible":
            if endpoint.endswith("/v1/chat/completions"):
                return endpoint
            return endpoint + "/v1/chat/completions"
        return endpoint

    def _build_body(self, runtime: str, request: Dict[str, Any]) -> Dict[str, Any]:
        prompt = str(request.get("prompt") or "")
        model = str(request.get("model") or "")
        params = request.get("params") or {}
        temperature = params.get("temperature", request.get("temperature", 0.1))
        max_tokens = params.get("max_tokens", params.get("num_predict", 512))
        seed = params.get("seed", request.get("seed"))
        json_mode = bool(params.get("json_mode", request.get("json_mode", True)))
        thinking = bool(params.get("thinking", request.get("thinking", False)))

        if runtime == "ollama":
            options = {
                "temperature": temperature,
                "num_ctx": params.get("context", params.get("num_ctx")),
                "num_predict": max_tokens,
            }
            if seed is not None and seed != "":
                options["seed"] = seed
            options = {key: value for key, value in options.items() if value is not None and value != ""}
            body: Dict[str, Any] = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "think": thinking,
                "options": options,
            }
            if json_mode:
                body["format"] = "json"
            return body

        if runtime in ("llama.cpp", "llamacpp"):
            body = {
                "prompt": prompt,
                "temperature": temperature,
                "n_predict": max_tokens,
                "cache_prompt": False,
            }
            if seed is not None and seed != "":
                body["seed"] = seed
            if params.get("context"):
                body["n_ctx"] = params.get("context")
            return body

        messages = request.get("messages")
        if not messages:
            messages = [{"role": "user", "content": prompt}]
        body = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if seed is not None and seed != "":
            body["seed"] = seed
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        return body

    def _normalize(self, runtime: str, parsed: Any, latency_ms: float) -> Dict[str, Any]:
        text = ""
        metrics: Dict[str, Any] = {
            "latency_ms": latency_ms,
            "prompt_tokens": None,
            "generated_tokens": None,
            "total_tokens": None,
            "tokens_per_s": None,
            "errors": 0,
            "timeouts": 0,
        }

        if isinstance(parsed, dict):
            if runtime == "ollama":
                text = str(parsed.get("response") or parsed.get("message", {}).get("content") or "")
                prompt_tokens = parsed.get("prompt_eval_count")
                gen_tokens = parsed.get("eval_count")
                metrics.update(
                    {
                        "prompt_tokens": prompt_tokens,
                        "generated_tokens": gen_tokens,
                        "total_tokens": _sum_ints(prompt_tokens, gen_tokens),
                    }
                )
                eval_duration_ns = parsed.get("eval_duration")
                if gen_tokens and eval_duration_ns:
                    metrics["tokens_per_s"] = round(float(gen_tokens) / (float(eval_duration_ns) / 1e9), 3)
            elif runtime in ("llama.cpp", "llamacpp"):
                text = str(parsed.get("content") or parsed.get("response") or "")
                timings = parsed.get("timings") or {}
                prompt_tokens = timings.get("prompt_n") or parsed.get("tokens_evaluated")
                gen_tokens = timings.get("predicted_n") or parsed.get("tokens_predicted")
                metrics.update(
                    {
                        "prompt_tokens": prompt_tokens,
                        "generated_tokens": gen_tokens,
                        "total_tokens": _sum_ints(prompt_tokens, gen_tokens),
                    }
                )
                if timings.get("predicted_per_second"):
                    metrics["tokens_per_s"] = round(float(timings["predicted_per_second"]), 3)
            else:
                choices = parsed.get("choices") or []
                if choices:
                    first = choices[0]
                    text = str((first.get("message") or {}).get("content") or first.get("text") or "")
                usage = parsed.get("usage") or {}
                metrics.update(
                    {
                        "prompt_tokens": usage.get("prompt_tokens"),
                        "generated_tokens": usage.get("completion_tokens"),
                        "total_tokens": usage.get("total_tokens"),
                    }
                )

        if metrics["tokens_per_s"] is None and metrics["generated_tokens"]:
            seconds = max(latency_ms / 1000.0, 0.001)
            metrics["tokens_per_s"] = round(float(metrics["generated_tokens"]) / seconds, 3)
        return {"text": text, "metrics": metrics}

    def _error(self, code: str, started: float, message: str, http_status: Optional[int] = None) -> Dict[str, Any]:
        return {
            "ok": False,
            "timestamp_utc": utc_now(),
            "error": {"code": code, "message": message, "http_status": http_status},
            "latency_ms": round((time.perf_counter() - started) * 1000.0, 3),
            "metrics": {"errors": 1, "timeouts": 1 if code == "timeout" else 0},
            "text": "",
            "raw": None,
        }


def _sum_ints(*values: Any) -> Optional[int]:
    total = 0
    found = False
    for value in values:
        try:
            if value is None:
                continue
            total += int(value)
            found = True
        except Exception:
            continue
    return total if found else None


def build_export_bundle(payload: Dict[str, Any]) -> bytes:
    manifest = sanitize(payload.get("manifest") or {})
    results = sanitize(payload.get("results") or [])
    telemetry = sanitize(payload.get("telemetry") or [])
    prompts = sanitize(payload.get("prompts") or [])
    responses = sanitize(payload.get("responses") or [])
    scoring = sanitize(payload.get("scoring") or {})
    events = sanitize(
        payload.get("events")
        or [
            event
            for result in results
            if isinstance(result, dict)
            for event in (result.get("events") or [])
        ]
    )
    config = sanitize(payload.get("config") or {})
    report_md = payload.get("report_markdown") or default_report_markdown(manifest, results)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json_bytes(manifest))
        zf.writestr("results.jsonl", jsonl(results))
        zf.writestr("results.csv", results_csv(results))
        zf.writestr("telemetry.jsonl", jsonl(telemetry))
        zf.writestr("events.jsonl", jsonl(events))
        zf.writestr("scoring.json", json_bytes(scoring))
        zf.writestr("config.sanitized.json", json_bytes(config))
        zf.writestr("report.md", str(report_md))
        for idx, prompt in enumerate(prompts):
            name = safe_artifact_name(prompt.get("name") if isinstance(prompt, dict) else None, idx, "prompt", "txt")
            content = prompt.get("content") if isinstance(prompt, dict) else str(prompt)
            zf.writestr(f"prompts/{name}", str(content))
        for idx, response in enumerate(responses):
            name = safe_artifact_name(response.get("name") if isinstance(response, dict) else None, idx, "response", "json")
            zf.writestr(f"raw_responses/{name}", json_bytes(response))
    return buffer.getvalue()


def jsonl(items: Iterable[Any]) -> str:
    return "".join(json.dumps(item, ensure_ascii=True) + "\n" for item in items)


def results_csv(results: Iterable[Dict[str, Any]]) -> str:
    fieldnames = [
        "run_id",
        "episode_id",
        "node_name",
        "model",
        "runtime",
        "status",
        "pass",
        "score",
        "json_valid",
        "expected_tools_ok",
        "hard_fails",
        "soft_warnings",
        "latency_ms",
        "tokens_per_s",
        "generated_tokens",
        "peak_temp_c",
        "peak_memory_bytes",
        "event_count",
    ]
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for result in results:
        row = flatten_result(result)
        writer.writerow(row)
    return buffer.getvalue()


def flatten_result(result: Dict[str, Any]) -> Dict[str, Any]:
    metrics = result.get("metrics") or {}
    scoring = result.get("scoring") or {}
    telemetry = result.get("telemetry_summary") or {}
    return {
        "run_id": result.get("run_id"),
        "episode_id": result.get("episode_id"),
        "node_name": result.get("node_name"),
        "model": result.get("model"),
        "runtime": result.get("runtime"),
        "status": result.get("status"),
        "pass": scoring.get("pass"),
        "score": scoring.get("score"),
        "json_valid": scoring.get("json_valid"),
        "expected_tools_ok": scoring.get("expected_tools_ok"),
        "hard_fails": ";".join(scoring.get("hard_fails") or []),
        "soft_warnings": ";".join(
            str(item.get("id") if isinstance(item, dict) else item)
            for item in (scoring.get("soft_warnings") or scoring.get("warnings") or [])
        ),
        "latency_ms": metrics.get("latency_ms"),
        "tokens_per_s": metrics.get("tokens_per_s"),
        "generated_tokens": metrics.get("generated_tokens"),
        "peak_temp_c": telemetry.get("peak_temp_c"),
        "peak_memory_bytes": telemetry.get("peak_memory_bytes"),
        "event_count": len(result.get("events") or []),
    }


def safe_artifact_name(value: Any, idx: int, prefix: str, ext: str) -> str:
    raw = str(value or f"{prefix}_{idx:04d}.{ext}")
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in raw)
    if not safe.endswith(f".{ext}"):
        safe += f".{ext}"
    return safe[:120]


def default_report_markdown(manifest: Dict[str, Any], results: Iterable[Dict[str, Any]]) -> str:
    results_list = list(results)
    total = len(results_list)
    passed = sum(1 for item in results_list if (item.get("scoring") or {}).get("pass"))
    return (
        "# AUSTRALIS AI Benchmark Report\n\n"
        f"- Generated UTC: {utc_now()}\n"
        f"- Session: {manifest.get('session_id', 'unknown')}\n"
        f"- Runs: {total}\n"
        f"- Pass: {passed}\n"
        f"- Fail: {total - passed}\n\n"
        "This report is generated from local benchmark artifacts. It does not "
        "declare any model flight-ready or validated for flight.\n"
    )


class BenchmarkAgentHandler(BaseHTTPRequestHandler):
    server_version = "AustralisBenchmarkAgent/0.2"

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_empty(HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path == "/api/health":
            self._send_json(self.server_state.health())
        elif path == "/api/status":
            self._send_json(self.server_state.status())
        elif path == "/api/metadata":
            self._send_json(self.server_state.metadata())
        elif path == "/api/scenarios/australis":
            self._send_json(self.server_state.scenario_pack())
        elif path == "/api/telemetry/stream":
            if not self.server_state.telemetry_enabled:
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": "capability_disabled",
                            "message": "Telemetry is disabled for this dashboard host.",
                        },
                    },
                    HTTPStatus.CONFLICT,
                )
            else:
                self._send_sse()
        elif path == "/api/version":
            self._send_json({"agent_version": AGENT_VERSION})
        else:
            self._send_static(path)

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        try:
            payload = read_json_body(self)
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
            return

        if path == "/api/infer":
            if not self.server_state.inference_enabled:
                self._send_json(
                    {
                        "ok": False,
                        "error": {
                            "code": "capability_disabled",
                            "message": "Inference is disabled for this agent role.",
                        },
                    },
                    HTTPStatus.CONFLICT,
                )
            else:
                result = self.server_state.proxy.infer(payload)
                self._send_json(result)
        elif path == "/api/export-bundle":
            bundle = build_export_bundle(payload)
            filename = f"australis-benchmark-{payload.get('manifest', {}).get('session_id', uuid.uuid4())}.zip"
            self.send_response(HTTPStatus.OK)
            self._cors_headers()
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(bundle)))
            self.end_headers()
            self.wfile.write(bundle)
        else:
            self._send_json({"ok": False, "error": "unknown endpoint"}, HTTPStatus.NOT_FOUND)

    @property
    def server_state(self) -> "AgentState":
        return self.server.state  # type: ignore[attr-defined]

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json_bytes(payload)
        self.send_response(status)
        self._cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_empty(self, status: HTTPStatus) -> None:
        self.send_response(status)
        self._cors_headers()
        self.end_headers()

    def _send_sse(self) -> None:
        self.send_response(HTTPStatus.OK)
        self._cors_headers()
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        interval = max(float(self.server_state.telemetry_interval_s), 0.5)
        while True:
            try:
                telemetry = self.server_state.collector.collect()
                line = "event: telemetry\n" + "data: " + json.dumps(telemetry, ensure_ascii=True) + "\n\n"
                self.wfile.write(line.encode("utf-8"))
                self.wfile.flush()
                time.sleep(interval)
            except (BrokenPipeError, ConnectionResetError):
                break
            except Exception as exc:
                try:
                    line = "event: error\n" + "data: " + json.dumps({"error": str(exc)}) + "\n\n"
                    self.wfile.write(line.encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(interval)
                except Exception:
                    break

    def _send_static(self, path: str) -> None:
        static_dir = self.server_state.static_dir
        if not static_dir:
            self._send_json({"ok": False, "error": "static disabled"}, HTTPStatus.NOT_FOUND)
            return
        requested = "index.html" if path in ("", "/") else path.lstrip("/")
        candidate = (static_dir / requested).resolve()
        try:
            candidate.relative_to(static_dir.resolve())
        except ValueError:
            self._send_json({"ok": False, "error": "invalid path"}, HTTPStatus.BAD_REQUEST)
            return
        if not candidate.exists() or not candidate.is_file():
            self._send_json({"ok": False, "error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        data = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self._cors_headers()
        self.send_header("Content-Type", content_type_for(candidate))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")

    def log_message(self, fmt: str, *args: Any) -> None:
        if not self.server_state.quiet:
            super().log_message(fmt, *args)


def content_type_for(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
    }.get(suffix, "application/octet-stream")


class AgentState:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.static_dir = Path(args.static_dir).resolve() if args.static_dir else None
        self.scenario_pack_path = Path(args.scenario_pack).resolve() if args.scenario_pack else None
        self.quiet = bool(args.quiet)
        self.telemetry_interval_s = float(args.telemetry_interval_s)
        self.dashboard_only = bool(args.dashboard_only)
        self.telemetry_only = bool(args.telemetry_only)
        self.telemetry_enabled = not self.dashboard_only
        self.inference_enabled = not self.dashboard_only and not self.telemetry_only
        self.collector = TelemetryCollector(args.runtime_process_hint or args.runtime)
        self.proxy = InferenceProxy()
        self.started_utc = utc_now()

    def metadata(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "agent_version": AGENT_VERSION,
            "node": {
                "name": self.args.node_name,
                "stage": self.args.stage,
                "type": self.args.node_type,
                "runtime": self.args.runtime if self.inference_enabled else None,
                "model": self.args.model if self.inference_enabled else None,
                "inference_endpoint": self.args.inference_endpoint if self.inference_enabled else None,
                "capabilities": self.capabilities(),
            },
            "host": {
                "hostname": platform.node(),
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": platform.python_version(),
            },
            "started_utc": self.started_utc,
            "role": self.role,
            "capabilities": self.capabilities(),
        }

    def health(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "agent_version": AGENT_VERSION,
            "timestamp_utc": utc_now(),
            "node_name": self.args.node_name,
            "stage": self.args.stage,
            "role": self.role,
            "capabilities": self.capabilities(),
        }

    def status(self) -> Dict[str, Any]:
        telemetry = self.collector.collect() if self.telemetry_enabled else None
        return {"ok": True, "metadata": self.metadata(), "telemetry": telemetry}

    @property
    def role(self) -> str:
        if self.dashboard_only:
            return "dashboard"
        if self.telemetry_only:
            return "telemetry-only"
        return "telemetry+inference"

    def capabilities(self) -> Dict[str, Any]:
        return {
            "telemetry": {
                "available": self.telemetry_enabled,
                "transport": "sse" if self.telemetry_enabled else None,
                "endpoint": "/api/telemetry/stream" if self.telemetry_enabled else None,
            },
            "inference": {
                "available": self.inference_enabled,
                "endpoint": "/api/infer" if self.inference_enabled else None,
                "runtimes": ["ollama", "llama.cpp", "openai-compatible"]
                if self.inference_enabled
                else [],
            },
            "scenario_pack": {"available": True, "endpoint": "/api/scenarios/australis"},
            "export_bundle": {"available": True, "endpoint": "/api/export-bundle"},
        }

    def scenario_pack(self) -> Dict[str, Any]:
        if not self.scenario_pack_path or not self.scenario_pack_path.exists():
            return {"ok": False, "error": "scenario pack not found", "path": str(self.scenario_pack_path)}
        with self.scenario_pack_path.open("r", encoding="utf-8") as handle:
            pack = json.load(handle)
        pack["ok"] = True
        return pack


def build_arg_parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve()
    default_static = here.parents[1] / "console"
    default_scenarios = here.parents[1] / "scenario-packs" / "australis" / "episodes.json"
    parser = argparse.ArgumentParser(description="AUSTRALIS AI Benchmark Suite node agent")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--node-name", default=platform.node() or "local-node")
    parser.add_argument("--stage", choices=["pre-staging", "staging"], default="pre-staging")
    parser.add_argument("--node-type", choices=["pc-windows", "pc-linux", "cm5", "other"], default="other")
    parser.add_argument("--runtime", choices=["ollama", "llama.cpp", "openai-compatible"], default="ollama")
    parser.add_argument("--model", default="")
    parser.add_argument("--inference-endpoint", default="")
    parser.add_argument("--runtime-process-hint", default="")
    parser.add_argument("--telemetry-interval-s", type=float, default=2.0)
    parser.add_argument("--static-dir", default=str(default_static))
    parser.add_argument("--scenario-pack", default=str(default_scenarios))
    role_group = parser.add_mutually_exclusive_group()
    role_group.add_argument(
        "--telemetry-only",
        action="store_true",
        help="Expose telemetry but reject inference requests.",
    )
    role_group.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Serve the central console/scenarios/exports without node telemetry or inference.",
    )
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser


def self_test(args: argparse.Namespace) -> int:
    state = AgentState(args)
    status = state.status()
    bundle = build_export_bundle(
        {
            "manifest": {"session_id": "self-test", "agent_version": AGENT_VERSION},
            "results": [{"run_id": "self-test", "scoring": {"pass": True, "score": 100}}],
            "telemetry": [status["telemetry"]],
            "config": {"api_key": "should-redact"},
            "prompts": [{"name": "self-test", "content": "Say JSON only."}],
            "responses": [{"name": "self-test", "raw": {"ok": True}}],
            "events": [{"run_id": "self-test", "type": "scoring_complete", "timestamp_utc": utc_now()}],
        }
    )
    with zipfile.ZipFile(io.BytesIO(bundle), "r") as zf:
        bundle_files = sorted(zf.namelist())
        config = json.loads(zf.read("config.sanitized.json"))
    print(
        json.dumps(
            {
                "ok": True,
                "status_ok": status["ok"],
                "role": state.role,
                "capabilities": state.capabilities(),
                "bundle_bytes": len(bundle),
                "bundle_files": bundle_files,
                "redaction_ok": config.get("api_key") == "<redacted>",
            },
            indent=2,
        )
    )
    return 0


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test(args)

    state = AgentState(args)
    server = ThreadingHTTPServer((args.host, args.port), BenchmarkAgentHandler)
    server.state = state  # type: ignore[attr-defined]
    print(f"AUSTRALIS benchmark agent {AGENT_VERSION} listening on http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping agent.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
