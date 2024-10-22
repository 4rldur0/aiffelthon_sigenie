import React, { useState } from 'react';
import styled from 'styled-components';

const PreviewContainer = styled.div`
  position: relative;
  display: inline-block;
`;

const PreviewContent = styled.div<{ isVisible: boolean }>`
  position: absolute;
  bottom: 0%;
  left: 50%;
  transform: translateX(-50%) scale(0.9);
  background-color: white;
  border: none;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: ${props => props.isVisible ? 'block' : 'none'};
  z-index: 1000;
  width: 400px;
  height: 300px;
  overflow: hidden;
  transition: all 0.2s ease-in-out;
`;

const PreviewFrame = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

interface LinkPreviewProps {
  href: string;
  children: React.ReactNode;
}

const LinkPreview: React.FC<LinkPreviewProps> = ({ href, children }) => {
  const [showPreview, setShowPreview] = useState(false);

  return (
    <PreviewContainer
      onMouseEnter={() => setShowPreview(true)}
      onMouseLeave={() => setShowPreview(false)}
    >
      <a href={href} target="_blank" rel="noopener noreferrer">{children}</a>
      <PreviewContent isVisible={showPreview}>
        <PreviewFrame src={href} title="Link Preview" />
      </PreviewContent>
    </PreviewContainer>
  );
};

export default LinkPreview;