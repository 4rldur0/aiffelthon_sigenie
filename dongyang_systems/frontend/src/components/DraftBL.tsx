/**
 * Draft BL 출력 컴포넌트
 */

import { useState, useEffect } from "react";
import companyLogo from "../assets/containergenie.png";
import "../styles/draftBL.css";

import type { SIDocument, Container } from "./InterfaceDefinition";

interface BLProps {
  doc?: SIDocument; // Draft BL 데이터
}

const DraftBL: React.FC<BLProps> = ({ doc }) => {
  // BL 데이터 내 컨테이너 데이터 목록
  const [containers, setContainers] = useState<Container[]>();

  // Draft BL 데이터 업데이트 시 컨테이너 목록 State 업데이트
  useEffect(() => {
    if (doc) {
      const containerList: Container[] = doc.containers;
      setContainers(containerList);
    }
  }, [doc]);

  // Draft BL 내부 출력 -------------------------------------------------------------------
  const generateParticulars = () => {
    let generation = undefined;
    if (doc && containers) {
      generation = (
        <>
          <h3>PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE</h3>
          <table className="draftbl bl-table">
            <thead>
              <tr>
                <th>MARKS AND NUMBERS</th>
                <th>NO. OF PKGS.</th>
                <th>DESCRIPTION OF PACKAGES AND GOODS</th>
                <th>GROSS WEIGHT (KG)</th>
                <th>MEASUREMENT (CBM)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{containers[0]?.marksAndNumbers}</td>
                <td>
                  {doc.totalShipment.totalPackages} {containers[0].packageType}
                </td>
                <td>{doc.commodityDescription}</td>
                <td>{doc.totalShipment.totalGrossWeight}</td>
                <td>{doc.totalShipment.totalMeasurement}</td>
              </tr>
            </tbody>
          </table>
        </>
      );
    } else {
      generation = <></>;
    }
    return generation;
  };

  const generateContainerInfo = () => {
    let generation = undefined;
    if (containers) {
      generation = (
        <>
          <h3>CONTAINER INFORMATION</h3>
          <table className="draftbl bl-table">
            <thead>
              <tr>
                <th>Container No.</th>
                <th>Seal No.</th>
                <th>Marks</th>
                <th>No. of Pkgs</th>
                <th>Description</th>
                <th>Gross Weight (KG)</th>
                <th>Measurement (CBM)</th>
              </tr>
            </thead>
            <tbody>
              {containers.map((cntr) => {
                return (
                  <tr>
                    <td>{cntr.containerNumber}</td>
                    <td>{cntr.sealNumber}</td>
                    <td>{cntr.marksAndNumbers}</td>
                    <td>
                      {cntr.numberOfPackages} {cntr.packageType}
                    </td>
                    <td>{cntr.cargoDescription}</td>
                    <td>{cntr.grossWeight}</td>
                    <td>{cntr.measurement}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </>
      );
    } else {
      generation = <></>;
    }
    return generation;
  };

  const generateFooterInfo = () => {
    let generation = undefined;
    if (doc) {
      generation = (
        <>
          <div className="draftbl bl-grid">
            <div>
              <p className="draftbl bl-row">
                <strong>{doc.shippingTerm}</strong>
              </p>
              <p className="draftbl bl-row">
                <strong>
                  "{doc.paymentDetails.freightPaymentTerms.toUpperCase()}"
                </strong>
              </p>
            </div>
            <div>
              <p className="draftbl bl-row">
                {doc.totalShipment.totalContainers}
              </p>
            </div>
          </div>
          <p className="draftbl bl-row">
            <strong>
              TOTAL No. OF CONTAINERS OF PACKAGES RECEIVED BY THE CARRIER:{" "}
              {doc.totalShipment.totalContainers}
            </strong>
          </p>
        </>
      );
    } else {
      generation = <></>;
    }
    return generation;
  };

  const generateDraftBL = () => {
    return (
      <div style={{ padding: "10px" }}>
        <div className="draftbl bl-form">
          <div className="draftbl watermark">DRAFT</div>
          <div className="draftbl bl-header">
            <div className="draftbl bl-title">
              <h2>BILL OF LADING (B/L)</h2>
            </div>
            <div>
              <p className="draftbl bl-row">
                <strong>Booking Number:</strong> {doc?.bookingReference}
              </p>
              <p className="draftbl bl-row">
                <strong>Service Type:</strong> {doc?.service}
              </p>
              <p className="draftbl bl-row">
                <strong>B/L Number:</strong> {doc?.bookingReference}
              </p>
            </div>
            <div className="draftbl bl-logo">
              <img src={companyLogo} alt="Company Logo" />
            </div>
          </div>
          <div className="draftbl bl-section">
            <h3>SHIPPER / EXPORTER (Full Name and Address)</h3>
            <p className="draftbl bl-row">{doc?.partyDetails.shipper.name}</p>
            <p className="draftbl bl-row">
              {doc?.partyDetails.shipper.address}
            </p>
            <p className="draftbl bl-row">
              Tel: {doc?.partyDetails.shipper.telephone}
            </p>
          </div>
          <div className="draftbl bl-section">
            <h3>CONSIGNEE (Full Name and Address)</h3>
            <p className="draftbl bl-row">{doc?.partyDetails.consignee.name}</p>
            <p className="draftbl bl-row">
              {doc?.partyDetails.consignee.address}
            </p>
            <p className="draftbl bl-row">
              Tel: {doc?.partyDetails.consignee.telephone}
            </p>
          </div>
          <div className="draftbl bl-section">
            <h3>NOTIFY PARTY (Full Name and Address)</h3>
            <p className="draftbl bl-row">
              {doc?.partyDetails.notifyParty.name}
            </p>
            <p className="draftbl bl-row">
              {doc?.partyDetails.notifyParty.address}
            </p>
            <p className="draftbl bl-row">
              Tel: {doc?.partyDetails.notifyParty.telephone}
            </p>
          </div>
          <div className="draftbl bl-grid">
            <div className="draftbl bl-section">
              <h3>PLACE OF RECEIPT</h3>
              <p className="draftbl bl-row">
                {doc?.routeDetails.placeOfReceipt}
              </p>
            </div>
            <div className="draftbl bl-section">
              <h3>PORT OF LOADING</h3>
              <p className="draftbl bl-row">
                {doc?.routeDetails.portOfLoading}
              </p>
            </div>
          </div>
          <div className="draftbl bl-grid">
            <div className="draftbl bl-section">
              <h3>PORT OF DISCHARGE</h3>
              <p className="draftbl bl-row">
                {doc?.routeDetails.portOfDischarge}
              </p>
            </div>
            <div className="draftbl bl-section">
              <h3>PLACE OF DELIVERY</h3>
              <p className="draftbl bl-row">
                {doc?.routeDetails.placeOfDelivery}
              </p>
            </div>
          </div>
          <div className="draftbl bl-grid">
            <div className="draftbl bl-section">
              <h3>VESSEL NAME</h3>
              <p className="draftbl bl-row">{doc?.voyageDetails.vesselName}</p>
            </div>
            <div className="draftbl bl-section">
              <h3>VOYAGE NUMBER</h3>
              <p className="draftbl bl-row">
                {doc?.voyageDetails.voyageNumber}
              </p>
            </div>
          </div>

          <div className="draftbl bl-section">{generateParticulars()}</div>
          <div className="draftbl bl-section">{generateContainerInfo()}</div>
          <div className="draftbl bl-section">{generateFooterInfo()}</div>
          <div className="draftbl bl-footer">
            <p className="draftbl small-text">
              The number of containers of packages shown in the 'TOTAL No. OF
              CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER's box which are
              said by the shipper to hold or consolidate the goods described in
              the PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE
              box, have been received by CHERRY SHIPPING LINE from the shipper
              in apparent good order and condition except as otherwise indicated
              hereon - weight, measure, marks, numbers, quality, quantity,
              description, contents and value unknown - for Carriage from the
              Place of Receipt or the Port of loading (whichever is applicable)
              to the Port of Discharge or the Place of Delivery (whichever is
              applicable) on the terms and conditions hereof INCLUDING THE TERMS
              AND CONDITIONS ON THE REVERSE SIDE HEREOF, THE CARRIER'S
              APPLICABLE TARIFF AND THE TERMS AND CONDITIONS OF THE PRECARRIER
              AND ONCARRIER AS APPLICABLE IN ACCORDANCE WITH THE TERMS AND
              CONDITIONS ON THE REVERSE SIDE HEREOF.
            </p>
            <p className="draftbl small-text">
              IN WITNESS WHEREOF {doc?.documentationDetails.numberOfOriginalBLs}{" "}
              ({doc?.documentationDetails.numberOfOriginalBLs} in words)
              ORIGINAL BILLS OF LADING (unless otherwise stated above) HAVE BEEN
              SIGNED ALL OF THE SAME TENOR AND DATE, ONE OF WHICH BEING
              ACCOMPLISHED THE OTHER(S) TO STAND VOID.
            </p>
            <div className="draftbl bl-grid">
              <div>
                <p className="draftbl bl-row">
                  <strong>CHERRY SHIPPING LINE</strong>
                </p>
                <p className="draftbl bl-row">
                  <strong>as Carrier</strong>
                </p>
                <p className="draftbl bl-row">By ContainerGenie.ai CO., LTD.</p>
                <p>as Agents only for Carrier</p>
              </div>
              <div>
                <p className="draftbl bl-row">
                  <strong>
                    Place Issued: {doc?.paymentDetails.freightPayableAt}
                  </strong>
                </p>
                <p className="draftbl bl-row">
                  <strong>
                    Date Issued: {doc?.additionalInformation.onboardDate}
                  </strong>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };
  // ---------------------------------------------------------------------------------

  // Draft BL 데이터가 존재해야만 문서 출력
  return doc ? generateDraftBL() : <></>;
};

export default DraftBL;
