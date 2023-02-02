interface Post {
  original_request_url: string;
  post_url: string;
  post_id: string;
  text: string;
  post_text: string;
  shared_text: string;
  comments_full: string;
  time: Date;
  timestamp: number;
  likes: number;
  reaction_count: number;
}
export default Post;
