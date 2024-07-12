# Notes

* Allg. auf Auflösung/Komprimierung achten -> Max: 2000px bzw. 768px
* Use-Case Data-Extraction: Relevante Infos bzgl. Prüfschema im Genehmigungsprozess

=> Resolution Curse -> Visual Search + Cropping
=> Missing Know-How -> Bounding-Boxes

## Planzeichnung

* Schlechte Ergebnisse. Ohne Object-Detection/Fine-Tuning nicht sinnvoll.
* TODO: a) Alle relevanten Bild-Ausschnitte b) Bild-Ausschnitt der Erklärung der Nutzungsschablone

## Zeichenerklärung

* Ausschnitt ist entscheidend, ob Text gut erkannt wird.
* Erklärung Nutzungsschablone muss dem LM klar sein. Sonst nicht konkret genug. -> TODO LLM muss Layout besser verstehen [Zeichen + Definition]
* Tabelle in Tabelle fällt dem LM schwer => Few-Shot könnte da helfen, damit das LM die Tabelle kennt.
* Bildausschnitt, Auflösung etc. sind wichtige Parameter wie gut OCR klappt.
* Koordinaten / Geo-Ref. geht verloren.
* Flaschenhals = Context-Window (maximum token count) -> Workarounds nötig wie z.B. Vector-Stores/Embeddings.

## Textteil (FOKUS)

* Hier kann das MLLM seine Stärken ausspielen / Ziel: Informationen zusammenfassen/exktrahieren/...
* Informationen verknüpfen -> BauGB/BauNVO (RAG)

## Experimente

Konzeptionelle, qualitative Herangehensweise (Proof Of Concept):

* 3 Cluster (Kriterien: Jahr, Layout, Doc-Typen)
* Pro Cluster Experimente zur Nutzungsschablone (Level1 + Level2)
* Evaluation mit Herr Hascher (Interview, 1 B-Plan) + Metriken (Reliability, ...) zu allen 3 Clustern

## Tutorials

1. [LinkedIn Learning](https://www.linkedin.com/learning/developing-with-nondeterministic-apis/setting-a-seed-value?resume=false&u=67660530)
2. ...


## EVALUATION

* BB enhalten kleine Fehler
* Visual Search + Cropping -> nutzbare Ergebnisse
* OCR sehr gut in GPT-4o, solange Bildauflösung ausreicht
* Textverständnis abhängig von Kontext, Prompt und Archhitektur
