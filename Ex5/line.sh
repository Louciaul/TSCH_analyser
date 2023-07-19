#!/bin/bash
# Line test

TYPE="line"
SITE="grenoble"
DURATION="30"
BOARD="m3"
SENDER="21+27+33+39+45+51+57+63"
COORDINATOR="69"
NODE_PARAMETER="-l $SITE,$BOARD,$COORDINATOR,../Firmware/coordinator.iotlab \
    -l $SITE,$BOARD,$SENDER,../Firmware/sender.iotlab"    
TEMP="res_line"
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
    iotlab-experiment submit -n "${TYPE}_${i}" \
        -d $DURATION $NODE_PARAMETER > $TEMP
    EXP_ID=`cat $TEMP | tail -n 2 | head -n 1 | cut -d' ' -f6`
    iotlab-experiment wait -i $EXP_ID
    echo $SITE:$EXP_ID:$TYPE >> exp_id.list
    rm -rf $TEMP
    serial_aggregator -i $EXP_ID > ~/.iot-lab/$EXP_ID/serial_aggregator_log 
    echo "Done"
    echo ""
done