
set AppleScript's text item delimiters to ", "


on convertCoordsToString(coords)
    set originalDelimiter to AppleScript's text item delimiters
    set AppleScript's text item delimiters to ","

    set formattedString to coords as string
    set AppleScript's text item delimiters to originalDelimiter
    return formattedString
end convertCoordsToString

delay 5

tell application "System Events"
    set activeApp to name of first application process whose frontmost is true
    set activeAppWindows to windows of process activeApp
    log "Active application name: " & activeApp & " (Initial Windows: " & count of activeAppWindows & ")"   

    repeat with currentWindow in activeAppWindows
        set windowContent to (entire contents of currentWindow as list)  

        set dragSourcePositions to {}
        set dragDestinationPosition to ""

        repeat with windowElement in windowContent
            if (class of windowElement is image) then
                set imageSize to size of windowElement
                set imageName to name of windowElement
                set imageDesc to description of windowElement
                set imagePosition to position of windowElement

                set imageWidth to item 1 of imageSize
                set imageHeight to item 2 of imageSize

                set imageCenterW to item 1 of imagePosition + imageWidth / 2
                set imageCenterH to item 2 of imagePosition + imageHeight / 2
                set imagePosition to my convertCoordsToString({imageCenterW div 1, imageCenterH div 1})

                if imageName is "Applications" or imageDesc is "Applications" then
                    set dragDestinationPosition to imagePosition
                    log "[+] Found image which might correspond to the Terminal / Applications folder (Pos: " & imagePosition & " | Size: " & imageSize & ")" 
                else
                    set dragSourcePositions to dragSourcePositions & {imagePosition}
                    log "[+] Found source image (Pos: " & imagePosition & " | Size: " & imageSize & ")"
                end if
            end if
        end repeat

        if dragDestinationPosition is "" then
            log "No destination element found"
        else
            repeat with sourceImg in dragSourcePositions
                log "[+] Starting to drag and drop from " & sourceImg & " to " & dragDestinationPosition
                do shell script "cliclick dd:" & sourceImg & " dm:" & dragDestinationPosition & " du:" & dragDestinationPosition
                delay 1
            end repeat
        end if
    end repeat
end tell