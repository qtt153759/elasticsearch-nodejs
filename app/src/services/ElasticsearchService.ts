import { Client } from "@elastic/elasticsearch";
import path from "path";
import Post from "../model/Post";
import Query from "../model/Query";
import fs from "fs";
import split from "split2";
const ELASTICSEARCH_HOSTS = process.env.ELASTICSEARCH_HOSTS;
const client = new Client({
  node: ELASTICSEARCH_HOSTS,
});
const getTextQuery = (text: string | undefined) => {
  if (!text) {
    return { match_all: {} };
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
  console.log("text", search.text);

  let currentDate = new Date().toJSON().slice(0, 10);
  console.log(currentDate);
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
                  source:
                    "_score * params.w1 + (doc['reaction_count'].value < 100 ? (doc['reaction_count'].value / 100) :1)*params.w2 + decayDateGauss(params.origin, params.scale, params.offset, params.decay, doc['time'].value)*params.w3", //doc['timestamp'].value*params.w3", //  +decayDateGauss(params.origin, params.scale, params.offset, params.decay, doc['timestamp'].value)*params.w3",
                  params: {
                    w1: 0.8,
                    w2: 0.1,
                    w3: 0.3,
                    origin: currentDate,
                    scale: "2d",
                    offset: "1d",
                    decay: 0.5,
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
        properties: {
          post_id: { type: "long" },
          post_url: { type: "keyword" },
          text: { type: "text" },
          shared_text: { type: "text" },
          time: {
            type: "date",
            format: "strict_date_optional_time",
            null_value: "2023-01-01T00:00:00",
          },
          comments_full: { type: "text" },
          timestamp: { type: "long", null_value: 1672531200 },
          reaction_count: { type: "integer" },
        },
      },
    },
  });
};
const create = async (datePicked: String) => {
  const datasetPath = path.join(`/data_facebook/data_final/${datePicked}.json`);
  console.log(datasetPath);
  const datasource = fs.createReadStream(datasetPath).pipe(split(JSON.parse));
  const result = await client.helpers.bulk<Post>({
    datasource,
    onDocument: (doc) => {
      console.log("doc: ", doc.post_id);
      return { create: { _index: "facebook", _id: doc.post_id } };
    },
    onDrop: (doc) => {
      console.log("can't index doc: ", doc.document.post_id);
    },
  });
  return result;
};
export default { getPage, createIfNotExistsIndex, create };
