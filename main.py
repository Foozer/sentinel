import speedtest
import datetime
import netifaces
import os
from elasticsearch import Elasticsearch
import time

def get_mac_address(interface_name):
    # Get the addresses associated with the interface
    addrs = netifaces.ifaddresses(interface_name)
    # Get the link layer addresses (AF_LINK on Unix)
    try:
        if netifaces.AF_LINK in addrs:
            # Extract the MAC address
            mac_address = addrs[netifaces.AF_LINK][0]['addr']
            return mac_address
    except KeyError:
        # The specified interface might not exist or have a MAC address
        return None

def add_results_to_elasticsearch(results):
    # take results and add them to elasticsearch
    username = 'elastic'
    password = os.getenv('ELASTIC_PASSWORD') # Value you set in the environment variable
    client = Elasticsearch("http://localhost:9200",
                           basic_auth=(username, password)
                           )
    #add mac address to results
    results['mac_address'] = get_mac_address('wlp64s0')
    #add results to elasticsearch
    client.index(index='speedtest_results', body=results)


    


def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    results = st.results.dict()
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results['timestamp'] = timestamp

    add_results_to_elasticsearch(results)


    
    
    with open('speedtest_results.csv', 'a') as f:
        f.write(f"{results['timestamp']},{results['download']},{results['upload']},{results['ping']},{results['server']['id']},{results['server']['country']},{results['server']['sponsor']}\n")


def main():
    while True:
        run_speedtest()
        print("Speedtest complete. Sleeping for 5 minutes.")
        time.sleep(300)

if __name__ == "__main__":
    main()

