import { Input, Button } from "antd";
import styled from "styled-components";

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
  padding: 20px;
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(15px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const StyledLinkPreview = styled(LinkPreview)`
  font-family: "Freesentation", sans-serif;
`;

const GradientButton = styled(Button)`
font-weight: bold;
inset: 0;
paddign: 20px
border-width: 0;
border-radius: 20px;
background: linear-gradient(135deg, #6253e1, #04befe);
  opacity: 1;
  transition: all 0.8s;

  :hover::before {
    opacity: 0;
  }
`;

const ChatDiv = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 20px;
  width: 100%;
  padding: 10px 15px;
  background: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const ChatInputField = styled(Input)`
  height: 60px;
  border: none;
  border-radius: 15px;
  font-size: 1.2rem;
`;

export {
  BackgroundCard,
  StyledLinkPreview,
  GradientButton,
  ChatDiv,
  ChatInputField,
};
