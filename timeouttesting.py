import signal

def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")

def loop_forever():
    import time
    for i in range(5):
        print("sec")
        time.sleep(1)


signal.signal(signal.SIGALRM, handler)
signal.alarm(10)

try:
    loop_forever()
except exc:
    print(exc)

signal.alarm(0)
import time
for i in range(15):
    print("sec")
    time.sleep(1)
