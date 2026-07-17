#!/usr/bin/env python3
"""Build and optionally probe ArcGIS FeatureServer/MapServer query URLs."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--service-url", required=True, help="Layer or service URL ending in FeatureServer[/layer] or MapServer[/layer].")
    parser.add_argument("--layer", default="", help="Layer id if not embedded in service URL.")
    parser.add_argument("--where", default="1=1")
    parser.add_argument("--out-fields", default="*")
    parser.add_argument("--geometry", default="")
    parser.add_argument("--geometry-type", default="esriGeometryEnvelope")
    parser.add_argument("--out-sr", default="4326")
    parser.add_argument("--result-record-count", type=int, default=10)
    parser.add_argument("--return-geometry", choices=("true", "false"), default="true")
    parser.add_argument("--format", choices=("json", "geojson"), default="json")
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    payload = build_payload(args)
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    layer_url = normalize_layer_url(args.service_url, args.layer)
    params = {
        "where": args.where,
        "outFields": args.out_fields,
        "returnGeometry": args.return_geometry,
        "outSR": args.out_sr,
        "resultRecordCount": str(max(args.result_record_count, 1)),
        "f": args.format,
    }
    if args.geometry:
        params["geometry"] = args.geometry
        params["geometryType"] = args.geometry_type
        params["inSR"] = args.out_sr
        params["spatialRel"] = "esriSpatialRelIntersects"
    query_url = f"{layer_url}/query?{urllib.parse.urlencode(params)}"
    metadata_url = f"{layer_url}?f=pjson"
    payload: dict[str, Any] = {
        "source_skill_id": "arcgis-platform",
        "metadata_url": metadata_url,
        "api_url": query_url,
        "direct_download_url": "",
        "finality": "candidate_until_metadata_and_query_probe",
        "strict_success_rule": "A layer URL is not strict success. Return a concrete /query URL or export URL and verify JSON/GeoJSON features with no ArcGIS error payload.",
        "pagination_notes": "Use resultOffset/resultRecordCount according to maxRecordCount for full extraction.",
    }
    if args.probe:
        payload["metadata_probe"] = get_json(metadata_url)
        payload["query_probe"] = classify_query_payload(get_json(query_url))
    return payload


def normalize_layer_url(service_url: str, layer: str) -> str:
    parsed = urllib.parse.urlparse(service_url)
    parts = [part for part in parsed.path.rstrip("/").split("/") if part]
    if not parts or parts[-1] not in {"FeatureServer", "MapServer"} and not parts[-1].isdigit():
        raise SystemExit("service-url must point to FeatureServer/MapServer or a numeric layer")
    if parts[-1].isdigit():
        return service_url.rstrip("/")
    if not layer:
        raise SystemExit("--layer is required when service-url does not include a numeric layer id")
    return f"{service_url.rstrip('/')}/{layer}"


def get_json(url: str) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return {"ok": True, "http_status": response.status, "json": json.loads(response.read().decode("utf-8", "replace"))}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "http_status": None, "error": str(exc)}


def classify_query_payload(probe: dict[str, Any]) -> dict[str, Any]:
    payload = probe.get("json")
    if not probe.get("ok") or not isinstance(payload, dict):
        return {"ok": False, "reason": "query_probe_failed", "probe": probe}
    if isinstance(payload.get("error"), dict):
        return {"ok": False, "reason": "arcgis_error_payload", "error": payload["error"]}
    features = payload.get("features")
    return {
        "ok": isinstance(features, list),
        "feature_count": len(features) if isinstance(features, list) else None,
        "has_fields": isinstance(payload.get("fields"), list),
        "exceeded_transfer_limit": bool(payload.get("exceededTransferLimit")),
    }


if __name__ == "__main__":
    main()

