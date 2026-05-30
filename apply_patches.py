import json
import os

transcript_path = "/Users/yamlam/.gemini/antigravity/brain/96f9f872-00c6-4623-a01a-bf571af51dd4/.system_generated/logs/transcript.jsonl"
targets = ["M00", "M01", "M05", "M06", "M07"]

with open(transcript_path, 'r') as f:
    for line in f:
        try:
            step = json.loads(line)
            if "tool_calls" in step:
                for tc in step["tool_calls"]:
                    if tc.get("name") in ["multi_replace_file_content", "replace_file_content"]:
                        args = tc.get("args") or tc.get("arguments")
                        if isinstance(args, str):
                            args = json.loads(args)
                        target_file = args.get("TargetFile", "").strip('"')
                        for t in targets:
                            if t in target_file:
                                print(f"Found patch for {t}")
                                try:
                                    with open(target_file, "r") as tf:
                                        content = tf.read()
                                    chunks = args.get("ReplacementChunks", [])
                                    if isinstance(chunks, str):
                                        chunks = json.loads(chunks, strict=False)
                                    for chunk in chunks:
                                        target_str = chunk.get("TargetContent", "")
                                        replace_str = chunk.get("ReplacementContent", "")
                                        if target_str in content:
                                            content = content.replace(target_str, replace_str)
                                            print(f"  Applied chunk for {t}")
                                        else:
                                            print(f"  WARNING: Target content not found in {t}")
                                    with open(target_file, "w") as tf:
                                        tf.write(content)
                                except Exception as inner_e:
                                    print(f"  Error modifying {target_file}: {inner_e}")
        except Exception as e:
            pass
