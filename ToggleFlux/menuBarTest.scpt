(*
ignoring application responses
	tell application "System Events" to tell process "Flux"
		tell menu bar item 1 of menu bar 2
       		click
			(*
			considering application responses
				set var to name of menu item 4 of menu 1
			end considering
			*)
    	end tell
	end tell
end ignoring

do shell script "killall System\\ Events"
*)

ignoring application responses
tell application "System Events" to tell process "Flux"

	tell menu bar item 1 of menu bar 2

		click

		delay 0.1


		tell menu item "Disable" of menu 1
			delay 0.1
           	click
			delay 0.5
        	click menu item "for an hour" of menu "Disable"
     	end tell

		(*
		try
			tell menu item "f.lux is off" of menu 1
				delay 0.1
                click
            end tell
		on error
			tell menu item "Disable" of menu 1
					delay 0.1
               		click
					delay 0.5
               		click menu item "for an hour" of menu "Disable"
     		end tell
		end try
		*)
	end tell

end tell
end ignoring

(*
tell application "System Events" to tell process "Flux"
	if((var as string) is equal to "f.lux is off") then
		tell menu bar item 1 of menu bar 2
			tell menu item "f.lux is off" of menu 1
                click
            end tell
		end tell
	else
		tell menu bar item 1 of menu bar 2
			tell menu item "Disable" of menu 1
               		click
               		click menu item "for an hour" of menu "Disable"
     		end tell
		end tell
	end if
end tell
*)
(*
tell application "System Events" to tell process "Flux"
        if exists menu item whose title is "f.lux is off" then
                tell menu bar item 1 of menu bar 2
                        tell menu item "f.lux is off" of menu 1
                                click
                        end tell
                end tell
        else
                tell menu bar item 1 of menu bar 2
                        tell menu item "Disable" of menu 1
                                click
                                click menu item "for an hour" of menu "Disable"
                        end tell
                end tell
        end if
end tell
*)
