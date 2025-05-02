# 🏔️ GHELO - Local File Inclusion Fuzzer

**GHELO** is a fast, customizable, and Norse-inspired **Local File Inclusion (LFI) fuzzing tool** written in Python. Designed for penetration testers, CTF enthusiasts, and red teamers, it allows you to quickly identify vulnerable file inclusion points in web applications with flexible filtering and targeting options.

---

## Why GHELO?

Sometimes, if you lack intelligence on how to use tools without errors. It may be better to code your own. Traditional fuzzers like FFUF and wfuzz sometimes fall short — especially when:

- You need custom logic (e.g., content-based response filtering)
- Responses must be analyzed by keyword or length, not just status code
- If you are as unintelligent as I am. 

**GHELO** is born out of this gap — a no-BS tool focused on **precise, flexible LFI fuzzing**, with a Nordic war-beast theme! 

---

## 🧩 Features

- ✅ **Interactive setup** (target, wordlist, filters)
- ✅ **Keyword filtering** (e.g., `root:x`, `/bin/bash`)
- ✅ **Status code exclusion** (e.g., skip 302/403)
- ✅ **Simple and hackable Python3 code**
- ✅ **ASCII art for morale boost**
- ⚙️ Easily extendable for POST, headers, cookies

---

## 🖥️ Demo Screenshot

## Usage

When prompted:

Enter the target URL, using FUZZ as the placeholder for payloads

`http://target.com/page.php?file=FUZZ`

Eins. Provide the path to your LFI payload list
Zwei. Add filter keywords to find hits in the response (e.g., root:x)
Drei. Exclude HTTP status codes you want to ignore (e.g., 302, 404)

