#!/bin/bash
# Start-Skript für den Zahnklinik Voice Agent
# Verwendung: ./run.sh [console|dev|download-files]

set -e
cd "$(dirname "$0")"

# uv in PATH
export PATH="${HOME}/.local/bin:${PATH}"

CMD="${1:-console}"
case "$CMD" in
  console)
    echo "Starte Agent im Console-Modus..."
    uv run agent.py console
    ;;
  dev)
    echo "Starte Agent im Dev-Modus (LiveKit)..."
    uv run agent.py dev
    ;;
  start)
    echo "Starte Agent im Produktions-Modus..."
    uv run agent.py start
    ;;
  download-files)
    echo "Lade Modelle herunter..."
    uv run agent.py download-files
    ;;
  *)
    echo "Verwendung: $0 [console|dev|start|download-files]"
    exit 1
    ;;
esac
