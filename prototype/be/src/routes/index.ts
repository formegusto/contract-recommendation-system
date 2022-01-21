import Express from "express";
import multer from "multer";
import path from "path";
import childProcess from "child_process";
import { Socket } from "socket.io";
import processRoutes from "./processRoutes";

class Routes {
  routes: Express.Router;
  upload: Express.RequestHandler;

  constructor() {
    this.routes = Express.Router();
    this.upload = multer({
      storage: multer.diskStorage({
        destination: (req, file, cb) => {
          cb(null, "static");
        },
        filename: (req, file, cb) => {
          cb(
            null,
            `original-data-${Date.now()}${path.extname(file.originalname)}`
          );
        },
      }),
    }).single("data");

    this.setRouter();
  }

  setRouter() {
    this.routes.use("/process", processRoutes);
    this.routes.post(
      "/",
      this.upload,
      (req: Express.Request, res: Express.Response) => {
        const filename = req.file?.filename;

        if (filename) {
          const readExcelProcess = childProcess.spawn("python3", [
            "python/reco_process.py",
            filename,
          ]);

          readExcelProcess.stderr.on("data", (data) => {
            console.log("error 발생!");
            console.log(data.toString());
          });

          return res.status(200).json({
            status: true,
            message: "추천 서비스를 시작합니다.",
          });
        }

        return res.status(403).json({
          status: false,
          message: "파일을 함께 보내주세요.",
        });
      }
    );
  }
}

export default new Routes().routes;
