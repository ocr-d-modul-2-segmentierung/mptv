Bitte irgendwo hin clonen und Ordnerstruktur beibehalten.  
Numpy wird benötigt.  
Alle Skripte bis auf conf_vote müssen mit Python 2 aufgerufen werden, also "python .../mptv/mptv-setup_folds.py ...".  
Für conf_vote bitte vorerst noch "python3 .../mptv/mptv-conf_vote.py ...". Mit Python 2 passieren eigenartige Fehler. Wird natürlich (hoffentlich) noch behoben.

### mptv-setup_folds
Input: Liste von Bildern (\*.png, \*.bin.png, \*.nrm.png, + zugehörige GT (\*.gt.txt))  
Output: Ordner (--output, default: ./Data) mit n (--folds, default = 5) Unterordnern die #lines/n Zeilen enthalten  

Zeilen wird die Ordner-ID voran gestellt, sodass gleichnamige Zeilen (Standard-OCRopus!) sich nicht überschreiben.

### mptv-run_multi_train
Input: Ordner der "Folds" Ordner enthält.  
Output: "Models" Ordner der die für jeden Fold trainierten Modelle enthält

In diesem und den folgenden Skripten muss bislang noch der Pfad zum den OCRopus-Skripten, zur Whitelist und zu den gemischten Modellen gesetzt werden.
Letztere befinden sich in ocropus_mptv/pretraining.
Das muss später noch schöner umgesetzt werden. 
Wichtig ist, dass, falls vorhanden, nicht die eigenen Skripte verwendet werden.  
--models: "LH,LH,FRK,ENG,ENG", bedeutet, dass die ersten beiden Folds ihr Training mit LH starten, Fold 3 mit ENG und 4,5 mit FRK.  
"LH,,,,LH" trainiert 1 und 5 von LH und den Rest von Null ab usw.

### mptv-find_best_model
Input: Ordner, der "Folds" als auch "Models" enthält.  
Output: Das beste Modell für jeden Fold in "Models/BestModels".  
Die Auswertung der verschiedenen Folds erfolgt nicht parallel. Daher -Q ruhig etwas hoch setzen.

### mptv-recognize_lines
Input: Ordner, die vorherzusagende Zeilen enthalten.  
Output: Ordner "Voting" in jedem Eingabeordner. Dieser enthält die Ergebnisse (\*.txt und \*.extLlocs) für jeden Fold.

### mptv-conf_vote  
Input: Liste der "Voting" Ordner aus dem vorherigen Schritt.  
Output: Gevotete .txts in den "Voting/Voted" Ordnern.  
Nach dem (hoffentlich erfolgreichen) Durchlaufen kommt eine Ausgabe wieviele llocs übersprungen und wieviele insgesamt bearbeitet wurden. 
Der erste Wert sollte nahe Null oder Null sein. Ansonsten mir bitte Bescheid geben und die Daten zukommen lassen.