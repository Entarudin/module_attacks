import json
from ui import Ui_MainWindow
from ui import Ui_ResultWindowTesting
from PySide6.QtWidgets import QMessageBox, QWidget, QMainWindow, QApplication, QFileDialog
from PySide6.QtCore import QRunnable, Slot, Signal, QObject, QThreadPool
import sys
import traceback
from structure import (
    network_translator,
    network_service,
    attack_service,
    target_service,
    scapy_wrapper,
    network_json_repository,
    attacks_translator,
    json_service
)

UDP_FLOOD = 'udp_flood'
SYN_FLOOD = 'syn_flood'
ARP_SPOOFING = 'arp_spoofing'
BRUTE_FORCE = 'brute_force'
DHCP_STARVATION = 'dhcp_starvation'
DHCP_SPOOFING = 'dhcp_spoofing'


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class ResultTestingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ResultWindowTesting()
        self.ui.setupUi(self)
        self.file_dialog = QFileDialog()
        self.ui.button_save_on_file_system.clicked.connect(self.hande_save_on_file_system)

    def hande_save_on_file_system(self):
        value_text_area = self.ui.text_area_result_testing.toPlainText()
        presented = json.loads(value_text_area)
        filename_to_save = self.file_dialog.getSaveFileName(self, 'Save result testing', '',
                                                            selectedFilter='*.json')[0]
        json_service.save_dict_in_file(filename_to_save, presented)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.result_attacks_window = ResultTestingWindow()
        self.ui.button_start_testing_system.clicked.connect(self.check_status_checkboxes)
        self.ui.button_start_testing_system.clicked.connect(self.push_button_clicked)
        self.q_message = QMessageBox()
        self.threadpool = QThreadPool()

    def get_output_results_attacks(self, result_attacks):
        self.q_message.close()
        status_check_boxes = self._get_status_checks_boxes()
        result = self._comparison_status_checkboxes_with_result_attacks(status_check_boxes, result_attacks)
        text = json.dumps(result, indent=2)
        self.result_attacks_window.ui.text_area_result_testing.setText(text)
        self.result_attacks_window.show()

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def start_attacks(self):
        network_data = network_json_repository.parse_in_dict('data.json')
        network = network_translator.from_json(network_data)
        network_with_ports = network_service.filter_out_network_with_ports(network)
        current_ip_address_with_subnet = f"{network.current_ip_address}/24"  # What is "24"?
        targets_tcp = target_service.cast_hosts_in_targets(network_with_ports.tcp_hosts)
        targets_udp = target_service.cast_hosts_in_targets(network_with_ports.udp_hosts)
        merged_network_with_ports_hosts = network_with_ports.tcp_hosts + \
                                          network_with_ports.udp_hosts + network_with_ports.ip_hosts

        targets_brute_force = target_service.cast_hosts_in_targets_brute_force(merged_network_with_ports_hosts)
        brute_force_attacks = attack_service.create_attacks(targets_brute_force, BRUTE_FORCE)
        syn_flood_attacks = attack_service.create_attacks(targets_tcp, SYN_FLOOD)
        udp_flood_attacks = attack_service.create_attacks(targets_udp, UDP_FLOOD)
        ip_gateway = scapy_wrapper.get_ip_gateway()
        arp_table = scapy_wrapper.arp_scan(current_ip_address_with_subnet)
        arp_targets = target_service.cast_arp_table_in_targets(arp_table)
        arp_flood_attacks = attack_service.create_attacks(arp_targets, ARP_SPOOFING, ip_gateway)
        dhcp_stavation_attacks = attack_service.create_dhcp_starvation_attack(network.current_networks_interface)
        dhcp_spoofing_attacks = attack_service.create_dhcp_spoofing_attack(network.current_networks_interface,
                                                                           network.current_ip_address)
        return {
            "syn_flood_attacks": attacks_translator.to_dict(syn_flood_attacks),
            "udp_flood_attacks": attacks_translator.to_dict(udp_flood_attacks),
            "arp_flood_attacks": attacks_translator.to_dict(arp_flood_attacks),
            "brute_force_attacks": attacks_translator.to_dict(brute_force_attacks),
            "dhcp_stavation_attack": attacks_translator.to_dict(dhcp_stavation_attacks),
            "dhcp_spoofing_attack": attacks_translator.to_dict(dhcp_spoofing_attacks)
        }

    def push_button_clicked(self):
        status_check_boxes = self._get_status_checks_boxes()
        if True not in status_check_boxes.values():
            return
        self.q_message.setWindowTitle("Attention")
        self.q_message.setText("Attention started scanning the network for security analysis."
                               "\nScan time is less than 5 minutes"
                               "\nClick ok to continue")
        self.q_message.exec()
        worker = Worker(self.start_attacks)
        worker.signals.result.connect(self.get_output_results_attacks)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def check_status_checkboxes(self):
        status_check_boxes = self._get_status_checks_boxes()
        if True not in status_check_boxes.values():
            msg = QMessageBox()
            msg.setWindowTitle("Invalid data")
            msg.setText("You must select at least 1 field")
            msg.exec()

    def _get_status_checks_boxes(self) -> dict:
        return {
            "status_check_boxes_arp_spoofing": self.ui.check_box_arp_spoofing.isChecked(),
            "status_check_boxes_syn_flood": self.ui.check_box_syn_flood.isChecked(),
            "status_check_boxes_udp_flood": self.ui.check_box_udp_flood.isChecked(),
            "status_check_boxes_brute_force": self.ui.check_box_brute_force.isChecked(),
            "status_check_boxes_dhcp_spoofing": self.ui.check_box_dhcp_spoofing.isChecked(),
            "status_check_boxes_dhcp_starvation": self.ui.check_box_dhcp_starvation.isChecked()
        }

    def _comparison_status_checkboxes_with_result_attacks(self, status_checks_boxes, attacks_result) -> dict:
        result = {}
        if status_checks_boxes['status_check_boxes_arp_spoofing']:
            result['arp_flood_attacks'] = attacks_result['arp_flood_attacks']

        if status_checks_boxes['status_check_boxes_syn_flood']:
            result['syn_flood_attacks'] = attacks_result['syn_flood_attacks']

        if status_checks_boxes['status_check_boxes_udp_flood']:
            result['udp_flood_attacks'] = attacks_result['udp_flood_attacks']

        if status_checks_boxes['status_check_boxes_brute_force']:
            result['brute_force_attacks'] = attacks_result['brute_force_attacks']

        if status_checks_boxes['status_check_boxes_dhcp_spoofing']:
            result['dhcp_spoofing_attack'] = attacks_result['dhcp_spoofing_attack']

        if status_checks_boxes['status_check_boxes_dhcp_starvation']:
            result['dhcp_stavation_attack'] = attacks_result['dhcp_stavation_attack']
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())