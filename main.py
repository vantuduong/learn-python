from parking_slot import ParkingSlot
from parking import park, pickup, get_history

options = ('park', 'pickup', 'history')

def input_parking_info() -> ParkingSlot:
    car_identity = ''
    arrival = ''

    while not car_identity:
        car_identity = input('Input identity:')

    while not arrival:
        arrival = input('Input arrival time:')

    frequent_parking_number = input('Input frequent parking number:')

    return ParkingSlot(car_identity, arrival, frequent_parking_number)

if __name__ == '__main__':
    option = ''

    while not option or option not in options:
        option = input('Please select option park, pickup or history: ')

        try:
            if option == 'park':
                parking_slot = input_parking_info()
                park(parking_slot)
                print('Park successfully')

            elif option == 'pickup':
                identity = ''
                while not identity:
                    identity = input('Input identity:')
                pickup(identity)
                print('Pickup successfully')

            elif option == 'history':
                identity = ''
                while not identity:
                    identity = input('Input identity:')
                print(get_history(identity))
        except Exception as e:
            print(e)
        finally:
            option = ''



