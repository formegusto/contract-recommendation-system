import React from "react";
import { connect, Socket } from "socket.io-client";

type ALERT_DATA = {
  type: string;
  status: boolean;
};

const MESSAGE_TYPE: { [key: string]: string } = {
  "alert-test": "연결상태확인",
};

function App() {
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

  return (
    <>
      <form>
        <input type="file" />
        <button type="submit">파일 보내기</button>
      </form>
      <hr />
      <div>{socketProcess.map((SP) => SP)}</div>
    </>
  );
}

export default App;
