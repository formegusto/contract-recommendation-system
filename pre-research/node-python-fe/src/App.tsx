import React from "react";
import axios from "axios";
import { connect } from "socket.io-client";

function App() {
  const formData = React.useRef<FormData>(new FormData());

  React.useEffect(() => {
    const io = connect("http://localhost:8080", {
      path: "/socket.io",
      transports: ["websocket"],
    });

    io.on("connect", () => {
      console.log("socket connected :)");
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
      <h1>Server Sent Test</h1>
      <form onSubmit={onSubmit}>
        <input type="file" name="datas" onChange={onChange} />
        <button type="submit">Test!</button>
      </form>
    </>
  );
}

export default App;
