# utils for TimeZ Django ver ($TimeZoneReminder) application
import datetime
# import logging
import os
import pytz
import re
import shutil
import sqlite3
import time
from dateutil.tz import tzoffset, tz


# logging.basicConfig(filename='tzr.log', level=logging.DEBUG, filemode='a',
#                     format='%(levelname)s - %(message)s')


class InfoBase:
    def __init__(self):
        self.n = 0

    @staticmethod
    def specify_destination():
        """Supporting method for def export_contact_book()"""
        path = input("Specify path to location for saving Contacts' Book:> ")
        folder = input('Enter name for folder(if necessary to create):> ')
        windows = input('Is Windows - your OS ? y/n:> ')
        if windows == 'y':
            full_path = os.path.join(path, folder).strip() + '\\'
        else:
            full_path = os.path.join(path, folder).strip() + '/'
        if not os.access(full_path, os.F_OK):
            try:
                os.mkdir(full_path)
            except OSError:
                print(f'Cannot create {full_path} so let`s use {os.getcwd()}.')
                return os.getcwd()
        return full_path

    @staticmethod
    def create_csv_from_sql():
        """Write .csv-file with data from tzrContactBook.db inside working directory;
        Supporting method for def export_contact_book()"""
        data = 'InfoBase.select_all()'
        file_name = 'tzr_contacts.csv'
        with open(file_name, 'w', encoding='utf-8') as out_file:
            out_file.write("Time Zone Reminder / Contacts' Book\n")
            out_file.write('contact_name,platform,comment,location,zone_name,utc_offset\n')
            for row in sorted(data):
                out_file.write(';'.join(list(map(str, row))) + '\n')
        return file_name

    @staticmethod
    def export_contact_book():
        """Get path for saving exported data and copy original .csv-file there;
        Check if export file exists in designated location; Remove original .csv-file"""
        file_name = InfoBase.create_csv_from_sql()
        dst_folder = InfoBase.specify_destination()
        try:
            shutil.copy(file_name, dst_folder)
            if 'tzr_contacts.csv' in os.listdir(dst_folder):
                print(f'{file_name} is successfully saved to {dst_folder}.')
                os.remove(file_name)
        except Exception as e:
            # logging.debug(e)
            print(f'Cannot save file to {dst_folder} so {file_name} is successfully saved to {os.getcwd()}')


def timer(func):
    def wrapper(func_argument):
        start = time.time()
        func(func_argument)
        end = time.time()
        # logging.info('def ... ran ' + str(end - start) + ' seconds')
    return wrapper


class TimeKeeper:
    def __init__(self):
        self.command = ''
        self.call = 0

    tz_short_names = {'UTC': 'Etc/UTC',
                      'ART': 'America/Argentina/Buenos_Aires',
                      'CST': 'US/Central',
                      'EST': 'US/Eastern',
                      'IST': 'Asia/Kolkata',
                      'JST': 'Asia/Tokyo',
                      'MSK': 'Europe/Moscow',
                      'PST': 'US/Pacific',
                      'TURKEY': 'Europe/Istanbul'
                      }

    def __repr__(self):
        return 'TimeZ app recognizes following short names for time zones:'

    def __str__(self):
        return TimeKeeper.tz_short_names

    @staticmethod
    def calculate_time(time_obj, time_interval: list) -> str:
        """ how much time will it be in ..2 hours?
        """
        # logging.info(f'***def calculate_time({time.strftime("%H:%M", time_obj)}, {time_interval})')
        print(time_obj.strftime('%H:%M'))
        time0 = list(map(int, time_obj.strftime('%H:%M').split(':')))
        print(time0)
        hours, minutes = time0[0], time0[1]
        hours2, minutes2 = hours + time_interval[0], minutes + time_interval[1]
        time2 = datetime.timedelta(hours=hours2, minutes=minutes2)
        # logging.debug(str(time2)[:5])
        return f"In {time_interval[0]} hours {time_interval[1]} minutes it'll be: {str(time2)[:5]}"
        # return str(time2)[:5]

    @staticmethod
    def define_tzinfo(tz_data):
        try:  # define tzinfo from number:
            # both options work:
            tz_ = datetime.timezone(datetime.timedelta(hours=float(tz_data)))
            # tz_ = tzoffset(None, int(float(tz_data) * 3600))
            return tz_
        except ValueError:  # define tzinfo from name:
            try:
                tz_ = pytz.timezone(tz_data)
                # tz_ = pytz.timezone(TimeKeeper.tz_short_names[tz_data.upper()])
                return tz_
            except KeyError:
                print(f'there are no {tz_data} time zone in Olsen database. Try again with offset')

    @staticmethod
    def get_current_time(tz_data):
        """Return current local time in a time zone as datetime object"""
        tz_ = TimeKeeper.define_tzinfo(tz_data)
        return datetime.datetime.now(tz_)

    @staticmethod
    def date_constructor(zone_info, date: list, time0: list):
        """Return time zone-aware object"""
        # logging.info(f'***def date_constructor({zone_info}, {date}, {time0})')
        try:
            return datetime.datetime(date[0], date[1], date[2], time0[0], time0[1], 0,
                                     tzinfo=zone_info)  # in seconds
        except ValueError:
            return zone_info.localize(datetime.datetime(date[0], date[1], date[2], time0[0], time0[1]))

    @staticmethod
    def display_offset(offset: float) -> str:
        pass

    @staticmethod
    def time_operation_0(time_period: list, tz_data) -> str:
        """0-display the time that will come after a certain time period"""
        # current_local_time = time.localtime()
        current_local_time = TimeKeeper.get_current_time(tz_data)
        # print(f"In {time_period[0]} hours {time_period[1]} minutes it'll be:")
        return TimeKeeper.calculate_time(current_local_time, list(map(int, time_period)))

    @staticmethod
    def time_operation_1(tz_data) -> str:
        """Return current time in {tz_data} time zone as tring"""
        return TimeKeeper.get_current_time(tz_data).strftime('%d-%m-%Y %H:%M %Z')

    @staticmethod
    def time_operation_2a(time_, tz_from, tz_to, from_local):
        # tz_from, tz_to - raw data from user input(from html form of Profile model)
        tz_from_ = TimeKeeper.define_tzinfo(tz_from)
        tz_to_ = TimeKeeper.define_tzinfo(tz_to)
        time0 = list(map(int, time_.split(':')))
        date = list(map(int, datetime.datetime.now().strftime('%Y-%m-%d').split('-')))  # [2022, 6, 29]
        dt = TimeKeeper.date_constructor(tz_from_, date, time0)
        print(dt)
        if not dt:
            return False
        dt_utc = dt.astimezone(pytz.utc)
        print(dt_utc)
        dt_converted = dt_utc.astimezone(tz=tz_to_)
        print(dt_converted)
        if from_local == 'y':
            return f"[{dt.strftime('%H:%M %d-%m-%Y')}] your local time = " \
                   f"[{dt_converted.strftime('%H:%M %d-%m-%Y %z %Z')}] time zone."
        else:
            return f"[{dt.strftime('%H:%M %d-%m-%Y %z %Z')}] time zone = " \
                   f"[{dt_converted.strftime('%H:%M %d-%m-%Y ')}] your local time."

