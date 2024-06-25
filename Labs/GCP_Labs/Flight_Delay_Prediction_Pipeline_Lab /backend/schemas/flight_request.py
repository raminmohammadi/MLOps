from pydantic import BaseModel, Field
from typing import Optional


class FlightData(BaseModel):
    FL_DATE: str
    OP_CARRIER: str
    OP_CARRIER_FL_NUM: int
    ORIGIN: str
    DEST: str
    CRS_DEP_TIME: int
    DEP_TIME: Optional[float] = Field(default=None)
    DEP_DELAY: Optional[float] = Field(default=None)
    TAXI_OUT: Optional[float] = Field(default=None)
    WHEELS_OFF: Optional[float] = Field(default=None)
    WHEELS_ON: Optional[float] = Field(default=None)
    TAXI_IN: Optional[float] = Field(default=None)
    CRS_ARR_TIME: int
    ARR_TIME: Optional[float] = Field(default=None)
    ARR_DELAY: Optional[float] = Field(default=None)
    CANCELLED: Optional[float] = Field(default=None)
    CANCELLATION_CODE: Optional[str] = Field(default=None)
    DIVERTED: Optional[float] = Field(default=None)
    CRS_ELAPSED_TIME: Optional[float] = Field(default=None)
    ACTUAL_ELAPSED_TIME: Optional[float] = Field(default=None)
    AIR_TIME: Optional[float] = Field(default=None)
    DISTANCE: Optional[float] = Field(default=None)
    CARRIER_DELAY: Optional[float] = Field(default=None)
    WEATHER_DELAY: Optional[float] = Field(default=None)
    NAS_DELAY: Optional[float] = Field(default=None)
    SECURITY_DELAY: Optional[float] = Field(default=None)
    LATE_AIRCRAFT_DELAY: Optional[float] = Field(default=None)
