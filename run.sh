#!/bin/bash
# Start-Skript für den Zahnklinik Voice Agent
# Verwendung: ./run.sh [console|dev|start|download-files]

set -e
cd "$(dirname "$0")"

export PATH="${HOME}/.local/bin:${PATH}"

CMD="${1:-console}"
case "$CMD" in
  console)
    echo "Starte Agent im Console-Modus..."
    uv run zahnklinik-agent console
    ;;
  dev)
    echo "Starte Agent im Dev-Modus (LiveKit)..."
    uv run zahnklinik-agent dev
    ;;
  start)
    echo "Starte Agent im Produktions-Modus..."
    uv run zahnklinik-agent start
    ;;
  download-files)
    echo "Lade Modelle herunter..."
    uv run zahnklinik-agent download-files
    ;;
  *)
    echo "Verwendung: $0 [console|dev|start|download-files]"
    exit 1
    ;;
esac
