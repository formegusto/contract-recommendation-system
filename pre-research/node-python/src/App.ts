import express from "express";
import morgan from "morgan";
import routes from "./routes";
import sse from "./sse";

class App {
  server: express.Application;

  constructor() {
    this.server = express();
    this.settingMW();
    this.Router();
    this.Start();
    sse(this.server);
  }

  settingMW() {
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
