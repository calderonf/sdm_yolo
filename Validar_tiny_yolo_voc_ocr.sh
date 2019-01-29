cowsay "Probando"

echo "Compilacion de resultados"> validationcsv/allresults.csv

for ((ii=100;ii<1000;ii+=100)); do
    cowsay "Probando backup/tiny-yolo-voc-ocr_$ii.weights"
    echo "Resultados finales de iteracion $ii" >> validationcsv/allresults.csv
    ./darknet detector recall cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backup/tiny-yolo-voc-ocr_$ii.weights >> validationcsv/allresults.csv
done

for ((ii=10000;ii<41000;ii+=1000)); do
    cowsay "Probando backup/tiny-yolo-voc-ocr_$ii.weights"
    echo "Resultados finales de iteracion $ii" >> validationcsv/allresults.csv
    ./darknet detector recall cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backup/tiny-yolo-voc-ocr_$ii.weights >> validationcsv/allresults.csv
done




#cowsay "Probando backup/tiny-yolo-voc-ocr_11000.weights"
#./darknet detector recall cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backup/tiny-yolo-voc-ocr_11000.weights
