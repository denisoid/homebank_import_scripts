#!/bin/python
# 
# Date: 2011_05_21 (First Release)
# Author: F.Quinto
# Special for Caixa d'Enginyers (https://www.caixa-enginyers.com)
# Ejemplo salida: 29/10/2007;6;;;DEBITO COMERCIO CAPRABO;-10.16;variable:tarjeta
# (dia+'/'+mes+'/20'+anyo+';'+pago+';;;'+info1+';'+signo+real+'.'+decimal+';'+categoria+'\n')
# 
# Use Python v.2.x

import os,string,sys

# Archivo de entrada
ARCHIVOIN = sys.argv[1]
fileIN = open(ARCHIVOIN, "r")

# Archivos de salida
ARCHIVOOUT = ARCHIVOIN[0:-4]+'.csv'
fileOUT = open(ARCHIVOOUT, "w")

dia=''
mes=''
anyo=''
pago=''
info1=''
signo=''
real=''
decimal=''
categoria=''

for line in fileIN.readlines():
	#print line[0:2]
	if line[0:2]=="22":
		# data operacio
		anyo=line[10:12]
		mes=line[12:14]
		dia=line[14:16]
		# data valor
		anyo2=line[16:18]
		mes2=line[18:20]
		dia2=line[20:22]
		if line[27:28]=='1':
			signo='-'
		if line[27:28]=='2':
			signo=''
		real=line[28:40]
		for i in range(12):
			if real.startswith("0"): real = real[1:]
		decimal=line[40:42]
	if line[0:2]=="23":
		# First comment
		info1=line[4:43].strip()
		# Categoria
		if info1[0:14] == 'INGRESO CHEQUE':
		  categoria = 'variable:banco'
		elif info1[0:13] == 'ADEUDO CHEQUE':
		  categoria = 'variable:banco'
		elif info1[0:6] == 'EFECTI':
		  categoria = 'variable:efectivo'
		elif info1[0:16] == 'INGRESO EFECTIVO':
		  categoria = 'variable:efectivo'
		elif info1[0:6] == 'TRANSF':
		  categoria = 'variable:transferencia'
		elif info1[0:10] == 'DEVOLUCION':
		  categoria = 'variable:entrada'
		elif (string.find(info1,'NOMINA'))!=-1:
		  categoria = 'fijo:entrada'
		elif info1[0:5] == 'TRASP':
		  categoria = 'variable:salida'
		elif info1[0:4] == 'PAGO':
		  categoria = 'variable:salida'
		elif info1[0:9] == 'REINTEGRO':
		  categoria = 'variable:salida'
		elif info1[0:5] == 'DEBIT':
		  categoria = 'variable:tarjeta'
		elif info1[0:16] == 'ANUL.LACIO DEBIT':
		  categoria = 'variable:tarjeta'
		elif info1[0:16] == 'ANULACION DEBITO':
		  categoria = 'variable:tarjeta'
		elif info1[0:7] == 'CUPONES':
		  categoria = 'variable:bolsa'
		elif info1[0:8] == 'DERECHOS':
		  categoria = 'variable:bolsa'
		elif info1[0:14] == 'ADEUDO VALORES':
		  categoria = 'variable:bolsa'
		elif info1[0:2] == 'R/':
		  categoria = 'fijo:rebuts'
		elif info1[0:13] == 'CARGA MOVILES':
		  categoria = 'variable:rebuts'
		elif info1[0:6] == 'SEGURO':
		  categoria = 'fijo:rebuts'
		elif info1[0:5] == 'QUOTA':
		  categoria = 'fijo:banco' #hipoteca
		elif info1[0:5] == 'CUOTA':
		  categoria = 'fijo:banco' #hipoteca
		elif info1[0:11] == 'BONIFICACIO':
		  categoria = 'variable:banco'
		elif info1[0:5] == 'COMIS':
		  categoria = 'variable:banco'
		elif info1[0:7] == 'INTERES':
		  categoria = 'variable:banco'
		elif info1[0:9] == 'ABONAMENT':
		  categoria = 'variable:banco'
		elif info1[0:13] == 'ADEUDO TITULO':
		  categoria = 'variable:banco'
		elif info1[0:16] == 'ADEUDO PROVISION':
		  categoria = 'variable:banco'
		elif info1[0:10] == 'ABONO PRES':
		  categoria = 'variable:banco'
		else:
		  categoria = '---------------------'
		# Pago
		if info1[0:14] == 'INGRESO CHEQUE':
		  pago = '2' # cheque
		elif info1[0:13] == 'ADEUDO CHEQUE':
		  pago = '2' # cheque
		elif info1[0:6] == 'EFECTI':
		  pago = '3' # efectivo
		elif info1[0:16] == 'INGRESO EFECTIVO':
		  pago = '3' # efectivo
		elif info1[0:6] == 'TRANSF':
		  pago = '4' # transferencia (-)
		elif info1[0:10] == 'DEVOLUCION':
		  pago = '4' # transferencia (-)
		elif (string.find(info1,'NOMINA'))!=-1:
		  pago = '4' # transferencia (-)
		elif info1[0:5] == 'TRASP':
		  pago = '5' # transferencia interna
		elif info1[0:4] == 'PAGO':
		  pago = '5' # transferencia interna
		elif info1[0:9] == 'REINTEGRO':
		  pago = '5' # transferencia interna
		elif info1[0:5] == 'DEBIT':
		  pago = '6' # tarjeta de debito
		elif info1[0:16] == 'ANUL.LACIO DEBIT':
		  pago = '6' # tarjeta de debito
		elif info1[0:16] == 'ANULACION DEBITO':
		  pago = '6' # tarjeta de debito
		elif info1[0:7] == 'CUPONES':
		  pago = '7' # orden de posicion
		elif info1[0:8] == 'DERECHOS':
		  pago = '7' # orden de posicion
		elif info1[0:14] == 'ADEUDO VALORES':
		  pago = '7' # orden de posicion
		elif info1[0:2] == 'R/':
		  pago = '8' # pago electronico
		elif info1[0:13] == 'CARGA MOVILES':
		  pago = '8' # pago electronico
		elif info1[0:6] == 'SEGURO':
		  pago = '8' # pago electronico
		elif info1[0:5] == 'QUOTA':
		  pago = '9' # deposito
		elif info1[0:5] == 'CUOTA':
		  pago = '9' # deposito
		elif info1[0:11] == 'BONIFICACIO':
		  pago = '10' # honorarios
		elif info1[0:5] == 'COMIS':
		  pago = '10' # honorarios
		elif info1[0:7] == 'INTERES':
		  pago = '10' # honorarios
		elif info1[0:9] == 'ABONAMENT':
		  pago = '10' # honorarios
		elif info1[0:13] == 'ADEUDO TITULO':
		  pago = '10' # honorarios
		elif info1[0:16] == 'ADEUDO PROVISION':
		  pago = '10' # honorarios 
		elif info1[0:10] == 'ABONO PRES':
		  pago = '10' # honorarios
		else:
		  pago = '0' # nada
# PAGO
# 0 nada
# 1 Tarjeta de credito
# 2 Cheque
# 3 Efectivo
# 4 Transferencia (-)
# 5 Transferencia interna
# 6 Tarjeta de debito
# 7 Orden de posicion
# 8 Pago electronico
# 9 Deposito
# 10 Honorarios
# FIN PAGO
	if (line[0:2]=="23"):
		fileOUT.write (dia+'/'+mes+'/20'+anyo+';'+pago+';;;'+info1+';'+signo+real+'.'+decimal+';'+categoria+'\n')
fileIN.close() 
fileOUT.close()