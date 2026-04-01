class CommentParser:

    @staticmethod
    def find_key(obj, target_key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == target_key:
                    yield v
                yield from CommentParser.find_key(v, target_key)
        elif isinstance(obj, list):
            for item in obj:
                yield from CommentParser.find_key(item, target_key)

    @staticmethod
    def extract_text(obj):
        if isinstance(obj, list):
            return "".join(CommentParser.extract_text(i) for i in obj)
        elif isinstance(obj, dict):
            if "runs" in obj:
                return CommentParser.extract_text(obj["runs"])
            if "text" in obj:
                return str(obj.get("text", ""))
            return ""
        elif isinstance(obj, (str, int, float)):
            return str(obj)
        return ""

    @classmethod
    def extract_batch(cls, data):
        comments = []
        next_token = None

        for renderer in cls.find_key(data, "commentRenderer"):
            author = cls.extract_text(renderer.get("authorText", {}))
            text = cls.extract_text(renderer.get("contentText", {}))
            reply_count = cls.extract_text(renderer.get("replyCount", {}))
            likes = cls.extract_text(renderer.get("voteCount", {}))

            if text:
                comments.append({
                    "type": "standard",
                    "author": author,
                    "text": text,
                    "replyCount": reply_count,
                    "likes": likes
                })

        if not comments:
            for vm in cls.find_key(data, "commentViewModel"):
                text = cls.extract_text(vm.get("content", {}).get("content", ""))
                if text:
                    comments.append({
                        "type": "viewmodel",
                        "author": "User",
                        "text": text,
                        "replyCount": "",
                        "likes": ""
                    })

        for item in cls.find_key(data, "continuationItemRenderer"):
            try:
                next_token = item["continuationEndpoint"]["continuationCommand"]["token"]
                break
            except (KeyError, TypeError):
                continue

        return comments, next_token
