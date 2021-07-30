import time
import pexpect
import sys
from uuid import getnode as get_mac
# Sensor MAC Address
DEVICE = "e0:62:34:df:a2:33"
if len(sys.argv) == 2:
    DEVICE = str(sys.argv[1])
# Run gatttool interactively.
child = pexpect.spawn("sudo gatttool -I")
#child = pexpect.spawn("sudo gatttool -b " + DEVICE + "-I -t random" )

# Connect to the device.
print("Connecting to:"),
print(DEVICE)

NOF_REMAINING_RETRY = 5

while True:

    try:
        child.sendline("connect {0}".format(DEVICE))
        child.expect("Connection successful", timeout=5)
    except pexpect.TIMEOUT:
        NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
        if (NOF_REMAINING_RETRY > 0):
            print("timeout, retry...")
            continue
        else:
            print("timeout, giving up.")
        break
    else:
        print("Connected!")
        break
#extract Raw Rate

def extractRate(rawRate):
    r1=rawRate[0:8]
    r2=[r1[i:i+2] for i in range(0, len(r1), 2)]
    r3=r2[::-1]
    r4="".join(r3);
    r5=int(r4, 16)
    #print(r5)
    return r5


def extractVolt(rate, rawVolt):
    v1=rawVolt[0:4]
    v2=[v1[i:i+2] for i in range(0, len(v1), 2)]
    v3=v2[::-1]
    v4="".join(v3)
    v5=int(v4, 16)
    return calculateVolt(rate, v5)

def calculateVolt(rate, adcValue):
    #print("rate = %s ; adc = %s" %(str(rate), str(adcValue)))
    val = float(((float(adcValue)*3300)/float(1024))/float(rate)*float(3000))/1000
    return val    

#RETRIEVE THE RAW RATE VALUE
def rawRate():
    child.sendline("char-read-hnd 0x0016")
    child.expect("Characteristic value/descriptor: ", timeout=5)
    child.expect("\r\n", timeout=5)
    rawRate = (child.before).decode('UTF-8').replace(" ","").replace("value:", "").strip()
    print("RawRate = %s " % rawRate)
    rate=extractRate(rawRate)
    print("RATE = %s" % str(rate))



if __name__ == '__main__':
    rawRate()    