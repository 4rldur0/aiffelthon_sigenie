from pydantic import BaseModel, Field

class VesselRouteDetails(BaseModel):
    vessel_name: str = Field(..., description="Status of Vessel Name (OK/Missing/Warning)")
    voyage_number: str = Field(..., description="Status of Voyage Number (OK/Missing/Warning)")
    place_of_receipt: str = Field(..., description="Status of Place of Receipt (OK/Missing/Warning)")
    port_of_loading: str = Field(..., description="Status of Port of Loading (OK/Missing/Warning)")
    port_of_discharge: str = Field(..., description="Status of Port of Discharge (OK/Missing/Warning)")
    place_of_delivery: str = Field(..., description="Status of Place of Delivery (OK/Missing/Warning)")

class PaymentDocumentation(BaseModel):
    freight_payment_terms: str = Field(..., description="Status of Freight Payment Terms (OK/Missing/Warning)")
    bl_type: str = Field(..., description="Status of Bill of Lading Type (OK/Missing/Warning)")
    number_of_original_bls: str = Field(..., description="Status of Number of Original BLs (OK/Missing/Warning)")

class PartyInformation(BaseModel):
    status: str = Field(..., description="Status of Party Information (OK/Missing/Warning)")

class ShippingDetails(BaseModel):
    status: str = Field(..., description="Status of Shipping Details (OK/Missing/Warning)")

class ContainerInformation(BaseModel):
    status: str = Field(..., description="Status of Container Information (OK/Missing/Warning)")

class TotalShipmentSummary(BaseModel):
    status: str = Field(..., description="Status of Total Shipment Summary (OK/Missing/Warning)")

class AdditionalInformation(BaseModel):
    status: str = Field(..., description="Status of Additional Information (OK/Missing/Warning)")

class SpecialCargoInformation(BaseModel):
    status: str = Field(..., description="Status of Special Cargo Information (OK/Missing/Warning)")

class ShipmentStatus(BaseModel):
    vessel_route_details: VesselRouteDetails = Field(..., description="Details of Vessel and Route status")
    payment_documentation: PaymentDocumentation = Field(..., description="Details of Payment and Documentation status")
    party_information: PartyInformation = Field(..., description="Details of Party Information status")
    shipping_details: ShippingDetails = Field(..., description="Details of Shipping Information status")
    container_information: ContainerInformation = Field(..., description="Details of Container Information status")
    total_shipment_summary: TotalShipmentSummary = Field(..., description="Details of Total Shipment Summary status")
    additional_information: AdditionalInformation = Field(..., description="Details of Additional Information status")
    special_cargo_information: SpecialCargoInformation = Field(..., description="Details of Special Cargo Information status")