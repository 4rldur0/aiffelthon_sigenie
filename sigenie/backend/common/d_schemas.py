import operator
from typing import Annotated, Sequence, Optional
from pydantic import BaseModel, Field, root_validator
from langchain_core.messages import BaseMessage

class MyAppState(BaseModel):
    messages: Annotated[Sequence[BaseMessage], operator.add]

class StatusWithReason(BaseModel):
    status: str = Field(..., description="The status of the field (OK/Missing/Warning)")
    reason: Optional[str] = Field(None, description="The reason for Missing or Warning status, if applicable")

    def is_problematic(self) -> bool:
        return self.status in ["Missing", "Warning"]

class VesselRouteDetails(BaseModel):
    vessel_name: StatusWithReason = Field(..., description="Status of Vessel Name")
    voyage_number: StatusWithReason = Field(..., description="Status of Voyage Number")
    place_of_receipt: StatusWithReason = Field(..., description="Status of Place of Receipt")
    port_of_loading: StatusWithReason = Field(..., description="Status of Port of Loading")
    port_of_discharge: StatusWithReason = Field(..., description="Status of Port of Discharge")
    place_of_delivery: StatusWithReason = Field(..., description="Status of Place of Delivery")
    total_status: str = Field(..., description="Overall status of Vessel Route Details")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        statuses = [
            values.get('vessel_name'),
            values.get('voyage_number'),
            values.get('place_of_receipt'),
            values.get('port_of_loading'),
            values.get('port_of_discharge'),
            values.get('place_of_delivery')
        ]
        if any(status.is_problematic() for status in statuses if status):
            values['total_status'] = "Warning"
        else:
            values['total_status'] = "OK"
        return values

class PaymentDocumentation(BaseModel):
    freight_payment_terms: StatusWithReason = Field(..., description="Status of Freight Payment Terms")
    bl_type: StatusWithReason = Field(..., description="Status of Bill of Lading Type")
    number_of_original_bls: StatusWithReason = Field(..., description="Status of Number of Original BLs")
    total_status: str = Field(..., description="Overall status of Payment Documentation")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        statuses = [
            values.get('freight_payment_terms'),
            values.get('bl_type'),
            values.get('number_of_original_bls')
        ]
        if any(status.is_problematic() for status in statuses if status):
            values['total_status'] = "Warning"
        else:
            values['total_status'] = "OK"
        return values

class PartyInformation(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Party Information")
    total_status: str = Field(..., description="Overall status of Party Information")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class ShippingDetails(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Shipping Details")
    total_status: str = Field(..., description="Overall status of Shipping Details")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class ContainerInformation(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Container Information")
    total_status: str = Field(..., description="Overall status of Container Information")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class TotalShipmentSummary(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Total Shipment Summary")
    total_status: str = Field(..., description="Overall status of Total Shipment Summary")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class AdditionalInformation(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Additional Information")
    total_status: str = Field(..., description="Overall status of Additional Information")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class SpecialCargoInformation(BaseModel):
    status: StatusWithReason = Field(..., description="Status of Special Cargo Information")
    total_status: str = Field(..., description="Overall status of Special Cargo Information")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        return {'total_status': values['status'].status}

class ShipmentStatus(BaseModel):
    vessel_route_details: VesselRouteDetails = Field(..., description="Details of Vessel and Route status")
    payment_documentation: PaymentDocumentation = Field(..., description="Details of Payment and Documentation status")
    party_information: PartyInformation = Field(..., description="Details of Party Information status")
    shipping_details: ShippingDetails = Field(..., description="Details of Shipping Information status")
    container_information: ContainerInformation = Field(..., description="Details of Container Information status")
    total_shipment_summary: TotalShipmentSummary = Field(..., description="Details of Total Shipment Summary status")
    additional_information: AdditionalInformation = Field(..., description="Details of Additional Information status")
    special_cargo_information: SpecialCargoInformation = Field(..., description="Details of Special Cargo Information status")
    total_status: str = Field(..., description="Overall status of the Shipment")

    @root_validator(pre=True)
    def calculate_total_status(cls, values):
        sub_statuses = [
            values['vessel_route_details'].get('total_status'),
            values['payment_documentation'].get('total_status'),
            values['party_information'].get('total_status'),
            values['shipping_details'].get('total_status'),
            values['container_information'].get('total_status'),
            values['total_shipment_summary'].get('total_status'),
            values['additional_information'].get('total_status'),
            values['special_cargo_information'].get('total_status')
        ]
        if "Warning" in sub_statuses or "Missing" in sub_statuses:
            values['total_status'] = "Warning"
        else:
            values['total_status'] = "OK"
        return values


class ShipmentSummary(BaseModel):
    summary: str = Field(description="Summary of the Shipping Instruction review")
    vessel_route_info: str = Field(description="Detailed explanation of Vessel and Route Information")
    shipper_details: str = Field(description="Detailed explanation of Shipper Details")
    container_info: str = Field(description="Detailed explanation of Container Information")
    other_sections: dict = Field(description="Detailed explanations of other relevant sections")
    identified_issues: list = Field(description="List of identified issues and their importance")
    proposed_solutions: dict = Field(description="Specific solutions for each identified problem")
    priority_actions: list = Field(description="Top 3 Priority Actions to be taken")
    additional_notes: str = Field(description="Any additional information or explanations of industry-specific terms")