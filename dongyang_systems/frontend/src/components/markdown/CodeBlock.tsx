import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";

interface CodeBlockProps {
  language?: string;
  value: string;
  children?: any;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ language, value, children }) => {
  return (
    <SyntaxHighlighter language={language} style={coy} PreTag={"div"}>
      {children}
    </SyntaxHighlighter>
  );
};

export default CodeBlock;
