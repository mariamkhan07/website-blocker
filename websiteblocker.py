from datetime import datetime
import platform

# start and end time for website blocking
start_time = datetime.now().replace(hour=9, minute=0)  # 9:00 am
end_time = datetime.now().replace(hour=17, minute=0)   # 5:00 pm

# websites I am planning to block
sites_to_block = ['twitter.com', 'www.twitter.com', 'facebook.com', 'www.facebook.com']

if platform.system() == "Windows":
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"

# using localhost to redirect blocked websites
redirect_ip = "127.0.0.1"


def block_sites():
    """Blocks the specified websites by modifying the hosts file."""
    print("Blocking websites")
    with open(hosts_path, "r+") as file:
        content = file.read()
        for website in sites_to_block:
            # check if the website is already blocked
            if website not in content:
                file.write("{} {}\n".format(redirect_ip, website))
        file.flush()  # flush the changes to the file
        file.close()


def unblock_sites():
    """Unblocks the websites by removing their entries from the host file."""
    print("Unblocking websites")
    with open(hosts_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        # rewrite the file with lines that do not contain blocked websites
        file.writelines(line for line in lines if not any(website in line for website in sites_to_block))
        file.truncate()  # resizing the file


def is_blocking_time():
    """Check if the current time is within the specified blocking time interval."""
    now = datetime.now()
    return start_time <= now <= end_time


if __name__ == "__main__":
    try:
        blocked = False
        while True:
            # check if it's time to block websites
            if is_blocking_time():
                if not blocked:
                    # block websites if not already blocked
                    block_sites()
                    blocked = True
            else:
                if blocked:
                    # unblock websites if they were previously blocked
                    unblock_sites()
                    blocked = False
    except KeyboardInterrupt:
        # use (Ctrl + C) to ensure websites are unblocked before exiting
        unblock_sites()
