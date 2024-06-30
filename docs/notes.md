# Notes
* Allg. auf Auflösung/Komprimierung achten -> Max: 2000px bzw. 768px
* Use-Case Data-Extraction: Relevante Infos bzgl. Prüfschema im Genehmigungsprozess

## Planzeichnung
* Schlechte Ergebnisse. Ohne Object-Detection/Fine-Tuning nicht sinnvoll.
* TODO: a) Alle relevanten Bild-Ausschnitte b) Bild-Ausschnitt der Erklärung der Nutzungsschablone

## Zeichenerklärung
* Ausschnitt ist entscheidend, ob Text gut erkannt wird.
* Erklärung Nutzungsschablone muss dem LM klar sein. Sonst nicht konkret genug. -> TODO LLM muss Layout besser verstehen [Zeichen + Definition]
* Tabelle in Tabelle fällt dem LM schwer => Few-Shot könnte da helfen, damit das LM die Tabelle kennt.
* Bildausschnitt, Auflösung etc. sind wichtige Parameter wie gut OCR klappt.

## Textteil (FOKUS)
* Hier könnte das MLLM seine Stärken ausspielen / Ziel: Informationen zusammenfassen/exktrahieren/...
* Informationen verknüpfen -> BauGB/BauNVO (RAG)