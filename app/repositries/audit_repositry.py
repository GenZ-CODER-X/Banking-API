from app.models.audit import Audit

class Audit_repositry():
    def create_audit(db,audit_details):
        audit_entry_query=Audit(**audit_details)
        db.add(audit_entry_query)
        db.flush()
        return audit_entry_query

