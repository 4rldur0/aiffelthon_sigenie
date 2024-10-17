/**
 * 임시로 사용할 Util 함수 모음
 */

import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

import { StyledLinkPreview } from "../components/StyledComponents";
import CodeBlock from "../components/markdown/CodeBlock";

const getNodeName = (key: string) => {
  switch (key) {
    case "get_si":
      return "Retrieve Shipping Instruction Data";
    case "check_missing_data":
      return "Check Missing Data";
    case "generate_intake_report":
      return "Intake Report";
    default:
      return "";
  }
};

const getNodeContent = (item: any) => {
  const key = item.key;
  switch (key) {
    case "get_si":
      // return jsonToMarkdown(item);
      return <pre>{JSON.stringify(item.data, null, 4)}</pre>;
    case "check_missing_data":
      return missingCheckNode(item.data);
    case "generate_intake_report":
      return intakeReportNode(item.data);
    default:
      return "";
  }
};

const jsonToMarkdown = (item: any) => {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeRaw]}
      remarkPlugins={[remarkGfm]}
      components={{
        code: ({ node, ...props }) => (
          <CodeBlock language="json" value={JSON.stringify(item)} {...props} />
        ),
      }}
    />
  );
};

const missingCheckNode = (input: any) => {
  let result = "";
  result += `# Overall Status: ${statusTextColor(input.total_status)}`;
  result += `\n## Vessel Route Details: ${statusTextColor(
    input.vessel_route_details.total_status
  )}\n`;
  result += `### Vessel Name: ${statusToMarkdown(
    input.vessel_route_details.vessel_name
  )}\n`;
  result += `### Voyage Number: ${statusToMarkdown(
    input.vessel_route_details.voyage_number
  )}\n`;
  result += `### Place of Receipt: ${statusToMarkdown(
    input.vessel_route_details.place_of_receipt
  )}\n`;
  result += `### Port of Loading: ${statusToMarkdown(
    input.vessel_route_details.port_of_loading
  )}\n`;
  result += `### Port of Discharge: ${statusToMarkdown(
    input.vessel_route_details.port_of_discharge
  )}\n`;
  result += `### Place of Delivery: ${statusToMarkdown(
    input.vessel_route_details.place_of_delivery
  )}\n`;

  result += `\n## Payment Documentation: ${statusTextColor(
    input.payment_documentation.total_status
  )}\n`;
  result += `### Freight Payment: ${statusToMarkdown(
    input.payment_documentation.freight_payment_terms
  )}\n`;
  result += `### B/L Type: ${statusToMarkdown(
    input.payment_documentation.bl_type
  )}\n`;
  result += `### Number of Original B/Ls: ${statusToMarkdown(
    input.payment_documentation.number_of_original_bls
  )}\n`;

  result += `\n## Party Information: ${statusToMarkdown(
    input.party_information.status
  )}\n`;
  result += `\n## Shipping Details: ${statusToMarkdown(
    input.shipping_details.status
  )}\n`;
  result += `\n## Container Information: ${statusToMarkdown(
    input.container_information.status
  )}\n`;
  result += `\n## Total Shipment Summary: ${statusToMarkdown(
    input.total_shipment_summary.status
  )}\n`;
  result += `\n## Additional Information: ${statusToMarkdown(
    input.additional_information.status
  )}\n`;

  result += `\n## Special Cargo Information: ${statusTextColor(
    input.special_cargo_information.total_status
  )}\n`;
  result += `### Out of Gauge Dimentions Information: ${statusToMarkdown(
    input.special_cargo_information.out_of_gauge_dimensions_info
  )}\n`;
  result += `### Hazardous Materials Information: ${statusToMarkdown(
    input.special_cargo_information.hazardous_materials_info
  )}\n`;
  result += `### Refrigerated Cargo Information: ${statusToMarkdown(
    input.special_cargo_information.refrigerated_cargo_info
  )}\n`;
  return generateMarkdown(result);
};

const intakeReportNode = (input: any) => {
  let result = "";
  result += `# Overall Status: ${statusTextColor(input.overall_status)}\n`;
  result += `# Issues Found:\n`;
  result += `${input.issues_found}\n\n`;
  result += `# Summary of Missing or Incomplete Information:\n`;
  result += `${input.missing_summary}\n\n`;
  result += `# Conclusion:\n`;
  result += `${input.conclusion}`;
  return generateMarkdown(result);
};

const statusTextColor = (status: string) => {
  switch (status) {
    case "OK":
      return `<span style="color: #0000FF">${status}</span>`;
    case "Warning":
      return `<span style="color: #ffd33d">${status}</span>`;
    case "Missing":
      return `<span style="color: red">${status}</span>`;
    default:
      return status;
  }
};

const statusToMarkdown = (input: any) => {
  let result = `${statusTextColor(input.status)}`;
  if (input.reason) {
    result += `\n${input.reason}`;
  }
  return result;
};

const generateMarkdown = (markdownContent: string) => {
  return (
    <ReactMarkdown
      rehypePlugins={[rehypeRaw]}
      remarkPlugins={[remarkGfm]}
      components={{
        p: ({ node, ...props }) => (
          <p
            style={{
              marginLeft: "2em",
              marginBottom: "0.5em",
              fontFamily: "Freesentation, sans-serif",
            }}
            {...props}
          />
        ),
        li: ({ node, ...props }) => (
          <li
            style={{
              fontFamily: "Freesentation, sans-serif",
            }}
            {...props}
          />
        ),
        h1: ({ node, ...props }) => (
          <h1
            style={{
              fontSize: "1.5em",
              marginTop: "0em",
              marginBottom: "0em",
              fontFamily: "Freesentation, sans-serif",
            }}
            {...props}
          />
        ),
        h2: ({ node, ...props }) => (
          <h2
            style={{
              textAlign: "start",
              marginTop: "0.5em",
              marginBottom: "0em",
              marginLeft: "0.5em",
              fontSize: "1.3em",
              fontFamily: "Freesentation, sans-serif",
            }}
            {...props}
          />
        ),
        h3: ({ node, ...props }) => (
          <h3
            style={{
              marginBottom: 0,
              marginLeft: "1.5em",
              fontSize: "1.1em",
              fontFamily: "Freesentation, sans-serif",
            }}
            {...props}
          />
        ),
        a: ({ node, href, children, ...props }) =>
          href ? (
            <StyledLinkPreview href={href}>{children}</StyledLinkPreview>
          ) : (
            <a {...props} style={{ fontFamily: "Freesentation, sans-serif" }}>
              {children}
            </a>
          ),
      }}
    >
      {markdownContent}
    </ReactMarkdown>
  );
};

export const temp = {
  getNodeName,
  getNodeContent,
  jsonToMarkdown,
  missingCheckNode,
  intakeReportNode,
};
