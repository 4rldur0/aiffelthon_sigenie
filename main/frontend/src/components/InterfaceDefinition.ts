import { StepProps } from "antd";

interface SIDocument {
  _id?: string;
  bookingReference: string;
  service?: string;
  voyageDetails: VoyageDetails;
  routeDetails: RouteDetails;
  paymentDetails: PaymentDetails;
  documentationDetails: DocumentationDetails;
  partyDetails: PartyDetails;
  shippingTerm: string;
  hsCode: string;
  commodityDescription: string;
  containers: Container[];
  totalShipment: TotalShipment;
  outOfGaugeDimensions?: OutOfGaugeDimensions;
  additionalInformation: AdditionalInformation;
  dangerousGoods?: DangerousGoods;
  filename: string;
}

interface VoyageDetails {
  vesselName: string;
  voyageNumber: string;
}

interface RouteDetails {
  placeOfReceipt: string;
  portOfLoading: string;
  portOfDischarge: string;
  placeOfDelivery: string;
}

interface PaymentDetails {
  freightPaymentTerms: string;
  freightPayableAt: string;
}

interface DocumentationDetails {
  blType: string;
  numberOfOriginalBLs: number;
  numberOfCopies: number;
}

interface PartyDetails {
  shipper: Shipper;
  consignee: Consignee;
  notifyParty: NotifyParty;
}

interface Shipper {
  name: string;
  address: string;
  telephone: string;
  email?: string;
  fax?: string;
}

interface Consignee {
  name: string;
  address: string;
  taxId?: string;
  president?: string;
  telephone: string;
  email?: string;
  fax?: string;
}

interface NotifyParty {
  name: string;
  address: string;
  taxId?: string;
  president?: string;
  telephone: string;
  email?: string;
  fax: string;
}

interface Container {
  containerNumber: string;
  sealNumber: string;
  marksAndNumbers: string;
  numberOfPackages: number;
  packageType: string;
  cargoDescription: string;
  grossWeight: number;
  measurement: number;
}

interface TotalShipment {
  totalContainers: string;
  totalPackages: number;
  packageType: string;
  containerType?: string;
  totalGrossWeight: number;
  totalMeasurement: number;
}

interface OutOfGaugeDimensions {
  length: string;
  width: string;
  height: string;
  additionalInfo: string;
}

interface AdditionalInformation {
  onboardDate: string;
  [key: string]: any;
}

interface LCDetails {
  lcNumber: string;
}

interface DistributionDetails {
  name: string;
  address: string;
  telephone: string;
  fax: string;
}

interface DangerousGoods {
  containerNumber: string;
  unClass: string;
  unCode: string;
  hsCode: string;
  flashPoint: string;
  additionalInfo: string;
}

// ===========================================================

interface StepsItem extends StepProps {
  key: string;
}

export type { SIDocument, Container, StepsItem };
