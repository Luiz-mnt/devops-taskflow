"""Métricas por rota normalizada e logs HTTP sem payload, query ou credenciais."""

import json
from datetime import UTC, datetime
from time import perf_counter

from prometheus_client import CollectorRegistry, Counter, Histogram
from starlette.types import ASGIApp, Message, Receive, Scope, Send

HTTP_METHODS = frozenset({"GET", "POST", "PATCH", "PUT", "DELETE", "HEAD", "OPTIONS"})


class HttpMetrics:
    def __init__(self) -> None:
        # Uma registry por app evita compartilhar estado entre instâncias/testes.
        self.registry = CollectorRegistry()
        self.requests = Counter(
            "taskflow_http_requests_total",
            "Total de requisições HTTP por método, rota normalizada e status.",
            ("method", "route", "status_code"),
            registry=self.registry,
        )
        self.duration = Histogram(
            "taskflow_http_request_duration_seconds",
            "Duração das requisições HTTP em segundos.",
            ("method", "route"),
            registry=self.registry,
        )


class ObservabilityMiddleware:
    def __init__(self, app: ASGIApp, metrics: HttpMetrics) -> None:
        self.app = app
        self.metrics = metrics

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope["method"] if scope["method"] in HTTP_METHODS else "OTHER"
        started = perf_counter()
        status_code = 500

        async def observe_response(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, observe_response)
        finally:
            elapsed = max(perf_counter() - started, 0)
            matched_route = scope.get("route")
            route = getattr(matched_route, "path", "unmatched")
            self.metrics.requests.labels(method, route, str(status_code)).inc()
            self.metrics.duration.labels(method, route).observe(elapsed)
            # O caminho bruto, IDs, query string, headers e corpo não são logados.
            print(
                json.dumps(
                    {
                        "timestamp": datetime.now(UTC).isoformat(),
                        "event": "http_request",
                        "method": method,
                        "route": route,
                        "status_code": status_code,
                        "duration_seconds": round(elapsed, 6),
                    },
                    ensure_ascii=True,
                    separators=(",", ":"),
                ),
                flush=True,
            )
