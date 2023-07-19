#!/bin/bash
# Scaling test

TYPE="scaling"
SITE="grenoble"
DURATION="10"
BOARD="m3:at86rf231"
NBSENDER=1
COORDINATOR="210"
TEMP="res_scaling"
re='^[0-9]+$'
NB_TEST_D=1
NB_TEST_A=10

echo "------------------------"
echo "Topology : $TYPE"
echo "Test duration : $DURATION min"
echo "Site : $SITE"
echo "Nb of tries : $(expr $(expr $NB_TEST_A - $NB_TEST_D) + 1)"
echo "------------------------"
echo ""

for i in $(seq $NB_TEST_D $NB_TEST_A)
do
    echo "Experience $i/$NB_TEST_A"
    NODE_PARAMETER="-l 1,archi=$BOARD+site=$SITE,../Firmware/coordinator.iotlab \
        -l $NBSENDER,archi=$BOARD+site=$SITE,../Firmware/sender.iotlab"    
    iotlab-experiment submit -n "${TYPE}_${i}" \
        -d $DURATION $NODE_PARAMETER > $TEMP
    EXP_ID=`cat $TEMP | tail -n 2 | head -n 1 | cut -d' ' -f6`
    iotlab-experiment wait -i $EXP_ID
    echo $SITE:$EXP_ID:$TYPE$NBSENDER >> exp_id.list
    rm -rf $TEMP
    serial_aggregator -i $EXP_ID > ~/.iot-lab/$EXP_ID/serial_aggregator_log
    echo "Done"
    echo ""
    if [ $(expr $(expr $i + 1) % 2) -eq 0 ]
    then
        NBSENDER=$(expr $NBSENDER + 1)
    fi
done