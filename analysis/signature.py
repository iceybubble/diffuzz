import re
from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, ConfigDict


class SignatureMatch(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vuln_type: str
    matched_pattern: str


class SignatureDB:
    def __init__(self, waf_signatures: list[dict], vuln_signatures: list[dict]):
        self.waf_signatures = [
            (item["name"], re.compile(item["pattern"], re.IGNORECASE))
            for item in waf_signatures
        ]
        self.vuln_signatures = [
            (item["vuln_type"], re.compile(item["pattern"], re.IGNORECASE))
            for item in vuln_signatures
        ]

    @classmethod
    def load_from_yaml(cls, filepath: str | Path) -> "SignatureDB":
        path = Path(filepath)
        if not path.is_absolute():
            # Resolve relative to data directory or repository root if needed
            base_dir = Path(__file__).parent.parent
            path = base_dir / filepath

        content = yaml.safe_load(path.read_text())
        waf_sigs = content.get("waf_signatures", [])
        vuln_sigs = content.get("vulnerability_signatures", [])
        return cls(waf_signatures=waf_sigs, vuln_signatures=vuln_sigs)

    def is_waf_blocked(self, body: str) -> bool:
        for _, regex in self.waf_signatures:
            if regex.search(body):
                return True
        return False

    def match(self, body: str) -> Optional[SignatureMatch]:
        # WAF check first to suppress false positives
        if self.is_waf_blocked(body):
            return None

        for vuln_type, regex in self.vuln_signatures:
            m = regex.search(body)
            if m:
                return SignatureMatch(vuln_type=vuln_type, matched_pattern=m.group(0))
        return None
