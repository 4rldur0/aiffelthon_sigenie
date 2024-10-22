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
import AitechImage from "../assets/aitech_en.png";
import StorystudioImage from "../assets/StoryStudio.png";
import StorystuidiodetailImage from "../assets/StoryStuidoDetails.png";
import styled from "styled-components";

const { Header, Footer, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

// Ant Design theme customization
const theme = {
  token: {
    colorPrimary: "#2563eb",
    borderRadius: 8,
    colorBgContainer: "#ffffff",
  },
};

// Styled component for translucent blur effect
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
        <Title level={4}>Key Benefits:</Title>
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
              <Title style={{ color: "white", marginBottom: 0 }}>SIGenie</Title>
              <Paragraph
                style={{ color: "white", fontSize: 20, marginBottom: 24 }}
              >
                AI-powered Shipping Instruction Management System
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
                Revolutionizing maritime operations by automating shipping
                document processing with an AI system powered by large language
                models and retrieval-augmented generation, significantly
                enhancing accuracy and efficiency in shipping operations.
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
                <CTA text="Get Started" type="primary" />
                <CTA
                  text="Learn More"
                  type="default"
                  href="https://bit.ly/sigenie_en"
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
                  Key Features
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie significantly improves overall process efficiency and
                  accuracy by automatically analyzing shipping instructions
                  using AI-based intelligent document processing, performing
                  accurate verification with context-based decision-making using
                  RAG technology, and dynamically automating complex shipping
                  tasks with flexible AI workflows using LangChain and
                  LangGraph.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<FileText size={60} className="text-blue" />}
                      title="Intelligent Document Processing"
                      description="AI-based automation for processing and verifying shipping instructions"
                      additionalInfo={{
                        overview:
                          "SIGenie automatically analyzes and processes shipping instructions using Meta's llama-3.1-70b model and OpenAI's ChatGPT-4o-mini model. Through LangChain and LangGraph technologies, it understands complex document structures and automatically identifies missing information or errors.",
                        benefits: [
                          "Automatic parsing of shipping instructions in JSON format and storage in MongoDB",
                          "Automatic identification and suggestion of missing data using LLM",
                          "Automatic compliance check to minimize legal risks",
                          "Ensuring global compatibility through DCSA standard compliance",
                          "Generation of automated Intake Reports",
                        ],
                        stats: {
                          "Reduction in document processing time": 60,
                          "Decrease in error rate compared to manual processing": 90,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Cpu size={60} className="text-green" />}
                      title="Context-based Decision Making"
                      description="Accurate shipping instruction verification using RAG technology"
                      additionalInfo={{
                        overview:
                          "We verify the accuracy of shipping instructions using FAISS vector database and RAG (Retrieval-Augmented Generation) technology. It comprehensively analyzes company policies, ship and port situations, and regulatory matters to identify potential issues.",
                        benefits: [
                          "High-speed similarity search using high-performance vector database",
                          "Implementation of complex reasoning chains through powerful LLM",
                          "Regulatory compliance check through CHERRY Compliance integration",
                          "Real-time ship and port situation checks",
                          "Automatic verification of company policy compliance",
                          "Generation of comprehensive Validation Reports",
                        ],
                        stats: {
                          "Reduction in regulatory compliance risk": 50,
                          "Improvement in shipping delay prevention": 30,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Network size={60} className="text-yellow" />}
                      title="Flexible AI Workflow"
                      description="Dynamic task processing with modularized AI agents"
                      additionalInfo={{
                        overview:
                          "The flexible AI workflow management system efficiently automates the diverse and complex business processes in the shipping industry. Based on LangChain and LangGraph technologies, this system dynamically combines independent AI agents to construct complex workflow processes.",
                        benefits: [
                          "End-to-end automation from shipping instruction receipt to final verification",
                          "Quick response to new business requirements through a modular approach",
                          "Configuration of specialized AI agents for each processing stage",
                          "Flexible process adjustment according to new regulations or requirements",
                          "Reduction in task processing time and improvement in operational efficiency",
                        ],
                        stats: {
                          "Improvement in process adaptability": 95,
                          "Increase in overall processing efficiency": 25,
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
                  Technical Architecture
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie implements a comprehensive and intelligent shipping
                  instruction processing system by using MongoDB as a data
                  store, large language models such as OpenAI's gpt-4o-mini and
                  Meta's llama-3.1-70b as AI engines, constructing complex
                  workflows with LangChain and LangGraph, performing efficient
                  similarity searches with FAISS, and integrating with external
                  services like Web Search.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={12}>
                    <Card title="Core Technology Stack" bordered={false}>
                      <TechFeature
                        icon={<Network className="text-blue" />}
                        title="LangChain & LangGraph"
                        description="AI agents automatically handle complex shipping tasks using LangChain and LangGraph."
                      />
                      <TechFeature
                        icon={<Cpu className="text-green" />}
                        title="Large Language Models (LLM)"
                        description="Advanced multilingual natural language processing capabilities are provided using OpenAI's gpt-4o-mini and Meta's llama-3.1-70b large language models."
                      />
                      <TechFeature
                        icon={<BookOpen className="text-blue" />}
                        title="RAG (Retrieval Augmented Generation"
                        description="Retrieval Augmented Generation (RAG) technology is used to provide accurate information through AI models based on shipping industry-specific knowledge and real-time updated regulatory and market information."
                      />
                    </Card>
                  </Col>
                  <Col xs={24} md={12}>
                    <Card
                      title="Additional Technical Elements"
                      bordered={false}
                    >
                      <TechFeature
                        icon={<Database className="text-blue" />}
                        title="MongoDB"
                        description="MongoDB provides flexible schema, high scalability, and fast query performance, efficiently storing and managing diverse and complex Booking Data and Shipping Instructions."
                      />
                      <TechFeature
                        icon={<Zap className="text-yellow" />}
                        title="FAISS"
                        description="FAISS offers high-performance vector similarity search, enabling quick and accurate information retrieval from large-scale shipping data, significantly improving the decision-making process."
                      />
                      <TechFeature
                        icon={<Globe className="text-blue" />}
                        title="External Service Integration"
                        description="ntegration of external services like Tavily Web Search provides access to real-time market trends and regulatory information, enriching insights for shipping operations and strengthening strategic decision-making."
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
                      mask: "View Details",
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
                  Shipping Instruction Verification Story Process Flow
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie provides an end-to-end automated process that includes
                  fetching and parsing JSON data of shipping instructions,
                  identifying missing data using LLM and generating intake
                  reports, followed by verifying related party information,
                  checking company policy compliance, inspecting ship and port
                  situations, and finally generating a validation report.
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
                      mask: "View Details",
                    }}
                  />
                </Row>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={12}>
                    <Card
                      title="Chapter 1: Shipping Instruction Receipt"
                      bordered={true}
                    >
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Database className="text-sky" />
                            get_bkg: Retrieves Booking Data.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Database className="text-sky" />
                            get_si: Imports Shipping Instruction data in JSON
                            format.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-sky" />
                            check_missing_data: Uses LLM (Large Language Model)
                            to identify missing fields.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-sky" />
                            generate_intake_report: Uses LLM to generate a
                            summary report of the intake process.
                          </Space>
                        </li>
                      </ul>
                    </Card>
                  </Col>
                  <Col xs={24} md={12}>
                    <Card
                      title="Chapter 2: Shipping Instruction Verification"
                      bordered={true}
                    >
                      <ul style={{ listStyle: "none", padding: 0 }}>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            check_parties: Uses LLM to validate information of
                            relevant parties.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            verify_company_policy: Uses LLM and VectorDB to
                            verify compliance with company policies.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Globe className="text-purple" />
                            verify_vessel_port_situation: Uses LLM and external
                            API (Tavily) to check vessel and port situations.
                          </Space>
                        </li>
                        <li style={{ marginBottom: 8 }}>
                          <Space>
                            <Bot className="text-purple" />
                            generate_validation_report: Uses LLM to generate a
                            summary report of the validation results.
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
                  Advantages of SIGenie
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  SIGenie significantly improves the accuracy and speed of
                  shipping instruction processing using AI technology, complies
                  with global standards, and strengthens connectivity with
                  external systems, leading the digital innovation in the
                  shipping industry.
                </Paragraph>
                <Row gutter={[32, 32]}>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<CheckCircle size={60} className="text-green" />}
                      title="Improved Accuracy"
                      description="AI-based shipping instruction verification and error reduction"
                      additionalInfo={{
                        overview:
                          "We greatly improve the accuracy of shipping instructions using Meta's llama-3.1-70b model, OpenAI's ChatGPT-4o-mini model, and RAG technology. By automatically identifying missing data, verifying company policy compliance, and checking real-time ship and port situations, we minimize human errors and improve data quality.",
                        benefits: [
                          "Automatic identification of missing data using LLM",
                          "Regulatory compliance check through CHERRY Compliance",
                          "Real-time ship and port situation checks",
                          "Generation of automated Validation Reports",
                        ],
                        stats: {
                          "Decrease in error rate compared to manual processing": 90,
                          "Reduction in regulatory compliance risk": 50,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Zap size={60} className="text-yellow" />}
                      title="Improved Processing Speed"
                      description="Maximized efficiency with automated end-to-end process"
                      additionalInfo={{
                        overview:
                          "We significantly reduce shipping instruction processing time with an AI workflow system using LangChain and LangGraph. By automating the entire process from JSON file parsing to final verification, we allow employees to focus on strategic decision-making.",
                        benefits: [
                          "Automatic parsing and MongoDB storage of shipping instructions in JSON format",
                          "Automated data verification and supplementation based on LLM",
                          "Dynamic workflow processing using AI agents",
                          "Real-time processing status monitoring and bottleneck identification",
                        ],
                        stats: {
                          "Reduction in document processing time": 70,
                          "Overall processing efficiency": 85,
                        },
                      }}
                    />
                  </Col>
                  <Col xs={24} md={8}>
                    <Feature
                      icon={<Ship size={60} className="text-blue" />}
                      title="Global Standard Compliance and Enhanced Connectivity"
                      description="DCSA standard application and external system integration"
                      additionalInfo={{
                        overview:
                          "We ensure compatibility with the global shipping industry by applying DCSA (Digital Container Shipping Association) standards. We also strengthen real-time information exchange and regulatory compliance through integration with CHERRY Compliance and external systems.",
                        benefits: [
                          "Ensure global compatibility through DCSA standard compliance",
                          "Real-time regulatory compliance check through CHERRY Compliance integration",
                          "Utilization of real-time ship and port information",
                          "Ensure scalability through flexible integration with external systems",
                        ],
                        stats: {
                          "Global standard compliance rate": 90,
                          "Improvement in external system integration efficiency": 75,
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
                  The Future of SIGenie
                </Title>
                <Paragraph
                  style={{
                    color: "black",
                    fontSize: 18,
                    marginBottom: 24,
                    textAlign: "center",
                  }}
                >
                  ContainerGenie.ai Story Studio perfectly integrates
                  cutting-edge AI technologies such as LLM, RAG, and Agentic
                  Workflow to innovatively simplify and intelligentize complex
                  processes in the container shipping industry, enabling
                  dramatic improvements in operational efficiency, accurate
                  decision-making based on real-time data, and unprecedented
                  levels of operational optimization.
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
                      mask: "View Details",
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
                      mask: "View Details",
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
                  Experience the Innovation in Shipping Instruction Management
                  with SIGenie
                </Title>
                <Space size="large">
                  <CTA text="Start Free Trial" type="primary" />
                  <CTA text="Contact Us" type="default" />
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
