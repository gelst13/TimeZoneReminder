# $TimeZoneReminder
"""
DESCRIPTION:
TimeZoneReminder app - command-line script that allows you to:
- keep info about your contacts' time zones
- display: "what time is it now at smbd's place?"
            [my current local time] and [contact's current time]
- easily convert time (my local time into chosen time zone and vice versa)

----
menu:
0.time operation:
- calculate time
- convert time
- show current time for a time zone
1.add contact
2.see contact info and current time for him/her
3.change existing contact(delete, rename or change some info in Contact' record)
4. export Contacts' Book (as .csv - file)
5. exit
----
* user can type contact_names/platform in any registry, but the program capitalize them

"""
import argparse
import datetime
import logging
import re
import time
from dateutil.tz import tzoffset, tzlocal, tz
from pprint import pprint
from tzr_utils import InfoBase
from tzr_utils import TimeKeeper


logging.basicConfig(filename='tzr.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class ContactsKeeper:
    def __init__(self):
        self.new_contact = ''
        self.user_input = ''
        self.call = 0
        self.args = self.args()

    @staticmethod
    def args():
        parser = argparse.ArgumentParser(description="This app has hidden command: 000 argument allows "
                                                     "to print existing Contact base.")
        parser.add_argument("--cmnd", default="",
                            help="Type '000' to print existing Contact base")
        return parser.parse_args()

    def time_operation(self):
        while True:
            print('''\nAvailable time operations:
0-display the time that will come after a certain time period
1-display current time in another time zone
2-convert time(local time to some other time zone or vice versa)
b-go back
''')
            self.user_input = input()
            if self.user_input == 'b':
                self.start()
            if self.user_input == '0':
                time_period = list()
                time_period.append(int(input('enter how many hours forward (00-24):> ')))
                time_period.append(int(input('enter how many minutes forward (00-59):> ')))
                current_local_time = time.localtime()
                print(f"In {time_period[0]} hours {time_period[1]} minutes it'll be:")
                print(TimeKeeper.calculate_time(current_local_time, time_period))
                self.time_operation()
            if self.user_input == '1':
                tz_data = input('Enter the name of time zone or offset (hours of time difference) to UTC/GMT:> ')
                time_now = TimeKeeper().get_current_time(tz_data)
                if time_now:
                    print(f"current time in {tz_data} time zone: {time_now}")
            elif self.user_input == '2':
                TimeKeeper.convert_time(self)

    @staticmethod
    def display_contact_current_time(contact_data):
        if contact_data[4]:
            contact_time_now = TimeKeeper().get_current_time(contact_data[4])
        else:
            contact_time_now = TimeKeeper().get_current_time(contact_data[5])
        if contact_time_now:
            print(f'time for {contact_data[0].capitalize()} now: {contact_time_now}')

    def see_info(self):
        logging.info('***def see_info')
        self.call += 0
        print('\nList of contacts: ')
        print(*sorted(x.capitalize() for x in InfoBase.select_column('contact_name')), sep='\n')
        if not self.check_if_db_empty():
            self.start()
        data_for_search = input('Enter data for search(contact name/platform/time zone/time difference):> ')
        if data_for_search.capitalize() in InfoBase.select_column('platform'):
            result = InfoBase.select_row('platform', data_for_search.capitalize())
            print(f'Contacts from {data_for_search.capitalize()}:')
            print(result if result else 'no such entries')
        elif data_for_search in TimeKeeper.tz_olson.keys():
            result = InfoBase.select_row('zone_name', data_for_search.upper())
            print(f'Contacts from {data_for_search}')
            print(result if result else 'no such entries')
        elif re.match('[-+]?[0-9.]', data_for_search):
            result = InfoBase.select_row('utc_offset', float(data_for_search))
            print(f'Contacts from UTC {data_for_search}:')
            print(result if result else 'no such entries')
        else:
            print('Contact info:')
            data = InfoBase.select_row('contact_name', data_for_search.capitalize())
            # [('Bo', 'Discord', 'Bocanada Hyperskill', 'Seul', 'JST', 9.0)]
            if data == list():
                logging.debug(f'data == list(): {data == list()}')
                print('no such entries')
                self.start()
            else:
                print(data[0])
                ContactsKeeper.display_contact_current_time(data[0])

    def add_contact(self):
        # contact = [ contact_name / platform / comment / location / zone_name / utc_offset ]
        while True:
            contact_name = input('\nEnter contact name/nick:> ').capitalize()
            if contact_name in InfoBase.select_column('contact_name'):
                print(f'Contact {contact_name} already exists. You can not add another contact with such name')
                self.add_contact()
            else:
                platform = input('Where do you communicate? (Discord, Skype, Telegram, WhatsApp, etc.):> ').capitalize()
                comment = input('Additional info/ commentary:> ')
                location = input('Where this contact lives?:> ').capitalize()
                time_zone = input('Enter the name of time zone or hours of time difference to UTC/GMT:> ')
                if time_zone.isalpha():
                    zone_name = time_zone.upper()
                    utc_offset = None
                    break
                elif re.match('[-+]?[0-9.]', time_zone):
                    zone_name = None
                    utc_offset = float(time_zone)
                    break
                else:
                    print('Incorrect format. Try again!')
        self.new_contact = (contact_name, platform, comment, location, zone_name, utc_offset)
        print(self.new_contact)
        InfoBase.transfer_to_sql(*self.new_contact)

    def change_contact(self):
        # contact = [ contact_name / platform / comment / location / zone_name / utc_offset ]
        contact_to_change = input('\nEnter contact name/nick to be changed:> ').capitalize()
        if contact_to_change not in InfoBase.select_column('contact_name'):
            print('error: no such contact')
            self.start()
        record_to_change = InfoBase.select_row('contact_name', contact_to_change)
        print(record_to_change)
        new_record = [x for x in record_to_change[0]]
        operation = input('\nchoose action:\nd - delete contact\nc - change contact\nb - go back\n> ')
        if operation == 'b':
            self.start()
        elif operation == 'd':
            InfoBase.delete_row(contact_to_change)
            print('Contact deleted')
        elif operation == 'c':
            while True:
                print('''What field do you wish to change:
                0 - contact name
                1 - platform
                2 - comment
                3 - location
                4 - zone name
                5 - difference to UTC
                s - save changes''')
                self.user_input = input()  # field number or command to save
                try:
                    if self.user_input == 's':
                        InfoBase.delete_row(contact_to_change)
                        InfoBase.transfer_to_sql(*new_record)
                        print('saved')
                        break
                    print(f'Current: {record_to_change[0][int(self.user_input)]}')
                    new_value = input('Change to:> ')
                    # print(new_record)
                    if self.user_input == '5':  # difference to UTC keep as float
                        new_record[int(self.user_input)] = float(new_value)
                    elif self.user_input == '4':  # zone name
                        new_record[int(self.user_input)] = new_value.upper()
                    else:
                        new_record[int(self.user_input)] = new_value.capitalize()
                    # print(new_record)
                except ValueError:
                    print('wrong command')
                    continue

    actions = {'0': time_operation,
               '1': add_contact,
               '2': see_info,
               '3': change_contact,
               }

    @staticmethod
    def check_if_db_empty():
        return 0 if not InfoBase.select_all() else 1

    def start(self):
        sql_operation = InfoBase()
        sql_operation.create_table()
        print('Contact base is empty' if self.check_if_db_empty() == 0 else '')
        print(sql_operation)
        if self.args.command == '000':
            sql_operation.print_contact_table()
        while True:
            print('\nchoose action:\n0.time operation\n1.add contact\n2.see contact info'
                  '\n3.change contact\n4.export contacts\n5.exit')
            self.user_input = input('> ')
            if self.user_input == '5':
                exit()
            elif self.user_input == '000':
                sql_operation.print_contact_table()
            elif self.user_input == '4':
                InfoBase.export_contact_book()
            elif self.user_input not in list(ContactsKeeper.actions.keys()):
                print('Incorrect command. Enter 00, 11, 22, 33 or 44')
            else:
                ContactsKeeper.actions[self.user_input](self)


def main():
    logging.info('+++++new start++++/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\')
    print('''___     ___   __ __      ___ 
 |||\/||__     //  \|\ ||__  
 |||  ||___   /_\__/| \||___ 
                            ''')  # https://patorjk.com/ font: Stick Letters
    print()
    print(''' __  ___          __  ___ __  
|__)|__ |\/|||\ ||  \|__ |__) 
|  \|___|  ||| \||__/|___|  \ 
                              ''')
    new = ContactsKeeper()
    time_keeper = TimeKeeper()
    print(repr(time_keeper))
    pprint(TimeKeeper.__str__(time_keeper))
    new.start()


if __name__ == '__main__':
    main()
