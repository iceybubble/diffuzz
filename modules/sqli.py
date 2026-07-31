from pydantic import BaseModel
from typing import Optional

class Finding(BaseModel):
    vuln_type: str
    param: str
    evidence: str

class SQLiModule:
    def __init__(self, engine):
        self.engine = engine

    async def run(self, base_url: str, params: dict) -> list[Finding]:
        findings = []
        for param, val in params.items():
            resp = await self.engine.send(url=base_url, params={param: val + "'"})
            if resp and "syntax" in resp.body.lower():
                findings.append(Finding(
                    vuln_type="sqli",
                    param=param,
                    evidence=resp.body
                ))
        return findings
