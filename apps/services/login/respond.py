"""Lectura de XML / JSON / formulario y serialización de respuestas."""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

from flask import Response, request

XML_ROOT = "response"


def requested_format():
    raw = (request.args.get("format") or "xml").strip().lower()
    if raw not in {"xml", "json"}:
        return None
    return raw


def parse_body():
    """Acepta JSON, XML o application/x-www-form-urlencoded."""
    ctype = (request.content_type or "").split(";")[0].strip().lower()

    if ctype in {"application/json", "text/json"}:
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}

    if ctype in {"application/xml", "text/xml"}:
        return _xml_to_dict(request.data)

    if request.form:
        return {k: v for k, v in request.form.items()}

    raw = request.get_data(cache=True) or b""
    if not raw:
        return {}

    stripped = raw.lstrip()
    if stripped.startswith(b"{") or stripped.startswith(b"["):
        try:
            data = json.loads(raw.decode("utf-8"))
            return data if isinstance(data, dict) else {}
        except (ValueError, UnicodeDecodeError):
            return {}
    if stripped.startswith(b"<"):
        return _xml_to_dict(raw)
    return {}


def _xml_to_dict(raw):
    if not raw:
        return {}
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return {}
    data = {}
    for child in root.iter():
        if child is root:
            continue
        if child.text and child.text.strip() and child.tag not in data:
            data[child.tag] = child.text.strip()
    return data


def public_user(row):
    if not row:
        return None
    return {
        "id_usuario": row["id_usuario"],
        "nombre": row["nombre"],
        "apellido_paterno": row["apellido_paterno"],
        "apellido_materno": row["apellido_materno"],
        "email": row["email"],
        "es_administrador": bool(row["es_administrador"]),
    }


def send(payload, status=200, fmt="xml"):
    if fmt == "json":
        return Response(
            json.dumps(payload, ensure_ascii=False, default=str),
            status=status,
            mimetype="application/json; charset=utf-8",
        )
    xml_bytes = _dict_to_xml(payload)
    return Response(xml_bytes, status=status, mimetype="application/xml; charset=utf-8")


def _dict_to_xml(payload):
    root = ET.Element(XML_ROOT)
    _append(root, payload)
    rough = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(rough)
    pretty = parsed.toprettyxml(indent="  ", encoding="utf-8")
    return pretty


def _append(parent, value):
    if isinstance(value, dict):
        for key, item in value.items():
            child = ET.SubElement(parent, _safe_tag(key))
            _append(child, item)
        return
    if isinstance(value, list):
        for item in value:
            child = ET.SubElement(parent, "item")
            _append(child, item)
        return
    if value is None:
        parent.text = ""
        return
    if isinstance(value, bool):
        parent.text = "true" if value else "false"
        return
    parent.text = str(value)


def _safe_tag(name):
    tag = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in str(name))
    if not tag or tag[0].isdigit():
        tag = f"field_{tag}"
    return tag
