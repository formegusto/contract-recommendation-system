import express from "express";
import multer from "multer";
import path from "path";
import childProcess from "child_process";

class Routes {
  routes: express.Router;
  upload: express.RequestHandler;

  constructor() {
    this.routes = express.Router();
    this.upload = multer({
      storage: multer.diskStorage({
        destination: (req, file, cb) => {
          cb(null, "static");
        },
        filename: (req, file, cb) => {
          cb(
            null,
            `original-datas-${Date.now()}${path.extname(file.originalname)}`
          );
        },
      }),
    }).single("datas");
    this.setRouter();
  }

  setRouter() {
    this.routes.get("/", (req: express.Request, res: express.Response) => {
      return res.send("<h1>Hello, This is Node-Python Test Page</h1>");
    });

    this.routes.post(
      "/",
      this.upload,
      (req: express.Request, res: express.Response) => {
        const filename = req.file?.filename;

        if (filename) {
          console.log(`[Express] ${filename} read start.`);
          console.log(`[Express] ${filename} time ${new Date()}`);
          const readExcel = childProcess.spawn("python3", [
            "python/excel_read.py",
            filename,
          ]);

          readExcel.stdout.on("data", (data) => {
            console.log(data.toString());
          });

          readExcel.stdout.on("end", () => {
            console.log(`[Express] ${filename} read end.`);
            console.log(`[Express] ${filename} time ${new Date()}`);
          });

          readExcel.stderr.on("error", (data) => {
            console.log(data.toString());
          });
        }

        return res.status(201).json("file upload success");
      }
    );
  }
}

export default new Routes().routes;
