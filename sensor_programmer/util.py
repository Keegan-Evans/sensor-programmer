import subprocess

# TODO: write for linux as well, currently works on mac
def get_ip_address(ifname):
    addr = subprocess.run(["ipconfig",  "getifaddr", ifname], capture_output=True).stdout.strip().decode()
    return addr

if __name__ == '__main__':
    a = get_ip_address('en0')
    print(a)