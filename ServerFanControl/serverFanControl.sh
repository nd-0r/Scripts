#! /bin/bash
DATE=$(date +%Y-%m-%d-%H%M%S)
echo "" && echo "" && echo "" && echo "" && echo ""
echo "$DATE"
#
IDRACIP=""
IDRACUSER=""
IDRACPASSWORD=""
STATICSPEEDBASE16="0x14"
SENSORNAME="Ambient"
TEMPTHRESHOLD=""
CONTINUE=true
trap "CONTINUE=false; sleep 3; ipmitool -I lanplus -H $IDRACIP -U $IDRACUSER -P $IDRACPASSWORD raw 0x30 0x30 0x01 0x01" INT
#
T=$(ipmitool -I lanplus -H $IDRACIP -U $IDRACUSER -P $IDRACPASSWORD sdr type temperature | grep $SENSORNAME | cut -d"|" -f5 | cut -d" " -f2)
# T=$(ipmitool -I lanplus -H $IDRACIP2 -U $IDRACUSER -P $IDRACPASSWORD sdr type temperature | grep $SENSORNAME2 | cut -d"|" -f5 | cut -d" " -f2 | grep -v "Disabled")
echo "$IDRACIP: -- current temperature --"
echo "$T"
#
while $CONTINUE; do
  if [[ $T > $TEMPTHRESHOLD ]]
    then
      echo "--> enable dynamic fan control $DATE"
      ipmitool -I lanplus -H $IDRACIP -U $IDRACUSER -P $IDRACPASSWORD raw 0x30 0x30 0x01 0x01
    else
      echo "--> disable dynamic fan control $DATE"
      ipmitool -I lanplus -H $IDRACIP -U $IDRACUSER -P $IDRACPASSWORD raw 0x30 0x30 0x01 0x00
      echo "--> set static fan speed"
      ipmitool -I lanplus -H $IDRACIP -U $IDRACUSER -P $IDRACPASSWORD raw 0x30 0x30 0x02 0xff $STATICSPEEDBASE16
  fi
  sleep 2
done
