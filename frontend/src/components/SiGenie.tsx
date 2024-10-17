import React, { useState, useEffect } from "react";
import axios from "axios";
import { Flex } from "antd";

import { EndpointUtil } from "../utils/EndpointUtil";
import { createGlobalStyle } from "styled-components";
import { BackgroundCard } from "./StyledComponents";
import ChatInput from "./ChatInput";
import DocPreview from "./DocPreview";
import DraftBL from "./DraftBL";
import SIResponseViewer from "./SiResponseViewer";

import type { SIDocument } from "./InterfaceDefinition";

// 글로벌 스타일 추가
const GlobalStyle = createGlobalStyle`
  @font-face {
    font-family: 'Freesentation';
    src: url('/fonts/Freesentation.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
  }

  body, .markdown-body {
    font-family: 'Freesentation', sans-serif;
  }
`;

interface SIGenieProps {
  bookingReference?: string;
}

const SIGenie: React.FC<SIGenieProps> = ({ bookingReference }) => {
  // session으로 사용할 booking reference 번호
  const [sessionBkgRef, setSessionBkgRef] = useState<string>();
  // session 존재 여부
  const [bkgRefExists, setBkgRefExists] = useState<boolean>(false);
  // Draft BL 생성용 데이터
  const [doc, setDoc] = useState<SIDocument>();
  // LLM Response 출력용 데이터
  const [responseChain, setResponseChain] = useState<any[]>([]);
  // 로딩 여부
  const [isLoading, setIsLoading] = useState<boolean>(false);
  // 스트리밍 통신용 EventSource 객체
  const [eventSource, setEventSource] = useState<EventSource>();

  // 부모 컴포넌트에서 Props로 넘어온 booking reference가 있으면
  // session으로 사용할 State 값 update
  useEffect(() => {
    if (bookingReference) {
      setSessionBkgRef(bookingReference);
    }
  }, [bookingReference]);

  // session bookingReference 값이 바뀌면 update
  useEffect(() => {
    setBkgRefExists(sessionBkgRef ? true : false);
    // setBkgRefExists(true);
  }, [sessionBkgRef]);

  // 검색 시 실행하는 함수
  const onSubmit = (query: string) => {
    getLLMResponse(query);
  };

  // LLM Response 출력용 데이터 가져오기
  const getLLMResponse = (query: string) => {
    getStreamingResponse(query);
  };

  // LLM Response 스트리밍 데이터 요청
  const getStreamingResponse = (input: string) => {
    setIsLoading(true);
    setResponseChain([]);
    const newChain: any[] = [];

    if (eventSource) {
      eventSource.close();
    }

    const endpoint = EndpointUtil.API.REQUEST.QUERY_CH1 + `?query=${input}`;
    const stream = new EventSource(endpoint, { withCredentials: true });

    stream.onopen = () => {
      console.log("::: SSE comm. start :::");
    };

    stream.onmessage = (e) => {
      console.log("message ::: ", e.data);
    };

    stream.addEventListener("get_si", (e) => {
      const nodeName = e.type;
      const nodeResponse = {
        key: nodeName,
        ...JSON.parse(e.data),
      };
      console.log("get_si ::: ", nodeResponse);
      const bkgRef = nodeResponse.bookingReference;
      setSessionBkgRef(bkgRef);
      setDoc(nodeResponse);
      newChain.push(nodeResponse);
      setResponseChain([...newChain]);
    });
    stream.addEventListener("check_missing_data", (e) => {
      const nodeName = e.type;
      const nodeResponse = {
        key: nodeName,
        ...JSON.parse(e.data),
      };
      console.log("check_missing_data ::: ", nodeResponse);
      newChain.push(nodeResponse);
      setResponseChain([...newChain]);
    });
    stream.addEventListener("generate_intake_report", (e) => {
      const nodeName = e.type;
      const nodeResponse = {
        key: nodeName,
        ...JSON.parse(e.data),
      };
      console.log("generate_intake_report ::: ", nodeResponse);
      newChain.push(nodeResponse);
      setResponseChain([...newChain]);
    });

    stream.addEventListener("done", (e) => {
      console.log("done ::: ", e.data);
      stream.close();
      setIsLoading(false);
      console.log("ResponseChain ::: ", responseChain);
    });

    stream.onerror = (e) => {
      console.log("Error while streaming!");
      // console.log(e);
      stream.close();
      setIsLoading(false);
    };

    setEventSource(stream);
  };

  return (
    <>
      <GlobalStyle />
      <Flex vertical={false} gap={"10px"}>
        <Flex flex={1} style={{ display: bkgRefExists ? undefined : "none" }}>
          <DocPreview template={<DraftBL doc={doc} />} />
        </Flex>
        <Flex flex={1} vertical align="center" gap={"10px"}>
          <ChatInput
            // placeholder="What is your episode for SIGenie story?"
            placeholder="Please input a Booking Reference Number."
            onSubmit={onSubmit}
            isLoading={isLoading}
          />
          <BackgroundCard
            style={{
              display: bkgRefExists ? undefined : "none",
            }}
          >
            <SIResponseViewer items={responseChain} />
          </BackgroundCard>
        </Flex>
      </Flex>
    </>
  );
};

export default SIGenie;
