/**
 * 검색값 입력 컴포넌트 (입력 필드 + 검색 버튼)
 */

import { useState } from "react";
import { Button } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { Bot } from "lucide-react";

import { ChatDiv, ChatInputField } from "./StyledComponents";

interface ChatInputProps {
  onSubmit: (input: string) => void; // 검색 시 실행할 함수
  placeholder?: string;
  isLoading?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  placeholder,
  isLoading = false,
}) => {
  // 검색 입력값 State
  const [inputValue, setInputValue] = useState<string>("");

  // 입력 필드에서 Enter 키 event -> 검색 요청
  const onPressEnter:
    | React.KeyboardEventHandler<HTMLInputElement>
    | undefined = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (inputValue && e.key === "Enter") {
      onSubmit(inputValue);
    }
  };

  // 검색 버튼 클릭 시 event -> 검색 요청
  const onClickButton:
    | React.MouseEventHandler<HTMLElement>
    | undefined = () => {
    if (inputValue) {
      onSubmit(inputValue);
    }
  };

  return (
    <ChatDiv>
      <Bot size={50} color="#1677ff" />
      <ChatInputField
        placeholder={placeholder}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyUp={isLoading ? undefined : onPressEnter} // 로딩 중일 때 Enter 키 event 막기
      />
      <Button
        type="primary"
        shape="circle"
        size="large"
        loading={isLoading}
        icon={<SendOutlined style={{ fontSize: 20 }} />}
        onClick={isLoading ? undefined : onClickButton} // 로딩 중일 때 클릭 event 막기
      />
    </ChatDiv>
  );
};

export default ChatInput;
