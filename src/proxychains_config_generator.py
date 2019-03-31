#! /usr/bin/python3

# Internal
from argparse import ArgumentParser
import json
from collections import namedtuple
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
                help="Whether print status messages to stdout.")
        self.parser.add_argument("-d", "--dry_run",
                dest="verbose", 
                help="Dry run will not make any filesystem changes.")
        # proxychains arguments
        self.parse_config_file()
        self.args = vars(self.parser.parse_args())
        self.save_config(self.args.get("output_path"))  

        
    def __str__(self):
        return self.__dict__      
    
    def parse_config_file(self):
        for k, v in self.config.items():
            arg_fields = dict(
                dest = k,
                action = None,
                nargs = None,
                const = None,
                default = None,
                type = None,
                choices = None,
                required = None,
                help = None,
                metavar = None,
            )         
            if "options" in v:
                arg_fields["choices"] = [x for x in v["options"].keys()]
            arg_fields["help"] = v.get("description")
            arg_fields["nargs"] = v.get("nargs")
            arg_fields["default"] = v.get("default")
            arg_short = v.get("short")
            self.parser.add_argument("-" + arg_short, "--" + k,
                                     **{k: v for k, v in arg_fields.items() if v is not None})
    
    """
    Saves config to filepaths.
    """
    def save_config(self, filepath="config/proxychains_test.conf"):
        # items = list(self.args.keys())
        #print(items)
        with open(filepath, "w") as ofile:
            key = self.args.get("chain_type")
            ofile.write("# {}\n# {}\n{}\n\n".format(self.config.get("chain_type").get("description"),
                                        self.config.get("chain_type").get("options").get(key).get("description"),
                                        key))
            key = self.args.get("chain_len")
            ofile.write("# {}\n# {} = {}\n\n".format(self.config.get("chain_len").get("description"),
                                        "chain_len",
                                        key))
            key = self.args.get("quiet_mode")
            ofile.write("# {}\n{}\n\n".format(self.config.get("quiet_mode").get("description"),
                                        "quiet_mode"))
            key = self.args.get("proxy_dns")
            ofile.write("# {}\n{}\n\n".format(self.config.get("proxy_dns").get("description"),
                                        "proxy_dns"))
            key = self.args.get("remote_dns_subnet")
            ofile.write("# {}\n{} {}\n\n".format(self.config.get("remote_dns_subnet").get("description"),
                                        "remote_dns_subnet",
                                        self.args.get("remote_dns_subnet")))       
            key = self.args.get("tcp_read_time_out")
            ofile.write("# {}\n{} {}\n\n".format(self.config.get("tcp_read_time_out").get("description"),
                                        "tcp_read_time_out",
                                        self.args.get("tcp_read_time_out")))                
            key = self.args.get("tcp_connect_time_out")
            ofile.write("# {}\n{} {}\n\n".format(self.config.get("tcp_connect_time_out").get("description"),
                                        "tcp_read_time_out",
                                        self.args.get("tcp_connect_time_out")))
            key = self.args.get("loopback_address_range")            
            ofile.write("# {}\n{}\n\n".format(self.config.get("loopback_address_range").get("description"),
                                        "loopback_address_range",
                                        self.args.get("loopback_address_range")))
            key = self.args.get("proxy_list")            
            ofile.write("# {}\n{}\n\n".format(self.config.get("proxy_list").get("description"),
                                        self.args.get("proxy_list")))


def main():
    internal_config_file = os.path.abspath("config/config.json")
    
    # load configuration file
    with open(internal_config_file, "r") as json_file:
        config = json.load(json_file)
    internal_config = InternalConfiguration(config)
    
main()
