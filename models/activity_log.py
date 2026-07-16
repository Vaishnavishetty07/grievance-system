from grievance_system.services.supabase_client import supabase

class ActivityLog:
    TABLE = 'activity_logs'

    @staticmethod
    def record(complaint_id, action, performed_by):
        try:
            return supabase.table(ActivityLog.TABLE).insert({
                'complaint_id': complaint_id,
                'action': action,
                'performed_by': performed_by
            }).execute()
        except Exception as e:
            print(f"Error recording log: {e}")
            return None

    @staticmethod
    def get_by_complaint(complaint_id):
        try:
            result = supabase.table(ActivityLog.TABLE).select('*').eq('complaint_id', complaint_id).order('timestamp', desc=False).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching logs: {e}")
            return []