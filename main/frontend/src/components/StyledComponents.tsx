import { Input, Button } from "antd";
import styled, { createGlobalStyle } from "styled-components";

import LinkPreview from "./LinkPreview";

const BackgroundCard = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  width: 100%;
  height: 100%;
  text-align: center;
  border-radius: 10px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ContentDiv = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 20px;
  border-radius: 15px;
  background: white;
  color: black;
  text-align: start;
`;

const StyledLinkPreview = styled(LinkPreview)`
  font-family: "Freesentation", sans-serif;
`;

const GradientButton = styled(Button)`
  font-size: 1.3em;
  font-weight: bold;
  inset: 0;
  border-width: 0;
  border-radius: 20px;
  background: linear-gradient(135deg, #6253e1, #04befe);
  opacity: 1;
  transition: all 0.5s;

  .ant-btn-icon {
    display: grid;
  }

  :hover::before {
    opacity: 0;
  }
`;

const ChatDiv = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 15px;
  border-radius: 20px;
  width: 100%;
  padding: 10px 20px;
  background: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ChatInputField = styled(Input)`
  height: 60px;
  padding-left: 7px;
  border: none;
  border-radius: 15px;
  font-size: 1.2rem;
`;

const MarkdownStyles = createGlobalStyle`
  .markdown-body {
    font-size: 16px;
    line-height: 1.6;
    color: #333;
  }

  .markdown-body h1, .markdown-body h2, .markdown-body h3, 
  .markdown-body h4, .markdown-body h5, .markdown-body h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
  }

  .markdown-body h1 { font-size: 2em; }
  .markdown-body h2 { font-size: 1.5em; text-align: start; }
  .markdown-body h3 { font-size: 1.25em; margin-left: 15px }
  .markdown-body h4 { 
    font-size: 1.1em;
    margin-left: 30px; /* Add indentation for h4 */
  }
  .markdown-body h5 { 
    font-size: 1em;
    margin-left: 40px; /* Add indentation for h5 */
  }

  .markdown-body ul, .markdown-body ol {
    padding-left: 20px; /* Indent list items */
  }

  .markdown-body li {
    margin-bottom: 8px;
  }

  .markdown-body p {
    margin-top: 0;
    margin-bottom: 16px;
  }

  .markdown-body code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    border-radius: 3px;
  }

  .markdown-body pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    border-radius: 3px;
  }

  .markdown-body span {
    word-wrap: break-word;
    white-space: pre-wrap;
  }
`;

export {
  BackgroundCard,
  ContentDiv,
  StyledLinkPreview,
  GradientButton,
  ChatDiv,
  ChatInputField,
  MarkdownStyles,
};
