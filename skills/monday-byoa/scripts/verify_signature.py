#!/usr/bin/env python3
"""Verify a Monday.com BYOA webhook signature.

Usage:
  MONDAY_AGENT_SIGNING_SECRET=... python3 verify_signature.py \
      --timestamp <x-monday-timestamp> --signature <x-monday-signature> \
      --raw-body-file body.json

Computes HMAC-SHA256 over "${timestamp}.${rawBody}" with the signing secret,
prefixes the hex digest with "sha256=", and constant-time compares against the
received signature. Exits 0 on match, 1 on mismatch.

Note: Gumloop webhook triggers currently forward only the POST body, not the
HTTP headers, so this cannot run inside the agent at trigger time. Use it for
offline testing, or if headers ever become available.
"""
import argparse
import hashlib
import hmac
import os
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--timestamp", required=True)
    p.add_argument("--signature", required=True)
    p.add_argument("--raw-body-file", required=True)
    args = p.parse_args()

    secret = os.environ.get("MONDAY_AGENT_SIGNING_SECRET")
    if not secret:
        sys.exit("MONDAY_AGENT_SIGNING_SECRET is not set.")

    with open(args.raw_body_file, "rb") as f:
        raw_body = f.read()

    signed = args.timestamp.encode() + b"." + raw_body
    expected = "sha256=" + hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected, args.signature):
        print("signature valid")
        sys.exit(0)
    print("signature INVALID")
    sys.exit(1)


if __name__ == "__main__":
    main()
