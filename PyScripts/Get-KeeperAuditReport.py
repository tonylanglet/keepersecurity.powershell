import sys
import getopt
import getpass
import string
import argparse

from keepercommander.record import Record
from keepercommander.commands.enterprise import AuditReportCommand
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
    parser.add_argument('--syntax-help',dest='syntax_help', type=bool, help='display help')
    parser.add_argument('--report-type', dest='report_type', choices=['raw', 'dim', 'hour', 'day', 'week', 'month', 'span'], action='store', help='report type')
    parser.add_argument('--report-format', dest='report_format', action='store', choices=['message', 'fields'], help='output format (raw reports only)')
    parser.add_argument('--columns', dest='columns', action='append', help='Can be repeated. (ignored for raw reports)')
    parser.add_argument('--aggregate', dest='aggregate', action='append', choices=['occurrences', 'first_created', 'last_created'], help='aggregated value. Can be repeated. (ignored for raw reports)')
    parser.add_argument('--timezone', dest='timezone', action='store', help='return results for specific timezone')
    parser.add_argument('--limit', dest='limit', type=int, action='store', help='maximum number of returned rows')
    parser.add_argument('--order', dest='order', action='store', choices=['desc', 'asc'], help='sort order')
    parser.add_argument('--created', dest='created', action='store', help='Filter: Created date. Predefined filters: today, yesterday, last_7_days, last_30_days, month_to_date, last_month, year_to_date, last_year')
    parser.add_argument('--event-type', dest='event_type', action='store', help='Filter: Audit Event Type')
    parser.add_argument('--username', dest='username', action='store', help='Filter: Username of event originator')
    parser.add_argument('--to-username', dest='to_username', action='store', help='Filter: Username of event target')
    parser.add_argument('--record-uid', dest='record_uid', action='store', help='Filter: Record UID')
    parser.add_argument('--shared-folder-uid', dest='shared_folder_uid', action='store', help='Filter: Shared Folder UID')
    parser.add_argument('-auser', '--ausername', type=str, help='Authentication username', required=True)
    parser.add_argument('-apass', '--apassword', type=str, help='Authentication password', required=True)
    args = parser.parse_args()

    Parameters = dict()
    if args.syntax_help is not None:
        Parameters.update({'syntax_help':args.syntax_help})
    if args.report_type is not None:
        Parameters.update({'report_type':args.report_type})
    if args.report_format is not None:
        Parameters.update({'report_format':args.report_format})
    if args.columns is not None:
        Parameters.update({'columns':args.columns})
    if args.aggregate is not None:
        Parameters.update({'aggregate':args.aggregate})
    if args.timezone is not None:
        Parameters.update({'timezone':args.timezone})
    if args.limit is not None:
        Parameters.update({'limit':args.limit})
    if args.order is not None:
        Parameters.update({'order':args.order})
    if args.created is not None:
        Parameters.update({'created':args.created})
    if args.event_type is not None:
        Parameters.update({'event-type':args.event_type})
    if args.username is not None:
        Parameters.update({'username':args.username})
    if args.to_username is not None:
        Parameters.update({'to_username':args.to_username})
    if args.record_uid is not None:
        Parameters.update({'record_uid':args.record_uid})
    if args.shared_folder_uid is not None:
        Parameters.update({'shared_folder_uid':args.shared_folder_uid})
                           
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
    command = AuditReportCommand()
    result = command.execute(my_params, **Parameters)
    print("Successfully")
    return result

if __name__ == "__main__":
    main(sys.argv[1:])
