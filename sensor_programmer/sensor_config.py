import os
import subprocess
import click
from sensor_programmer.util import get_ip_address

def get_host_ip():
    pass


# add prompting for each value 
@click.command()
@click.option('--sensor_id', help='what to call this particular sensor')
@click.option('--hub_ip',
              default = get_ip_address('en0'),
              help='ip address of mqtt broker, this should be collected '
              'directly from the sensor hub raspberry pi itself')
def configure_sensor(sensor_id, hub_ip):
    if sensor_id is None:
        sensor_id = click.prompt('Sensor-ID')
    config_file_fp = os.path.join(os.getcwd(), 'configs.py')
    out_file_text = ""
    with open(config_file_fp, 'w') as f:
        out_file_text += "sensor_id = '{}'\n".format(sensor_id)
        out_file_text += "hub_mqtt_ip = '{}'\n".format(hub_ip)

        f.write(out_file_text)

def create_sensor_package(sensors: iter):
    """Takes a list of sensor modules to be written into the board firmware and then adds them to the manifest to be used to create the firmware"""
    with open("./manifest.py", 'w') as fh:
        # start by including the default manifest for board so pre-existing port libraries are included
        fh.write("include(\"$(BOARD_DIR)/manifest.py\")")
        for sensor in sensors:
            fh.write("package(\"{}\", base_path=\"../sensors\")".format(sensor))

def compile_sensor_firmware():
    subprocess.run(["make", "BOARD=PICO_W", "FROZEN_MANIFEST=\"./mainfest.py\""])
            

if __name__ == '__main__':
    configure_sensor()