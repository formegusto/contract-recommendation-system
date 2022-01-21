import React from "react";
import { connect, Socket } from "socket.io-client";
import axios from "axios";

type ALERT_DATA = {
  type: string;
  status: boolean;
};

const MESSAGE_TYPE: { [key: string]: string } = {
  "alert-test": "연결상태확인",
  "read-excel": "엑셀 로딩",
  "data-preprocessing": "데이터 전처리",
  "reco-process-start": "추천 서비스 시작",
};

function App() {
  const formData = React.useRef<FormData>(new FormData());
  const [socketProcess, setSocketProcess] = React.useState<
    React.ReactElement[]
  >([]);
  const [ioConnected, setIoConnected] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (!ioConnected) {
      const API_SERVER = process.env.REACT_APP_API_SERVER;
      const SOCKET_PATH = process.env.REACT_APP_SOCKET_PATH;

      const io: Socket = connect(`${API_SERVER}`, {
        path: `/${SOCKET_PATH}`,
        transports: ["websocket"],
      });

      io.on("connect", () => {
        setIoConnected(true);

        setSocketProcess((state) =>
          state.concat(<h1 key="socket-connected">알림 소켓 연결완료</h1>)
        );

        io.on("alert", (data: ALERT_DATA) => {
          setSocketProcess((state) =>
            state.concat(
              <h1 key={`${data.type}`}>
                {MESSAGE_TYPE[data.type]} : {data.status ? "성공" : "실패"}
              </h1>
            )
          );
        });
      });
    }
  }, [ioConnected]);

  const onChange = React.useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.name && e.target.files) {
        if (e.target.files[0])
          formData.current.append(e.target.name, e.target.files[0]);
      }
    },
    [formData]
  );

  const onSubmit = React.useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      const API_SERVER = process.env.REACT_APP_API_SERVER;

      axios.post(API_SERVER!, formData.current, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },
    [formData]
  );

  return (
    <>
      <form onSubmit={onSubmit}>
        <input type="file" onChange={onChange} name="data" />
        <button type="submit">파일 보내기</button>
      </form>
      <hr />
      <div>{socketProcess.map((SP) => SP)}</div>
    </>
  );
}

export default App;
