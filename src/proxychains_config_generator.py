#! /usr/bin/python3

from argparse import ArgumentParser
import json
import os
import sys


class InternalConfiguration:
    def __init__(self, config):
        self.raw_proxychain_args = None
        self.raw_program_args = None
        # parse/validate arguments for program and proxychains
        self.parser = ArgumentParser("proxychains_config_generator")
        self.parse_config_file(config)
        self.parsed_args = vars(self.parser.parse_args())

    def __str__(self):
        return self.__dict__

    def parse_config_file(self, config):

        def parse_proxychain_args(self):
            if not self.raw_proxychain_args:
                return None
            argparse_arg_fields = ["dest", "action", "nargs",
                                   "const", "default", "type",
                                   "choices", "required", "help",
                                   "metavar"]
            for k, v in self.raw_proxychain_args.items():
                arg_fields = dict((z, None) for z in argparse_arg_fields)
                for field in argparse_arg_fields:
                    if field not in v:
                        continue
                    arg_fields[field] = v.get(field)
                    if "metavar" in v:
                        arg_fields["metavar"] = list(x.upper() for x in v.get("metavar").keys())
                    if "options" in v:
                        arg_fields["choices"] = [x for x in v["options"].keys()]
                self.parser.add_argument("-" + v.get("short"), "--" + k,
                                         **{k: v for k, v in arg_fields.items() if v is not None})
            return True

        def parse_program_args(self):
            if not self.raw_program_args:
                return None
            argparse_arg_fields = ["dest", "action", "nargs",
                                   "const", "default", "type",
                                   "choices", "required", "help",
                                   "metavar"]
            for k, v in self.raw_program_args.items():
                arg_fields = dict((z, None) for z in argparse_arg_fields)
                for field in argparse_arg_fields:
                    if field not in v:
                        continue
                    arg_fields[field] = v.get(field)
                self.parser.add_argument("-" + v.get("short"), "--" + k,
                                         **{k: v for k, v in arg_fields.items() if v is not None})
            return True

        if not config:
            return None
        self.raw_program_args = config.get("program_args")
        if not parse_program_args(self):
            print("Error parsing program config. Exiting.")
            sys.exit(1)
        self.raw_proxychain_args = config.get("proxychain_args")
        if not parse_proxychain_args(self):
            print("Error parsing proxychain config. Exiting.")
            sys.exit(1)

    """
    Builds configuration as a string.
    
    Note: "Choices" argument returns a list type.
    Returns:
        str
    """
    def build_proxychain_conf_str(self, config):
        if self.raw_proxychain_args is None:
            raise RuntimeError("Unable to open configuration.")
        data = ""

        # CHAIN TYPE
        key = self.parsed_args.get("chain_type")
        if type(key) is list:
            key = key[0]
        data += "# {}\n# {}\n{}\n\n".format(
            self.raw_proxychain_args.get("chain_type").get("help"),
            self.raw_proxychain_args.get("chain_type").get("options").get(key).get("help"),
            key
        )

        # CHAIN LEN
        key = self.parsed_args.get("chain_len")
        data += "# {}\n{}{} = {}\n\n".format(
            self.raw_proxychain_args.get("chain_len").get("help"),
            "# " if self.parsed_args.get("chain_type") is not "random_chain" else "",
            "chain_len",
            key
        )

        # QUIET MODE
        key = self.parsed_args.get("quiet_mode")
        data += "# {}\n{}{}\n\n".format(
            self.raw_proxychain_args.get("quiet_mode").get("help"),
            "# " if not key else "",
            "quiet_mode"
        )

        # PROXY DNS
        key = self.parsed_args.get("proxy_dns")
        data += "# {}\n{}{}\n\n".format(
            self.raw_proxychain_args.get("proxy_dns").get("help"),
            "# " if not key else "",
            "proxy_dns"
        )

        # REMOTE DNS SUBNET
        data += "# {}\n{} {}\n\n".format(
            self.raw_proxychain_args.get("remote_dns_subnet").get("help"),
            "remote_dns_subnet",
            self.parsed_args.get("remote_dns_subnet")
        )

        # TCP READ TIMEOUT
        data += "# {}\n{} {}\n\n".format(
            self.raw_proxychain_args.get("tcp_read_time_out").get("help"),
            "tcp_read_time_out",
            self.parsed_args.get("tcp_read_time_out")
        )

        # TCP CONNECTION TIMEOUT
        data += "# {}\n{} {}\n\n".format(
            self.raw_proxychain_args.get("tcp_connect_time_out").get("help"),
            "tcp_read_time_out",
            self.parsed_args.get("tcp_connect_time_out")
        )

        # LOOPBACK ADDRESS RANGE
        addrs = self.parsed_args.get("loopback_address_range")
        data += "# {}\n".format(self.raw_proxychain_args.get("loopback_address_range").get("help"))
        if addrs:
            if len(addrs) == 1:
                data += "{}\n".format(''.join(addrs))
            if len(addrs) > 1:
                del addrs[0]  # delete default
                for addr in addrs:
                    data += "{}\n".format(' '.join(addr))
            data += "\n"

        # PROXY LIST
        proxies = self.parsed_args.get("proxy_list")
        data += "# {}\n".format(self.raw_proxychain_args.get("proxy_list").get("help"))
        if proxies:
            if len(proxies) == 1:
                data += "{}\n".format(''.join(proxies))
            if len(proxies) > 1:
                del proxies[0]  # delete default
                for proxy in proxies:
                    data += "{}\n".format(' '.join(proxy))
            data += "\n"
        return data

    """
    Saves config to filepath.
    """

    def save_config(self, filepath="config/proxychains_test.conf"):
        data = self.build_proxychain_conf_str(config=self.raw_proxychain_args)
        if self.parsed_args.get("dry_run"):
            print(data)
            return
        try:
            with open(filepath, "w") as ofile:
                ofile.write(data)
        except Exception as e:
            print("Could not write out to file. Exiting.")
            sys.exit(1)


def main():
    internal_config_file = os.path.abspath("config/config.json")
    try:
        with open(internal_config_file, "r") as json_file:
            config = json.load(json_file)
    except Exception as e:
        print("Could not open file. Exiting.")
        sys.exit(1)
    internal_config = InternalConfiguration(config)
    internal_config.save_config()


main()
