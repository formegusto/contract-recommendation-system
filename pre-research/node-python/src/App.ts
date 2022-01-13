import express from "express";
import morgan from "morgan";
import routes from "./routes";
import cors from "cors";

class App {
  server: express.Application;

  constructor() {
    this.server = express();
    this.settingMW();
    this.Router();
    this.Start();
  }

  settingMW() {
    this.server.use(cors());
    this.server.use(morgan("dev"));
  }

  Router() {
    this.server.use(routes);
  }

  Start() {
    this.server.listen(8080, () => {
      console.log("[Express] Server Start :)");
    });
  }
}

export default App;
