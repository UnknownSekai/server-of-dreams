"""Generate a self-signed TLS cert + key for the realtime StreamingHub, no openssl needed.

    python -m scripts.generate_realtime_cert                 # host from config -> configured paths
    python -m scripts.generate_realtime_cert --host lb-realtime.wds-stellarium.com
    python -m scripts.generate_realtime_cert --force         # overwrite existing files

Equivalent to the openssl recipe in realtime/README.md (rsa:4096, sha256, self-signed, 365
days, SAN = the realtime host + localhost + 127.0.0.1) but built with the ``cryptography``
package, whose wheel bundles its own OpenSSL -- so no system ``openssl`` binary is required.

The realtime cert must be one the client trusts; see realtime/README.md and realtime_main.py.
"""

import argparse
import ipaddress
import ssl
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.yml"

DEFAULT_CERT = "certs/realtime-cert.pem"
DEFAULT_KEY = "certs/realtime-key.pem"


def _load_config() -> dict:
    if not CONFIG.is_file():
        return {}
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _host_from_url(url: str) -> str:
    # multi_real_time_server_url looks like https://lb-realtime.wds-stellarium.com[:port]
    netloc = urlparse(url).netloc or url
    return netloc.rsplit("@", 1)[-1].split(":", 1)[0].strip()


def _resolve(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else ROOT / p


def _build_sans(host: str) -> list[x509.GeneralName]:
    loopback = x509.IPAddress(ipaddress.ip_address("127.0.0.1"))
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        # a hostname: carry it as DNS, plus localhost + loopback for local tests
        sans: list[x509.GeneralName] = [x509.DNSName(host)]
        if host != "localhost":
            sans.append(x509.DNSName("localhost"))
        sans.append(loopback)
        return sans
    # a literal IP: SAN must carry it as an IPAddress, not a DNSName
    sans = [x509.IPAddress(ip), x509.DNSName("localhost")]
    if ip != ipaddress.ip_address("127.0.0.1"):
        sans.append(loopback)
    return sans


def generate(host: str, cert_path: Path, key_path: Path, days: int) -> None:
    key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    pub = key.public_key()
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, host)])
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(pub)
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(hours=1))  # small backdate tolerates device clock skew
        .not_valid_after(now + timedelta(days=days))
        .add_extension(x509.SubjectAlternativeName(_build_sans(host)), critical=False)
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(pub), critical=False)
        .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(pub), critical=False)
        .sign(key, hashes.SHA256())
    )

    cert_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    try:
        key_path.chmod(0o600)
    except OSError:
        pass
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


def main() -> None:
    cfg = _load_config()
    rt = cfg.get("realtime") or {}
    parser = argparse.ArgumentParser(
        description="generate a self-signed realtime TLS cert + key (no openssl needed)"
    )
    parser.add_argument(
        "--host",
        default=None,
        help="cert CN/SAN hostname (default: host of multi_real_time_server_url in config.yml)",
    )
    parser.add_argument(
        "--cert",
        default=rt.get("certfile") or DEFAULT_CERT,
        help="output cert path (default: realtime.certfile, else certs/realtime-cert.pem)",
    )
    parser.add_argument(
        "--key",
        default=rt.get("keyfile") or DEFAULT_KEY,
        help="output key path (default: realtime.keyfile, else certs/realtime-key.pem)",
    )
    parser.add_argument("--days", type=int, default=365, help="validity in days (default 365)")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()

    host = args.host or _host_from_url(cfg.get("multi_real_time_server_url", ""))
    if not host:
        sys.exit("no host: pass --host or set multi_real_time_server_url in config.yml")

    cert_path = _resolve(args.cert)
    key_path = _resolve(args.key)
    if (cert_path.exists() or key_path.exists()) and not args.force:
        sys.exit(
            f"refusing to overwrite existing {cert_path}/{key_path}; pass --force to replace"
        )

    generate(host, cert_path, key_path, args.days)

    # sanity: load the pair exactly as realtime/transport.py will, so a bad cert fails here
    # rather than at first client connect
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(str(cert_path), str(key_path))
    ctx.set_alpn_protocols(["h2"])

    print(f"wrote {cert_path}")
    print(f"wrote {key_path}")
    print(f"  CN / primary SAN : {host}")
    print("  SAN              : "
          + ", ".join(f"{'IP' if _is_ip(g) else 'DNS'}:{_san_value(g)}" for g in _build_sans(host)))
    print(f"  valid            : {args.days} days, RSA-4096, SHA-256, self-signed")
    print("point realtime.certfile/keyfile in config.yml at these paths (relative to server CWD).")


def _is_ip(g: x509.GeneralName) -> bool:
    return isinstance(g, x509.IPAddress)


def _san_value(g: x509.GeneralName) -> str:
    return str(g.value)


main()
