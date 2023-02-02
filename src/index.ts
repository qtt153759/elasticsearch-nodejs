import express, { Express } from "express";
import dotenv from "dotenv";
import initWebRoutes from "./routes/api";
import configViewEngine from "./configs/viewEngine";

dotenv.config();

const app: Express = express();
const port = process.env.PORT;

configViewEngine(app);
initWebRoutes(app);

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at http://localhost:${port}`);
});
