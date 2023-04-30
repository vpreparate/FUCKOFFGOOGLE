from colorama import Fore, Style
from bs4 import BeautifulSoup
import webbrowser
import argparse
import requests
import datetime
import random
import time




def txt_grn(text):
    return Fore.GREEN + text + Style.RESET_ALL


def txt_rd(text):
    return Fore.RED + text + Style.RESET_ALL


def txt_yel(text):
    return Fore.YELLOW + text + Style.RESET_ALL


def open_url(url, bool_url):
    if bool_url:
        webbrowser.open(url)


def now():
    dt_obj = datetime.datetime.now()
    return dt_obj.strftime("%b %d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="search site")
    parser.add_argument("-m", "--max",
                        type=int,
                        dest="max",
                        default=10,
                        help="maximum length website domain generation")
    parser.add_argument("-b", "--bigchar",
                        action="store_true",
                        dest="bigchar",
                        help="add bigchar in alphabet")
    parser.add_argument("-c", "--smallchar",
                        action="store_true",
                        dest="smallchar",
                        help="add smallchar in alphabet")
    parser.add_argument("-n", "--number",
                        action="store_true",
                        dest="number",
                        help="add number in alphabet")
    parser.add_argument("-s", "--symbols",
                        action="store_true",
                        dest="symbols",
                        help="add symbols in alphabet")
    parser.add_argument("-u", "--url",
                        default=False,
                        action="store_true",
                        dest="url",
                        help="open url")
    parser.add_argument("-o", "--out",
                        default="site.txt",
                        dest="out",
                        help="out file")
    parser.add_argument("-t", "--time",
                        type=int,
                        default=10,
                        dest="time",
                        help="timeout for a request to the site")

    args = parser.parse_args()

    args_big_char = args.bigchar
    args_small_char = args.smallchar
    args_number = args.number
    args_symbols = args.symbols

    bool_url = args.url
    out = args.out

    maximus = args.max
    
    with open("input.txt") as file:
        words = [word[:-1] for word in file.readlines()]
    with open("wordsbad.txt") as f:
        wordsbad = [wordsbad[:-1] for wordsbad in f.readlines()]
    root = [".com"]
    used_url = []

    found = 0
    not_found = 0
    exist = 0
    all_site = 0

    print("----- search site -----")

    while 1:
        try:
            url = ""
            domain = ""
            length = random.randrange(1, maximus)
            file = open(out, "a+", encoding="utf-8")

            sep = random.choice([True, True, False])
            word1 = random.choice(words)
            word2 = random.choice(wordsbad)

            if sep:
                domain = f"{word1}"
            else:
                domain = f"{word1}-{word2}"

            for i in range(len(root)):
                url = "http://" + domain + root[i]

                if url not in used_url:
                    used_url.append(url)
                else:
                    continue

                try:
                    r = requests.get(url, timeout=args.time)
                    soup = BeautifulSoup(r.content, "html.parser")
                    title = soup.title.string

                    if r.status_code in [200, 302, 304]:
                        file.write('{} - {}\n'.format(url, title))
                        open_url(url, bool_url)
                        found += 1
                        all_site += 1
                        print(f'{now()} [{all_site}]: {txt_grn(f"found {url}!")}')

                    elif r.status_code in [502, 404, 403]:
                        not_found += 1
                        all_site += 1
                        print(f'{now()} [{all_site}]: {url} {txt_yel("not found or not available!")}')

                except Exception:
                    exist += 1
                    all_site += 1
                    print(f"{now()} [{all_site}]: {url}  {txt_rd('site not exist!')}")

                finally:
                    file.close()
                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n----- search statistics -----")
            print(f"all/found/not/exist = {all_site}/{found}/{not_found}/{exist}")
            break


if __name__ == "__main__":
    main()
