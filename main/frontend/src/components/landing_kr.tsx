import React, { useState } from "react";
import {
  ArrowRight,
  CheckCircle,
  Ship,
  FileText,
  Zap,
  Globe,
  Database,
  Cpu,
  Network,
  Clock,
  BookOpen,
  Bot,
  Quote,
} from "lucide-react";
import {
  Layout,
  Typography,
  Button,
  Card,
  Row,
  Col,
  Space,
  ConfigProvider,
  Modal,
  Statistic,
  Image,
} from "antd";
import "../styles/landing.css";
import SIGenieImage from "../assets/SIGenie.gif";
import AitechImage from "../assets/aitech.png";
import StorystudioImage from "../assets/StoryStudio.png";
import StorystuidiodetailImage from "../assets/StoryStuidoDetails.png";
import styled from "styled-components";

const { Header, Footer, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

// Ant Design 테마 커스터마이징
const theme = {
  token: {
    colorPrimary: "#2563eb",
    borderRadius: 8,
    colorBgContainer: "#ffffff",
  },
};

// 반투명 블러 효과를 위한 스타일드 컴포넌트
const TransparentSection = styled.section`
  background-color: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 80px 0;
`;

const BenefitsList = styled.ul`
  padding-left: 20px;
`;

const PercentageValue = styled.span`
  font-size: 28px;
  font-weight: bold;
`;

interface FeatureProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  additionalInfo: {
    overview: string;
    benefits: string[];
    stats: {
      [key: string]: number;
    };
  };
}

const Feature: React.FC<FeatureProps> = ({
  icon,
  title,
  description,
  additionalInfo,
}) => {
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showModal = () => setIsModalVisible(true);
  const handleOk = () => setIsModalVisible(false);
  const handleCancel = () => setIsModalVisible(false);

  return (
    <>
      <Card
        bordered={true}
        className="feature-card"
        style={{ textAlign: "center", height: "100%" }}
        hoverable
        onClick={showModal}
      >
        <Space direction="vertical" align="center" size="middle">
          <div className="feature-icon">{icon}</div>
          <Title level={4}>{title}</Title>
          <Text>{description}</Text>
        </Space>
      </Card>
      <Modal
        title={<Title level={3}>{title}</Title>}
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={700}
        footer={null}
      >
        <Paragraph>{additionalInfo.overview}</Paragraph>
        <Title level={4}>주요 이점:</Title>
        <BenefitsList>
          {additionalInfo.benefits.map((benefit, index) => (
            <li key={index}>{benefit}</li>
          ))}
        </BenefitsList>
        <Row gutter={16} style={{ marginTop: "30px" }}>
          {Object.entries(additionalInfo.stats).map(([key, value], index) => (
            <Col span={12} key={index}>
              <Statistic
                title={key}
                value={value}
                suffix="%"
                valueStyle={{ fontSize: "28px", fontWeight: "bold" }}
                prefix={
                  index === 0 ? <CheckCircle size={30} /> : <Clock size={30} />
                }
              />
            </Col>
          ))}
        </Row>
      </Modal>
    </>
  );
};

interface CTAProps {
  text: string;
  type?: "default" | "primary" | "dashed" | "link" | "text";
}

const CTA: React.FC<{
  text: string;
  type: "primary" | "default";
  href?: string;
}> = ({ text, type, href }) => {
  const handleClick = () => {
    if (href) {
      window.open(href, "_blank");
    }
  };

  return (
    <Button type={type} size="large" onClick={handleClick}>
      {text}
    </Button>
  );
};

interface TechFeatureProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const TechFeature: React.FC<TechFeatureProps> = ({
  icon,
  title,
  description,
}) => (
  <Space align="start" size="middle" style={{ marginBottom: 16 }}>
    <div className="icon-sm">{icon}</div>
    <Space direction="vertical" size="small">
      <Text strong>{title}</Text>
      <Text type="secondary">{description}</Text>
    </Space>
  </Space>
);

const LandingPage = () => {
  const renderTransparentImagePreview = (originalNode: React.ReactElement) => {
    originalNode.props.style["backgroundColor"] = "white";
    return originalNode;
  };

  return (
    <ConfigProvider theme={theme}>
      <Layout style={{ background: "transparent" }}>
        {/* Hero Section */}
        <Header
          style={{
            background: "rgba(29, 78, 216, 0.9)",
            padding: "60px 0",
            height: "auto",
          }}
        >
          <Row justify="center" align="middle">
            <Col span={20} style={{ textAlign: "center" }}>
              <Title style={{ color: "white", marginBottom: 0 }}>
                SIGenie (에스아이지니)
              </Title>
              <Paragraph
                style={{ color: "white", fontSize: 20, marginBottom: 24 }}
              >
                AI 기반의 선적지시서 관리 시스템
              </Paragraph>
              <Paragraph
                style={{
                  color: "white",
                  fontSize: 24,
                  lineHeight: 1.4,
                  marginBottom: 24,
                  fontWeight: "bold",
                  fontStyle: "italic",
                  background:
                    "linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.2))",
                  padding: "40px 20px", // 상하 패딩을 동일하게 설정
                  borderRadius: "10px",
                  // border: "2px solid rgba(255, 255, 255, 0.3)",
                  boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
                  position: "relative",
                  textAlign: "center",
                }}
              >
                <Quote
                  size={30}
                  style={{
                    position: "absolute",
                    top: 10,
                    left: "50%",
                    transform: "translateX(-50%) rotate(180deg)",
                    opacity: 0.6,
                    color: "white",
                  }}
                />
                대규모 언어 모델과 검색 증강 생성 기술을 활용한 AI 시스템으로
                선적 문서 처리를 자동화하여 해운 업무의 정확성과 효율성을
                혁신적으로 향상시킵니다.
                <Quote
                  size={30}
                  style={{
                    position: "absolute",
                    bottom: 10,
                    left: "50%",
                    transform: "translateX(-50%)", // 아이콘을 180도 회전
                    opacity: 0.6,
                    color: "white",
                  }}
                />
              </Paragraph>
              <Space size="middle">
                <CTA text="시작하기" type="primary" />
                <CTA
                  text="자세히 알아보기"
                  type="default"
                  href="https://bit.ly/sigenie"
                />
              </Space>
            </Col>
          </Row>
        </Header>

        <Content>
          {/* Key Features */}
          <TransparentSection>
            <Row justify="center">
              <Col span={20}>
                <Title
                  level={2}
                  style={{ textAlign: "center", marginBottom: 20 }}
                >
                  주요 기능
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie는 AI 기반의 지능형 문서 처리로 선적지시서를 자동으로
                  분석하고, RAG 기술을 활용한 컨텍스트 기반 의사결정으로 정확한
                  검증을 수행하며, LangChain과 LangGraph를 이용한 유연한 AI
                  워크플로우로 복잡한 해운 업무를 동적으로 자동화하여 전체적인
                  프로세스 효율성과 정확성을 크게 향상시킵니다.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<FileText size={60} className="text-blue" />}
                      title="지능형 문서 처리"
                      description="AI 기반 자동화로 선적 지시서 처리 및 검증"
                      additionalInfo={{
                        overview:
                          "SIGenie는 Meta의 llama-3.1-70b 모델 그리고 OpenAI의 ChatGPT-4o-mini 모델을 활용하여 선적지시서를 자동으로 분석하고 처리합니다. LangChain과 LangGraph 기술을 통해 복잡한 문서 구조를 이해하고, 누락된 정보나 오류를 자동으로 식별합니다.",
                        benefits: [
                          "JSON 형식의 선적지시서 자동 파싱 및 MongoDB 저장",
                          "LLM을 활용한 누락 데이터 자동 식별 및 보완 제안",
                          "규정 준수 자동 확인으로 법적 리스크 최소화",
                          "DCSA 표준 준수를 통한 글로벌 호환성 확보",
                          "자동화된 접수 보고서(Intake Report) 생성",
                        ],
                        stats: {
                          "문서 처리 시간 단축": 60,
                          "수동 처리 대비 오류율 감소": 90,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Cpu size={60} className="text-green" />}
                      title="컨텍스트 기반 의사결정"
                      description="RAG 기술을 활용한 정확한 선적지시서 검증"
                      additionalInfo={{
                        overview:
                          "FAISS 벡터 데이터베이스와 RAG (Retrieval-Augmented Generation) 기술을 활용하여 선적지시서의 정확성을 검증합니다. 회사 정책, 선박 및 항구 상황, 규제 사항 등을 종합적으로 분석하여 잠재적 문제를 식별합니다.",
                        benefits: [
                          "고성능 벡터 데이터베이스를 활용한 고속 유사성 검색",
                          "강력한 LLM을 통한 복잡한 추론 체인 구현",
                          "CHERRY Compliance 통합을 통한 규제 준수 확인",
                          "실시간 선박 및 항구 상황 점검",
                          "회사 정책 준수 여부 자동 검증",
                          "종합적인 검증 보고서(Validation Report) 생성",
                        ],
                        stats: {
                          "규정 준수 리스크 감소": 50,
                          "선적 지연 예방 향상": 30,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Network size={60} className="text-yellow" />}
                      title="유연한 AI 워크플로우"
                      description="모듈화된 AI 에이전트로 동적 업무 처리"
                      additionalInfo={{
                        overview:
                          "유연한 AI 워크플로우 관리 시스템은 해운 산업의 다양하고 복잡한 업무 프로세스를 효율적으로 자동화합니다. LangChain과 LangGraph 기술을 기반으로 한 이 시스템은 독립적인 AI 에이전트들을 동적으로 조합하여 복잡한 업무 흐름을 구성합니다.",
                        benefits: [
                          "선적지시서 접수부터 최종 검증까지 end-to-end 자동화",
                          "모듈식 접근 방식으로 새로운 비즈니스 요구사항에 빠르게 대응",
                          "각 처리 단계별 특화된 AI 에이전트 구성",
                          "새로운 규정이나 요구사항에 따른 유연한 프로세스 조정",
                          "업무 처리 시간 단축 및 운영 효율성 향상",
                        ],
                        stats: {
                          "프로세스 적응성 향상": 95,
                          "전체 처리 효율성 증가": 25,
                        },
                      }}
                    />
                  </Col>
                </Row>
              </Col>
            </Row>
          </TransparentSection>

          {/* Technical Architecture */}
          <section style={{ padding: "80px 0", background: "#f5f5f5" }}>
            <Row justify="center">
              <Col span={20}>
                <Title
                  level={2}
                  style={{ textAlign: "center", marginBottom: 20 }}
                >
                  기술 아키텍처
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie는 MongoDB를 데이터 저장소로, OpenAI의 gpt-4o-mini와
                  Meta의 llama-3.1-70b등 대규모 언어 모델을 AI 엔진으로
                  활용하며, LangChain과 LangGraph로 복잡한 워크플로우를
                  구성하고, FAISS로 효율적인 유사성 검색을 수행하며, Web Search
                  같은 외부 서비스와 연동하여 종합적이고 지능적인 선적지시서
                  처리 시스템을 구현합니다.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={12}>
                    <Card title="핵심 기술 스택" bordered={false}>
                      <TechFeature
                        icon={<Network className="text-blue" />}
                        title="LangChain & LangGraph"
                        description="LangChain과 LangGraph를 활용하여 복잡한 해운 업무를 AI 에이전트가 자동으로 처리 합니다."
                      />
                      <TechFeature
                        icon={<Cpu className="text-green" />}
                        title="대규모 언어 모델 (LLM)"
                        description="OpenAI의 gpt-4o-mini 그리고 Meta의 llama-3.1-70b 대규모 언어 모델을 사용하여 고급 다국어 자연어 처리 기능을 제공합니다."
                      />
                      <TechFeature
                        icon={<BookOpen className="text-blue" />}
                        title="RAG (Retrieval-Augmented Generation)"
                        description="검색 증강 생성(RAG) 기술을 이용하여 해운 산업 특화 지식과 실시간 업데이트되는 규제 및 시장 정보를 기반으로 AI 모델 통한 정확한 정보 제공 합니다."
                      />
                    </Card>
                  </Col>
                  <Col xs={24} md={12}>
                    <Card title="추가 기술 요소" bordered={false}>
                      <TechFeature
                        icon={<Database className="text-blue" />}
                        title="MongoDB"
                        description="MongoDB는 유연한 스키마, 높은 확장성, 빠른 쿼리 성능을 제공하여 다양하고 복잡한 Booking Data와 Shipping Instruction을 효율적으로 저장하고 관리 합니다."
                      />
                      <TechFeature
                        icon={<Zap className="text-yellow" />}
                        title="FAISS"
                        description="FAISS는 고성능 벡터 유사성 검색이 가능하여 대규모 해운 데이터에서 신속하고 정확한 정보 검색을 가능하게 하며, 이는 의사결정 과정을 크게 개선합니다."
                      />
                      <TechFeature
                        icon={<Globe className="text-blue" />}
                        title="외부 서비스 통합"
                        description="Web Search 등의 외부 서비스 통합은 실시간 시장 동향과 규제 정보에 대한 접근을 제공하여 해운 업무의 인사이트를 풍부하게 하고 전략적 의사결정을 강화합니다."
                      />
                    </Card>
                  </Col>
                </Row>
                {/* AI Tech Image */}
                <Row justify="center" style={{ marginTop: "50px" }}>
                  <Image
                    src={AitechImage}
                    alt="AI Tech Image"
                    style={{
                      width: "100%",
                      display: "block",
                      margin: "0 auto",
                    }}
                    preview={{
                      mask: "자세히 보기",
                    }}
                  />
                </Row>
              </Col>
            </Row>
          </section>

          {/* Process Flow */}
          <TransparentSection>
            <Row justify="center">
              <Col span={20}>
                <Title
                  level={2}
                  style={{ textAlign: "center", marginBottom: 20 }}
                >
                  선적지시서 검증 스토리 프로세스 흐름
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie는 선적지시서의 JSON 데이터 가져오기와 파싱, LLM을
                  활용한 누락 데이터 식별 및 접수 보고서 생성을 수행한 후, 관련
                  당사자 정보 확인, 회사 정책 준수 검증, 선박 및 항구 상황
                  점검을 거쳐 최종 검증 보고서를 생성하는 end-to-end 자동화
                  프로세스를 제공합니다.
                </Paragraph>
                {/* SIGenie Image */}
                <Row justify="center" style={{ marginBottom: "30px" }}>
                  <Image
                    src={SIGenieImage}
                    alt="SIGenie Process Flow"
                    style={{
                      width: "100%",
                      height: "auto",
                      display: "block",
                      margin: "0 auto",
                    }}
                    preview={{
                      mask: "자세히 보기",
                    }}
                  />
                </Row>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={12}>
                    <Card title="Chapter 1: 선적지시서 접수" bordered={true}>
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Database className="text-sky" />
                            get_bkg: Booking Data를 가져옵니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Database className="text-sky" />
                            get_si: JSON 형식의 Shipping Instruction 데이터를
                            가져옵니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-sky" />
                            check_missing_data: LLM(Large Language Model)을
                            사용하여 누락된 필드를 식별합니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-sky" />
                            generate_intake_report: LLM을 사용하여 접수 과정을
                            요약한 보고서를 생성합니다.
                          </Space>
                        </li>
                      </ul>
                    </Card>
                  </Col>
                  <Col xs={24} md={12}>
                    <Card title="Chapter 2: 선적지시서 검증" bordered={true}>
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            check_parties: LLM을 사용하여 관련 당사자들의 정보를
                            검증합니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            verify_company_policy: LLM과 VectorDB를 사용하여
                            회사 정책 준수 여부를 확인합니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Globe className="text-purple" />
                            verify_vessel_port_situation: LLM과 외부
                            API(Tavily)를 사용하여 선박 및 항구 상황을
                            확인합니다.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            generate_validation_report: LLM을 사용하여 검증
                            결과를 요약한 보고서를 생성합니다.
                          </Space>
                        </li>
                      </ul>
                    </Card>
                  </Col>
                </Row>
              </Col>
            </Row>
          </TransparentSection>

          {/* Benefits */}
          <section style={{ padding: "80px 0", background: "#f5f5f5" }}>
            <Row justify="center">
              <Col span={20}>
                <Title
                  level={2}
                  style={{ textAlign: "center", marginBottom: 20 }}
                >
                  SIGenie의 장점
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie는 AI 기술을 활용하여 선적지시서 처리의 정확성과 속도를
                  크게 향상시키고, 글로벌 표준을 준수하며 외부 시스템과의
                  연계성을 강화하여 해운 업계의 디지털 혁신을 선도합니다.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<CheckCircle size={60} className="text-green" />}
                      title="정확성 향상"
                      description="AI 기반 선적지시서 검증 및 오류 감소"
                      additionalInfo={{
                        overview:
                          "Meta의 llama-3.1-70b 모델, OpenAI의 ChatGPT-4o-mini 모델과 RAG 기술을 활용하여 선적지시서의 정확성을 크게 향상시킵니다. 누락된 데이터 자동 식별, 회사 정책 준수 확인, 실시간 선박 및 항구 상황 점검을 통해 인적 오류를 최소화하고 데이터 품질을 개선합니다.",
                        benefits: [
                          "LLM을 활용한 누락 데이터 자동 식별",
                          "CHERRY Compliance를 통한 규제 준수 확인",
                          "실시간 선박 및 항구 상황 점검",
                          "자동화된 검증 보고서(Validation Report) 생성",
                        ],
                        stats: {
                          "수동 처리 대비 오류율 감소": 90,
                          "규정 준수 리스크 감소": 50,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Zap size={60} className="text-yellow" />}
                      title="처리 속도 향상"
                      description="자동화된 end-to-end 프로세스로 효율성 극대화"
                      additionalInfo={{
                        overview:
                          "LangChain과 LangGraph를 활용한 AI 워크플로우 시스템으로 선적지시서 처리 시간을 대폭 단축합니다. JSON 파일 자동 파싱부터 최종 검증까지 전 과정을 자동화하여, 직원들이 전략적 의사결정에 집중할 수 있도록 합니다.",
                        benefits: [
                          "JSON 형식의 선적지시서 자동 파싱 및 MongoDB 저장",
                          "LLM 기반의 자동화된 데이터 검증 및 보완",
                          "AI 에이전트를 활용한 동적 워크플로우 처리",
                          "실시간 처리 현황 모니터링 및 병목 구간 식별",
                        ],
                        stats: {
                          "문서 처리 시간 단축": 70,
                          "전체 처리 효율성": 85,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Ship size={60} className="text-blue" />}
                      title="글로벌 표준 준수 및 연계성 강화"
                      description="DCSA 표준 적용 및 외부 시스템 통합"
                      additionalInfo={{
                        overview:
                          "DCSA(Digital Container Shipping Association) 표준을 적용하여 글로벌 해운 업계와의 호환성을 확보합니다. 또한 CHERRY Compliance 및 외부 시스템과의 통합을 통해 실시간 정보 교환 및 규제 준수를 강화합니다.",
                        benefits: [
                          "DCSA 표준 준수로 글로벌 호환성 확보",
                          "CHERRY Compliance 통합으로 실시간 규제 준수 확인",
                          "실시간 선박 및 항구 정보 활용",
                          "외부 시스템과의 유연한 통합으로 확장성 확보",
                        ],
                        stats: {
                          "글로벌 표준 준수율": 90,
                          "외부 시스템 통합 효율성 향상": 75,
                        },
                      }}
                    />
                  </Col>
                </Row>
              </Col>
            </Row>
          </section>

          {/* Key Features */}
          <TransparentSection>
            <Row justify="center">
              <Col span={20}>
                <Title
                  level={2}
                  style={{ textAlign: "center", marginBottom: 20 }}
                >
                  SIGenie 미래
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  ContainerGenie.ai Story Studio는 LLM, RAG, 그리고 Agentic
                  Workflow의 첨단 AI 기술을 완벽하게 융합하여, 컨테이너 해운
                  산업의 복잡한 프로세스를 혁신적으로 간소화하고 지능화함으로써,
                  업무 효율성의 획기적 향상, 실시간 데이터 기반의 정확한
                  의사결정, 그리고 전례 없는 수준의 운영 최적화를 가능하게
                  합니다.
                </Paragraph>
                {/* Story Studio Image */}
                <Row justify="center" style={{ marginBottom: "10px" }}>
                  <Image
                    src={StorystudioImage}
                    alt="Story Studio UI Image"
                    style={{
                      width: "100%",
                      display: "block",
                      margin: "0 auto",
                    }}
                    preview={{
                      mask: "자세히 보기",
                      imageRender: renderTransparentImagePreview,
                    }}
                  />
                </Row>
                {/* Story Studio Detail Image */}
                <Row justify="center" style={{ marginBottom: "10px" }}>
                  <Image
                    src={StorystuidiodetailImage}
                    alt="Story Studio UI Image Details"
                    style={{
                      width: "100%",
                      display: "block",
                      margin: "0 auto",
                    }}
                    preview={{
                      mask: "자세히 보기",
                      imageRender: renderTransparentImagePreview,
                    }}
                  />
                </Row>
              </Col>
            </Row>
          </TransparentSection>

          {/* Call to Action */}
          <section
            style={{ padding: "80px 0", background: "rgba(29, 78, 216, 0.9)" }}
          >
            <Row justify="center">
              <Col span={20} style={{ textAlign: "center" }}>
                <Title level={2} style={{ color: "white", marginBottom: 24 }}>
                  SIGenie로 선적지시서 관리의 혁신을 경험하세요
                </Title>
                <Space size="large">
                  <CTA text="무료 체험 시작하기" type="primary" />
                  <CTA text="상담 문의" type="default" />
                </Space>
              </Col>
            </Row>
          </section>
        </Content>

        <Footer style={{ textAlign: "center" }}>
          © 2024 SIGenie. All rights reserved.
        </Footer>
      </Layout>
    </ConfigProvider>
  );
};

export default LandingPage;
