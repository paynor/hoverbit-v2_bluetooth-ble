ReceivedString = ""
Sposition = 0
Avalue = ""
armstate = 0
ConnectedString = ""
connected = 0
CheckCharacter = ""
Rsign = ""
Runits = ""
Rtens = ""
Tunit = ""
Ttens = ""
Tint = 0
Tinttens = 0
Tvalue = ""
Rint = 0
Rinttens = 0
RValue = ""
Speed = 0

def on_uart_data_received():
    global ReceivedString, Sposition, Avalue, armstate
    if bluetooth.uart_read_until(serial.delimiters(Delimiters.COLON)).includes("S"):
        ReceivedString = bluetooth.uart_read_until(serial.delimiters(Delimiters.COLON))
        Sposition = ReceivedString.index_of("S")
        Avalue = ReceivedString.char_at(Sposition - 1)
        armstate = parse_float(Avalue)
        if armstate == 1:
            bluetooth.uart_write_string(ConnectedString)
        else:
            bluetooth.uart_write_string("ACC:T0R0A0")
    else:
        basic.pause(50)
        if bluetooth.uart_read_until(serial.delimiters(Delimiters.COLON)).includes("S"):
            pass
        else:
            bluetooth.uart_write_string("ACC:T0R0A0")
            hoverbit.stop_all_motors()
            basic.show_icon(IconNames.NO)
bluetooth.on_uart_data_received(serial.delimiters(Delimiters.COLON), on_uart_data_received)

def on_bluetooth_connected():
    global connected
    bluetooth.start_uart_service()
    connected = 1
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    global connected, armstate
    connected = 0
    armstate = 0
    hoverbit.stop_all_motors()
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_forever():
    global CheckCharacter, Rsign, Runits, Rtens, Tunit, Ttens, Tint, Tinttens, Tvalue, Rint, Rinttens, RValue, Speed, ConnectedString
    from microbit import *  
    
    if connected == 0:
        basic.pause(100)
        if connected == 0:
            basic.show_icon(IconNames.NO)
            hoverbit.stop_all_motors()
    if connected == 0 and armstate == 0:
        basic.pause(100)
        if connected == 0 and armstate == 0:
            basic.show_icon(IconNames.NO)
            hoverbit.stop_all_motors()
    if connected and armstate == 0:
        basic.pause(100)
        if connected and armstate == 0:
            basic.show_icon(IconNames.TARGET)
    if connected and armstate:
        basic.clear_screen()
        hoverbit.start_cushion_simple()
        CheckCharacter = ReceivedString.char_at(Sposition - 4)
        if CheckCharacter == "R":
            Rsign = "+"
            Runits = ReceivedString.char_at(Sposition - 3)
            Rtens = "0"
        CheckCharacter = ReceivedString.char_at(Sposition - 5)
        if CheckCharacter == "R":
            CheckCharacter = ReceivedString.char_at(Sposition - 4)
            if CheckCharacter == "-":
                Runits = ReceivedString.char_at(Sposition - 3)
                Rtens = "0"
                Rsign = "-"
            else:
                Rsign = "+"
                Runits = ReceivedString.char_at(Sposition - 3)
                Rtens = ReceivedString.char_at(Sposition - 4)
        else:
            CheckCharacter = ReceivedString.char_at(Sposition - 6)
            if CheckCharacter == "R":
                Rsign = "-"
                Runits = ReceivedString.char_at(Sposition - 3)
                Rtens = ReceivedString.char_at(Sposition - 4)
        CheckCharacter = ReceivedString.char_at(Sposition - 6)
        if CheckCharacter == "T":
            Tunit = ReceivedString.char_at(Sposition - 5)
            Ttens = "0"
        CheckCharacter = ReceivedString.char_at(Sposition - 7)
        if CheckCharacter == "T":
            if ReceivedString.char_at(Sposition - 4) == "R":
                Tunit = ReceivedString.char_at(Sposition - 5)
                Ttens = ReceivedString.char_at(Sposition - 6)
            else:
                Tunit = ReceivedString.char_at(Sposition - 6)
                Ttens = "0"
        CheckCharacter = ReceivedString.char_at(Sposition - 8)
        if CheckCharacter == "T":
            if ReceivedString.char_at(Sposition - 5) == "R":
                Tunit = ReceivedString.char_at(Sposition - 6)
                Ttens = ReceivedString.char_at(Sposition - 7)
            elif ReceivedString.char_at(Sposition - 6) == "R":
                Tunit = ReceivedString.char_at(Sposition - 7)
                Ttens = "0"
            else:
                pass
        CheckCharacter = ReceivedString.char_at(Sposition - 9)
        if CheckCharacter == "T":
            Tunit = ReceivedString.char_at(Sposition - 7)
            Ttens = ReceivedString.char_at(Sposition - 8)
        Tint = parse_float(Tunit)
        Tinttens = parse_float(Ttens)
        Tinttens = Tinttens * 10
        Tint = Tinttens + Tint
        hoverbit.forward_power_simple(Tint)
        Tvalue = convert_to_text(Tint)
        Rint = parse_float(Runits)
        Rinttens = parse_float(Rtens)
        Rinttens = Rinttens * 10
        Rint = Rinttens + Rint
        RValue = convert_to_text(Rint)
        if Rsign == "-":
            RValue = "" + Rsign + RValue
            Rint = parse_float(RValue)
        led.plot((Rint + 90) / 45, 0)
        hoverbit.direction_simple(Rint)
        Speed = abs(Tint - 100)
        led.plot(4, Speed / 24)
        ConnectedString = "ACC:T" + Tvalue + "R" + RValue + "A1"
    else:
        hoverbit.stop_all_motors()

basic.forever(on_forever)
