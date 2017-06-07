ls pdfs/fetched/20*.pdf | while read -r fname; do
   maxpages=$(pdfinfo $fname | ack 'Pages:\s+(\d+)' --output '$1')
#   echo $fname has $maxpages
   for i in $(seq 1 $maxpages); do
    printf -v pagenum "%03d" $i
    pagename="${fname%.pdf}_$pagenum.txt"
    echo pdftotext -f "$i" -l  "$i" -layout $fname $pagename
    # GO
    pdftotext -f "$i" -l  "$i" -layout $fname $pagename


    done;
done
