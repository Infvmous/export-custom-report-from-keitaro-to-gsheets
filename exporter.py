from keitaro import Keitaro

import utils

from pprint import pprint


def main(sys_args):
    keitaro = Keitaro()
    report = keitaro.build_custom_report()
    utils.write_keitaro_report_to_file(report)
    # print(report)