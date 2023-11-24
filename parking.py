import os

from parking_slot import ParkingSlot
from datetime import datetime, timedelta, time
from os import path

working_hour_price = {
    'weekday': 10,
    'saturday': 3,
    'sunday': 2,
}

working_hour_max_time = {
    'weekday': 2,
    'saturday': 4,
    'sunday': 8,
}

afternoon_to_midnight_price = 5
midnight_to_morning_price = 20


def park(parking_slot: ParkingSlot):
    f = open(f'parking_slots/{parking_slot.identity}.txt', "x")
    f.writelines([
        f'{parking_slot.identity}\n',
        f'{parking_slot.arrival_time}\n',
        f'{parking_slot.frequent_parking_number}',
    ])
    f.close()


def pickup(identity: str):
    f = open(f'parking_slots/{identity}.txt', "r")
    identity = f.readline().replace('\n', '')
    arrival_time = f.readline().replace('\n', '')
    frequent_parking_number = f.readline().replace('\n', '')
    f.close()
    parking_slot = ParkingSlot(identity, arrival_time, frequent_parking_number,
                               datetime.now().strftime('%Y-%m-%d %H:%M'))

    price = get_price(parking_slot)

    print(f'Price: {round(price, 2)}')
    amount_paid = 0
    total_payment = 0
    available_credit = 0
    file_lines = []

    if path.exists(f'histories/{identity}.txt'):
        f2 = open(f'histories/{identity}.txt', 'r')
        for line in f2:
            file_lines.append(line)

        total_payment = float (file_lines[0].replace('Total payment: $', '').replace('\n', ''))
        available_credit = float (file_lines[1].replace('Available credits: $', '').replace('\n', ''))
        f2.close()


    total_require_to_paid = price - available_credit
    while amount_paid < total_require_to_paid:
        amount_paid = float(input('Please in put amount paid: '))

    total_payment += price
    available_credit = (amount_paid + available_credit) - price

    if len(file_lines) == 0:
        file_lines.append(f'Total payment: ${total_payment}\n')
        file_lines.append(f'Available credits: ${available_credit}\n')
        file_lines.append(f'Parked dates:\n')
    else:
        file_lines[0] = f'Total payment: ${total_payment}\n'
        file_lines[1] = f'Available credits: ${available_credit}\n'
    file_lines.append(f'{parking_slot.arrival_time} - {parking_slot.pickup_time}\n')
    f3 = open(f'histories/{identity}.txt', 'w')
    f3.writelines(file_lines)
    f3.close()
    os.remove(f'parking_slots/{identity}.txt')


def get_price(parking_slot: ParkingSlot):
    time_list = get_time_list(
        datetime.strptime(parking_slot.arrival_time, '%Y-%m-%d %H:%M'),
        datetime.strptime(parking_slot.pickup_time, '%Y-%m-%d %H:%M')
    )

    total_price = 0
    for day_of_week in time_list:
        day = time_list[day_of_week]

        if day_of_week == 0:
            price = working_hour_price['sunday'] * (0.9 if parking_slot.frequent_parking_number else 1)
            max_hour = working_hour_max_time['sunday']
        elif day_of_week == 6:
            price = working_hour_price['saturday'] * (0.9 if parking_slot.frequent_parking_number else 1)
            max_hour = working_hour_max_time['saturday']
        else:
            price = working_hour_price['weekday'] * (0.9 if parking_slot.frequent_parking_number else 1)
            max_hour = working_hour_max_time['weekday']

        if day['working_hour_time'] <= max_hour:
            total_price += price * day['working_hour_time']
        else:
            total_price += price * max_hour + 2 * price * (day['working_hour_time'] - max_hour)

        total_price += afternoon_to_midnight_price * day['afternoon_to_midnight_time'] * (0.5 if parking_slot.frequent_parking_number else 1)
        total_price += (midnight_to_morning_price if day['midnight_to_morning_time'] else 0) * (0.5 if parking_slot.frequent_parking_number else 1)

    return total_price

def get_time_list(start_time: datetime, end_time: datetime):
    times = {}

    while start_time < end_time:
        day_of_week = start_time.strftime('%w')
        time_to_compare = datetime.combine(start_time, time.max)
        if time_to_compare > end_time:
            time_to_compare = end_time

        start_hour = start_time.hour
        end_hour = time_to_compare.hour + (1 if time_to_compare.minute > 0 else 0)
        day = times.get(day_of_week, {
            'working_hour_time': 0,
            'afternoon_to_midnight_time': 0,
            'midnight_to_morning_time': 0,
        })
        if start_hour < 8:
            day['midnight_to_morning_time'] += min(8, end_hour) - start_hour
            start_hour = 8

        if start_hour < 17 and start_hour < end_hour:
            day['working_hour_time'] += min(17, end_hour) - start_hour
            start_hour = 17

        if start_hour < end_hour:
            day['afternoon_to_midnight_time'] += min(24, end_hour) - start_hour
        times[day_of_week] = day

        start_time = datetime.combine(start_time + timedelta(days=1), time.min)

    return times

def get_history(identity: str):
    f3 = open(f'histories/{identity}.txt', 'r')
    history = f3.read()
    f3.close()

    return history
