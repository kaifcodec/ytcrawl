class CommentParser:
    @staticmethod
    def find_key(obj, target_key):
        """Recursive generator to find any key in a deep JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == target_key:
                    yield v
                yield from CommentParser.find_key(v, target_key)
        elif isinstance(obj, list):
            for item in obj:
                yield from CommentParser.find_key(item, target_key)

    @classmethod
    def extract_batch(cls, data):
        comments = []
        next_token = None

        for renderer in cls.find_key(data, "commentRenderer"):
            author = "".join([r.get("text", "") for r in renderer.get(
                "authorText", {}).get("runs", [])])
            text = "".join([r.get("text", "") for r in renderer.get(
                "contentText", {}).get("runs", [])])
            if text:
                comments.append(
                    {"type": "standard", "author": author, "text": text})

        if not comments:
            for vm in cls.find_key(data, "commentViewModel"):
                text = vm.get("content", {}).get("content", "")
                if text:
                    comments.append(
                        {"type": "viewmodel", "author": "User", "text": text})

        for item in cls.find_key(data, "continuationItemRenderer"):
            try:
                next_token = item["continuationEndpoint"]["continuationCommand"]["token"]
                break
            except (KeyError, TypeError):
                continue

        return comments, next_token
