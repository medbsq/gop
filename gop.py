import optparse
import requests
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
import threading
import time


queue = Queue()
def done( stop_event,output):
    while not stop_event.is_set():
        data = queue.get()
        with open(output, "a") as file:
            for ip in data:
                file.write(f"{ip}\n")
                print(ip)
def get_open_port(file,output):
    ips = [i.replace("\n","") for i in open(file,"r").readlines()]
    stop_event = threading.Event()
    t = threading.Thread(target=done, args=(stop_event,output), daemon=True)
    t.start()
    features = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        for ip in ips:
            features.append(executor.submit(ip_open_port, ip, ))
        wait(features)
    time.sleep(4)
def ip_open_port(ip):
    try:
        ip = ip.replace(' ','')
        response = requests.get(f"https://internetdb.shodan.io/{ip}")
        ips = [f"{ip}:{port}" for port in response.json()['ports']]
        queue.put(ips)
    except:
       pass


def Main():
    parser = optparse.OptionParser(" help: \n\tchaos_bbp.py -f <ips file> -o <output> \n")
    parser.add_option("-f", dest="ips_file", type="string", default=None, help="spicify ips_file")
    parser.add_option("-o", dest="output", type="string", default="open_ports.txt", help="spicify output file")
    parser.add_option("-i", dest="ip", type="string", default=None, help="spicify ip")
    (options, args) = parser.parse_args()

    if (options.ips_file != None):
        get_open_port(options.ips_file,options.output)
    elif (options.ip != None):
        ip_open_port(options.ip)

    else:
        print(parser.usage)
        exit(1)


if __name__ == '__main__':
    Main()
