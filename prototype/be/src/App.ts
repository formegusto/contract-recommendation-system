import Express from "express";
import http from "http";
import morgan from "morgan";
import cors from "cors";
import socketConnect from "./Socket";
import routes from "./routes";

class App {
  server: http.Server;
  app: Express.Application;

  constructor() {
    this.app = Express();
    this.SettingMW();
    this.Router();

    this.server = http.createServer(this.app);
  }

  SettingMW() {
    this.app.use(cors());
    this.app.use(morgan("dev"));
    this.app.use(Express.json());
  }

  Router() {
    this.app.use(routes);
  }

  Start() {
    const port = process.env.PORT || "8000";
    this.server.listen(parseInt(port), () => {
      console.log(`----[Server] Start Server :)----
Port : ${port}
--------------------------------`);
    });
    socketConnect(this.server, this.app);
  }
}

export default new App();
