#!/bin/bash
#
# This awk script process csv WebMoney operations log to Homebank's csv.
#
awk 'BEGIN {ORS="";  FS=";" }
$1~/[0-9]/ {
	print substr($1,10,2) "-" substr($1,7,2) "-" substr($1,4,2) ";";		#date
	;print 0  ";"; 		#mode
	print    ";";		#info
	print $6 ";";		#payee name
	print $7 ";";		#description

	if ($2) print $2; 	  #amount
	if ($3) print "-" $3;   #amount
	print     ";"           #amount
		
	print 		""		#category
	print "\n"
	sum+=$4
}
END {
"date +\"%d-%m-%y\"" | getline; print;
print 		";0;;\"Webmoney\";\"courtage\";-" sum ";\n"
}
'  $1 |
sed  's/"//g' |
iconv -f cp1251 -t utf-8 > out_$1