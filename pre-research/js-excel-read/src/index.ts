// import ExcelJS from "exceljs";
import path from "path";
import { XLSX } from "xlsx-extract";

const filePath = path.join(__dirname, "../datas/datas.xlsx");

new XLSX()
  .extract(filePath, { sheed_id: 1 })
  .on("sheet", (sheet: any) => {
    console.log(sheet);
  })
  .on("row", (row: any) => {
    console.log(row);
  });

// async function loadExcelFile(filePath: string) {
//   const workbook = new ExcelJS.Workbook();
//   await workbook.xlsx.readFile(filePath);
//   const worksheet = workbook.worksheets;

//   console.log(worksheet);
// }

// loadExcelFile(filePath);
