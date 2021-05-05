#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Demo Tx
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from get_header import get_header  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from stream_source import stream_source  # grc-generated hier_block
import osmosdr
import time
from gnuradio import qtgui

class demo_tx(gr.top_block, Qt.QWidget):

    def __init__(self, header_00=digital.header_format_default(digital.packet_utils.default_access_code, 0)):
        gr.top_block.__init__(self, "Demo Tx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Demo Tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "demo_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.header_00 = header_00

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.samp_rate = samp_rate = 2e6
        self.nfilts = nfilts = 25
        self.msg_str = msg_str = "Hello World! \r\n"
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 45*nfilts)
        self.noise = noise = 0
        self.delay_0 = delay_0 = 0
        self.delay = delay = 0
        self.baseband_LO = baseband_LO = samp_rate/sps
        self.QPSK = QPSK = digital.constellation_rect([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 3, 2],
        4, 2, 2, 1, 1).base()
        self.Bpp = Bpp = len(msg_str)

        ##################################################
        # Blocks
        ##################################################
        self._noise_range = Range(0, 1, 0.05, 0, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, 'noise', "counter_slider", float)
        self.top_grid_layout.addWidget(self._noise_win)
        self.stream_source_0 = stream_source(
            a_msg_str=msg_str,
            b_Bpp=Bpp,
        )
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + "hackrf=1,bias_tx=1"
        )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(890e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(30, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                baseband_LO,
                1.6E3,
                firdes.WIN_HAMMING,
                6.76))
        self.get_header_0 = get_header(
            a_header=header_00,
            b_tag="packet_len",
            c_payload_len=Bpp+18,
            d_in=8,
            e_out=8,
        )
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=QPSK,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self._delay_0_range = Range(-8, 8, 1, 0, 200)
        self._delay_0_win = RangeWidget(self._delay_0_range, self.set_delay_0, 'Reciever Delay', "counter_slider", float)
        self.top_grid_layout.addWidget(self._delay_0_win)
        self._delay_range = Range(-8, 8, 1, 0, 200)
        self._delay_win = RangeWidget(self._delay_range, self.set_delay, 'Decoder Delay', "counter_slider", float)
        self.top_grid_layout.addWidget(self._delay_win)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise, 0)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1.55)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.get_header_0, 1), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.get_header_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.stream_source_0, 0), (self.get_header_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "demo_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_header_00(self):
        return self.header_00

    def set_header_00(self, header_00):
        self.header_00 = header_00
        self.get_header_0.set_a_header(self.header_00)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_baseband_LO(self.samp_rate/self.sps)
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_baseband_LO(self.samp_rate/self.sps)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.baseband_LO, 1.6E3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 45*self.nfilts))

    def get_msg_str(self):
        return self.msg_str

    def set_msg_str(self, msg_str):
        self.msg_str = msg_str
        self.set_Bpp(len(self.msg_str))
        self.stream_source_0.set_a_msg_str(self.msg_str)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_delay_0(self):
        return self.delay_0

    def set_delay_0(self, delay_0):
        self.delay_0 = delay_0

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def get_baseband_LO(self):
        return self.baseband_LO

    def set_baseband_LO(self, baseband_LO):
        self.baseband_LO = baseband_LO
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.baseband_LO, 1.6E3, firdes.WIN_HAMMING, 6.76))

    def get_QPSK(self):
        return self.QPSK

    def set_QPSK(self, QPSK):
        self.QPSK = QPSK

    def get_Bpp(self):
        return self.Bpp

    def set_Bpp(self, Bpp):
        self.Bpp = Bpp
        self.get_header_0.set_c_payload_len(self.Bpp+18)
        self.stream_source_0.set_b_Bpp(self.Bpp)


def argument_parser():
    parser = ArgumentParser()
    return parser


def main(top_block_cls=demo_tx, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
