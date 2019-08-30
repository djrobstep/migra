#Wrapper to hook into Migra Package

from migra import do_command
import version
import argparse

def parse_cli():
   parser = argparse.ArgumentParser(description='Process a yaml file')
 
   parser.add_argument("--version", help="Version of executable", action="store_true")
   args = parser.parse_args()
   return args 

a = parse_cli()
if a.version:
    print(version.version_dict)
else:
    do_command()