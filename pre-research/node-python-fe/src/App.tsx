import React from "react";
import axios from "axios";
import { connect } from "socket.io-client";

function App() {
  const formData = React.useRef<FormData>(new FormData());
  const [startTime, setStartTime] = React.useState<string>("");
  const [endTime, setEndTime] = React.useState<string>("");

  React.useEffect(() => {
    const io = connect("http://localhost:8080", {
      path: "/socket.io",
      transports: ["websocket"],
    });

    io.on("connect", () => {
      console.log("socket connected :)");
    });
    io.on("read-start", () => {
      console.log("datas read start");
      setStartTime(new Date().toISOString());
    });
    io.on("read-success", () => {
      console.log("datas read success");
      setEndTime(new Date().toISOString());
    });
  }, []);

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

      axios.post("http://localhost:8080", formData.current, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    },
    [formData]
  );

  return (
    <>
      <h1>Socket.IO Test</h1>
      <p>startTime:{startTime}</p>
      <p>endTime:{endTime}</p>
      <form onSubmit={onSubmit}>
        <input type="file" name="datas" onChange={onChange} />
        <button type="submit">Test!</button>
      </form>
    </>
  );
}

export default App;
