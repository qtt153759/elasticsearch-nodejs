import { Router, Express, Request, Response } from "express";
export const defaultRoute = Router();
import ElasticSearchController from "../controllers/elasticsearchController";
const initWebRoutes = (app: Express) => {
  defaultRoute.get("/fbScraper", ElasticSearchController.handleIndexPost);
  defaultRoute.get("/", ElasticSearchController.handleSearchPage);

  defaultRoute.get("/test", (req: Request, res: Response) => {
    return res.status(200).json({
      message: "ok",
      data: "test",
    });
  });
  return app.use("/", defaultRoute);
};
export default initWebRoutes;
