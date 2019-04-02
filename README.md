# proxychains-config-generator

A tool to generate configurations for the [proxychains](https://github.com/haad/proxychains) tool.

## Usage

```
usage: proxychains_config_generator [-h] [-o OUTPUT_PATH] [-v] [-d]
                                    [-t {dynamic_chain,strict_chain,random_chain}]
                                    [-l] [-q] [-p PROXY_DNS]
                                    [-r REMOTE_DNS_SUBNET]
                                    [-b TCP_READ_TIME_OUT]
                                    [-c TCP_CONNECT_TIME_OUT]
                                    [-a [LOOPBACK_ADDRESS_RANGE [LOOPBACK_ADDRESS_RANGE ...]]]
                                    [-e [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD']
                                    [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD']
                                    ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to store file.
  -v, --verbose         Whether print status messages to stdout.
  -d, --dry_run         Dry run will not make any filesystem changes.
  -t {dynamic_chain,strict_chain,random_chain}, --chain_type {dynamic_chain,strict_chain,random_chain}
                        The option below identifies how the ProxyList is
                        treated.
  -l, --chain_len       Make sense only if random_chain
  -q, --quiet_mode      Quiet mode (no output from library)
  -p PROXY_DNS, --proxy_dns PROXY_DNS
                        Proxy DNS requests - no leak for DNS data
  -r REMOTE_DNS_SUBNET, --remote_dns_subnet REMOTE_DNS_SUBNET
                        set the class A subnet number to usefor use of the
                        internal remote DNS mapping
  -b TCP_READ_TIME_OUT, --tcp_read_time_out TCP_READ_TIME_OUT
                        Some timeouts in milliseconds
  -c TCP_CONNECT_TIME_OUT, --tcp_connect_time_out TCP_CONNECT_TIME_OUT
                        Some timeouts in milliseconds
  -a [LOOPBACK_ADDRESS_RANGE [LOOPBACK_ADDRESS_RANGE ...]], --loopback_address_range [LOOPBACK_ADDRESS_RANGE [LOOPBACK_ADDRESS_RANGE ...]]
                        By default enable localnet for loopback address ranges
  -e [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD'] [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD'] ...]], --proxy_list [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD'] [['PROTOCOL', 'HOST', 'PORT', 'USERNAME', 'PASSWORD'] ...]]
                        proxy types: http, socks4, socks5. Defaults to 'tor'
```

## Issues

- Fix up `InternalConfiguration.save_config()` to more closely match the original proxychains config file.