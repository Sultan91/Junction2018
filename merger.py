import csv
import datetime
from typing import List, Dict, Tuple


class Record:
    headers = ['timestamp', 'humidity', 'co2', 'temperature', 'sensor_r', 'sensor_l', 'thermal', 'day_of_week']

    def __init__(self, _timestamp: datetime, _thermal: float):
        self.timestamp: datetime = _timestamp
        self.thermal: float = _thermal
        self.co2 = None
        self.humidity = None
        self.temperature = None
        self.sensor_r: int = None
        self.sensor_l: int = None
        self.week_day: int = None

    def to_dict(self):
        time_template = '%Y-%m-%dT%H:%M:%S.%fZ'
        return {
            'timestamp': self.timestamp.strftime(time_template),
            'humidity': self.humidity,
            'co2': self.co2,
            'temperature': self.temperature,
            'sensor_r': self.sensor_r,
            'sensor_l': self.sensor_l,
            'thermal': self.thermal,
            'day_of_week': self.week_day
        }


def read_thermal() -> List[Record]:
    main_records = []
    with open('csv/thermal.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            time_template = '%Y-%m-%dT%H:%M:%SZ'
            t_s = datetime.datetime.strptime(row['timestamp'], time_template).replace(second=0)
            therml = float(row['thermal'])
            main_records.append(Record(t_s, therml))
    return main_records


def read_occ() -> Dict[datetime.datetime, Tuple[int, int]]:
    occ_dict_records = {}
    with open('csv/occ.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            time_template = '%Y-%m-%d %H:%M:%S'
            t_s = datetime.datetime.strptime(row['timestamp'], time_template)
            sensor_r_val = int(row['sensor_r'])
            sensor_l_val = int(row['sensor_l'])
            occ_dict_records[t_s] = (sensor_r_val, sensor_l_val)
    return occ_dict_records


def read_ds1():
    ds1_list_records = {}
    with open('csv/ds1.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            parsed_time = row['time'].split(':')
            h = int(parsed_time[0])
            m = int(parsed_time[1])
            t_s = datetime.datetime(2018, int(row['month']), int(row['day']), h, m, 0)
            co2 = int(row['co2'])
            humidity = float(row['humidity'])
            temperature = float(row['temperature'])
            week_d = int(row['timestamp'])
            ds1_list_records[t_s] = (co2, humidity, temperature, week_d)
    return ds1_list_records


def get_term_with_occ(records_list: List[Record], occ_dict):
    for rec in records_list:
        if rec.timestamp in occ_dict:
            # occ_dict[rec.timestamp] is a tuple of (right, left) sensors
            rec.sensor_r = occ_dict[rec.timestamp][0]
            rec.sensor_l = occ_dict[rec.timestamp][1]
        else:
            # interpolation process
            sum_r = 0
            sum_l = 0
            count = 1
            for m in range(-8, 8):
                tmp_d_t = rec.timestamp + datetime.timedelta(minutes=m)
                if tmp_d_t in occ_dict:
                    sum_r += occ_dict[tmp_d_t][0]
                    sum_l += occ_dict[tmp_d_t][1]
                    count += 1
            if sum_r:
                rec.sensor_r = int(sum_r // count)
            if sum_l:
                rec.sensor_l = int(sum_l // count)
            if count > 1:
                continue
            print(f'Error, Timestamp: {rec.timestamp} not in occ.csv')

    return records_list


def get_records_with_ds1(records_list: List[Record], ds1):
    for rec in records_list:
        if rec.timestamp in ds1:
            # occ_dict[rec.timestamp] is a tuple of (co2, humidity, temperature, week_day) sensors
            rec.co2 = ds1[rec.timestamp][0]
            rec.humidity = ds1[rec.timestamp][1]
            rec.temperature = ds1[rec.timestamp][2]
            rec.week_day = ds1[rec.timestamp][3]
        else:
            sum_co2 = 0
            sum_humidity = 0
            sum_temperature = 0
            count = 1
            for m in range(-8, 8):
                tmp_d_t = rec.timestamp + datetime.timedelta(minutes=m)
                if tmp_d_t in ds1:
                    sum_co2 += ds1[tmp_d_t][0]
                    sum_humidity += ds1[tmp_d_t][1]
                    sum_temperature += ds1[tmp_d_t][2]
                    count += 1
            if sum_co2:
                rec.co2 = int(sum_co2 / count)
            if sum_humidity:
                rec.humidity = sum_humidity / count
            if sum_temperature:
                rec.temperature = sum_temperature / count
            if count > 1:
                continue
            print(f'Error, Timestamp: {rec.timestamp} not in ds1.csv')

    return records_list


if __name__ == '__main__':
    term = read_thermal()
    occ = read_occ()
    ds1 = read_ds1()

    records = get_term_with_occ(term, occ)

    records_final = get_records_with_ds1(records, ds1)

    with open('final.csv', 'w') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=Record.headers)
        csv_writer.writeheader()
        for rec in records_final:
            csv_writer.writerow(rec.to_dict())

    print(records_final)
