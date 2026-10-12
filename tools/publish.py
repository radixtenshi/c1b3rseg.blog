#!/usr/bin/env python3
"""
Publica notas en Blogger (c1b3rseg.blogspot.com) via Blogger API v3.

Uso:
  python tools/publish.py auth                       # autorizar con Google (una vez)
  python tools/publish.py list                       # listar posts recientes
  python tools/publish.py post posts/mi-nota.md      # crear como BORRADOR
  python tools/publish.py post posts/mi-nota.md --publicar
  python tools/publish.py publish <post-id>          # pasar un borrador a publicado
  python tools/publish.py update <post-id> posts/mi-nota.md [--publicar]
  python tools/publish.py delete <post-id>

Las imagenes/archivos de las notas se suben al repo (assets/) y el script
reescribe las rutas relativas a URLs de GitHub raw. Subi y pushea los assets
ANTES de publicar la nota.
"""
import argparse
import json
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import markdown
import requests

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
CLIENT_SECRET = TOOLS / "client_secret.json"
TOKEN_FILE = TOOLS / ".blogger_token.json"
CONFIG_FILE = TOOLS / ".blog_config.json"

BLOG_URL = "https://c1b3rseg.blogspot.com/"
SCOPE = "https://www.googleapis.com/auth/blogger"
REDIRECT_PORT = 8551
RAW_BASE = "https://raw.githubusercontent.com/radixtenshi/c1b3rseg.blog/main/"
MD_EXTENSIONS = ["fenced_code", "tables", "sane_lists", "smarty"]


# ---------------------------------------------------------------- credenciales

def _load_client_secret() -> dict:
    if not CLIENT_SECRET.exists():
        sys.exit(
            f"Falta {CLIENT_SECRET}\n"
            "Descarga el JSON de OAuth (Desktop app) desde Google Cloud Console\n"
            "y guardalo con ese nombre. Guia: tools/README.md"
        )
    data = json.loads(CLIENT_SECRET.read_text(encoding="utf-8"))
    if "installed" in data:
        data = data["installed"]
    elif "web" in data:
        data = data["web"]
    return data


def _save_token(token: dict) -> None:
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding="utf-8")


def _load_token() -> dict:
    if not TOKEN_FILE.exists():
        sys.exit(f"Falta {TOKEN_FILE}. Corre primero: python tools/publish.py auth")
    return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))


def _access_token() -> str:
    """Devuelve un access_token vigente, refrescando si hace falta."""
    token = _load_token()

    if token.get("expires_at", 0) - time.time() < 60:
        cs = _load_client_secret()
        r = requests.post(
            cs.get("token_uri", "https://oauth2.googleapis.com/token"),
            data={
                "client_id": cs["client_id"],
                "client_secret": cs["client_secret"],
                "refresh_token": token["refresh_token"],
                "grant_type": "refresh_token",
            },
            timeout=30,
        )
        if r.status_code != 200:
            sys.exit(f"Error refrescando el token ({r.status_code}): {r.text}\nVolve a correr: python tools/publish.py auth")
        token["access_token"] = r.json()["access_token"]
        token["expires_at"] = time.time() + r.json().get("expires_in", 3500)
        _save_token(token)
    return token["access_token"]


def auth() -> None:
    """Flujo OAuth de Google con redirect en localhost (tipo Desktop app)."""
    cs = _load_client_secret()
    redirect_uri = f"http://localhost:{REDIRECT_PORT}/"
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(
        {
            "client_id": cs["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent",
        }
    )

    captured = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            q = parse_qs(urlparse(self.path).query)
            captured["code"] = q.get("code", [None])[0]
            captured["error"] = q.get("error", [None])[0]
            ok = captured["code"] and not captured["error"]
            msg = (
                "Autorizacion recibida. Ya podes cerrar esta pestana."
                if ok
                else f"No llego el codigo: {captured['error']}"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h3>{msg}</h3>".encode())

        def log_message(self, *args):
            pass

    srv = HTTPServer(("127.0.0.1", REDIRECT_PORT), Handler)
    print("1) Abrí esta URL en tu navegador y aceptá los permisos:\n")
    print(url + "\n")
    print(f"2) Esperando autorización (localhost:{REDIRECT_PORT})...")
    while not captured:
        srv.handle_request()
    srv.server_close()

    if not captured.get("code"):
        sys.exit(f"Authorization denegada: {captured.get('error')}")

    r = requests.post(
        cs.get("token_uri", "https://oauth2.googleapis.com/token"),
        data={
            "client_id": cs["client_id"],
            "client_secret": cs["client_secret"],
            "code": captured["code"],
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        timeout=30,
    )
    if r.status_code != 200:
        sys.exit(f"Error intercambiando el codigo ({r.status_code}): {r.text}")
    data = r.json()
    _save_token(
        {
            "access_token": data["access_token"],
            "refresh_token": data.get("refresh_token", ""),
            "expires_at": time.time() + data.get("expires_in", 3500),
        }
    )
    print("OK. Token guardado en tools/.blogger_token.json")
    print("Ya podés publicar: python tools/publish.py post posts/mi-nota.md")


# ---------------------------------------------------------------- API Blogger

def _api(method: str, path: str, **kwargs) -> requests.Response:
    r = requests.request(
        method,
        f"https://www.googleapis.com/blogger/v3{path}",
        headers={"Authorization": f"Bearer {_access_token()}"},
        timeout=60,
        **kwargs,
    )
    if r.status_code == 401:
        sys.exit("Token invalido/expirado. Corre de nuevo: python tools/publish.py auth")
    return r


def blog_id() -> str:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))["blog_id"]
    r = _api("GET", "/blogs/byurl", params={"url": BLOG_URL})
    if r.status_code != 200:
        sys.exit(f"No pude resolver el blog ID ({r.status_code}): {r.text}")
    bid = str(r.json()["id"])
    CONFIG_FILE.write_text(json.dumps({"blog_id": bid, "url": BLOG_URL}, indent=2), encoding="utf-8")
    return bid


def list_posts() -> None:
    r = _api("GET", f"/blogs/{blog_id()}/posts", params={"max-results": 20, "status": "draft"})
    r2 = _api("GET", f"/blogs/{blog_id()}/posts", params={"max-results": 20})
    posts = {}
    for p in r.json().get("items", []) + r2.json().get("items", []):
        posts[p["id"]] = p
    if not posts:
        print("No hay posts (¿blog nuevo o sin permisos?).")
        return
    for p in sorted(posts.values(), key=lambda x: x.get("published", ""), reverse=True):
        status = p.get("status", "?")
        print(f"{p['id']}  [{status:6}]  {p.get('published', '')[:10]}  {p['title']}")


# ---------------------------------------------------------------- contenido

def _parse_front_matter(text: str) -> tuple[dict, str]:
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        val = v.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        meta[k.strip().lower()] = val
    return meta, m.group(2)


def _labels(raw: str | None) -> list[str]:
    if not raw:
        return []
    raw = raw.strip().strip("[]")
    return [x.strip() for x in raw.split(",") if x.strip()]


def _build_body(md_text: str, meta: dict) -> str:
    html = markdown.markdown(md_text, extensions=MD_EXTENSIONS)
    # assets/... -> URL cruda de GitHub (requiere que el asset este en el repo)
    html = re.sub(r'(src|href)="(assets/[^"]+)"', rf'\1="{RAW_BASE}\2"', html)
    return html


def _read_post(path: str) -> dict:
    p = ROOT / path if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        sys.exit(f"No existe el archivo: {p}")
    meta, md_text = _parse_front_matter(p.read_text(encoding="utf-8"))
    title = meta.get("title")
    if not title:
        sys.exit(f"El front-matter de {p} no tiene 'title:'")
    return {
        "title": title,
        "labels": _labels(meta.get("labels")),
        "content": _build_body(md_text, meta),
    }


# ---------------------------------------------------------------- comandos

def cmd_post(path: str, publicar: bool) -> None:
    body = _read_post(path)
    r = _api(
        "POST",
        f"/blogs/{blog_id()}/posts",
        params={"isDraft": not publicar},
        json=body,
    )
    if r.status_code != 200:
        sys.exit(f"Error creando el post ({r.status_code}): {r.text}")
    p = r.json()
    estado = "PUBLICADO" if publicar else "BORRADOR"
    print(f"[{estado}] id={p['id']}")
    print(f"  {p.get('url', '')}")


def cmd_update(post_id: str, path: str, publicar: bool) -> None:
    body = _read_post(path)
    body["id"] = post_id
    if publicar:
        body["status"] = "LIVE"
    r = _api("PUT", f"/blogs/{blog_id()}/posts/{post_id}", json=body)
    if r.status_code != 200:
        sys.exit(f"Error actualizando el post ({r.status_code}): {r.text}")
    p = r.json()
    print(f"[ACTUALIZADO] id={p['id']} status={p.get('status')}")
    print(f"  {p.get('url', '')}")


def cmd_publish(post_id: str) -> None:
    r = _api("POST", f"/blogs/{blog_id()}/posts/{post_id}/publish")
    if r.status_code != 200:
        sys.exit(f"Error publicando ({r.status_code}): {r.text}")
    p = r.json()
    print(f"[PUBLICADO] id={p['id']}")
    print(f"  {p.get('url', '')}")


def cmd_delete(post_id: str) -> None:
    confirm = input(f"Borrar el post {post_id}? (escribi SI): ").strip()
    if confirm != "SI":
        print("Cancelado.")
        return
    r = _api("DELETE", f"/blogs/{blog_id()}/posts/{post_id}")
    if r.status_code != 204:
        sys.exit(f"Error borrando ({r.status_code}): {r.text}")
    print(f"[BORRADO] id={post_id}")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Publica notas en Blogger (c1b3rseg)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("auth", help="autorizar con Google (una vez)")
    sub.add_parser("list", help="listar posts recientes")

    sp = sub.add_parser("post", help="crear un post desde un archivo markdown")
    sp.add_argument("file")
    sp.add_argument("--publicar", action="store_true", help="publicar en vez de dejar borrador")

    sp = sub.add_parser("publish", help="pasar un borrador a publicado")
    sp.add_argument("post_id")

    sp = sub.add_parser("update", help="actualizar un post existente")
    sp.add_argument("post_id")
    sp.add_argument("file")
    sp.add_argument("--publicar", action="store_true")

    sp = sub.add_parser("delete", help="borrar un post")
    sp.add_argument("post_id")

    args = ap.parse_args()

    if args.cmd == "auth":
        auth()
    elif args.cmd == "list":
        list_posts()
    elif args.cmd == "post":
        cmd_post(args.file, args.publicar)
    elif args.cmd == "publish":
        cmd_publish(args.post_id)
    elif args.cmd == "update":
        cmd_update(args.post_id, args.file, args.publicar)
    elif args.cmd == "delete":
        cmd_delete(args.post_id)


if __name__ == "__main__":
    main()
