from grievance_system.services.supabase_client import supabase

class Complaint:
    TABLE = 'complaints'

    @staticmethod
    def create(title, description, category, priority, summary, image_url, student_id):
        try:
            result = supabase.table(Complaint.TABLE).insert({
                'title': title,
                'description': description,
                'category': category,
                'priority': priority,
                'summary': summary,
                'image_url': image_url,
                'student_id': student_id,
                'status': 'Pending'
            }).execute()
            return result
        except Exception as e:
            print(f"Error creating complaint: {e}")
            return None

    @staticmethod
    def get_all():
        try:
            result = supabase.table(Complaint.TABLE).select('*').order('created_at', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching all complaints: {e}")
            return []

    @staticmethod
    def get_by_student(student_id):
        try:
            result = supabase.table(Complaint.TABLE).select('*').eq('student_id', student_id).order('created_at', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching student complaints: {e}")
            return []

    @staticmethod
    def get_by_staff(staff_id):
        try:
            result = supabase.table(Complaint.TABLE).select('*').eq('assigned_staff', staff_id).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching staff complaints: {e}")
            return []

    @staticmethod
    def get_by_id(complaint_id):
        try:
            result = supabase.table(Complaint.TABLE).select('*').eq('id', complaint_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching complaint: {e}")
            return None

    @staticmethod
    def assign_staff(complaint_id, staff_id):
        try:
            return supabase.table(Complaint.TABLE).update({
                'assigned_staff': staff_id,
                'status': 'In Progress'
            }).eq('id', complaint_id).execute()
        except Exception as e:
            print(f"Error assigning staff: {e}")
            return None

    @staticmethod
    def update_status(complaint_id, status):
        try:
            return supabase.table(Complaint.TABLE).update({
                'status': status
            }).eq('id', complaint_id).execute()
        except Exception as e:
            print(f"Error updating status: {e}")
            return None