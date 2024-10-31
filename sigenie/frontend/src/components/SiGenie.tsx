import React, { useState, useEffect } from "react";
import { Flex, Steps, Modal, Result, Image, Select } from "antd";
import { LoadingOutlined, CheckCircleTwoTone } from "@ant-design/icons";
import { Expand, Shrink } from "lucide-react";

import type { SIDocument, StepsItem } from "./InterfaceDefinition";
import { EndpointUtil } from "../utils/EndpointUtil";
import { createGlobalStyle } from "styled-components";
import { BackgroundCard, GradientButton } from "./StyledComponents";
import SIGenieLogo from "../assets/sigenie_logo.svg";
import ChatInput from "./ChatInput";
import DocPreview from "./DocPreview";
import DraftBL from "./DraftBL";
import SIResponseContent from "./SiResponseContent";
import "../styles/siGenie.css";

import { temp } from "../utils/TemporaryUtil";

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

const errorModal = (content: string) => {
  Modal.error({
    content: <Result status={"error"} title={content} />,
    centered: true,
    maskClosable: true,
    zIndex: 10,
    className: "sigenie-modal-error",
  });
};

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
  // Draft BL Preview Open 여부
  const [isPreviewOpen, setIsPreviewOpen] = useState<boolean>(false);
  // ===== 임시 ==================================================
  // Progress Bar 노드
  const [steps, setSteps] = useState<string[]>(temp.steps_1);
  // Progress Bar 노드
  const [stepsItems, setStepsItems] = useState<StepsItem[]>(
    JSON.parse(JSON.stringify(temp.progressItems_1))
  );
  // ============================================================
  // Progress Bar 현재 선택된 노드
  const [stepsCurrent, setStepsCurrent] = useState<number>(0);
  // LLM Response 출력용 데이터
  const [responseChain, setResponseChain] = useState<any[]>([]);
  // 조회 여부
  const [hasSearched, setHasSearched] = useState<boolean>(false);
  // 로딩 여부
  const [isLoading, setIsLoading] = useState<boolean>(false);
  // 스트리밍 통신용 EventSource 객체
  const [eventSource, setEventSource] = useState<EventSource>();

  // ===== 임시 select ==================================================
  const [chapterSelection, setChapterSelection] = useState<string>("chapter 1");
  const onSelectChapter = (value: string) => {
    setChapterSelection(value);
    if (value === "chapter 1") {
      setSteps(temp.steps_1);
    } else if (value === "chapter 2") {
      setSteps(temp.steps_2);
    } else if (value === "chapter 1 & 2") {
      setSteps(temp.steps_all);
    }
  };
  // ===================================================================

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
  }, [sessionBkgRef]);

  // 검색 시 실행하는 함수
  const onSubmit = (query: string) => {
    setHasSearched(true);
    initializeProgressItems();
    setResponseChain([]);
    if (chapterSelection === "chapter 1") {
      getStreamingResponseCh1(query);
    } else if (chapterSelection === "chapter 2") {
      getStreamingResponseCh2(query);
    } else if (chapterSelection === "chapter 1 & 2") {
      getChainedStreamingResponse(query);
    }
  };

  // Progress Bar 데이터 초기화
  const initializeProgressItems = () => {
    const newProgressItems: StepsItem[] = temp.getProgressItems(steps);
    newProgressItems.forEach((item: StepsItem) => {
      item.icon = <LoadingOutlined />;
    });
    setStepsItems(newProgressItems);
  };

  // chapter 1 LLM Response 스트리밍 데이터 요청
  const getStreamingResponseCh1 = (input: string) => {
    if (chapterSelection !== "chapter 1") {
      errorModal("Chapter Selection Error");
      return;
    }

    setIsLoading(true);
    const newChain: any[] = [];

    if (eventSource) {
      eventSource.close();
    }

    const endpoint = EndpointUtil.API.REQUEST.QUERY_CH1 + `?query=${input}`;
    const stream = new EventSource(endpoint, { withCredentials: true });

    stream.onopen = () => {
      console.log("::: SSE comm. start :::");
    };

    steps.forEach((eventId) => {
      stream.addEventListener(eventId, (e) => {
        const nodeName = e.type;
        const nodeResponse = {
          key: nodeName,
          data: JSON.parse(e.data),
        };
        // console.log(`${eventId} ::: `, nodeResponse);
        if (nodeName === "get_si") {
          const bkgRef = nodeResponse.data.bookingReference;
          setSessionBkgRef(bkgRef);
          setDoc(nodeResponse.data);
        }
        newChain.push(nodeResponse);
        setResponseChain([...newChain]);
        changeStepStatus(nodeName);
      });
    });

    stream.addEventListener("done", (e) => {
      console.log("SSE comm. done ::: ", e.data);
      stream.close();
      setIsLoading(false);
    });

    stream.onerror = (e) => {
      console.log("Error while streaming!");
      // console.log(e);
      stream.close();
      setIsLoading(false);
      onErrorChangeStepStatus();
      errorModal("Generation Failed");
    };

    setEventSource(stream);
  };

  // chapter 2 LLM Response 스트리밍 데이터 요청
  const getStreamingResponseCh2 = (input: string) => {
    if (chapterSelection !== "chapter 2") {
      errorModal("Chapter Selection Error");
      return;
    }

    setIsLoading(true);
    const newChain: any[] = [];

    if (eventSource) {
      eventSource.close();
    }

    const endpoint = EndpointUtil.API.REQUEST.QUERY_CH2 + `?query=${input}`;
    const stream = new EventSource(endpoint, { withCredentials: true });

    stream.onopen = () => {
      console.log("::: SSE comm. start :::");
    };

    stream.onmessage = (e) => {
      const nodeName = e.lastEventId;
      const nodeResponse = {
        key: nodeName,
        data: JSON.parse(e.data),
      };
      // console.log(`message ::: ${nodeName} ::: `, nodeResponse);
      if (nodeName === "get_si") {
        const bkgRef = nodeResponse.data.bookingReference;
        setSessionBkgRef(bkgRef);
        setDoc(nodeResponse.data);
      }
      newChain.push(nodeResponse);
      setResponseChain([...newChain]);
      changeStepStatus(nodeName);
    };

    stream.addEventListener("done", (e) => {
      console.log("SSE comm. done ::: ", e.data);
      stream.close();
      setIsLoading(false);
    });

    stream.onerror = (e) => {
      console.log("Error while streaming!");
      // console.log(e);
      stream.close();
      setIsLoading(false);
      onErrorChangeStepStatus();
      errorModal("Generation Failed");
    };

    setEventSource(stream);
  };

  // chapter 1 & chapter 2 LLM Response 스트리밍 데이터 요청
  const getChainedStreamingResponse = (input: string) => {
    if (chapterSelection !== "chapter 1 & 2") {
      errorModal("Chapter Selection Error");
      return;
    }
    setIsLoading(true);
    const newChain: any[] = [];

    if (eventSource) {
      eventSource.close();
    }

    let endpoint = EndpointUtil.API.REQUEST.QUERY_CH1 + `?query=${input}`;
    const streamCh1 = new EventSource(endpoint, { withCredentials: true });

    streamCh1.onopen = () => {
      console.log("::: SSE comm. start :::");
    };

    temp.steps_1.forEach((eventId) => {
      streamCh1.addEventListener(eventId, (e) => {
        const nodeName = e.type;
        const nodeResponse = {
          key: nodeName,
          data: JSON.parse(e.data),
        };
        // console.log(`${eventId} ::: `, nodeResponse);
        if (nodeName === "get_si") {
          const bkgRef = nodeResponse.data.bookingReference;
          setSessionBkgRef(bkgRef);
          setDoc(nodeResponse.data);
          // streamCh1.close(); //@@@@@@@@@@@@@@@@@@@@@@@@@
          // setIsLoading(false);
        }
        newChain.push(nodeResponse);
        setResponseChain([...newChain]);
        changeStepStatus(nodeName);
      });
    });

    streamCh1.addEventListener("done", (e) => {
      console.log("SSE comm. done ::: ", e.data);
      streamCh1.close();

      // request chapter 2 =======================
      endpoint = EndpointUtil.API.REQUEST.QUERY_CH2 + `?query=${input}`;
      const streamCh2 = new EventSource(endpoint, { withCredentials: true });
      streamCh2.onopen = () => {
        console.log("::: SSE comm. start :::");
      };

      streamCh2.onmessage = (e) => {
        const nodeName = e.lastEventId;
        if (nodeName === "get_si") {
          return;
        }
        const nodeResponse = {
          key: nodeName,
          data: JSON.parse(e.data),
        };
        // console.log(`message ::: ${nodeName} ::: `, nodeResponse);
        newChain.push(nodeResponse);
        setResponseChain([...newChain]);
        changeStepStatus(nodeName);
      };

      streamCh2.addEventListener("done", (e) => {
        console.log("SSE comm. done ::: ", e.data);
        streamCh2.close();
        setIsLoading(false);
      });

      streamCh2.onerror = (e) => {
        console.log("Error while streaming!");
        // console.log(e);
        streamCh2.close();
        setIsLoading(false);
        onErrorChangeStepStatus();
        errorModal("Generation Failed");
      };

      setEventSource(streamCh2);
    });

    streamCh1.onerror = (e) => {
      console.log("Error while streaming!");
      // console.log(e);
      streamCh1.close();
      setIsLoading(false);
      onErrorChangeStepStatus();
      errorModal("Generation Failed");
    };

    setEventSource(streamCh1);
  };

  const changeStepStatus = (stepKey: string) => {
    setStepsItems((prevItems) => {
      const newItems = [...prevItems];
      const targetStep = newItems.find((item) => item.key === stepKey);
      if (targetStep) {
        targetStep.status = "finish";
        targetStep.icon =
          stepKey === "generate_intake_report" ||
          stepKey === "generate_validation_report" ? (
            <CheckCircleTwoTone
              twoToneColor={"#00cc00"}
              style={{ fontSize: "30px" }}
            />
          ) : (
            <CheckCircleTwoTone style={{ fontSize: "30px" }} />
          );
      }
      return newItems;
    });
  };

  const onErrorChangeStepStatus = () => {
    setStepsItems((prevItems) => {
      const newItems = [...prevItems];
      newItems.forEach((item) => {
        if (item.status !== "finish") {
          item.icon = undefined;
        }
      });
      return newItems;
    });
  };

  const onClickSteps = (current: number) => {
    setStepsCurrent(current);
  };

  return (
    <>
      <GlobalStyle />
      <Flex vertical gap={"10px"}>
        {/* ========== 임시 Select ========== */}
        <div style={{ position: "absolute", top: "70px" }}>
          <Select
            options={[
              { value: "chapter 1" },
              { value: "chapter 2" },
              { value: "chapter 1 & 2" },
            ]}
            value={chapterSelection}
            onChange={onSelectChapter}
            style={{ width: "130px" }}
          />
        </div>
        {/* ================================ */}
        <Flex vertical={false} align="center">
          {bkgRefExists && (
            <Flex
              flex={isPreviewOpen ? "1 0 0%" : "0 0 0%"} // transition 적용 시 flicker 현상 방지를 위해
              align={"end"}
              style={{
                height: "80px",
                paddingBottom: isPreviewOpen ? 0 : "18px",
                marginRight: "10px",
                transition: "all 0.3s ease-in-out",
              }}
            >
              <GradientButton
                type="primary"
                size="large"
                icon={
                  isPreviewOpen ? (
                    <Shrink color="#ffffff" />
                  ) : (
                    <Expand color="#ffffff" />
                  )
                }
                onClick={() => {
                  setIsPreviewOpen(!isPreviewOpen);
                }}
              >
                Draft B/L
              </GradientButton>
            </Flex>
          )}
          <Flex vertical flex={1} align="center">
            {!hasSearched && (
              <Image
                src={SIGenieLogo}
                alt="SIGenie Logo"
                preview={false}
                style={{
                  width: "25vw",
                  marginTop: "50px",
                  marginBottom: "50px",
                }}
              />
            )}
            <ChatInput
              // placeholder="What is your episode for SIGenie story?"
              placeholder="Please input a Booking Reference Number."
              onSubmit={onSubmit}
              isLoading={isLoading}
            />
          </Flex>
        </Flex>
        <Flex
          vertical={false}
          align="start"
          gap={bkgRefExists && isPreviewOpen ? "10px" : undefined}
        >
          {bkgRefExists && (
            <Flex
              flex={isPreviewOpen ? 1 : "0 0 auto"}
              style={{
                transition: "flex 0.3s ease-in-out",
              }}
            >
              <DocPreview template={<DraftBL doc={doc} />} />
            </Flex>
          )}
          {hasSearched && (
            <Flex vertical gap={"10px"} flex={1}>
              <BackgroundCard
                style={{
                  display: "grid", // 내용이 너무 길어질 때 스크롤 활성화를 위해
                  gridTemplateColumns: "1fr", // 내용이 너무 짧을 때 내용의 너비를 늘리기 위해
                }}
              >
                <Steps
                  className="sigenie-steps"
                  labelPlacement="vertical"
                  current={stepsCurrent}
                  items={stepsItems}
                  onChange={onClickSteps}
                />
              </BackgroundCard>
              {responseChain?.at(stepsCurrent) && (
                <BackgroundCard>
                  <SIResponseContent
                    className="sigenie-response"
                    item={responseChain[stepsCurrent]}
                  />
                </BackgroundCard>
              )}
            </Flex>
          )}
        </Flex>
      </Flex>
    </>
  );
};

export default SIGenie;
