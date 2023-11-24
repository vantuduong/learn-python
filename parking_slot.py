def check_frequent_parking_number(value):
    result = 0
    for position in range(0, 4):
        result += int(value[position]) * (5 - position)

    return (11 - (result % 11)) == int(value[4])


class ParkingSlot:

    def __init__(self, identity, arrival_time, frequent_parking_number, pickup_time=None):
        self.__identity = identity
        self.__arrival_time = arrival_time
        self.frequent_parking_number = frequent_parking_number
        self.pickup_time = pickup_time

    @property
    def identity(self):
        return self.__identity

    @property
    def arrival_time(self):
        return self.__arrival_time

    @property
    def pickup_time(self):
        return self.__pickup_time

    @pickup_time.setter
    def pickup_time(self, value):
        if value and value < self.arrival_time:
            raise Exception('Leave time must be greater than arrival time')

        self.__pickup_time = value

    @property
    def frequent_parking_number(self):
        return self.__frequent_parking_number

    @frequent_parking_number.setter
    def frequent_parking_number(self, value):
        if not value or (len(value) == 5 and check_frequent_parking_number(value)):
            self.__frequent_parking_number = value
        else:
            raise Exception('Invalid frequent parking number')

    def get_parking_time(self):
        if not self.pickup_time:
            raise Exception('The car has not been picked up yet')


