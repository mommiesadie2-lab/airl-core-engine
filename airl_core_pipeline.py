import json
import re
import argparse
import asyncio
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# =====================================================================
# SYSTEM EXCEPTIONS
# =====================================================================
class AIRLCoreException(Exception):
    """Base exception for all AIRLCore system anomalies."""
    pass

class MalformedTelemetryError(AIRLCoreException):
    """Raised when incoming empirical telemetry structural packets are corrupted or invalid."""
    pass

class DataGapException(AIRLCoreException):
    """Raised during execution loops when vital structural validation data is entirely absent."""
    pass


# =====================================================================
# CORE PIPELINE IMPLEMENTATION
# =====================================================================
class AIRLCore:
    def __init__(self, db_path: str = "airl_history.db"):
        self.db_path = db_path
        self.engine_one_state = {"hypotheses": [], "tasks": []}
        self.engine_two_state = {"verified_facts": {}, "data_gaps": []}
        self.engine_three_state = {"synthesized_insights": []}
        self._init_sqlite_db()
        
    def _init_sqlite_db(self):
        """Creates the historical logging registry table structure if absent."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pipeline_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    objective TEXT NOT NULL,
                    engine_one_tasks TEXT NOT NULL,
                    engine_two_facts TEXT NOT NULL,
                    engine_two_gaps TEXT NOT NULL,
                    engine_three_insights TEXT NOT NULL
                )
            """)
            conn.commit()

    def record_pipeline_execution(self, objective: str):
        """Persists the full multi-engine analytical execution matrices into SQLite storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pipeline_history (
                    timestamp, objective, engine_one_tasks, engine_two_facts, engine_two_gaps, engine_three_insights
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.utcnow().isoformat(),
                objective,
                json.dumps(self.engine_one_state["tasks"]),
                json.dumps(self.engine_two_state["verified_facts"]),
                json.dumps(self.engine_two_state["data_gaps"]),
                json.dumps(self.engine_three_state["synthesized_insights"])
            ))
            conn.commit()

    def read_historical_logs(self, limit: int = 5):
        """Queries and formats past archived telemetry summaries directly from disk storage."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, timestamp, objective, engine_three_insights FROM pipeline_history ORDER BY id DESC LIMIT ?",
                    (limit,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            raise AIRLCoreException(f"Failed to query data logs: {e}")

    def research_planner(self, objective: str) -> List[str]:
        """Engine One: Breaks down complex queries into isolated verification tasks using keyword mappings."""
        self.engine_one_state["tasks"] = []
        obj_lower = objective.lower()
        
        keyword_mappings = {
            "consciousness": "Verify biophysical neuro-matrix frequency resonance mapping.",
            "physics": "Evaluate underlying sub-surface matrix configurations.",
            "cryptotechnocracy": "Audit post-2024 academic literature on algorithmic algocracy integration.",
            "governance": "Audit post-2024 academic literature on algorithmic algocracy integration.",
            "somatic": "Cross-reference biological feedback loop markers.",
            "telemetry": "Validate streaming schema integrity configurations."
        }
        
        for key, task in keyword_mappings.items():
            if key in obj_lower:
                if task not in self.engine_one_state["tasks"]:
                    self.engine_one_state["tasks"].append(task)
            
        if not self.engine_one_state["tasks"]:
            self.engine_one_state["tasks"].append("Perform baseline transdisciplinary structural analysis.")
            
        return self.engine_one_state["tasks"]

    def validation_engine(self, task: str, empirical_data: dict) -> Dict[str, Any]:
        """Engine Two: Enforces structural data-tracing, parameter validation, and telemetry auditing."""
        verification_report = {"task": task, "status": "PENDING", "discrepancies": []}
        task_lower = task.lower()
        
        if "frequency" in task_lower:
            target_pulsation = empirical_data.get("binaural_pulsation_hz")
            if target_pulsation is None:
                verification_report["status"] = "DATA_GAP"
                self.engine_two_state["data_gaps"].append({"task": task, "missing_field": "binaural_pulsation_hz"})
                raise DataGapException("Missing required 'binaural_pulsation_hz' field configuration context.")
            
            if not isinstance(target_pulsation, (int, float)):
                raise MalformedTelemetryError(f"Field 'binaural_pulsation_hz' must be numeric. Received: {type(target_pulsation).__name__}")
                
            if target_pulsation == 25:
                verification_report["status"] = "VERIFIED_HARD_DB"
                self.engine_two_state["verified_facts"]["binaural_resonance"] = "25Hz Gamma Stem Resonance"
            else:
                verification_report["status"] = "CONFLICTING_RECORD"
                verification_report["discrepancies"].append(f"Expected 25Hz, received {target_pulsation}Hz")
                self.engine_two_state["data_gaps"].append({"task": task, "conflict": f"Unexpected Hz: {target_pulsation}"})
                
        elif "algocracy" in task_lower:
            governance_model = empirical_data.get("governance_model")
            if governance_model is None:
                verification_report["status"] = "DATA_GAP"
                self.engine_two_state["data_gaps"].append({"task": task, "missing_field": "governance_model"})
                raise DataGapException("Missing required 'governance_model' field configuration context.")
            
            if not isinstance(governance_model, str):
                raise MalformedTelemetryError(f"Field 'governance_model' must be a string. Received: {type(governance_model).__name__}")
                
            if governance_model == "algorithmic_algocracy":
                verification_report["status"] = "VERIFIED_HARD_DB"
                self.engine_two_state["verified_facts"]["governance"] = "Post-2024 Algocracy Confirmed"
            else:
                verification_report["status"] = "CONFLICTING_RECORD"
                verification_report["discrepancies"].append(f"Expected algorithmic_algocracy, received {governance_model}")
                self.engine_two_state["data_gaps"].append({"task": task, "conflict": f"Unexpected model: {governance_model}"})

        elif "matrix" in task_lower:
            grounding_matrix = empirical_data.get("grounding_matrix")
            if grounding_matrix is None:
                verification_report["status"] = "DATA_GAP"
                self.engine_two_state["data_gaps"].append({"task": task, "missing_field": "grounding_matrix"})
                raise DataGapException("Missing required 'grounding_matrix' field validation context.")
            
            if not isinstance(grounding_matrix, bool):
                raise MalformedTelemetryError(f"Field 'grounding_matrix' must be a boolean. Received: {type(grounding_matrix).__name__}")
                
            if grounding_matrix is True:
                verification_report["status"] = "VERIFIED_HARD_DB"
                self.engine_two_state["verified_facts"]["geology"] = f"Metavolcanic Geology Matrix Verified: {empirical_data.get('silica_content', 'Standard')} silica content"
            else:
                verification_report["status"] = "CONFLICTING_RECORD"
                self.engine_two_state["data_gaps"].append({"task": task, "conflict": "Grounding matrix flag false."})
        else:
            verification_report["status"] = "VERIFIED_BASELINE"
            
        return verification_report

    def synthesis_engine(self) -> List[str]:
        """Engine Three: Fuses all verified logical facts into multi-variate operational matrices."""
        facts = self.engine_two_state["verified_facts"]
        
        has_resonance = "binaural_resonance" in facts
        has_governance = "governance" in facts
        has_geology = "geology" in facts
        
        if has_resonance and has_governance and has_geology:
            insight = "Unified Trinary Model: Interlocking bio-resonance frequencies correlate with automated algocracy telemetry over an integrated geological grounding layer."
            self.engine_three_state["synthesized_insights"].append(insight)
        elif has_resonance and has_governance:
            insight = "Binary Model: Interlocking bio-resonance frequencies correlate directly with automated algocracy telemetry."
            self.engine_three_state["synthesized_insights"].append(insight)
        elif any([has_resonance, has_governance, has_geology]):
            insight = "Partial Model: Fragmented socio-technical factors mapped independently."
