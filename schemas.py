from enum import Enum
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field

# Define enums for extraction.
class LoginStatus(str, Enum):
    successful = "successful"
    blocked = "blocked"
    failed = "failed"
    in_progress = "in_progress"
    other = "other"

class EnergyType(str, Enum):
    electricity = "electricity"
    natural_gas = "natural_gas"
    other = "other"

class UsageUnits(str, Enum):
    kWh = "kWh"
    therms = "therms"
    other = "other"

# Define a Pydantic model for each category of data.
class AccountData(BaseModel):
    account_id: Optional[str] = Field(None, description="The unique identifier for the utility account.")
    account_status: Optional[str] = Field(None, description="The current status of the account, e.g., 'active' or 'inactive'.")
    login_status: Optional[LoginStatus] = Field(None, description="The status of the login attempt.")

class BillingData(BaseModel):
    amount_due: Optional[float] = Field(None, description="The total amount currently due on the account.")
    due_date: Optional[date] = Field(None, description="The date the current bill is due in YYYY-MM-DD format.")
    past_due_amount: Optional[float] = Field(None, description="Any amount that is past due.")
    last_payment_date: Optional[date] = Field(None, description="The date of the most recent payment in YYYY-MM-DD format.")
    last_payment_amount: Optional[float] = Field(None, description="The amount of the last payment.")
    energy_type: Optional[EnergyType] = Field(None, description="The type of energy service billed.")
    previous_balance: Optional[float] = Field(None, description="The amount of the previous bill.")

class UsageData(BaseModel):
    usage_units: Optional[UsageUnits] = Field(None, description="The units of measurement for the energy usage, e.g., 'kWh' or 'therms'.")
    usage_amount: Optional[float] = Field(None, description="The total amount of energy used.")
    meter_number: Optional[str] = Field(None, description="The identifying number for the meter.")

class UtilityData(BaseModel):
    account: Optional[AccountData] = Field(None, description="Account-related information.")
    billing: Optional[BillingData] = Field(None, description="Billing and payment details.")
    usage: Optional[List[UsageData]] = Field(None, description="A list of energy usage records.")
