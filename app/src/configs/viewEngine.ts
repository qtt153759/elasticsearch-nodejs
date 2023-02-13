import express, { Express } from "express";

const configViewEngine = (app: Express) => {
  app.use(express.static("./src/views"));
  app.set("view engine", "ejs");
  app.set("views", "./src/views");
};
export default configViewEngine;
