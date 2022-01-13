import express from "express";
import morgan from "morgan";
import routes from "./routes";
import cors from "cors";
import socket from "./socket";
import http from "http";

class App {
  server: http.Server;
  app: express.Application;

  constructor() {
    this.app = express();
    this.server = http.createServer(this.app);
    this.settingMW();
    this.Router();
    this.Start();
  }

  settingMW() {
    this.app.use(cors());
    this.app.use(morgan("dev"));
  }

  Router() {
    this.app.use(routes);
  }

  Start() {
    this.server.listen(8080, () => {
      console.log("[Express] Server Start :)");
    });
    socket(this.server, this.app);
  }
}

export default App;
