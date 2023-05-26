import serial
import pynmea2


def port_setup(port):
    ser = serial.Serial(port, baudrate=9600, timeout=2)
    return ser


def parseGPSdata(ser):
    keywords = ["$GPRMC", "$GPGGA"]
    gps_data = ser.readline()
    gps_data = gps_data.decode("utf-8")  # transform data into plain string

    if len(gps_data) > 5:  # Check to see if the GPS gave any useful data
        if gps_data[0:6] in keywords:  # Check t see if the message code
            gps_msg = pynmea2.parse(gps_data)
            lat = gps_msg.latitude
            lng = gps_msg.longitude
            return (lat, lng)
        else:
            return None
    else:
        return None


if __name__ == "__main__":
    # access serial port
    gps_port = "/dev/ttyUSB0"
    ser = port_setup(gps_port)

    # Print out GPS cordinates
    print("GPS coordinate Stream:")
    while True:
        try:
            gps_coords = parseGPSdata(ser)
            if gps_coords is None:  # if no valid data was received
                print("No Data")
            else:
                print(f"latitude: {gps_coords[0]}, longitude: {gps_coords[1]}")

        except serial.SerialException as e:  # catch any serial communication errors
            print(f"\nERROR: {e}")
            print("... reconnecting to serial\n")
            ser = port_setup()

        except KeyboardInterrupt as e:  # Catch when user hits Ctrl-C and end program
            print("--- Program shutting down ---")
            break
