#text highlighting module is imported
#works only on nix systems
from colorama import Fore, Style
#module for parsing page content
from bs4 import BeautifulSoup
#module for receiving responses from the server
import requests
#random module
import random
import time

#text highlighting functions

def txt_grn(text):
    return Fore.GREEN + text + Style.RESET_ALL

def txt_rd(text):
    return Fore.RED + text + Style.RESET_ALL

def txt_yel(text):
    return Fore.YELLOW + text + Style.RESET_ALL

# main function that runs at the end
def main():
    #read the file with keywords and remember it as file
    with open("input.txt") as file:
        #split and read line by line
        words = [word.strip() for word in file.readlines()]
    #read the file with the second set of words shop \\ market
    with open("wordsbad.txt") as f:
        wordsbad = [wordsbad.strip() for wordsbad in f.readlines()]
    #domain zone can be changed    
    root = [".jp"]

    #counters for displaying information about found and passed
    found = 0
    not_found = 0
    exist = 0
    all_site = 0

    print("----- search site -----")
    #Endless loop to stop the program you need to press Ctrl+C \ Ctrl+D
    while True:
        try:
            url = ""
            domain = ""
            #open the file to record the result
            file = open("find-sites.txt", "a+", encoding="utf-8")
            #random selection True or False
            sep = random.choice([True, True, False])
            #random \ random choice of words
            word1 = random.choice(words)
            word2 = random.choice(wordsbad)
            #if you select True - searches only for the word
            if sep:
                domain = f"{word1}"
            #if you select False - searches for a combined word with a second word separated by a dash
            else:
                domain = f"{word1}-{word2}"

            for i in range(len(root)):
                #substitutes http:// + words + domain zone
                url = "http://" + domain + root[i]
                #check to see if this domain has been used before
                
                try:
                    #sending a request
                    r = requests.get(url)
                    #parse the page
                    soup = BeautifulSoup(r.content, "html.parser")
                    #rip out the title
                    title = soup.title.string
                    #checking if the site is live
                    if r.status_code in [200, 302, 304]:
                        file.write('{} - {}\n'.format(url, title))
                        found += 1
                        all_site += 1
                        print(f' [{all_site}]: {txt_grn(f"found {url}!")}')
                    #checking that he is not alive
                    elif r.status_code in [502, 404, 403]:
                        not_found += 1
                        all_site += 1
                        print(f' [{all_site}]: {url} {txt_yel("not found or not available!")}')
                #avoid various connection errors
                except Exception as e:
                    print(e)
                    exist += 1
                    all_site += 1
                    print(f" [{all_site}]: {url}  {txt_rd('site not exist!')}")
                #close the result recording file and sleep for half a second
                finally:
                    file.close()
                    time.sleep(0.5)
        #output the result of closing with Ctrl+C keys
        except KeyboardInterrupt:
            print("\n----- search statistics -----")
            print(f"all/found/not/exist = {all_site}/{found}/{not_found}/{exist}")
            break
#launching the main function is necessary to take over the function in other scripts;
#if this file is launched as the main one, it works
#if you adopt a function into another script, it will only run when called in that script
if __name__ == "__main__":
    main()
