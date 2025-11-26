set AppleScript's text item delimiters to ", "

set autofillPassword to "testpass"
set screenshotsDir to "./screenshots/"

set forwardButtonKeywords to {"install", "accept", "continue", "next", "advance", "allow", "agree", "use password"}
set finishedButtonKeywords to {"finish", "done", "complete", "close"}

set exceptedButtonRoles to {"AXMinimizeButton", "AXFullScreenButton", "AXCloseButton"}

on convertToLower(str)
    set lowercaseStr to do shell script "echo " & quoted form of str & " | tr '[:upper:]' '[:lower:]'"
    return lowercaseStr
end convertToLower

on takeScreenshot(stepIdx)
    global screenshotsDir
    do shell script ("mkdir -p " & screenshotsDir)
    do shell script ("screencapture " & screenshotsDir & "step-" & stepIdx & ".png")
end takeScreenshot

delay 3

tell application "System Events"
    set activeApp to name of first application process whose frontmost is true
    set activeAppWindows to windows of process activeApp
    log "Active application name: " & activeApp & " (Initial Windows: " & count of activeAppWindows & ")"   

    -- Repeat the process until the installation is finished
    set stepIdx to 1
    repeat
        log "Starting step " & stepIdx & " (Windows: " & count of activeAppWindows & ")"

        set windowIdx to 1
        set buttonPressed to false
        repeat with currentWindow in activeAppWindows
            set buttonsInfo to {}
            set windowContent to (entire contents of currentWindow as list)     
            repeat with windowElement in windowContent
                if (class of windowElement is scroll bar) then
                    log "Found scrollbar"
                    set scrollbarName to name of windowElement
                    if scrollbarName is not missing value then
                        log "Scrollbar name: " & scrollbarName
                    end if

                    set scrollbarValue to value of windowElement
                    if scrollbarValue is not missing value then
                        log "Scrollbar initial value: " & scrollbarValue
                    end if

                    # Scrolling - method 1
                    set value of windowElement to 1

                    # Scrolling - method 2
                    click windowElement
                    repeat
                        try
                            set currentPosition to value of windowElement
                            key code 125 -- Press Arrow down key
                            delay 0.1
                            
                            set newPosition to value of windowElement
                            if newPosition is equal to currentPosition then
                                exit repeat
                            end if
                        end try
                    end repeat
                    
                else if (class of windowElement is text field) then
                    log "Found input"
                    set inputName to name of windowElement
                    if inputName is not missing value then
                        set lowercaseInputName to my convertToLower(inputName)
                        log "Input name: " & lowercaseInputName

                        if lowercaseInputName contains "password" then
                            log "Password input found. Entering password.."
                            set value of windowElement to autofillPassword
                            keystroke return
                        end if
                    end if 
                    log "------------------------------"                
                
                else if (class of windowElement is button) then                
                    set buttonRole to ""
                    set buttonInfo to {name: name of windowElement}
                    set targetedButtonAttributes to {"AXHelp", "AXSize", "AXTitle", "AXFocused", "AXIdentifier", "AXDescription", "AXSubrole", "AXRoleDescription"}
                    repeat with attr in targetedButtonAttributes
                        try
                            set attrVal to value of attribute attr of windowElement
                            if attrVal is missing value then
                                set attrVal to "-"
                            end if
                        on error errMsg
                            set attrVal to "-"
                        end try

                        if (attr as string) is equal to "AXSubrole" then
                            set buttonRole to attrVal
                        end if 

                        set buttonInfo to buttonInfo & (run script "return {" & attr & ":\"" & attrVal & "\"}")
                    end repeat     

                    -- Exclude the Close, Minimize and Full Screen buttons
                    if buttonRole is not equal to "AXCloseButton" and buttonRole is not equal to "AXMinimizeButton" and buttonRole is not equal to "AXZoomButton" then
                        set buttonsInfo to buttonsInfo & {buttonInfo}
                    end if

                end if    
            end repeat

            repeat with extractedButton in buttonsInfo 
                -- Proceed to the next step
                repeat with targetKeyword in forwardButtonKeywords
                    set buttonName to name of extractedButton
                    if (buttonName starts with targetKeyword) then
                        log "[+] Found advance button: " & buttonName
                        tell process activeApp
                            try
                                click button buttonName of window windowIdx
                                set buttonPressed to true
                            on error errorMsg
                                log "[-] Unable to press advance button: " & buttonName & " (" & errorMsg & ")"
                                
                                set windowSheets to sheets of window windowIdx
                                if count of windowSheets > 0 then
                                    log "[+] Found more sheets: " & count of windowSheets
                                    repeat with currentSheet in windowSheets
                                        try
                                            click button buttonName of currentSheet
                                        on error errorMsgSheet
                                            log "[-] Unable to press button inside sheet " & name of currentSheet
                                        end try
                                    end repeat
                                end if 
                            end try
                        end tell
                    end if
                end repeat

                -- Finish the installation process
                repeat with finishKeyword in finishedButtonKeywords
                    set buttonName to name of extractedButton
                    if (buttonName contains finishKeyword) then
                        log "[+] Found finish button: " & buttonName
                        tell process activeApp
                            try
                                click button buttonName of window windowIdx
                                set buttonPressed to true
                            on error errorMsg
                                log "[-] Unable to press finish button: " & buttonName & " (" & errorMsg & ")"
                            end try
                        end tell
                    end if
                end repeat
            end repeat

            set windowIdx to windowIdx + 1
        end repeat

        if buttonPressed is False then
            -- Check if Security Agent is present (requiring password)
            if exists process "SecurityAgent" then
                set securityAgentWindows to windows of process "SecurityAgent"
                if count of securityAgentWindows > 0 then
                    log "[+] Found active SecurityAgent"
                    repeat with securityWindow in securityAgentWindows
                        try
                            click button 1 of securityWindow -- Click the "Use Password" button
                            
                            -- repeat with i from 1 to (count text fields of securityWindow)
                            set value of text field 2 of securityWindow to autofillPassword
                            -- end repeat
                            
                            click button 1 of securityWindow -- Click the "Install Software" button
                            set buttonPressed to true
                        on error errMsg
                            log "[-] Unable to pass SecurityAgent: " & errMsg
                        end try
                    end repeat 
                end if
            end if
        end if

        if(buttonPressed) then
            my takeScreenshot(stepIdx)
            set stepIdx to stepIdx + 1
            set activeAppWindows to windows of process activeApp
            delay 1
        else
            error "No buttons found to press. Exiting..." number -1
        end if

    end repeat
end tell