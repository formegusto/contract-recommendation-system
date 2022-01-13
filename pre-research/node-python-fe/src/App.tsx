import React from "react";
import axios from "axios";

function App() {
  const formData = React.useRef<FormData>(new FormData());

  React.useEffect(() => {}, []);

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
