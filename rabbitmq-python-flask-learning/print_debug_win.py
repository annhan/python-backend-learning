import sys, datetime

def print_debug(*msg):
    print(datetime.datetime.now().strftime("%H:%M:%S"), "|" , *msg, flush=True)
    sys.stdout.flush()