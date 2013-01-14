#!/bin/bank
#
# This awk script process csv Alpha Bank operations log to Homebank's csv.
#
awk 'BEGIN {ORS="";  FS=";" }
$2~/[0-9]/ {
	print substr($4,1,2) "-" substr($4,4,2) "-" substr($4,9,11) ";";		#date
	;print 0  ";"; 		#mode
	print    ";";		#info
	print   ";";		#payee name
	print $6 ";";		#description

	if ($7>"0.00") print $7; 	  #amount
	if ($8>"0.00") print "-" $8;   #amount
	print     ";"           #amount
		
	print 		""		#category
	print "\n"

}
'  $1 |
iconv -f cp1251 -t utf-8 > out_$1