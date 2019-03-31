# proxychains-config-generator

A tool to generate configurations for the [proxychains](https://github.com/haad/proxychains) tool.

## Usage

```
usage: proxychains_config_generator.py [-h] [-o OUTPUT_PATH] [-v VERBOSE]
                                       [-d VERBOSE]
                                       [-t {dynamic_chain,strict_chain,random_chain}]
                                       [-l CHAIN_LEN] [-q QUIET_MODE]
                                       [-p PROXY_DNS] [-r REMOTE_DNS_SUBNET]
                                       [-b TCP_READ_TIME_OUT]
                                       [-c TCP_CONNECT_TIME_OUT]
                                       [-a LOOPBACK_ADDRESS_RANGE]
                                       [-e PROXY_LIST]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to store file.
  -v VERBOSE, --verbose VERBOSE
                        Whether print status messages to stdout.
  -d VERBOSE, --dry_run VERBOSE
                        Dry run will not make any filesystem changes.
  -t {dynamic_chain,strict_chain,random_chain}, --chain_type {dynamic_chain,strict_chain,random_chain}
                        The option below identifies how the ProxyList is
                        treated.
  -l CHAIN_LEN, --chain_len CHAIN_LEN
                        Make sense only if random_chain
  -q QUIET_MODE, --quiet_mode QUIET_MODE
                        Quiet mode (no output from library)
  -p PROXY_DNS, --proxy_dns PROXY_DNS
                        Proxy DNS requests - no leak for DNS data
  -r REMOTE_DNS_SUBNET, --remote_dns_subnet REMOTE_DNS_SUBNET
                        set the class A subnet number to usefor use of the
                        internal remote DNS mapping
  -b TCP_READ_TIME_OUT, --tcp_read_time_out TCP_READ_TIME_OUT
                        Some timeouts in milliseconds
  -c TCP_CONNECT_TIME_OUT, --tcp_connect_time_out TCP_CONNECT_TIME_OUT
                        Some timeouts in milliseconds
  -a LOOPBACK_ADDRESS_RANGE, --loopback_address_range LOOPBACK_ADDRESS_RANGE
                        By default enable localnet for loopback address ranges
  -e PROXY_LIST, --proxy_list PROXY_LIST
                        proxy types: http, socks4, socks5. defaults set to
                        'tor

```

## Issues

- Fix up `InternalConfiguration.save_config()` to more closely match the original proxychains config file.