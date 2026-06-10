#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: lookup_concept.sh \"<Concept Name>\""
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GRAPH_PATH="$SKILL_DIR/graphify-out/graph.json"

if [ ! -f "$GRAPH_PATH" ]; then
  echo "Error: Knowledge graph not found at $GRAPH_PATH"
  exit 1
fi

graphify explain "$1" --graph "$GRAPH_PATH"
