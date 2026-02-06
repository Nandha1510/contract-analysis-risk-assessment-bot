import json
import datetime
from threading import Lock
from typing import Dict, List
import hashlib


class AuditLogger:
    """Advanced audit logging with detailed event tracking and compliance."""
    
    def __init__(self, path: str = "audit_logs.json"):
        self.path = path
        self.lock = Lock()
        self.session_id = hashlib.md5(datetime.datetime.utcnow().isoformat().encode()).hexdigest()[:12]

    def log_event(self, event_type: str, payload: dict, severity: str = "INFO", user: str = "anonymous"):
        """Log an event with detailed metadata."""
        
        entry = {
            "id": self._generate_event_id(),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "session_id": self.session_id,
            "event": event_type,
            "severity": severity,
            "user": user,
            "payload": payload,
        }
        
        with self.lock:
            try:
                existing = []
                with open(self.path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
            
            existing.append(entry)
            
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        timestamp = datetime.datetime.utcnow().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]

    def log_contract_upload(self, filename: str, file_size: int, contract_type: str = None):
        """Log contract upload event."""
        self.log_event(
            "contract_uploaded",
            {
                "filename": filename,
                "size_bytes": file_size,
                "contract_type": contract_type,
            },
            severity="INFO"
        )

    def log_risk_analysis(self, filename: str, high_risk_count: int, medium_risk_count: int, overall_risk: str):
        """Log risk analysis completion."""
        self.log_event(
            "risk_analysis_completed",
            {
                "filename": filename,
                "high_risk_clauses": high_risk_count,
                "medium_risk_clauses": medium_risk_count,
                "overall_risk": overall_risk,
            },
            severity="INFO"
        )

    def log_compliance_check(self, filename: str, missing_issues: int, total_checks: int):
        """Log compliance check."""
        self.log_event(
            "compliance_check",
            {
                "filename": filename,
                "missing_clauses": missing_issues,
                "total_checks": total_checks,
                "compliance_percentage": round((1 - missing_issues/total_checks) * 100, 2) if total_checks > 0 else 0,
            },
            severity="INFO"
        )

    def log_report_generation(self, filename: str, report_format: str):
        """Log report generation."""
        self.log_event(
            "report_generated",
            {
                "filename": filename,
                "format": report_format,
            },
            severity="INFO"
        )

    def log_error(self, error_message: str, context: str = ""):
        """Log error event."""
        self.log_event(
            "error",
            {
                "message": error_message,
                "context": context,
            },
            severity="ERROR"
        )

    def log_data_access(self, resource: str, action: str, user: str = "anonymous"):
        """Log data access for compliance."""
        self.log_event(
            "data_access",
            {
                "resource": resource,
                "action": action,
            },
            severity="INFO",
            user=user
        )

    def log_export(self, filename: str, format_type: str, record_count: int = 0):
        """Log data export for compliance."""
        self.log_event(
            "data_exported",
            {
                "filename": filename,
                "format": format_type,
                "record_count": record_count,
            },
            severity="INFO"
        )

    def get_audit_report(self, filters: Dict = None) -> List[Dict]:
        """Get audit logs with optional filtering."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            return []

        if not filters:
            return logs

        filtered = logs
        
        if "event_type" in filters:
            filtered = [log for log in filtered if log.get("event") == filters["event_type"]]
        
        if "severity" in filters:
            filtered = [log for log in filtered if log.get("severity") == filters["severity"]]
        
        if "start_date" in filters:
            filtered = [log for log in filtered if log.get("timestamp") >= filters["start_date"]]
        
        if "end_date" in filters:
            filtered = [log for log in filtered if log.get("timestamp") <= filters["end_date"]]

        return filtered

    def get_session_events(self, session_id: str = None) -> List[Dict]:
        """Get all events for a session."""
        session = session_id or self.session_id
        return self.get_audit_report({"session_id": session})

    def get_compliance_summary(self) -> Dict:
        """Get compliance audit summary."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            return {"status": "No logs available"}

        total_events = len(logs)
        events_by_type = {}
        errors_count = 0
        
        for log in logs:
            event_type = log.get("event", "unknown")
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
            
            if log.get("severity") == "ERROR":
                errors_count += 1

        return {
            "total_events": total_events,
            "total_errors": errors_count,
            "event_types": events_by_type,
            "error_rate_percent": round((errors_count / total_events * 100), 2) if total_events > 0 else 0,
            "first_event": logs[0].get("timestamp") if logs else None,
            "last_event": logs[-1].get("timestamp") if logs else None,
        }

