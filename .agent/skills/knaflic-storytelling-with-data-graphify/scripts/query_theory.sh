#!/bin/bash
if [ -z "$1" ]; then
  echo "Usage: query_theory.sh \"<Theoretical Question>\""
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GRAPH_PATH="$SKILL_DIR/graphify-out/graph.json"

if [ ! -f "$GRAPH_PATH" ]; then
  echo "Error: Knowledge graph not found at $GRAPH_PATH"
  exit 1
fi

# Fetch exactly up to 1500 tokens of dynamically scoped theory
graphify query "$1" --budget 1500 --graph "$GRAPH_PATH"
