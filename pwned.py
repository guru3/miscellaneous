import hashlib
import sys
import requests

#Reference : https://www.youtube.com/watch?v=hhUb5iknVJs
#pwnedpasswords.com api allows you to check if your
#input password has been pwned before - without you 
#actually sending them the complete password. Instead you
#send the initial few characters of hashed value, and get
#list of suffixes for all hashed values with that prefix, that
#have been pwned.
#You compare suffix of hash value of your password with it, and
#you can assert if your password is safe
#If you password is in the list, it is likely it is part of various
#dictionaries with passwords that hackers use to crack yours.

def check_pwned( password ):
    sha1Password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper();

    breakHashAt = 5;
    head, tail = sha1Password[:breakHashAt], sha1Password[breakHashAt:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    
    hashesToCountMap = res.text;
    hashesToCountMap = (line.split(':') for line in hashesToCountMap.splitlines());
    for tailIs, count in hashesToCountMap:
        if( tailIs == tail ):
            return sha1Password, count;
    return sha1Password, 0;

def main(args):
    for pwd in args or sys.stdin:
        pwd = pwd.strip()
        sha1Password, count =  check_pwned(pwd);
        if count == 0:
            print("No occurrences found for {0}".format(pwd));
            return;
        print( "{0} was found with {1} occurrences (hash: {2})".format(
            pwd, count, sha1Password));

if __name__ == '__main__':
    main(sys.argv[1:]);