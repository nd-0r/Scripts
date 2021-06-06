b=$(/usr/local/bin/brightness -l | grep 'brightness' | cut -c 23-30)
/usr/local/bin/brightness 0; sleep 0.01; /usr/local/bin/brightness $b

vms=$(/Applications/VMware\ Fusion.app/Contents/Public/vmrun list)
if [[ $vms == *"Boot Camp"* ]]; then
	/Applications/VMware\ Fusion.app/Contents/Public/vmrun -T fusion stop '/Users/andreworals/Library/Application Support/VMware Fusion/Virtual Machines/Boot Camp/Boot Camp.vmwarevm' && osascript -e 'quit app "VMware Fusion"'
else
	/Applications/VMware\ Fusion.app/Contents/Public/vmrun -T fusion start '/Users/andreworals/Library/Application Support/VMware Fusion/Virtual Machines/Boot Camp/Boot Camp.vmwarevm'
fi
