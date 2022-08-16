from follow_bot import spotify
import threading, os, time, urllib, colorama
colorama.init(convert=True)

lock = threading.Lock()
counter = 0
errorcounter = 0
proxyfilelines = 0
proxies = []
proxy_counter = 0
spotify_profile = str(input("Spotify User Link: "))
threads = int(input("\nThreads: "))

def load_proxies():
    global proxyfilelines
    if not os.path.exists("proxies.txt"):
        print(colorama.Fore.YELLOW + "\nFile proxies.txt not found")
        time.sleep(5)
        os._exit(0)
    with open("proxies.txt", "r", encoding = "UTF-8") as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            proxyfilelines = len(proxies)
            proxyfilelines += 1
            proxies.append(line)            
        if not len(proxies):
            print(colorama.Fore.YELLOW + "\nNo proxies loaded in proxies.txt")
            time.sleep(5)
            os._exit(0)


def getfreeproxy():
    # HTTP Proxies
    urllib.request.urlretrieve("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all", "proxies.txt")
    # Socks4 Proxies
    with urllib.request.urlopen("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all&ssl=all&anonymity=all") as response:
        socks4data = response.read().decode("utf-8")
        with open("proxies.txt", "a+") as fp: fp.write(str(socks4data))
    # Socks5 Proxies
    with urllib.request.urlopen("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all") as response:
        socks5data = response.read().decode("utf-8")
        with open("proxies.txt", "a+") as fp : fp.write(str(socks5data))
    # Remove Blank Lines    
    with open("proxies.txt", "a+", encoding = "UTF-8") as f:
        for line in f:
            if not line.isspace():  
                f.write(line)




print("\n[1] Proxies(Recommended)\n[2] Get Free Proxies(Maybe you get bad proxies)\n[3] Proxyless(Not Recommended)")
proxyinput = int(input("\n> "))
os.system("cls")
if proxyinput == 2:
    getfreeproxy()
    time.sleep(1)
    load_proxies()

if proxyinput == 1:
    load_proxies()

def safe_print(arg):
    lock.acquire()
    print(arg)
    lock.release()

def count():
        os.system(f'title Followed = {counter} / Error = {errorcounter} / TotalProxy = {proxyfilelines}')

def thread_starter():
    global counter, errorcounter
    if proxyinput == 1:
        obj = spotify(spotify_profile, proxies[proxy_counter])
    if proxyinput == 2:
        obj = spotify(spotify_profile, proxies[proxy_counter])
    else:
        obj = spotify(spotify_profile)
    result, error = obj.follow()
    if result == True:
        counter += 1
        safe_print(colorama.Fore.GREEN + "Followed {}".format(counter))
        count()
    else:
        errorcounter += 1
        safe_print(colorama.Fore.RED + f"Error {error}")
        count()

while True:
    if threading.active_count() <= threads:
        try:
            threading.Thread(target = thread_starter).start()
            proxy_counter += 1
        except:
            pass
        if len(proxies) <= proxy_counter: #Loops through proxy file
            proxy_counter = 0
