# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
    # Check the CLI arguments
    if len(sys.argv)<5 :
        print("Usage: python3 %s <url> <username>"%sys.argv[0])
        return
    
    # Prep the arguments blob
    args = dict()
    args['username']  = sys.argv[2]
    args['password'] = sys.argv[3]
    args['role'] = sys.argv[4]

    # Print a message to let the user know what is being tried
    print("Activating user: %s"%args['username'])

    data = urlencode(args)
    
    # Make the resquest
    my_route = "activate_user"
    req = Request(sys.argv[1] + my_route, data.encode('ascii'),method='POST')
    # just need to return a string success
    res = urlopen(req)
    
    
    
    # Print the result code
    print("Call to LOST returned: %s"%res.read())
    

if __name__=='__main__':
    main()
    