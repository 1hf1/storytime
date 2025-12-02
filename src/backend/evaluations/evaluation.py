import json
import os

REPORT_STORAGE_DIR = "backend/evaluations/json_storage"
class EvaluationReport:
    def __init__(self, story):
        self.story = story
        self.accuracy_proportion = None
        self.citations_proportion = None
        self.report = {"accuracy_report": {"Metric": self.accuracy_proportion, "Report": ""}, "citations_report": {"Metric": self.citations_proportion, "Report" : ""}}
    def update_report(self, accuracy_proportion: float = None, citations_proportion: float = None, accuracy_report: str = None, citations_report: str = None):
        if accuracy_proportion is not None:
            self.report["accuracy_report"]["Metric"] = accuracy_proportion
        if accuracy_report is not None:
            self.report["accuracy_report"]["Report"] = accuracy_report
        if citations_proportion is not None:
            self.report["citations_report"]["Metric"] = citations_proportion
        if citations_report is not None:
            self.report["citations_report"]["Report"] = citations_report
    def save_report(self, report_name: str):
        report_path = os.path.join(REPORT_STORAGE_DIR, report_name + ".json")
        os.makedirs(REPORT_STORAGE_DIR, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(self.report, f)
    def to_json(self):
        """Return the evaluation report as a JSON-serializable dict."""
        return self.report