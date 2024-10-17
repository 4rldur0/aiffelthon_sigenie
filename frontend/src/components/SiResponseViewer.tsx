/**
 * SIGenie LLM 응답을 출력하는 배경 컴포넌트
 */

import { Space } from "antd";

import ResponseNode from "./ResponseNode";
import type { ResponseProps } from "./ResponseNode";

interface ResponseViewerProps {
  items: ResponseProps[];
}

const SIResponseViewer: React.FC<ResponseViewerProps> = ({ items }) => {
  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      {items.map((obj) => (
        <ResponseNode item={obj} />
      ))}
    </Space>
  );
};

export default SIResponseViewer;
