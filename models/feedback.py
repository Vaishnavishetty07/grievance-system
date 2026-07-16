from grievance_system.services.supabase_client import supabase
class Feedback:
    TABLE = 'feedback'

    @staticmethod
    def create(complaint_id, rating, comment):
        try:
            return supabase.table(Feedback.TABLE).insert({
                'complaint_id': complaint_id,
                'rating': rating,
                'comment': comment
            }).execute()
        except Exception as e:
            print(f"Error creating feedback: {e}")
            return None

    @staticmethod
    def get_by_complaint(complaint_id):
        try:
            result = supabase.table(Feedback.TABLE).select('*').eq('complaint_id', complaint_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching feedback: {e}")
            return None