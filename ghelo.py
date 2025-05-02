import requests

ascii_art = r"""
  ________  __    __   _______  __        ______   
 /  _____/ |  |  |  | |   ____||  |      /  __  \  
|  |  __   |  |__|  | |  |__   |  |     |  |  |  | 
|  | |_ |  |   __   | |   __|  |  |     |  |  |  | 
|  |__| |  |  |  |  | |  |____ |  `----.|  `--'  | 
 \______|  |__|  |__| |_______||_______| \______/  

        GHELO - Local File Inclusion Fuzzer
                By: @hhkolberg
---------------------------------------------------
"""

def main():
    print(ascii_art)

    # 1. Ask for URL with FUZZ placeholder
    url = input("[+] Enter target URL (use FUZZ where payload goes): ").strip()
    if "FUZZ" not in url:
        print("[-] You must include 'FUZZ' in the URL.")
        return

    # 2. Wordlist
    wordlist_path = input("[+] Enter path to wordlist (e.g. lfi.txt): ").strip()
    try:
        with open(wordlist_path, "r") as f:
            payloads = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Failed to load wordlist: {e}")
        return

    # 3. Filter INCLUDES (search in response)
    includes = input("[+] Enter filter keywords to match in response (comma-separated, or leave empty): ").split(",")
    includes = [i.strip() for i in includes if i.strip()]

    # 4. Status codes to IGNORE
    ignores = input("[+] Enter status codes to ignore (comma-separated, or leave empty): ").split(",")
    ignores = [int(code.strip()) for code in ignores if code.strip().isdigit()]

    print("\n🚀 Starting LFI fuzzing...\n")

    baseline_len = None
    baseline_body = ""

    for i, payload in enumerate(payloads):
        test_url = url.replace("FUZZ", payload)
        try:
            r = requests.get(test_url, timeout=5)
            code = r.status_code
            content = r.text
            content_len = len(content)

            # Set the first response as baseline
            if i == 0:
                baseline_len = content_len
                baseline_body = content
                print(f"[~] Baseline response length: {baseline_len}")

            # Skip ignored status codes
            if code in ignores:
                continue

            # Check keyword hits
            keyword_hit = False
            for keyword in includes:
                if keyword.lower() in content.lower():
                    keyword_hit = True
                    break

            # Compare content length vs baseline
            length_differs = content_len != baseline_len

            if keyword_hit or length_differs:
                reason = []
                if keyword_hit:
                    reason.append("Keyword Match")
                if length_differs:
                    reason.append(f"Length Diff (Got {content_len}, Baseline {baseline_len})")

                print(f"[+] HIT [{code}] Payload: {payload} => {' | '.join(reason)}")
        except Exception as e:
            print(f"[-] Request failed for {payload}: {e}")

if __name__ == "__main__":
    main()
