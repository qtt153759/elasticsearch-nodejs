import { Request, Response } from "express";
import Post from "../model/Post";
import Query from "../model/Query";
import ElasticsearchService from "../services/ElasticsearchService";
interface SearchQuery extends Express.Request {
  query: Query;
}
const handleSearchPage = async (req: SearchQuery, res: Response) => {
  // let userList = await userService.getUserList();
  // return res.render("user.ejs", { userList });
  try {
    const posts = await ElasticsearchService.getPage(req.query);

    return res.render("elasticsearch.ejs", { posts: posts });
  } catch (e) {
    console.error(e);
  }
};

const handleIndexPost = async (req: Request, res: Response) => {
  await ElasticsearchService.createIfNotExistsIndex();
  const response = await ElasticsearchService.create();
  console.log("total", response.total);
};

export default { handleSearchPage, handleIndexPost };
