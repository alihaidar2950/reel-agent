#!/usr/bin/env python3
"""Queue one ComfyUI job per prompt, using a workflow exported with "Export (API)".

Usage:
  python queue_comfy.py --server http://127.0.0.1:8188 --workflow wan_api.json --prompts prompts.txt
  python queue_comfy.py ... --dry-run          # show what would be sent
  python queue_comfy.py ... --node 6           # the positive prompt node id, if auto-detect fails

prompts.txt: one prompt per line; empty lines and lines starting with # are skipped.
Standard library only.
"""
import argparse
import copy
import json
import random
import sys
import urllib.error
import urllib.request
import uuid

SEED_KEYS = ("seed", "noise_seed")


def find_positive_node(wf):
    # 1) Follow a sampler's "positive" input back to a node with a text input.
    for node in wf.values():
        inputs = node.get("inputs", {})
        link = inputs.get("positive")
        if isinstance(link, list) and link:
            target = wf.get(str(link[0]), {})
            if isinstance(target.get("inputs", {}).get("text"), str):
                return str(link[0])
    # 2) A text-encode node titled "Positive".
    for nid, node in wf.items():
        title = node.get("_meta", {}).get("title", "").lower()
        if "positive" in title and isinstance(node.get("inputs", {}).get("text"), str):
            return nid
    # 3) The only text-encode node, if there is exactly one.
    texts = [nid for nid, n in wf.items() if isinstance(n.get("inputs", {}).get("text"), str)]
    if len(texts) == 1:
        return texts[0]
    return None


def read_prompts(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]


def post(server, body):
    req = urllib.request.Request(
        server.rstrip("/") + "/prompt",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--server", required=True, help="ComfyUI URL, e.g. https://<pod>-8188.proxy.runpod.net")
    p.add_argument("--workflow", required=True, help="workflow saved with Export (API)")
    p.add_argument("--prompts", required=True, help="text file, one prompt per line")
    p.add_argument("--node", help="id of the positive prompt node (auto-detected if omitted)")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    with open(a.workflow, encoding="utf-8") as f:
        wf = json.load(f)
    if "nodes" in wf and "links" in wf:
        sys.exit("This is the UI format. In ComfyUI use Workflow -> Export (API) and pass that file.")

    node = a.node or find_positive_node(wf)
    if not node or node not in wf:
        sys.exit("Couldn't find the positive prompt node. Pass its id with --node.")
    prompts = read_prompts(a.prompts)
    if not prompts:
        sys.exit("No prompts found in " + a.prompts)

    client_id = str(uuid.uuid4())
    print(f"Prompt node {node} ({wf[node].get('class_type')}); {len(prompts)} clip(s).")
    for i, text in enumerate(prompts, 1):
        job = copy.deepcopy(wf)
        job[node]["inputs"]["text"] = text
        for n in job.values():
            for k in SEED_KEYS:
                if isinstance(n.get("inputs", {}).get(k), int):
                    n["inputs"][k] = random.randint(0, 2**48)
        if a.dry_run:
            print(f"[dry run] {i}: {text[:80]}")
            continue
        try:
            res = post(a.server, {"prompt": job, "client_id": client_id})
        except urllib.error.HTTPError as e:
            sys.exit(f"ComfyUI refused job {i}: {e.code} {e.read().decode('utf-8', 'replace')[:300]}")
        except urllib.error.URLError as e:
            sys.exit(f"Can't reach {a.server}: {e.reason}. Is the pod running and port 8188 exposed?")
        print(f"queued {i}/{len(prompts)}: {res.get('prompt_id')}  {text[:60]}")
    if not a.dry_run:
        print("Done. Clips appear in ComfyUI's output folder. Stop the pod when they finish.")


if __name__ == "__main__":
    main()
