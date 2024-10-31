#!/bin/bash

# 스크립트 실행 중 에러 발생 시 중지
set -e

# 프론트엔드 실행
echo "프론트엔드를 실행합니다..."
cd frontend
npm install
npm start &  # 프론트엔드를 백그라운드에서 실행

# 백엔드 실행
echo "백엔드를 실행합니다..."
cd ../backend
docker-compose build
docker-compose up

# 완료 메시지
echo "프론트엔드 및 백엔드가 실행 중입니다."