from pydantic import BaseModel, ConfigDict, Field


class _SonarQubeBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class SonarQubeProject(_SonarQubeBase):
    key: str
    name: str
    qualifier: str


class SonarQubeToken(_SonarQubeBase):
    name: str
    token: str
    type: str


class QualityGateCondition(_SonarQubeBase):
    status: str
    metric_key: str = Field(alias="metricKey")
    comparator: str
    error_threshold: str = Field(alias="errorThreshold")
    actual_value: str = Field(alias="actualValue")


class QualityGateStatus(_SonarQubeBase):
    status: str
    conditions: list[QualityGateCondition]
