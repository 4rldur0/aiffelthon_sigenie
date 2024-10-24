/**
 * 임시로 사용할 Util 함수 모음
 */

import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy as CodeTheme } from "react-syntax-highlighter/dist/esm/styles/prism";

import { StepsItem } from "../components/InterfaceDefinition";
import { StyledLinkPreview } from "../components/StyledComponents";

const getNodeName = (key: string) => {
  switch (key) {
    case "get_bkg":
      return "Retrieve Booking Data";
    case "get_si":
      return "Retrieve Shipping Instruction Data";
    case "check_missing_data":
      return "Check Missing Data";
    case "generate_intake_report":
      return "Intake Report";
    case "check_parties":
      return "Party Details Check";
    case "verify_company_policy":
      return "Compliance Check";
    case "verify_vessel_port_situation":
      return "Vessel/Port Situation";
    case "generate_validation_report":
      return "Validation Report";
    default:
      return "";
  }
};

const steps_1 = [
  "get_bkg",
  "get_si",
  "check_missing_data",
  "generate_intake_report",
];
const steps_2 = [
  "get_si",
  "check_parties",
  "verify_company_policy",
  "verify_vessel_port_situation",
  "generate_validation_report",
];
const steps_all = [
  "get_bkg",
  "get_si",
  "check_missing_data",
  "generate_intake_report",
  "check_parties",
  "verify_company_policy",
  "verify_vessel_port_situation",
  "generate_validation_report",
];

const progressItems_1: StepsItem[] = steps_1.map((key: string) => ({
  key: key,
  subTitle: getNodeName(key),
  status: "wait",
  icon: undefined,
}));
const progressItems_2: StepsItem[] = steps_2.map((key: string) => ({
  key: key,
  subTitle: getNodeName(key),
  status: "wait",
  icon: undefined,
}));
const progressItems_all: StepsItem[] = steps_all.map((key: string) => ({
  key: key,
  subTitle: getNodeName(key),
  status: "wait",
  icon: undefined,
}));

const getProgressItems = (steps: string[]): StepsItem[] => {
  return steps.map((key: string) => ({
    key: key,
    subTitle: getNodeName(key),
    status: "wait",
    icon: undefined,
  }));
};

const getNodeContent = (item: any) => {
  const key = item.key;
  switch (key) {
    case "get_bkg":
      return jsonToMarkdown(item);
    case "get_si":
      return jsonToMarkdown(item);
    case "check_missing_data":
      return missingCheckNode(item.data);
    case "generate_intake_report":
      return intakeReportNode(item.data);
    case "check_parties":
      return generateMarkdown(item.data.markdown);
    case "verify_company_policy":
      return generateMarkdown(item.data.markdown);
    case "verify_vessel_port_situation":
      return vesselPortSituationNode(item.data);
    case "generate_validation_report":
      return generateMarkdown(item.data.markdown);
    default:
      return "";
  }
};

const jsonToMarkdown = (item: any) => {
  const json_str = JSON.stringify(item.data, null, 8);
  const markdown = "```json\n" + json_str + "\n```\n";
  return generateMarkdown(markdown);
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

  if (input.special_cargo_information.status) {
    result += `\n## Special Cargo Information: ${statusToMarkdown(
      input.special_cargo_information.status
    )}\n`;
  } else {
    result += `\n## Special Cargo Information: ${statusTextColor(
      input.special_cargo_information.total_status
    )}\n`;

    result += `### Out of Gauge Dimensions Information: ${statusToMarkdown(
      input.special_cargo_information.out_of_gauge_dimensions_info
    )}\n`;
    result += `### Hazardous Materials Information: ${statusToMarkdown(
      input.special_cargo_information.hazardous_materials_info
    )}\n`;
    result += `### Refrigerated Cargo Information: ${statusToMarkdown(
      input.special_cargo_information.refrigerated_cargo_info
    )}\n`;
  }
  return generateMarkdown(result);
};

// const intakeReportNode = (input: any) => {
//   let result = "";
//   result += `# Overall Status: ${statusTextColor(input.overall_status)}\n`;
//   result += `# Issues Found:\n`;
//   result += `${input.issues_found}\n\n`;
//   result += `# Summary of Missing or Incomplete Information:\n`;
//   result += `${input.missing_summary}\n\n`;
//   result += `# Conclusion:\n`;
//   result += `${input.conclusion}`;
//   return generateMarkdown(result);
// };
const intakeReportNode = (input: any) => {
  const other_sections = input.other_sections
    ? Object.keys(input.other_sections)
        .map(
          (key) =>
            `### ${key.split("_").join(" ")}\n${input.other_sections[key]}`
        )
        .join("\n")
    : "No Information Found";
  const identified_issues = input.identified_issues
    ? input.identified_issues
        .map((item: any) => {
          return typeof item === "string"
            ? `- ${item}`
            : `- ${item.issue}\n\t- ${item.importance}`;
        })
        .join("\n")
    : "No Issues Found";
  const proposed_solutions = input.proposed_solutions
    ? Object.keys(input.proposed_solutions)
        .map((key) => `### ${key}\n${input.proposed_solutions[key]}`)
        .join("\n")
    : "No Proposals Found";

  let result = "";
  result += `# Summary\n${input.summary}\n\n`;
  result += `# Vessel Route Information\n${input.vessel_route_info}\n\n`;
  result += `# Shipper Details\n${input.shipper_details}\n\n`;
  result += `# Container Information\n${input.container_info}\n\n`;
  result += `# Other Sections\n${other_sections}\n\n`;
  result += `# Identified Issues\n${identified_issues}\n\n`;
  result += `# Proposed Solutions\n${proposed_solutions}\n\n`;
  result += `# Priority Actions\n- ${input.priority_actions.join("\n- ")}\n\n`;
  result += `# Additional Notes\n${input.additional_notes}`;
  return generateMarkdown(result.replace(/(\n)+(?!-)/g, "\n\n"));
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
  if (typeof input === "string") {
    return statusTextColor(input);
  }

  let result = statusTextColor(input.status);
  if (input.reason) {
    result += `\n${input.reason}`;
  }
  return result;
};

const vesselPortSituationNode = (input: any) => {
  const llmAnswer = input.answer;
  let markdown = llmAnswer + "<br /><br />";
  input.results.forEach((src: any) => {
    markdown += `Source: [${src.title}](${src.url})<br />`;
  });
  return generateMarkdown(markdown);
};

const generateMarkdown = (markdownContent: string) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw]}
      components={{
        code({ node, inline, className, children, ...props }: any) {
          const match = /language-(\w+)/.exec(className || "");
          return !inline && match ? (
            <SyntaxHighlighter
              style={{ ...CodeTheme }}
              language={match[1]}
              PreTag="div"
              {...props}
            >
              {String(children).replace(/\n$/, "")}
            </SyntaxHighlighter>
          ) : (
            <code className={className} {...props}>
              {children}
            </code>
          );
        },
        a: ({ node, href, children, ...props }) => {
          if (!href) {
            return (
              <a {...props} style={{ fontFamily: "Freesentation, sans-serif" }}>
                {children}
              </a>
            );
          } else if (href.startsWith("mailto:")) {
            return (
              <a
                {...props}
                href={href}
                style={{ fontFamily: "Freesentation, sans-serif" }}
              >
                {children}
              </a>
            );
          } else {
            return (
              <StyledLinkPreview href={href}>{children}</StyledLinkPreview>
            );
          }
        },
      }}
    >
      {markdownContent}
    </ReactMarkdown>
  );
};

export const temp = {
  steps_1,
  steps_2,
  steps_all,
  progressItems_1,
  progressItems_2,
  progressItems_all,
  getProgressItems,
  getNodeName,
  getNodeContent,
};
