import json

transcript_path = "/Users/yamlam/.gemini/antigravity/brain/96f9f872-00c6-4623-a01a-bf571af51dd4/.system_generated/logs/transcript.jsonl"
targets = ["M00", "M01", "M05", "M06", "M07"]

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            step = json.loads(line)
            if "tool_calls" in step:
                for tc in step["tool_calls"]:
                    if tc["name"] in ["multi_replace_file_content", "replace_file_content"]:
                        args = tc["arguments"]
                        if isinstance(args, str):
                            args = json.loads(args)
                        target_file = args.get("TargetFile", "")
                        for t in targets:
                            if t in target_file:
                                print(f"--- Patch for {t} ---")
                                print(json.dumps(args, ensure_ascii=False, indent=2))
        except Exception as e:
            pass
