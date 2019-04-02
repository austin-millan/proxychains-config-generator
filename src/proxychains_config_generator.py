#! /usr/bin/python3

from argparse import ArgumentParser
import json
import os
import sys


class InternalConfiguration:

    def __init__(self, config_filepath):
        self.config_filepath = config_filepath
        self.raw_proxychain_args = None
        self.raw_program_args = None
        self.parsed_args = None
        # parse/validate arguments for program and proxychains
        self.parser = ArgumentParser("proxychains-config-generator")
        self.argparse_arg_fields = ["dest", "action", "nargs",
                                    "const", "default", "type",
                                    "choices", "required", "help",
                                    "metavar"]

    def __str__(self):
        return self.__dict__

    """
    Wrapper for `parse_proxychain_args` and `parse_program_args`,
    this method ingests the program's `config.json` file and fills 
    the ArgumentParser with the arguments for proxychain and the program.
    
    Simply exits if error.
    """
    def load_config_file(self):

        def parse_proxychain_args(self):
            if not self.raw_proxychain_args:
                return None
            for k, v in self.raw_proxychain_args.items():
                arg_fields = dict((z, None) for z in self.argparse_arg_fields)
                for field in self.argparse_arg_fields:
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
            for k, v in self.raw_program_args.items():
                arg_fields = dict((z, None) for z in self.argparse_arg_fields)
                for field in self.argparse_arg_fields:
                    if field not in v:
                        continue
                    arg_fields[field] = v.get(field)
                self.parser.add_argument("-" + v.get("short"), "--" + k,
                                         **{k: v for k, v in arg_fields.items() if v is not None})
            return True

        if not self.config_filepath:
            print("Could not open configuration.")
            return None
        try:
            with open(self.config_filepath, "r") as json_file:
                config = json.load(json_file)
        except Exception as e:
            print("Could not open configuration file. Exiting.")
            sys.exit(1)
        self.raw_program_args = config.get("program_args")
        if not parse_program_args(self):
            print("Error parsing program config. Exiting.")
            sys.exit(1)
        self.raw_proxychain_args = config.get("proxychain_args")
        if not parse_proxychain_args(self):
            print("Error parsing proxychain config. Exiting.")
            sys.exit(1)
        self.parsed_args = vars(self.parser.parse_args())

    """
    Returns a string representing the proxychain configuration.
    """
    def build_proxychain_conf_str(self):
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
    Saves proxychain configuration to filepath.
    """
    def save_config(self):
        data = self.build_proxychain_conf_str()
        write_out = True
        if self.parsed_args.get("dry_run"):
            print(data)
            write_out = False
        if os.path.exists(self.parsed_args.get("output_path")) and write_out is True:
            user_resp = input("Would you like to override '{0}? (y/n): ".format(self.parsed_args.output_path))
            if user_resp.lower() == 'yes' or user_resp.lower() == 'y':
                write_out = True
            elif user_resp.lower() == 'no' or user_resp.lower() == 'n':
                write_out = False
            else:
                print("No input, exiting.")
        if write_out is True:
            try:
                with open(self.parsed_args.output_path, "w") as ofile:
                    ofile.write(data)
            except Exception as e:
                print("Could not write out to file. Exiting.")
                sys.exit(1)


def main():
    internal_config_path = os.path.abspath("config/config.json")
    internal_config = InternalConfiguration(internal_config_path)
    internal_config.load_config_file()
    internal_config.save_config()


main()
