from utils.get_user_data import get_database_reference

ref = get_database_reference('/users')
print(ref.get())