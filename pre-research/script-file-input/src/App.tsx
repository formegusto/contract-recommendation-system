import React from "react";
import XLSXEx from "xlsx-extract";

function App() {
  const [filePath, setFilePath] = React.useState<string | null>(null);
  const onExcel = React.useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files)
        if (e.target.files[0]) {
          console.log("excel load start.");
          console.log("startTime:", new Date().getTime());
          const path = (e.target.files[0] as any).path;

          setFilePath(path);
        }
    },
    []
  );

  React.useEffect(() => {
    if (filePath) {
      const XLSX = XLSXEx.XLSX;
      console.log(XLSX);
    }
  }, [filePath]);

  return (
    <form>
      <input type="file" name="file" onChange={onExcel} />;
    </form>
  );
}

export default App;
