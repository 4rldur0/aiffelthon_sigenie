/**
 * LLM Response Streaming의 각각의 응답을 출력하는 컴포넌트
 */

import { useState, useEffect, ReactNode } from "react";
import { Collapse } from "antd";
import type { CollapseProps } from "antd";
import "../styles/siGenie.css";

import { temp } from "../utils/TemporaryUtil";

interface ResponseNodeProps {
  item: ResponseProps;
}

export interface ResponseProps {
  [key: string]: any;
}

const ResponseNode: React.FC<ResponseNodeProps> = ({ item }) => {
  const [contentItems, setContentItems] = useState<CollapseProps["items"]>();

  useEffect(() => {
    if (item) {
      const itemKey = item.key;
      const itemLabel = temp.getNodeName(itemKey);
      const itemContent = temp.getNodeContent(item);
      const content = {
        key: itemKey,
        label: itemLabel,
        children: itemContent,
      };
      setContentItems([content]);
    }
  }, [item]);

  return (
    <Collapse
      className="sigenie-node-collapse"
      items={contentItems}
      expandIconPosition="end"
    />
  );
};

export default ResponseNode;
