/**
 * SIGenie LLM 응답을 출력하는 배경 컴포넌트
 */

import { Divider } from "antd";

import { ContentDiv, MarkdownStyles } from "./StyledComponents";
import { temp } from "../utils/TemporaryUtil";

interface ResponseViewerProps {
  item?: any;
  className?: string;
  style?: React.CSSProperties;
}

const SIResponseContent: React.FC<ResponseViewerProps> = ({
  item,
  className,
  style,
}) => {
  return item ? (
    <>
      <MarkdownStyles />
      <ContentDiv className={className} style={{ ...style }}>
        <h2 className="sigenie-response-title">{temp.getNodeName(item.key)}</h2>
        <Divider style={{ margin: "5px" }} />
        <div className="markdown-body">{temp.getNodeContent(item)}</div>
      </ContentDiv>
    </>
  ) : (
    <></>
  );
};

export default SIResponseContent;
