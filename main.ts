let ReceivedString = ""
let Sposition = 0
let Avalue = ""
let armstate = 0
let ConnectedString = ""
let connected = 0
let CheckCharacter = ""
let Rsign = ""
let Runits = ""
let Rtens = ""
let Tunit = ""
let Ttens = ""
let Tint = 0
let Tinttens = 0
let Tvalue = ""
let Rint = 0
let Rinttens = 0
let RValue = ""
let Speed = 0
bluetooth.onUartDataReceived(serial.delimiters(Delimiters.Colon), function () {
    if (bluetooth.uartReadUntil(serial.delimiters(Delimiters.Colon)).includes("S")) {
        ReceivedString = bluetooth.uartReadUntil(serial.delimiters(Delimiters.Colon))
        Sposition = ReceivedString.indexOf("S")
        Avalue = ReceivedString.charAt(Sposition - 1)
        armstate = parseFloat(Avalue)
        if (armstate == 1) {
            bluetooth.uartWriteString(ConnectedString)
        } else {
            bluetooth.uartWriteString("ACC:T0R0A0")
        }
    } else {
        basic.pause(50)
        if (bluetooth.uartReadUntil(serial.delimiters(Delimiters.Colon)).includes("S")) {
        	
        } else {
            bluetooth.uartWriteString("ACC:T0R0A0")
            hoverbit.stop_all_motors()
            basic.showIcon(IconNames.No)
        }
    }
})
bluetooth.onBluetoothConnected(function () {
    bluetooth.startUartService()
    connected = 1
})
bluetooth.onBluetoothDisconnected(function () {
    connected = 0
    armstate = 0
    hoverbit.stop_all_motors()
})
basic.forever(function () {
    if (connected == 0) {
        basic.pause(100)
        if (connected == 0) {
            basic.showIcon(IconNames.No)
            hoverbit.stop_all_motors()
        }
    }
    if (connected == 0 && armstate == 0) {
        basic.pause(100)
        if (connected == 0 && armstate == 0) {
            basic.showIcon(IconNames.No)
            hoverbit.stop_all_motors()
        }
    }
    if (connected && armstate == 0) {
        basic.pause(100)
        if (connected && armstate == 0) {
            basic.showIcon(IconNames.Target)
        }
    }
    if (connected && armstate) {
        basic.clearScreen()
        hoverbit.cushion_power(45)
        CheckCharacter = ReceivedString.charAt(Sposition - 4)
        if (CheckCharacter == "R") {
            Rsign = "+"
            Runits = ReceivedString.charAt(Sposition - 3)
            Rtens = "0"
        }
        CheckCharacter = ReceivedString.charAt(Sposition - 5)
        if (CheckCharacter == "R") {
            CheckCharacter = ReceivedString.charAt(Sposition - 4)
            if (CheckCharacter == "-") {
                Runits = ReceivedString.charAt(Sposition - 3)
                Rtens = "0"
                Rsign = "-"
            } else {
                Rsign = "+"
                Runits = ReceivedString.charAt(Sposition - 3)
                Rtens = ReceivedString.charAt(Sposition - 4)
            }
        } else {
            CheckCharacter = ReceivedString.charAt(Sposition - 6)
            if (CheckCharacter == "R") {
                Rsign = "-"
                Runits = ReceivedString.charAt(Sposition - 3)
                Rtens = ReceivedString.charAt(Sposition - 4)
            }
        }
        CheckCharacter = ReceivedString.charAt(Sposition - 6)
        if (CheckCharacter == "T") {
            Tunit = ReceivedString.charAt(Sposition - 5)
            Ttens = "0"
        }
        CheckCharacter = ReceivedString.charAt(Sposition - 7)
        if (CheckCharacter == "T") {
            if (ReceivedString.charAt(Sposition - 4) == "R") {
                Tunit = ReceivedString.charAt(Sposition - 5)
                Ttens = ReceivedString.charAt(Sposition - 6)
            } else {
                Tunit = ReceivedString.charAt(Sposition - 6)
                Ttens = "0"
            }
        }
        CheckCharacter = ReceivedString.charAt(Sposition - 8)
        if (CheckCharacter == "T") {
            if (ReceivedString.charAt(Sposition - 5) == "R") {
                Tunit = ReceivedString.charAt(Sposition - 6)
                Ttens = ReceivedString.charAt(Sposition - 7)
            } else if (ReceivedString.charAt(Sposition - 6) == "R") {
                Tunit = ReceivedString.charAt(Sposition - 7)
                Ttens = "0"
            } else {
            	
            }
        }
        CheckCharacter = ReceivedString.charAt(Sposition - 9)
        if (CheckCharacter == "T") {
            Tunit = ReceivedString.charAt(Sposition - 7)
            Ttens = ReceivedString.charAt(Sposition - 8)
        }
        Tint = parseFloat(Tunit)
        Tinttens = parseFloat(Ttens)
        Tinttens = Tinttens * 10
        Tint = Tinttens + Tint
        hoverbit.forward_power_simple(Tint)
        Tvalue = convertToText(Tint)
        Rint = parseFloat(Runits)
        Rinttens = parseFloat(Rtens)
        Rinttens = Rinttens * 10
        Rint = Rinttens + Rint
        Rint = Rint / 2
        RValue = convertToText(Rint)
        if (Rsign == "-") {
            RValue = "" + Rsign + RValue
            Rint = parseFloat(RValue)
        }
        led.plot((Rint + 90) / 45, 0)
        hoverbit.direction_simple(Rint)
        Speed = Math.abs(Tint - 100)
        led.plot(4, Speed / 24)
        ConnectedString = "ACC:T" + Tvalue + "R" + RValue + "A1"
    } else {
        hoverbit.stop_all_motors()
    }
})
