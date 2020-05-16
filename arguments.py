import argparse
import time

parser = argparse.ArgumentParser(description='pass your agruments!')
parser.add_argument("--name", required=True, type=str, help="Your name")
parser.add_argument("--sleep", required=True, type=int, help="sleep seconds")
args = parser.parse_args()
a = args.name
b = args.sleep
print(a)
time.sleep(b)