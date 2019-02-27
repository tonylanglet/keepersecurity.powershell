import sys
import getopt
import getpass
import string
import argparse

from keepercommander.record import Record
from keepercommander.commands.enterprise import EnterpriseInfoCommand
from keepercommander.params import KeeperParams
from keepercommander import display, api

my_params = KeeperParams()
      
# MAIN FUNCTION
def main(argv):
    # Variables
    entNodes = None
    endUsers = None
    entTeams = None
    endRoles = None
    endNode = None
    # Authentication credentials
    authUsername = None
    authPassword = None

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-ns', '--nodes', type=str, help='print node tree')
    parser.add_argument('-u', '--users', type=str, help='print user list')
    parser.add_argument('-t', '--teams', type=str, help='print team list')
    parser.add_argument('-r', '--roles', type=str, help='print role list')
    parser.add_argument('-n', '--node', type=str, help='limit results to node (name or ID)')
    parser.add_argument('-auser', '--ausername', type=str, help='Authentication username', required=True)
    parser.add_argument('-apass', '--apassword', type=str, help='Authentication password', required=True)
    args = parser.parse_args()

    if args.nodes:
        endNodes = args.nodes
    if args.users:
        entUsers = args.users
    if args.roles:
        entRoles = args.roles
    if args.teams:
        entTeams = args.teams
    if args.node:
        entNode = args.node
    if args.ausername:
        authUsername = args.ausername
    if args.apassword:
        authPassword = args.apassword

    while not my_params.user:
        my_params.user = authUsername

    while not my_params.password:
        my_params.password = authPassword
    api.sync_down(my_params)

    # KEEPER COMMAND
    command = EnterpriseInfoCommand()
    recordResult = command.execute(my_params, nodes=entNodes, users=entUsers, teams=entTeams, roles=entRoles, node=entNode)
    print("Success")
    return recordResult

if __name__ == "__main__":
    main(sys.argv[1:])