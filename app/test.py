from utils.get_user_data import get_database_reference

ref = get_database_reference('/ride_data').get()

for i, v in ref.items():
    print(i)