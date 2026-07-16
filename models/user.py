from grievance_system.services.supabase_client import supabase

class User:
    TABLE = 'users'

    @staticmethod
    def create(name, email, password_hash, role, hostel_block='', room_number=''):
        try:
            result = supabase.table(User.TABLE).insert({
                'name': name,
                'email': email,
                'password': password_hash,
                'role': role,
                'hostel_block': hostel_block,
                'room_number': room_number
            }).execute()
            return result
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        try:
            result = supabase.table(User.TABLE).select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        try:
            result = supabase.table(User.TABLE).select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching user by id: {e}")
            return None

    @staticmethod
    def get_all_staff():
        try:
            result = supabase.table(User.TABLE).select('*').eq('role', 'Staff').execute()
            return result.data
        except Exception as e:
            print(f"Error fetching staff: {e}")
            return []