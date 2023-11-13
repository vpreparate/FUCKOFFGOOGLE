#импотируется модуль подсветки текста
#работает только в nix системах
from colorama import Fore, Style
#модуль для разбора содержимого страницы
from bs4 import BeautifulSoup
#модуль для получения ответов с сервера
import requests
#модуль случайного выбора
import random
import time

#функции подстветки текста

def txt_grn(text):
    return Fore.GREEN + text + Style.RESET_ALL

def txt_rd(text):
    return Fore.RED + text + Style.RESET_ALL

def txt_yel(text):
    return Fore.YELLOW + text + Style.RESET_ALL

# главная функция которая запускается в конце
def main():
    #читаем файл с ключевыми словами запоминаем как file
    with open("input.txt") as file:
        #режим и читаем построчно
        words = [word.strip() for word in file.readlines()]
    #читаем файл со вторым набором слов shop \\ market
    with open("wordsbad.txt") as f:
        wordsbad = [wordsbad.strip() for wordsbad in f.readlines()]
    #доменная зона можно изменить    
    root = [".jp"]

    #счётчики для вывода информации о найденых и пройденых
    found = 0
    not_found = 0
    exist = 0
    all_site = 0

    print("----- search site -----")
    #Бесконечный цикл чтобы остановить программу надо нажать Ctrl+C \ Ctrl+D
    while True:
        try:
            url = ""
            domain = ""
            #открываем файл для записи результата
            file = open("find-sites.txt", "a+", encoding="utf-8")
            #рандомный выбор True или False
            sep = random.choice([True, True, False])
            #рандомный \ случайный выбор слов
            word1 = random.choice(words)
            word2 = random.choice(wordsbad)
            #если выБирает True - ищет только слово
            if sep:
                domain = f"{word1}"
            #если выБирает False - ищет совмещённое слово с вторым через тире
            else:
                domain = f"{word1}-{word2}"

            for i in range(len(root)):
                #подставляет http:// + слова + доменную зону
                url = "http://" + domain + root[i]
                #проверка на использование этого домена ранее
                
                try:
                    #посылаем запрос
                    r = requests.get(url)
                    #парсим страницу
                    soup = BeautifulSoup(r.content, "html.parser")
                    #выдираем заголовок
                    title = soup.title.string
                    #проверяем живой ли сайт
                    if r.status_code in [200, 302, 304]:
                        file.write('{} - {}\n'.format(url, title))
                        found += 1
                        all_site += 1
                        print(f' [{all_site}]: {txt_grn(f"found {url}!")}')
                    #проверяем что не живой
                    elif r.status_code in [502, 404, 403]:
                        not_found += 1
                        all_site += 1
                        print(f' [{all_site}]: {url} {txt_yel("not found or not available!")}')
                #исключение разных ошибок соединения
                except Exception as e:
                    print(e)
                    exist += 1
                    all_site += 1
                    print(f" [{all_site}]: {url}  {txt_rd('site not exist!')}")
                #закрываем файл записи результата и спим пол секунды
                finally:
                    file.close()
                    time.sleep(0.5)
        #вывод результата по закрытию клавишами Ctrl+C
        except KeyboardInterrupt:
            print("\n----- search statistics -----")
            print(f"all/found/not/exist = {all_site}/{found}/{not_found}/{exist}")
            break
#запуск главной функции нужно для перенимания функции в другие скрипты если запущен этот файл как главный - работает
#если Вы перенимаете функцию в другой скрипт то запустится только при вызове в том скрипте
if __name__ == "__main__":
    main()
