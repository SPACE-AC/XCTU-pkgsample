import random
import binascii
import time
import json
from datetime import datetime
import sys
from os import path


class Package:
    def __init__(self, name, frequency, seperater, ending, package) -> None:
        self.name = name
        self.frequency = frequency
        self.package = package
        self.seperater = seperater
        self.data = ["" for i in package]
        self.ending = ending
        self.pkg = 0

    def set_data_range(self):
        for key, item in self.package.items():
            if item == "pkg":
                pass
            elif item == "time":
                pass
            elif isinstance(item, list):
                if all(isinstance(x, float) for x in item):
                    pass
                elif all(isinstance(x, str) for x in item):
                    pass
                else:
                    raise f"invalid form of random at {key}:{item}"

    def write(self):
        self.pkg += 1
        for index, key in enumerate(self.package.keys()):
            if self.package[key] == "pkg":
                self.data[index] = str(self.pkg)
            elif self.package[key] == "time":
                times = datetime.now().time()
                self.data[index] = str('%02d' % times.hour) + ':' + str('%02d' %
                                                                        times.minute) + ':' + str('%02d' % times.second)
            elif isinstance(self.package[key], list):
                if all(isinstance(x, int) for x in self.package[key]):
                    self.data[index] = str(random.randrange(
                        self.package[key][0], self.package[key][1]))
                elif all(isinstance(x, float) for x in self.package[key]):
                    self.data[index] = str(round(random.uniform(
                        self.package[key][0], self.package[key][1]), 7 if key.startswith("GPS") else 2))
                elif all(isinstance(x, str) for x in self.package[key]):
                    self.data[index] = random.choice(self.package[key])
                else:
                    raise f"invalid form of random at {key}:{ self.package[key]}"
            elif isinstance(self.package[key], str):
                self.data[index] = self.package[key]
            elif isinstance(self.package[key], dict):
                if self.data[index] == "":
                    self.data[index] = str(self.package[key]["start"])
                try:

                    if eval(self.data[index] + self.package[key]["condition"]):
                        self.data[index] = str(eval(
                            f"{self.data[index]}{self.package[key]['action']}"))
                    else:
                        self.data[index] = str(self.package[key]["else"])
                except ValueError:
                    self.data[index] = self.package[key]["else"]
        return self.data

    @staticmethod
    def convert_to_hex(data):
        data = str(data)
        return str(binascii.hexlify((data.encode())), "ascii")


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def main(filename):
    config = open(filename)
    config = json.load(config)

    file_header = """
<?xml version=\"1.0\" encoding=\"UTF-8\"?>

<data>
    <loop>true</loop>
    <repeat_times>1</repeat_times>
    <repeat_period>1000</repeat_period>
    <packets_list>
	"""
    file_data = """"""
    file_ending = """
    </packets_list>
</data>
	"""
    print(f"Makeing tester of {config['projectName']}")
    output_num = config['outputNum']
    output_name = config['outputName']
    containers = []
    try:
        for data_type in config['data']:
            containers.append(
                Package(data_type["name"], data_type["frequency"], data_type["seperater"], data_type["ending"], data_type["package"]))
    except KeyError as E:
        raise E
    printProgressBar(0, output_num, prefix="Progress:",
                     suffix="Complete", length=50)
    for index in range(output_num):
        for package in containers:
            for frequency in range(package.frequency):
                unhex = package.seperater.join(package.write())
                content = package.convert_to_hex(unhex+package.ending)
                file_data += f"""    
        <packet name=\"{package.name}_{package.pkg}\">
            <payload>{content}</payload>
        </packet>"""
        printProgressBar(index+1, output_num, prefix="Progress:",
                         suffix="Complete", length=50)
    with open(output_name, "w") as file:
        file.write(file_header)
        file.write(file_data)
        file.write(file_ending)


if __name__ == "__main__":
    print(
        """
	#############################################################
	#     _____ ____    ____     __    ___       ____     __    #
	#    / ___/|    \  /    |   /  ]  /  _]     /    |   /  ]   #
	#   (   \_ |  o  )|  o  |  /  /  /  [_     |  o  |  /  /    #
	#    \__  ||   _/ |     | /  /  |    _]    |     | /  /     #
	#    /  \ ||  |   |  _  |/   \_ |   [_     |  _  |/   \_    #
	#    \    ||  |   |  |  |\     ||     |    |  |  |\     |   #
	#     \___||__|   |__|__| \____||_____|    |__|__| \____|   #
	#############################################################
 	""")
    file_name = input("[Configuration File]: ")
    if path.exists(file_name):
        main(file_name)
    else:
        print("invalid file path")
