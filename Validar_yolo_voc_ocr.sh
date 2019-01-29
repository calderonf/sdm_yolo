cowsay "Probando por favor cambiar la ruta en darknet/examples/detector.c"

echo "Compilacion de resultados"> validationcsv/allresults.csv

for ((ii=100;ii<1100;ii+=100)); do
    cowsay "Probando backupocr/yolo-voc-ocr_$ii.weights"
    echo "Resultados finales de iteracion $ii" >> validationcsv/allresults.csv
    ./darknet detector recall cfg/tinyocr.data /home/francisco/Dropbox/pesos_voc_ocr/yolo-ocr.cfg /home/francisco/Dropbox/pesos_voc_ocr/yolo-ocr_$ii.weights >> validationcsv/allresults.csv
done

for ((ii=1000;ii<81000;ii+=1000)); do
    cowsay "Probando backupocr/yolo-voc-ocr_$ii.weights"
    echo "Resultados finales de iteracion $ii" >> validationcsv/allresults.csv
    ./darknet detector recall cfg/tinyocr.data /home/francisco/Dropbox/pesos_voc_ocr/yolo-ocr.cfg /home/francisco/Dropbox/pesos_voc_ocr/yolo-ocr_$ii.weights >> validationcsv/allresults.csv
done




#cowsay "Probando backupocr/tiny-yolo-voc-ocr_11000.weights"
#./darknet detector recall cfg/tinyocr.data cfg/tiny-yolo-voc-ocr-predict.cfg backupocr/tiny-yolo-voc-ocr_11000.weights
