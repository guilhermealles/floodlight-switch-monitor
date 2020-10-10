import time
import os
import requests
import json
from tabulate import tabulate

def main():
  baseurl = os.environ['FLOODLIGHT_BASEURL']

  while True:
    response = requests.get(baseurl + '/wm/statistics/bandwidth/all/all/json').json()
    os.system('clear')
    response = [x for x in response if switch_port(x) != 'local']
    response.sort(key=switch_port)
    response.sort(key=switch_name)
    tabulated_data = [[switch_name(x), switch_port(x), switch_tx_mbps(x), switch_rx_mbps(x)] for x in response]
    print(tabulate(tabulated_data, headers=['Switch', 'Port', 'Tx', 'Rx'], tablefmt="orgtbl"))
    time.sleep(1)

def switch_name(switch_obj):
  return switch_obj['dpid']

def switch_port(switch_obj):
  return switch_obj['port']

def switch_tx_mbps(switch_obj):
  bits = int(switch_obj['bits-per-second-tx'])
  mbits = bps_to_mbps(bits)
  return 'NA' if mbits < 1 else f"{mbits:.9f}"

def switch_rx_mbps(switch_obj):
  bits = int(switch_obj['bits-per-second-rx'])
  mbits = bps_to_mbps(bits)

  return 'NA' if mbits < 1 else f"{mbits:.9f}"

def bps_to_mbps(bps):
  return bps/1024/1024


if __name__ == '__main__':
  main()
