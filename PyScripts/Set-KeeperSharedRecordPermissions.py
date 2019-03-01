import sys
import getopt
import getpass
import string
import argparse

from keepercommander.record import Record
from keepercommander.commands.register import ShareRecordCommand
from keepercommander.params import KeeperParams
from keepercommander import display, api

my_params = KeeperParams()
      
# MAIN FUNCTION
def main(argv):
    # Authentication credentials
    authUsername = None
    authPassword = None

    #Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--record', type=str, help='Record UID', required=True)
    parser.add_argument('-e', '--email', type=str, help='user email', required=True)
    parser.add_argument('-a', '--action', choices=['grant', 'revoke', 'owner'], default='grant', help='user share action. \'grant\' if omitted')
    parser.add_argument('-s', '--share', type=str, help='can re-share record')
    parser.add_argument('-w', '--write', type=str, help='can modify record')
    parser.add_argument('-auser', '--ausername', type=str, help='Authentication username', required=True)
    parser.add_argument('-apass', '--apassword', type=str, help='Authentication password', required=True)
    args = parser.parse_args()

    Parameters = dict()
    if args.record is not None:
        Parameters.update({'record':args.record})
    if args.notes is not None:
        Parameters.update({'email':args.email})
    if args.record is not None:
        Parameters.update({'action':args.action})
    if args.notes is not None:
        Parameters.update({'share':args.share})
    if args.record is not None:
        Parameters.update({'write':args.write})
            
    if args.ausername:
        authUsername = args.ausername
    if args.apassword:
        authPassword = args.apassword

    #Authentication login
    while not my_params.user:
        my_params.user = authUsername

    while not my_params.password:
        my_params.password = authPassword
    api.sync_down(my_params)

    # KEEPER COMMAND
    command = ShareRecordCommand()
    result = command.execute(my_params, **Parameters)
    print("Successfully")
    return result

if __name__ == "__main__":
    main(sys.argv[1:])