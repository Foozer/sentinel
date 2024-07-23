import speedtest
import datetime
import netifaces

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
    
def run_speedtest():
    st = speedtest.Speedtest()
    st.download()
    st.upload()
    results = st.results.dict()
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    results['timestamp'] = timestamp

    
    
    with open('speedtest_results.csv', 'a') as f:
        f.write(f"{results['timestamp']},{results['download']},{results['upload']},{results['ping']},{results['server']['id']},{results['server']['country']},{results['server']['sponsor']}\n")


def main():
    interface = 'wlp64s0'
    mac_address = get_mac_address(interface)
    print(f"MAC address of {interface}: {mac_address}")
    run_speedtest()

if __name__ == "__main__":
    main()

