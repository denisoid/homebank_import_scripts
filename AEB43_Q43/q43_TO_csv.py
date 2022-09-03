#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author   Version  Date        Comments
# FQuinto  1.0.0    2011-05-21  First Release
# FQuinto  1.0.1    2016-12-27  New version for Homebank v.5.0.9 and for Python v.3.x
# FQuinto  1.0.2    2017-01-01  New output qif

# Special for Caixa d'Enginyers (https://www.caixa-enginyers.com)
# Copyright (C) 2011-2016 Fran Quinto

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import string
import sys

# Archivo de entrada
filename_Q43 = sys.argv[1]
fileIN_Q43 = open(filename_Q43, "r")

# Archivos de salida
qif_output = False
fileOUT_CSV = open(filename_Q43[0:-4] + '.csv', "w")
if qif_output:
    fileOUT_QIF = open(filename_Q43[0:-4] + '.qif', "w")

dia = ''
mes = ''
anyo = ''
paymode = ''
info = ''
real = ''
decimal = ''
category = ''

for line in fileIN_Q43.readlines():
    if line[0:2] == '11':
        cuenta = line[2:18]
        date_inicio_volcado = line[20:22] + '/' + line[22:24] + '/20' + line[18:20]
        date_final_volcado = line[26:28] + '/' + line[28:30] + '/20' + line[24:26]

        fileOUT_CSV.write('date;paymode;info;payee;wording;amount;category;tags' + '\n')

        if qif_output:
            fileOUT_QIF.write('!Account\n' +
                              'N' + cuenta + '\n' +
                              'TOth A\n' +
                              '^\n' +
                              '!Type:Oth A\n')

    if line[0:2] == '22':
        # data operacio
        anyo = line[10:12]
        mes = line[12:14]
        dia = line[14:16]
        # data valor
        anyo2 = line[16:18]
        mes2 = line[18:20]
        dia2 = line[20:22]
        signo = 'error'
        if line[27:28] == '1':
            signo = '-'
        if line[27:28] == '2':
            signo = ''
        real = line[28:40]
        for i in range(12):
            if real.startswith("0"):
                real = real[1:]
        decimal = line[40:42]
    if line[0:2] == "23":
        # First comment
        maxlinechars = 60
        info = line[4:maxlinechars].strip()

        # set payee
        payee = ''  # default
        payeeNu = ['*4016', 'NURIA LAGO', 'Nuria Lago']
        if any(txt in info for txt in payeeNu):
            payee = 'Nuria Lago'
        payeeFr = ['*5013', 'FRANCISCO JOS']
        if any(txt in info for txt in payeeFr):
            payee = 'Fran Quinto'

        # set category
        if info[0:14] == 'INGRESO CHEQUE':
            category = 'variable:banco'
        elif info[0:13] == 'ADEUDO CHEQUE':
            category = 'variable:banco'
        elif info[0:6] == 'EFECTI':
            category = 'variable:efectivo'
        elif info[0:16] == 'INGRESO EFECTIVO':
            category = 'variable:efectivo'
        elif 'INGRES EFECTIU' in info:
            category = 'variable:efectivo'
        elif (string.find(info, 'NOMINA')) != -1:
            category = 'fijo:entrada'
        elif info[0:5] == 'TRASP':
            if signo == '-':
                category = 'transferencia:negativa'
            else:
                category = 'transferencia:positiva'
        elif info[0:6] == 'TRANSF':
            if signo == '-':
                category = 'transferencia:negativa'
            else:
                category = 'transferencia:positiva'
        elif info[0:4] == 'paymode':
            category = 'variable:salida'
        elif info[0:9] == 'REINTEGRO':
            category = 'variable:salida'
        elif info[0:5] == 'DEBIT':
            category = 'variable:tarjeta'
        elif info[0:16] == 'ANUL.LACIO DEBIT':
            category = 'variable:tarjeta'
        elif info[0:16] == 'ANULACION DEBITO':
            category = 'variable:tarjeta'
        else:
            category = '-------ERROR--------'

        # Casa:impuestos
        categoryArray = ['OALGT', 'MUSA', 'FINCAS CARBONELL']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:impuestos'
        # Casa:hipoteca
        categoryArray = ['QUOTA', 'CUOTA']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:hipoteca'
        # Banco:bolsa
        categoryArray = ['ADEUDO VALORES', 'DERECHOS', 'CUPONES']
        if any(txt in info for txt in categoryArray):
            category = 'Banco:bolsa'
        # Banco:comisiones
        categoryArray = ['COM. CAIXER', 'COMIS']
        if any(txt in info for txt in categoryArray):
            category = 'Banco:comisiones'
        # Banco:otros
        categoryArray = ['ABONO PRES', 'ADEUDO PROVISION', 'ADEUDO TITULO', 'ABONAMENT', 'INTERES', 'BONIFICACIO']
        if any(txt in info for txt in categoryArray):
            category = 'Banco:otros'

        # Casa:movil
        categoryArray = ['Pepemobile', 'PEPEMOBILE', 'CARGA MOVILES']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:movil'

        # Casa:telefono
        categoryArray = ['TELEFONICA', 'ORANGE']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:telefono'
        # Casa:electricidad
        categoryArray = ['ENDESA ENERGIA']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:electricidad'
        # Casa:agua
        categoryArray = ['AIGUES DE BARCELONA']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:agua'
        # Casa:gas
        categoryArray = ['Gas Natural', 'GAS NATURAL']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:gas'
        # Seguros
        categoryArray = ['VIDA', 'SEGURO']
        if any(txt in info for txt in categoryArray):
            category = 'Seguros'
        # Casa:deco
        categoryArray = ['IKEA', 'LEROY']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:deco'
        # Casa:parking
        categoryArray = ['JOSEL S.L.U.']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:parking'

        # Ocio:viajes
        categoryArray = ['VIAJES']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:viajes'

        # Ocio:alojamiento
        categoryArray = ['HOTEL', 'ILUNION BILBAO']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:alojamiento'

        # Casa:comida
        categoryArray = ['Markt', 'MARKT', 'MARCHE', 'EROSKI', 'CARREFOURMARKET', 'ALDI S JOAN DESPI TDA 30', 'EMBUTIDOS LA MASIA', 'BON AREA', 'BON PREU SAU', '02 MAKRO BARCEL', 'MERCADONA', 'CARREFOUR', 'CAPRABO', 'LIDL']
        if any(txt in info for txt in categoryArray):
            category = 'Casa:comida'

        # Ocio:restaurante
        categoryArray = ['Restaurant', 'STARBUCKS', 'McDonald\'s', 'CERVECERIA MORITZ', 'RESTAURANT', 'MCDONALDS', 'NOSTRUM', 'ENRIQUE TOMAS', 'TOMMY MEL\'S', 'RESTAURANTE', 'ES ALAR DEL REY', 'CACHON SL', 'CUYNES SCP', 'EINSTEIN AM BIKINI PS GM', 'Kaisers', 'PINTXOS SELECTOS', 'PANS LA ROCA', 'LA MARQUESINA', 'PEIXOS ELS BOMBA', 'CUINATS', 'TIO CRISTOBAL', 'LA LLOSA', 'FOSTERS HOLLYWOOD', 'Buon appetito', 'maravillas', 'EL BUEN TAPEOCASA', 'VIENA']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:restaurante'

        # Ocio:billetes
        categoryPeajes = ['FENE', 'GUISAMO', 'A.C.E.S.A', 'S/AP15', 'AP6', 'A8/A1', 'INVICAT', 'AUTOPISTA', 'ARTEIXO', 'LA RIBERA']
        if any(txt in info for txt in categoryPeajes):
            category = 'Ocio:billetes'
        categoryBici = ['Reisebuero Im Europa Cen']
        if any(txt in info for txt in categoryBici):
            category = 'Ocio:billetes'
        categoryMetro = ['RATP', 'METRO BARCELONA']
        if any(txt in info for txt in categoryMetro):
            category = 'Ocio:billetes'
        categoryTren = ['RENFE', 'SNCF']
        if any(txt in info for txt in categoryTren):
            category = 'Ocio:billetes'
        categoryAvion = ['IBERIA', 'RYANAIR']
        if any(txt in info for txt in categoryAvion):
            category = 'Ocio:billetes'
        categoryBarco = ['EMBARCACIO']
        if any(txt in info for txt in categoryBarco):
            category = 'Ocio:billetes'

        # Ocio:otros
        categoryArray = ['HOSPEDAJE', 'BEEP INFORMATICA']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:informatica'
        categoryArray = ['DECATHLON']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:deporte'
        categoryArray = ['WONDERFUL', 'PEPPA PAPER', 'PPPO DEU I MATA', 'PAPYRUS']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:papeleria'
        categoryArray = ['promobo']
        if any(txt in info for txt in categoryArray):
            category = 'Ocio:otros'

        # Ocio:experience
        categoryMuseos = ['museum', 'MUSE']
        if any(txt in info for txt in categoryMuseos):
            category = 'Ocio:experience'
        categoryBalneario = ['SEMTEE SA WWW']
        if any(txt in info for txt in categoryBalneario):
            category = 'Ocio:experience'
        categoryCine = ['MULTICINES']
        if any(txt in info for txt in categoryCine):
            category = 'Ocio:experience'

        # paymode
        if info[0:14] == 'INGRESO CHEQUE':
            paymode = '2'  # cheque
        elif info[0:13] == 'ADEUDO CHEQUE':
            paymode = '2'  # cheque
        elif info[0:6] == 'EFECTI':
            paymode = '3'  # efectivo
        elif info[0:16] == 'INGRESO EFECTIVO':
            paymode = '3'  # efectivo
        elif info[0:14] == 'INGRES EFECTIU':
            paymode = '3'  # efectivo
        elif info[0:14] == 'CAIXER TARG. *':
            paymode = '3'  # efectivo
            category = 'variable:efectivo'
        elif info[0:6] == 'TRANSF':
            paymode = '4'  # transferencia (-)
        elif info[0:10] == 'DEVOLUCION':
            paymode = '4'  # transferencia (-)
        elif (string.find(info, 'NOMINA')) != -1:
            paymode = '4'  # transferencia (-)
        elif info[0:5] == 'TRASP':
            paymode = '4'  # transferencia
        elif info[0:4] == 'paymode':
            paymode = '4'  # transferencia
        elif info[0:9] == 'REINTEGRO':
            paymode = '4'  # transferencia
        elif info[0:5] == 'DEBIT':
            paymode = '6'  # tarjeta de debito
        elif info[0:16] == 'ANUL.LACIO DEBIT':
            paymode = '6'  # tarjeta de debito
        elif info[0:16] == 'ANULACION DEBITO':
            paymode = '6'  # tarjeta de debito
        elif info[0:9] == 'TARGETA *':
            paymode = '6'  # tarjeta de debito
        elif info[0:9] == 'DEVOLUCIO':
            paymode = '6'  # tarjeta de debito
        elif info[0:7] == 'CUPONES':
            paymode = '7'  # orden de posicion
        elif info[0:8] == 'DERECHOS':
            paymode = '7'  # orden de posicion
        elif info[0:14] == 'ADEUDO VALORES':
            paymode = '7'  # orden de posicion
        elif info[0:2] == 'R/':
            paymode = '8'  # paymode electronico
        elif info[0:13] == 'CARGA MOVILES':
            paymode = '8'  # paymode electronico
        elif info[0:6] == 'SEGURO':
            paymode = '8'  # paymode electronico
        elif info[0:5] == 'QUOTA':
            paymode = '9'  # deposito
        elif info[0:5] == 'CUOTA':
            paymode = '9'  # deposito
        elif info[0:11] == 'BONIFICACIO':
            paymode = '10'  # honorarios
        elif info[0:5] == 'COMIS':
            paymode = '10'  # honorarios
        elif info[0:7] == 'INTERES':
            paymode = '10'  # honorarios
        elif info[0:9] == 'ABONAMENT':
            paymode = '10'  # honorarios
        elif info[0:13] == 'ADEUDO TITULO':
            paymode = '10'  # honorarios
        elif info[0:16] == 'ADEUDO PROVISION':
            paymode = '10'  # honorarios
        elif info[0:10] == 'ABONO PRES':
            paymode = '10'  # honorarios
        elif info[0:11] == 'COM. CAIXER':
            paymode = '10'  # honorarios
        else:
            paymode = '0'  # nada

        # paymode
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
        # FIN paymode
        # date;paymode;info;payee;wording;amount;category;tags
        # info = string.replace(info, ':', '')
        print(info)
        print('   category ' + category)
        print('   payee ' + payee)
        # set homebank to %d/%m/%Y
        # default inside homebank is %x
        date = dia + '/' + mes + '/' + anyo
        wording = ''
        amount = signo + real + '.' + decimal
        tags = ''
        fileOUT_CSV.write(date + ';' + paymode + ';' + info + ';' + payee + ';' + wording + ';' + amount + ';' + category + ';' + tags + '\n')
        if qif_output:
            fileOUT_QIF.write('D' + date + '\nT' + amount + '\nC\nP' + payee + '\nM' + wording + '\nL' + category + '\n^\n')

fileIN_Q43.close()
fileOUT_CSV.close()
if qif_output:
    fileOUT_QIF.close()
