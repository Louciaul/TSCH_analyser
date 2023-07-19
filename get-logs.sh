#!/bin/bash

USER="wifi2023stras8"
SITE="strasbourg grenoble"
PATH="~/iot-lab/parts/iot-lab-contiki-ng/contiki-ng/tp-tsch/Ex5"
SITE_SUF=".iot-lab.info"
/usr/bin/mkdir -p all_data

echo "--------------------------------"
echo "Récuperation des id d'expérience"
echo "--------------------------------"
echo ""

for site in $SITE
do
    echo "Récuperation sur le site $site"
    VAL+=$(/usr/bin/ssh $USER@$site$SITE_SUF \
        "cat \
        ~/iot-lab/parts/iot-lab-contiki-ng/contiki-ng/tp-tsch/Ex5/exp_id.list" \
        )$'\n'
    echo $VAL
done 

echo "---------------------------------------"
echo " Récuperation sur chaque site des logs"
echo "---------------------------------------"
echo ""

for site in $SITE
do
    tmp=$(echo "$VAL" | /usr/bin/grep $site | /usr/bin/cut -d ":" -f2)
    echo "Récuperation des logs de $site"
    echo ""
    for j in $tmp
    do
        topo=$(echo "$VAL" | /usr/bin/grep $site | /usr/bin/grep $j | /usr/bin/cut -d ":" -f3)
        /usr/bin/mkdir -p ./all_data/${topo}
        if [[ ! -f ./all_data/${topo}/${topo}_${j}.log ]] || \
            [[ ! -f ./all_data/${topo}/${topo}_${j}.json ]] || \
            [[ ! -f ./all_data/${topo}/${topo}_${j}.data ]]
        then
            echo "Expérience $j"
            /usr/bin/scp $USER@$site$SITE_SUF:~/.iot-lab/$j/serial_aggregator_log \
                ./all_data/${topo}/${topo}_${j}.log
            if [ $? == 0 ]; then
                /usr/bin/ssh $USER@$site$SITE_SUF "iotlab-experiment get -i $j --nodes" \
                    > ./all_data/${topo}/${topo}_${j}.json
                /usr/bin/ssh $USER@$site$SITE_SUF \
                    "iotlab-experiment get -p -i $j" \
                    > ./all_data/${topo}/${topo}_${j}.data
            fi
            echo ""
        else
            echo "Expérience $j - existe déjà"
        fi
    done
    echo ""
done
