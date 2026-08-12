# LLM-Obsidian

**LLM-Obsidian** ist ein lokaler KI-Assistent, der über Python ein Gemma-Modell mit meinen Obsidian-Notizen verbindet.

Das Projekt ermöglicht es, Fragen zu meinen Notizen zu stellen, Inhalte zusammenzufassen und zukünftig mein Kanban-Board sowie ein persönliches Memory einzubinden.

Aktuell werden die Obsidian-Notizen nur gelesen und nicht verändert.

## Architektur

Python ist die zentrale Anwendung und steuert die Kommunikation zwischen Obsidian, SQLite und Ollama.

```text
          LLM-Obsidian
               │
             Python
        ┌──────┼──────┐
        │      │      │
    Obsidian SQLite Ollama
                    │
                    ▼
                  Gemma

```

- Python – zentrale Anwendung
- Obsidian – Wissensquelle
- SQLite – Konversationshistorie
- Ollama – lokale Modelllaufzeit
- Gemma – Sprachmodell

 Das Modell greift nicht direkt auf Obsidian oder SQLite zu. Python liest die benötigten Daten und übergibt sie an Gemma.

## Installation unter Ubuntu

## Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```
## Python-Bibliothek
```python
pip install ollama
```
## LLM-Obsidian starten

```python
python3 main.py
```
 ## Ziel
Ein lokaler KI-Assistent, der meine Obsidian-Wissensbasis versteht und mich beim Lernen und Organisieren unterstützt.
