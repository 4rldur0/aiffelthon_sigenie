import React, { useState } from "react";
import { Layout, Menu, Button, Space, Typography, Select } from "antd";
import {
  GlobalOutlined,
  LaptopOutlined,
  HomeOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  PushpinOutlined,
} from "@ant-design/icons";
import "./App.css";
import "./styles/fonts.css";
import backgroundImage from "./assets/background.jpg";
import LandingKR from "./components/landing_kr";
import LandingEN from "./components/landing_en";
import SIGenie from "./components/SiGenie";
import styled, { createGlobalStyle } from "styled-components";

const { Header, Content, Sider, Footer } = Layout;
const { Link } = Typography;
const { Option } = Select;

const PinButton = styled(Button)`
  position: fixed;
  bottom: 15px;
  left: 15px;
  border: none;
  border-top: 0px solid #f0f0f0;
  background-color: transparent; // 배경색을 투명하게 설정

  &:hover {
    background-color: rgba(
      0,
      0,
      0,
      0.05
    ); // 호버 시 약간의 배경색 추가 (선택사항)
  }

  &.ant-btn-primary {
    background-color: transparent; // primary 상태에서도 배경 투명 유지
    color: #1890ff; // primary 상태일 때 텍스트 색상 변경 (선택사항)
  }
`;

const App: React.FC = () => {
  const [selectedMenuItem, setSelectedMenuItem] = useState<string>("1");
  const [collapsed, setCollapsed] = useState(true);
  const [pinned, setPinned] = useState(false);
  const [language, setLanguage] = useState<"kr" | "en">("kr");

  const toggleCollapsed = () => {
    if (!pinned) {
      setCollapsed(!collapsed);
    }
  };

  const handleMouseEnter = () => {
    if (!pinned) {
      setCollapsed(false);
    }
  };

  const handleMouseLeave = () => {
    if (!pinned) {
      setCollapsed(true);
    }
  };

  const togglePinned = () => {
    setPinned(!pinned);
    if (!pinned) {
      setCollapsed(false);
    }
  };

  const renderContent = () => {
    if (!selectedMenuItem) {
      return language === "kr" ? <LandingKR /> : <LandingEN />;
    }

    switch (selectedMenuItem) {
      case "1":
        return language === "kr" ? <LandingKR /> : <LandingEN />;
      case "2":
        return <SIGenie />;
      default:
        return language === "kr" ? <LandingKR /> : <LandingEN />;
    }
  };

  const currentBackgroundStyle =
    selectedMenuItem !== "2"
      ? {
          backgroundImage: `url(${backgroundImage})`, // 동적으로 배경 이미지 설정
          backgroundSize: "cover",
          backgroundPosition: "center",
        }
      : { backgroundColor: "#f0f4f8" };

  const GlobalStyle = createGlobalStyle`
    body, #root, .ant-typography, .ant-input, .ant-btn, .ant-menu {
      font-family: 'Freesentation', sans-serif !important;
    }
  `;

  return (
    <>
      <GlobalStyle />
      <Layout
        style={{
          display: "flex",
          minHeight: "100vh",
          maxHeight: "100vh", // 추가
          overflow: "hidden", // 추가
          fontFamily: "Freesentation, sans-serif",
          // backgroundImage: `url(${backgroundImage})`, // 동적으로 배경 이미지 설정
          // backgroundSize: "cover",
          // backgroundPosition: "center",
          ...currentBackgroundStyle,
        }}
      >
        <Header
          style={{
            background: "rgba(255, 255, 255, 0.8)",
            padding: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between", // 추가: 내용을 양쪽 끝으로 정렬
            position: "fixed",
            zIndex: 1,
            width: "100%",
            height: "64px",
          }}
        >
          <div style={{ display: "flex", alignItems: "center" }}>
            {React.createElement(
              collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
              {
                className: "trigger",
                onClick: toggleCollapsed,
                style: {
                  fontSize: "18px",
                  padding: "0 24px",
                  cursor: "pointer",
                },
              }
            )}
            <h2
              style={{
                margin: "0 16px",
                fontFamily: "Freesentation, sans-serif",
              }}
            >
              ContainerGenie.ai
            </h2>
          </div>
          <Space style={{ marginRight: "24px" }}>
            <Link href="https://bit.ly/containergenie_k" target="_blank">
              White Paper KR
            </Link>
            <span>/</span>
            <Link href="https://bit.ly/containergenie" target="_blank">
              EN
            </Link>
            <Select
              defaultValue={language}
              style={{ width: 120 }}
              onChange={(value: "kr" | "en") => setLanguage(value)}
              suffixIcon={
                <GlobalOutlined
                  style={{ fontSize: "1.2rem", pointerEvents: "none" }}
                />
              }
            >
              <Option value="kr">한국어</Option>
              <Option value="en">English</Option>
            </Select>
          </Space>
        </Header>
        <Layout
          style={{
            display: "flex",
            flexDirection: "row",
            background: "transparent",
            // marginTop: 64, // Header의 높이만큼 여백 추가
          }}
        >
          <Sider
            // width={200}
            style={{
              background: "rgba(255, 255, 255, 0.8)",
              position: "fixed",
              height: `calc(100vh - 64px)`,
              top: 64, // Header 아래에 위치
            }}
            collapsible
            collapsed={collapsed}
            onCollapse={(value) => setCollapsed(value)}
            collapsedWidth={65}
            trigger={null}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          >
            <Menu
              mode="inline"
              defaultSelectedKeys={["1"]}
              selectedKeys={[selectedMenuItem]}
              style={{
                height: `calc(100vh - 62px - 60px)`,
                borderRight: 0,
                background: "transparent",
                overflow: "auto",
              }}
              onSelect={({ key }) => setSelectedMenuItem(key)}
            >
              <Menu.Item key="1" icon={<HomeOutlined />}>
                Home
              </Menu.Item>
              <Menu.Item key="2" icon={<LaptopOutlined />}>
                SI Genie
              </Menu.Item>
            </Menu>
            <Footer
              style={{
                position: "fixed",
                textAlign: "center",
                background: "transparent",
                height: "60px",
                width: "200px",
              }}
            >
              <PinButton
                icon={<PushpinOutlined />}
                onClick={togglePinned}
                type={pinned ? "primary" : "default"}
              />
            </Footer>
          </Sider>
          <Layout
            style={{
              background: "transparent",
              marginTop: 64,
              marginLeft: collapsed ? 65 : 200,
              overflow: "auto",
              transition: "all 0.35s, background 0s",
            }}
          >
            <Content
              style={{
                padding: 24,
                margin: 0,
                height: "100%", // 수정
                background: "transparent",
                overflow: "auto", // 수정
              }}
            >
              {renderContent()}
            </Content>
            <Footer
              style={{
                textAlign: "center",
                background: "rgba(255, 255, 255, 0.8)",
                padding: "20px 0",
                height: "60px",
              }}
            >
              © 2024 ContainerGenie.ai. All rights reserved. | 0.06
            </Footer>
          </Layout>
        </Layout>
      </Layout>
    </>
  );
};

export default App;
