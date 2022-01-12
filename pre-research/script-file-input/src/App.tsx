import React from "react";
// import XLSX from "xlsx";

function App() {
  // const onExcel = React.useCallback(
  //   (e: React.ChangeEvent<HTMLInputElement>) => {
  //     const reader = new FileReader();

  //     reader.onload = (e) => {
  //       const data = e.target?.result;
  //       console.log(data && data.toString().length);
  //       const wb = XLSX.read(data, { type: "binary" });
  //       const ws = wb.Sheets[wb.SheetNames[0]];
  //       console.log("WorkBook", wb);
  //       console.log("WorkSheet", ws);

  //       // console.log(ws[XLSX.utils.encode_cell({ r: 6, c: 8 })]);
  //       console.log("excel load end.");
  //       console.log("endTime:", new Date().getTime());
  //     };

  //     if (e.target.files)
  //       if (e.target.files[0]) {
  //         console.log("excel load start.");
  //         console.log("startTime:", new Date().getTime());
  //         reader.readAsBinaryString(e.target.files[0]);
  //       }
  //   },
  //   []
  // );

  return (
    <form>
      <input type="file" name="file" />;
    </form>
  );
}

export default App;
