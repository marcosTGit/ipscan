import sys, subprocess
#000000000000000000000000000000000000000000000000000000000000
#000000000000000000000000000000000000000000000000000000000000
# HACEMOS PING

ip = sys.argv[1]

nombre_equipo_default="*S/D"
workgrupo_default="*S/D"
mac_default="00:00:00:00:00:00"

i=ip.split(".")
if len(i)!=4: #verifico que tenga 4 segmentos
    print("EROOR ip invalida")
    exit
if ip[0].isnumeric==False or ip[0].isnumeric==False or ip[0].isnumeric==False or ip[0].isnumeric==False: # verifico q cada segmento sea numerico
    print("EROOR ip formato invalido")
    exit
if int(i[0]) in range(0,256) and int(i[1]) in range(0,256) and int(i[2]) in range(0,256) and int(i[3]) in range(0,256):
    # LA IP INGRESADA ES VALIDA
    comando_ping="ping -n 2 -w 1 "+ip
    res=subprocess.Popen(comando_ping, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err=res.communicate()
    lineout='{0}'.format(out)

    est=lineout.split("(")
    estadisticas=est[1].split("),")
    estadisticas=str(estadisticas[0])

    if res.returncode==0:
        # SI RESPONDE LA IP HACEMOS UN ARP
        comando_arp='arp -a |find "'+ip+'"'
        res=subprocess.Popen(comando_arp, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err=res.communicate()
        lineout='{0}'.format(out)

        rutas=lineout.split("\r\n")
        mac=lineout.split("-")
        if len(mac) == 6:  
            # // Le damos formato a la mac si tiene un formato valido de 6 segmentos
            macs1=mac[0][-2:]
            macs2=mac[3].split(" ")
            direccion_mac = str(macs1)+":"+str(mac[1])+":"+str(mac[2])+":"+str(mac[3])+":"+str(mac[4])+":"+str(macs2[0])
        else:
            direccion_mac=mac_default

        if res.returncode==0:
            # AHORA INTENTAMOS OBTENER EL NOMBRE DE EQUIPO 
            comando_nbtstat="nbtstat -a "+ip
            res=subprocess.Popen(comando_nbtstat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err=res.communicate()
            lineout='{0}'.format(out)
            if "<00>" in '{0}'.format(out):
                nom_equip=lineout.split("<")
                nombre_equipo=nom_equip[0].split("---------------------------------------------\\r\\n   ")
                # print(nombre_equipo[1])
                nombre_equipo=nombre_equipo[1]
                workgroup=nom_equip[0].split("Registrado \r\n   ")
                workgroup=workgroup[0].split("---------------------------------------------\\r\\n   ")
                # print(workgroup[1].strip())
                workgroup=workgroup[1].strip()
            else:
                nombre_equipo=nombre_equipo_default
                workgroup=workgrupo_default  
        else:
            direccion_mac=mac_default
            # LA DIRECCION MAC NO SE PUDO OBTENER
        print("> "+ str(ip) + " responde: "+str(estadisticas)+" MAC: "+str(direccion_mac)+ " NOM_EQUIPO: "+str(nombre_equipo)+" GRUPO:"+str(workgroup))
    else:
        print("< SIN RESPUESTA >")
        exit
else:
    print("ERROR ip fuera de rango valido")
    exit



