echo "Probando por favor cambiar la ruta en darknet/examples/detector.c"

echo "pesos en /home/francisco/darknet_mio/backup/"
echo "Compilacion de resultados"> validationcsv/allresults.csv

for ((ii=100;ii<1000;ii+=100)); do
    echo "Probando backup/yolo-obj_$ii.weights"
    echo "Resultados finales de iteracion $ii" | tee -a validationcsv/allresults.csv
    ./darknet detector map data/obj.data yolo-obj.cfg backup/yolo-obj_$ii.weights | tee -a validationcsv/allresults.csv
done

for ((ii=1000;ii<90000;ii+=1000)); do
    echo "Probando backup/yolo-obj_$ii.weights"
    echo "Resultados finales de iteracion $ii" | tee -a validationcsv/allresults.csv
    ./darknet detector map data/obj.data yolo-obj.cfg backup/yolo-obj_$ii.weights | tee -a validationcsv/allresults.csv
done

