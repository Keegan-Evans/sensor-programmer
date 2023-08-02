import os
import subprocess
import click
from sensor_programmer.util import get_ip_address

@click.group
def configure_sensor():
    click.echo("pre-compilation configuration completed")

# add prompting for each value 
@configure_sensor.command()
@click.option('--sensor_id', help='The id to be give to the pico this firwmare is to be flashed to. You should create a unique one for each pico to be connected to the system.')
@click.option('--hub_ip',
              default = get_ip_address('en0'),
              help='ip address of mqtt broker, generally this will be collected '
              'directly and automatically from the sensor hub raspberry pi itself')
def create_sensor_config_file(sensor_id, hub_ip):
    if sensor_id is None:
        sensor_id = click.prompt('Sensor-ID')
    config_file_fp = os.path.join(os.getcwd(), 'configs.py')

    out_file_text = ""
    with open(config_file_fp, 'w') as f:
        out_file_text += "sensor_id = '{}'\n".format(sensor_id)
        out_file_text += "hub_mqtt_ip = '{}'\n".format(hub_ip)

        f.write(out_file_text)

@configure_sensor.command()
@click.option('--sensors', help='A list of Sensor Libraries to be included in the compiled firmware.')
def create_sensor_package(sensors: iter):
    """Takes a list of sensor modules to be written into the board firmware and then adds them to the manifest to be used to create the firmware"""
    if sensors is None:
        click.echo("Which of the following sensor modules would you like to include on this device?\n")
        for sensor in enumerated_sensor_library:
            click.echo("{}".format(sensor))
        click.prompt(":")
    sensors = sensors.split(",")
    with open("./manifest.py", 'w') as fh:
        # start by including the default manifest for board so pre-existing port libraries are included
        fh.write("include(\"$(BOARD_DIR)/manifest.py\")\n")
        for sensor in sensors:
            fh.write("package(\"{}\", base_path=\"../sensors\")\n".format(sensor.strip()))

def compile_sensor_firmware():
    subprocess.run(["make", "BOARD=PICO_W", "FROZEN_MANIFEST=\"./mainfest.py\""])
            

if __name__ == '__main__':
    configure_sensor()