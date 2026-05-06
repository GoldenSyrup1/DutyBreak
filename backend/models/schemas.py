from pydantic import BaseModel
from typing import Optional


class ComplianceRequest(BaseModel):
    product_description: str
    origin_country: str       # ISO 3166-1 alpha-2, e.g. "VN"
    destination_country: str  # ISO 3166-1 alpha-2, e.g. "DE"
    supplier_name: Optional[str] = None


class TariffData(BaseModel):
    hs_code: str
    mfn_rate: Optional[str] = None
    preferential_rate: Optional[str] = None
    trade_agreement: Optional[str] = None
    estimated_duty_usd: Optional[float] = None


class ComplianceData(BaseModel):
    required_certificates: list[str] = []
    import_restrictions: list[str] = []
    labeling_requirements: list[str] = []
    estimated_processing_days: Optional[int] = None


class SanctionsData(BaseModel):
    is_sanctioned: bool = False
    risk_level: str = "LOW"   # LOW / MEDIUM / HIGH / BLOCKED
    flags: list[str] = []
    screened_lists: list[str] = []


class ComplianceBrief(BaseModel):
    product_description: str
    hs_code: str
    origin_country: str
    destination_country: str
    tariff: TariffData
    compliance: ComplianceData
    sanctions: SanctionsData
    summary: str
    action_items: list[str] = []
    overall_risk: str = "LOW"
