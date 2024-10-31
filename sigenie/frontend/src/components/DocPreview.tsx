/**
 * 문서 템플릿을 출력하는 wrapper 컴포넌트
 * 템플릿(template Props 안의 React 컴포넌트)을 실제 문서와 유사한 배율로 출력하는 역할
 */

import React, { useRef, useLayoutEffect, useState, ReactNode } from "react";
import "../styles/docPreview.css";

interface DocPreviewProps {
  template: ReactNode;
  style?: React.CSSProperties;
}

const DocPreview: React.FC<DocPreviewProps> = ({ template, style }) => {
  // 브라우저 크기 감지용 Ref
  const previewRef = useRef<HTMLDivElement>(null);
  // 렌더링된 문서 템플릿 크기 감지용 Ref
  const contentRef = useRef<HTMLDivElement>(null);
  // 렌더링 배율
  const [scale, setScale] = useState(1);
  // 렌더링 후 컴포넌트 높이 조절용
  const [scaledHeight, setScaledHeight] = useState(0);

  // A4 용지 크기 (픽셀 단위)
  const A4_WIDTH_PX = 794; // 210mm * 3.7795
  // const A4_HEIGHT_PX = 1123; // 297mm * 3.7795

  useLayoutEffect(() => {
    const updateScaleAndHeight = () => {
      if (previewRef.current && contentRef.current) {
        const containerWidth = previewRef.current.clientWidth;

        // 배율 계산: 컨테이너 너비 대비 콘텐츠 원래 너비
        const newScale = containerWidth / A4_WIDTH_PX;
        setScale(newScale);

        // 강제로 리렌더링을 위해 setScale을 사용한 후에,
        // DOM이 업데이트된 후 실제 렌더링된 높이를 가져옵니다.
        requestAnimationFrame(() => {
          if (contentRef.current) {
            // transform이 적용된 실제 렌더링된 높이 가져오기
            const rect = contentRef.current.getBoundingClientRect();
            setScaledHeight(rect.height);
          }
        });
      }
    };

    updateScaleAndHeight();

    // ResizeObserver를 사용하여 컨테이너의 크기 변경 감지
    const resizeObserver = new ResizeObserver(() => {
      updateScaleAndHeight();
    });

    if (previewRef.current) {
      resizeObserver.observe(previewRef.current);
    }

    return () => {
      if (previewRef.current) {
        resizeObserver.unobserve(previewRef.current);
      }
    };
  }, []);

  return (
    <div
      className="docpreview-preview-container"
      ref={previewRef}
      style={{
        ...style,
        height: `${scaledHeight}px`,
      }}
    >
      <div
        className="docpreview-document-content"
        ref={contentRef}
        style={{
          width: `${A4_WIDTH_PX}px`,
          transform: `scale(${scale})`,
          transformOrigin: "top left",
        }}
      >
        {template}
      </div>
    </div>
  );
};

export default DocPreview;
