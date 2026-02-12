from pydantic import BaseModel
from typing import List

class ForwardGuidance(BaseModel):
    revenue: str
    margin: str
    capex: str


class EarningsOutput(BaseModel):
    document_type: str
    management_tone: str
    confidence_level: str
    confidence_reasoning: str
    key_positives: List[str]
    key_concerns: List[str]
    forward_guidance: ForwardGuidance
    capacity_utilization: str
    growth_initiatives: List[str]

