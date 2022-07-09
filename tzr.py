# $TimeZoneReminder
"""
DESCRIPTION:
command-line script that allows you to:
- keep info about your contacts' time zones
- display: "what time is it now at smbd's place?"
            [my current local time] and [contact's current time]
- easily convert time (my local time into chosen time zone and vice versa)

----
menu:
00.time operation:
- calculate time
- convert time
- show current time for a time zone
11.add contact
22.see contact info and current time for him/her
33.change existing contact(delete, rename or change some info in Contact' record)
44. export Contacts' Book (as .csv - file)
55. exit
----
* user can type contact_names/platform in any registry, but the program capitalize them

"""
import datetime
import logging
import re
import time
from dateutil.tz import tzoffset, tzlocal, tz
from tzr_utils import InfoBase
from tzr_utils import TimeKeeper


logging.basicConfig(filename='tzr.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class ContactsKeeper:
    def __init__(self):
        self.new_contact = ''
        self.command = ''
        self.call = 0

    def time_operation(self):
        self.call += 0
        while True:
            print('''\nAvailable time operations:
0-display the time that will come after a certain time period
1-display current time in another time zone
2-convert time(local time to some other time zone or vice versa)
bbb - go back
''')
            operation = input()
            if operation == 'bbb':
                self.start()
            if operation == '0':
                time_period = list()
                time_period.append(int(input('enter how many hours forward (00-24):> ')))
                time_period.append(int(input('enter how many minutes forward (00-59):> ')))
                current_local_time = time.localtime()
                print(f"In {time_period[0]} hours {time_period[1]} minutes it'll be:")
                print(TimeKeeper.calculate_time(current_local_time, time_period))
                self.time_operation()
            if operation == '1':
                tz_data = input('Enter the name of time zone or offset (hours of time difference) to UTC/GMT:> ')
                time_now = TimeKeeper.show_current_time(tz_data)
                if time_now:
                    print(f"current time in {tz_data} time zone: {time_now}")
            elif operation == '2':
                from_local = input('convert local time? y/n ')
                if from_local.lower() == 'y':
                    tz_from = float(datetime.datetime.now().astimezone().strftime('%z')) / 100  # get local offset
                    tz_to = input('Enter the destination time zone: name or offset to UTC/GMT:> ')
                elif from_local.lower() != 'n':
                    print('Wrong command!')
                    self.time_operation()
                else:
                    tz_from = input('Enter the original time zone: name or offset to UTC/GMT:> ')
                    tz_to = tz.tzlocal()  # get local tz from PC

                _time = input('Enter time in format 00:00:> ')
                TimeKeeper.convert_time(tz_from, tz_to, _time)
            elif operation == '3':
                your_friend_time = input('Enter time from another time zone in format 00:00:> ')
                print(f'{your_friend_time} of {tz} time zone corresponds to ... your local time')

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
                logging.debug(data == list())
                print('no such entries')
                self.start()
            else:
                print(data[0])
                if data[0][4]:
                    contact_time_now = TimeKeeper.show_current_time(data[0][4])
                else:
                    contact_time_now = TimeKeeper.show_current_time(data[0][5])
                if contact_time_now:
                    print(f'time for {data_for_search.capitalize()} now: {contact_time_now}')

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
            self.change_contact()
        record_to_change = InfoBase.select_row('contact_name', contact_to_change)
        print(record_to_change)
        new_record = [x for x in record_to_change[0]]
        change = input('\nchoose action:\ndel - delete contact\nccc - change contact\nbbb - go back\n> ')
        if change == 'bbb':
            self.start()
        elif change == 'del':
            InfoBase.delete_row(contact_to_change)
            print('Contact deleted')
        elif change == 'ccc':
            while True:
                print('''What field do you wish to change:
                0 - contact name
                1 - platform
                2 - comment
                3 - location
                4 - zone name
                5 - difference to UTC
                sss - save changes''')
                field_no = input()
                try:
                    if field_no == 'sss':
                        InfoBase.delete_row(contact_to_change)
                        InfoBase.transfer_to_sql(*new_record)
                        print('saved')
                        break
                    print(record_to_change[0][int(field_no)])
                    new_value = input('Change to:> ')
                    print(new_record)
                    if field_no == '5':  # difference to UTC keep as float
                        new_record[int(field_no)] = float(new_value)
                    elif field_no == '4':  # zone name
                        new_record[int(field_no)] = new_value.upper()
                    else:
                        new_record[int(field_no)] = new_value.capitalize()
                    print(new_record)
                except ValueError:
                    print('wrong command')
                    continue

    actions = {'00': time_operation,
               '11': add_contact,
               '22': see_info,
               '33': change_contact,
               }

    @staticmethod
    def check_if_db_empty():
        return 0 if not InfoBase.select_all() else 1

    def start(self):
        sql_operation = InfoBase()
        sql_operation.create_table()
        print('Contact base is empty' if self.check_if_db_empty() == 0 else '')
        while True:
            print('\nchoose action:\n00.time operation\n11.add contact\n22.see contact info'
                  '\n33.change contact\n44.export contacts\n55.exit')
            self.command = input('> ')
            if self.command == '55':
                exit()
            elif self.command == '000':
                sql_operation.print_contact_table()
            elif self.command == '44':
                InfoBase.export_contact_book()
            elif self.command not in list(ContactsKeeper.actions.keys()):
                print('Incorrect command. Enter 00, 11, 22, 33 or 44')
            else:
                ContactsKeeper.actions[self.command.lower()](self)


def main():
    logging.info('+++++new start++++++++++++++++++++++++++++++++++++++++')
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
    new.start()


if __name__ == '__main__':
    main()
