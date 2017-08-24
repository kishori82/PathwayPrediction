
i=0

cat names2.txt | while IFS='	'  read  -r org  f
do 
  i=$(( $i + 1 ))
  echo $i" "${org}
  p=`tar -tf  biocyc_pgdbs/${f}.tar.gz | grep pathways.dat`;
  tar -xOf   biocyc_pgdbs/${f}.tar.gz  ${p} |  grep UNIQUE-ID | sed -e 's/^.*- //g'  > corepathways/${f}.txt
done;
