/**
 * 백엔드 서버와 통신하는 API Endpoint 관리용 파일
 * 백엔드와 통신할 컴포넌트에서 import하여 사용
 *
 * ex)
 * import { EndpointUtil } from "../utils/EndpointUtil";
 *
 * const response = axios.get(EndpointUtil.API.REQUEST.SAMPLE)
 */

const API_HOST = process.env.REACT_APP_API_HOST;
const API_PORT = process.env.REACT_APP_API_PORT;

const apiUrl = `${API_HOST}:${API_PORT}`;

export class EndpointUtil {
  public static readonly API = {
    REQUEST: {
      SAMPLE: apiUrl + "/sample",
      SAMPLE_WITH_ID: apiUrl + "/sample/{sampleId}",
      QUERY_CH1: apiUrl + "/streaming_sync/chat/ch1",
      QUERY_CH2: apiUrl + "/streaming_sync/chat/ch2",
    },
  };
}
