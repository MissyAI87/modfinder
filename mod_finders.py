# === Mod Finder Script ===
# Author: [Your Name Here]
# Description:
#   - CLI tool to find Sims 4 mod download links based on keyword search.
#   - Simulates scraping results from major search engines.
#   - Filters links using known trusted mod-hosting domains and verifies download type.
#   - Saves results to JSON.

# --- Imports ---
import sys
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

# --- Config: Trusted Domains ---
KNOWN_MOD_DOMAINS = [
    "patreon.com",
    "thesimsresource.com",
    "tumblr.com",
    "snootysims.com",
    "modthesims.info",
    "curseforge.com",
    "simfileshare.net",
    "nexusmods.com"
]

# --- Config: Output Path ---
results_path = os.path.expanduser("~/Documents/Mod Manager/modfinder_results.json")
if os.path.exists(results_path):
    os.remove(results_path)

# --- Function: is_probable_download(url) ---
# Checks if the given URL likely leads to a downloadable mod file
def is_probable_download(url):
    try:
        head = requests.head(url, timeout=5, allow_redirects=True)
        content_type = head.headers.get("Content-Type", "").lower()
        return any(x in content_type for x in ["zip", "octet-stream", "package", "rar"])
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

# --- Function: scrape_mod_links(keywords) ---
# For each keyword, perform simulated scraping from search engines and filter results
def scrape_mod_links(keywords):
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    search_engines = [
        ("https://www.google.com/search?q=sims+4+{}+mod", "Google"),
        ("https://duckduckgo.com/html?q=sims+4+{}+mod", "DuckDuckGo")
    ]

    for keyword in keywords:
        for engine_url, engine_name in search_engines:
            query = engine_url.format(keyword.replace(" ", "+"))
            try:
                print(f"Searching {engine_name} for '{keyword}'...")
                response = requests.get(query, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a", href=True)

                for link in links:
                    url = unquote(link['href'])
                    if "/url?q=" in url:
                        url = url.split("/url?q=")[-1].split("&")[0]
                    if not url.startswith("http"):
                        continue
                    if any(domain in url for domain in KNOWN_MOD_DOMAINS):
                        try:
                            # Visit the result URL to look for download links inside the page
                            sub_response = requests.get(url, headers=headers, timeout=10)
                            sub_soup = BeautifulSoup(sub_response.text, "html.parser")
                            sub_links = sub_soup.find_all("a", href=True)
                            for sub_link in sub_links:
                                sub_url = unquote(sub_link['href'])
                                if not sub_url.startswith("http"):
                                    continue
                                if any(domain in sub_url for domain in KNOWN_MOD_DOMAINS):
                                    if any(result["url"] == sub_url for result in results):
                                        continue
                                    if keyword.lower() not in sub_url.lower():
                                        continue
                                    if not is_probable_download(sub_url):
                                        continue
                                    results.append({
                                        "keyword": keyword,
                                        "url": sub_url,
                                        "source": f"{engine_name} > {url}"
                                    })
                        except Exception as e:
                            print(f"Error scraping secondary links from {url}: {e}")
                        if keyword.lower() not in url.lower():
                            continue
                        if any(result["url"] == url for result in results):
                            continue
                        if not is_probable_download(url):
                            continue
                        results.append({
                            "keyword": keyword,
                            "url": url,
                            "source": engine_name
                        })
            except Exception as e:
                print(f"Error during {engine_name} search for '{keyword}': {e}")
    
    if not results:
        print("No results found for the given keywords.")
    else:
        print("Finished searching and found results.")
    return results

# --- Function: save_results(results) ---
# Saves the list of results to a JSON file in the Mod Manager directory
def save_results(results):
    if not results:
        print("No results to save. Skipping write.")
        return
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"Results written to {results_path}")

# --- CLI Entrypoint ---
def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if "--keywords" in args:
        index = args.index("--keywords")
        keywords = args[index + 1:]
    else:
        print("No keywords provided.")
        return

    keywords = [kw.strip() for kw in keywords if kw.strip()]
    if not keywords:
        print("No keywords found after --keywords.")
        return

    print(f"Searching for keywords: {keywords}")
    results = scrape_mod_links(keywords)
    save_results(results)

# --- Run Script ---
if __name__ == "__main__":
    main()
