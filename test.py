import serial
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Initialize serial connection
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to match your Arduino's serial port

# Initialize plot with custom layout
plt.ion()  # Turn on interactive mode
fig = plt.figure(figsize=(10, 10))

# Create gridspec
gs_upper = gridspec.GridSpec(3, 2, figure=fig)

# Define axes for upper half
axes = [fig.add_subplot(gs_upper[i]) for i in range(5)]

lines = [ax.plot([], [])[0] for ax in axes]

for ax in axes:
    ax.set_xlabel('Time')
    ax.set_ylabel('Sensor Value')
    ax.set_xlim(0, 10)  # Adjust as needed
    ax.set_ylim(0, 1)
    # Assuming analog readings (adjust as needed)

# Main loop to continuously read and plot data
try:
    while True:
        if ser.in_waiting > 0:
            # Read data from serial port
            data = ser.readline().decode().strip()
            
            # Split data by comma and extract sensor values
            sensor_values = [int(value.split(':')[1]) for value in data.split(',') if ':' in value]

            # Update plot data
            for line, sensor_value in zip(lines, sensor_values):
                x_data = list(range(len(line.get_xdata()) + 1))
                y_data = list(line.get_ydata()) + [sensor_value]
                line.set_data(x_data, y_data)

            # Update plot
            for ax in axes:
                ax.relim()
                ax.autoscale_view()
            plt.draw()
            plt.pause(0.001)

except KeyboardInterrupt:
    # Close serial connection and plot window on keyboard interrupt
    ser.close()
    plt.close()
