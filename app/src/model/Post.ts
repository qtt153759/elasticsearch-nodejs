interface Post {
  post_url: string;
  post_id: string;
  text: string;
  shared_text: string;
  comments_full: string;
  time: Date;
  timestamp: number;
  reaction_count: number;
}
export default Post;
