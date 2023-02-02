import { Client } from "@elastic/elasticsearch";
import path from "path";
import Post from "../model/Post";
import Query from "../model/Query";
import fs from "fs";
import split from "split2";

const client = new Client({
  node: "http://localhost:9200",
});
const getTextQuery = (text: string) => {
  const sort = [
    {
      timestamp: {
        order: "desc",
      },
    },
  ];
  if (!text) {
    return { match_all: {}, sort: sort };
  }
  return {
    bool: {
      should: [
        { match: { text: { query: text, boost: 2 } } },
        {
          match: {
            comments_full: text,
          },
        },
      ],
    },
  };
};
const getPage = async (search: Query) => {
  // let userList = await userService.getUserList();
  // return res.render("user.ejs", { userList });
  const response = await client.search<Post>({
    index: "facebook",

    body: {
      from: search?.page || 0,
      size: search?.offset || 10,

      query: {
        function_score: {
          query: getTextQuery(search.text),
          functions: [
            {
              script_score: {
                script: {
                  source: "_score * params.w1 + doc['reaction_count'].value", // * params.w2+decayDateGauss(params.origin, params.scale, params.offset, params.decay, doc['timestamp'].value)*params.w3",
                  params: {
                    w1: 0.7,
                    w2: 0.2,
                    // w3: 0.2,
                    // origin: 1675219018,
                    // scale: 259200,
                    // offset: 172800,
                    // decay: 0.5,
                  },
                },
              },
            },
          ],
        },
      },
    },
  });

  return response.hits.hits;
};
const createIfNotExistsIndex = async () => {
  const exists = await client.indices.exists({ index: "facebook" });
  if (exists) return;
  await client.indices.create({
    index: "facebook",
    body: {
      mappings: {
        dynamic: "strict",
        properties: {},
      },
    },
  });
};
const create = async () => {
  const datasetPath = path.join(
    "/home/qtt/facebook-scraper/final_data/2023-01-14/data_job_url.json"
  );
  const datasource = fs.createReadStream(datasetPath).pipe(split(JSON.parse));
  const result = await client.helpers.bulk<Post>({
    datasource,
    onDocument: (doc) => {
      console.log("doc: ", doc.post_id);
      return { create: { _index: "facebook", _id: doc.post_id } };
    },
    onDrop: (doc) => {
      console.log("can index doc: ", doc.document.post_id);
    },
  });
  return result;
};
export default { getPage, createIfNotExistsIndex, create };
