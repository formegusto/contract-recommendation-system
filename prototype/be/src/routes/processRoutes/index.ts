import Express from "express";
import { Socket } from "socket.io";

class ProcessRoutes {
  processRoutes: Express.Router;

  constructor() {
    this.processRoutes = Express.Router();
    this.setRouter();
  }

  setRouter() {
    this.processRoutes.patch(
      "/",
      (req: Express.Request, res: Express.Response) => {
        const body = <UpdateProcess>req.body;
        console.log(body);

        const socket = req.app.get("socket") as Socket;
        socket.emit("alert", {
          ...body,
        });

        return res.status(200).json({
          status: true,
          message: "해당 프로세스가 업데이트 되었습니다.",
        });
      }
    );
  }
}

export default new ProcessRoutes().processRoutes;
