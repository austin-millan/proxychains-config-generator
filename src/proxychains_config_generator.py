#! /usr/bin/python3

from argparse import ArgumentParser
import json
import os
import sys

class InternalConfiguration:
    def __init__(self, config):
        self.config = config
        # parse/validate Arguments
        self.parser = ArgumentParser()
        # program arguments
        self.parser.add_argument("-o", "--output_path", 
                dest="output_path",
                help="Path to store file.",
                default="config/proxychains_test.conf")
        self.parser.add_argument("-v", "--verbose",
                dest="verbose",
                action="store_true",
                help="Whether print status messages to stdout.")
        self.parser.add_argument("-d", "--dry_run",
                dest="dry_run",
                action="store_true",
                help="Dry run will not make any filesystem changes.",
                default=False)
        # proxychains arguments
        self.parse_config_file()
        #print(self.parser.parse_args())
        self.args = vars(self.parser.parse_args())

    def __str__(self):
        return self.__dict__      
    
    def parse_config_file(self):
        for k, v in self.config.items():
            arg_fields = dict(
                dest=k,
                action=None,
                nargs=None,
                const=None,
                default=None,
                type=None,
                choices=None,
                required=None,
                help=None,
                metavar=None,
            )
            if "options" in v:
                arg_fields["choices"] = [x for x in v["options"].keys()]
            arg_fields["help"] = v.get("description")
            arg_fields["nargs"] = v.get("nargs")
            arg_fields["default"] = v.get("default")
            arg_fields["action"] = v.get("action")
            arg_fields["required"] = v.get("required")
            self.parser.add_argument("-" + v.get("short"), "--" + k,
                                     **{k: v for k, v in arg_fields.items() if v is not None})

    """
    Builds configuration in string.
    
    Note: "Choices" argument returns a list type.
    Returns:
        str
    """    
    def create_config_str(self):
        if self.config is None:
            raise RuntimeError("Unable to open configuration.")
        data = ""
        key = self.args.get("chain_type")
        if type(key) is list:
            key = key[0]
        data += "# {}\n# {}\n{}\n\n".format(
            self.config.get("chain_type").get("description"),
            self.config.get("chain_type").get("options").get(key).get("description"),
            key
        )
        key = self.args.get("chain_len")
        data += "# {}\n{}{} = {}\n\n".format(
            self.config.get("chain_len").get("description"),
            "# " if self.args.get("chain_type") is not "random_chain" else "",
            "chain_len",
            key
        )
        key = self.args.get("quiet_mode")
        data += "# {}\n{}{}\n\n".format(
            self.config.get("quiet_mode").get("description"),
            "# " if not key else "",
            "quiet_mode"
        )
        key = self.args.get("proxy_dns")
        data += "# {}\n{}\n\n".format(
            self.config.get("proxy_dns").get("description"),
            "proxy_dns"
        )
        key = self.args.get("remote_dns_subnet")
        data += "# {}\n{} {}\n\n".format(
            self.config.get("remote_dns_subnet").get("description"),
            "remote_dns_subnet",
            self.args.get("remote_dns_subnet")
        )
        key = self.args.get("tcp_read_time_out")
        data += "# {}\n{} {}\n\n".format(
            self.config.get("tcp_read_time_out").get("description"),
            "tcp_read_time_out",
            self.args.get("tcp_read_time_out")
        )      
        key = self.args.get("tcp_connect_time_out")
        data += "# {}\n{} {}\n\n".format(
            self.config.get("tcp_connect_time_out").get("description"),
            "tcp_read_time_out",
            self.args.get("tcp_connect_time_out")
        )
        key = self.args.get("loopback_address_range")
        data += "# {}\n{}\n\n".format(
            self.config.get("loopback_address_range").get("description"),
            "loopback_address_range",
            self.args.get("loopback_address_range")
        )
        key = self.args.get("proxy_list")
        proxies = self.args.get("proxy_list")
        data += "# {}\n".format(self.config.get("proxy_list").get("description"))
        if len(proxies) > 1:
            del proxies[0]  # deletes default value
        for proxy in proxies:
            data += "{}\n".format(' '.join(proxy))
        return data
    
    """
    Saves config to filepath.
    """
    def save_config(self, filepath="config/proxychains_test.conf"):
        data = self.create_config_str()
        if self.args.get("dry_run"):
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
