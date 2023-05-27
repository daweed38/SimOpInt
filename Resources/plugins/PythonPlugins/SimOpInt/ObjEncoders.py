# System Modules Import
import math
import threading
import time
# Device Base Import
from ObjBase import ObjBase
# MCP23017 Import
from DeviceMCP23017 import MCP23017

##################################################
# FarmerSoft Sim Open Interface
##################################################
# Object Rotary Encoder Class REV 2.0
# FarmerSoft © 2023
# By Daweed
##################################################


class RotaryEncoder(ObjBase):
    # Just the encoder, no switch, no LEDs

    def __init__(self, name: str, node: dict, nodetype: str, nodeformat: str, nodeconds: dict, device: MCP23017, port: str, pin1: int, pin2: int, swpin: int, initvalue: int, minvalue: int, maxvalue: int, increment: int, exported: bool = False, imported: bool = False, debug: bool = False) -> None:
        super().__init__(name, node, nodetype, nodeformat, nodeconds, exported, imported, debug)
        self.objtype = 'Push Button'
        self.device = device
        self.port = port
        self.a_pin = pin1
        self.b_pin = pin2
        self.sw_pin = swpin
        self.value = initvalue
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.increment = increment
        self.last_delta = 0
        self.r_seq = self.rotation_sequence()
        self.steps_per_cycle = 4    # 4 steps between detents
        self.remainder = 0
        self.noderef = {}

    def rotation_sequence(self) -> int:
        a_state = self.device.readGpioPin(self.port, self.a_pin)
        b_state = self.device.readGpioPin(self.port, self.b_pin)
        r_seq = (a_state ^ b_state) | b_state << 1
        return r_seq

    # Returns offset values of -2,-1,0,1,2
    def get_delta(self) -> int:
        delta = 0
        r_seq = self.rotation_sequence()
        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4
            if delta == 3:
                delta = -1
            elif delta == 2:
                delta = int(math.copysign(delta, self.last_delta))  # same direction as previous, 2 steps

            self.last_delta = delta
            self.r_seq = r_seq

        return delta

    def get_cycles(self) -> int:
        self.remainder += self.get_delta()
        cycles = self.remainder // self.steps_per_cycle
        self.remainder %= self.steps_per_cycle  # remainder always remains positive
        return cycles

    def get_switchstate(self) -> int:
        return self.device.readGpioPin(self.port, self.sw_pin)

    def getEncoderValue(self) -> int:
        return self.value

    def setEncoderValue(self, value) -> None:
        self.value = value

    ########################################
    # System Methods Override
    ########################################

    # Method getNode(direction)
    # Return Object Node
    def getNode(self, direction: str) -> str:
        return self.node[direction]

    # Method setNode(direction, node)
    # Set Object Node to node
    # node is str
    def setNode(self, node: str, direction: str) -> None:
        self.node[direction] = node

    # Method getNodeRef(direction)
    # Return X-Plane Node Reference
    def getNodeRef(self, direction: str) -> object:
        return self.noderef[direction]

    # Method setNodeRef(direction, noderef)
    # Set X-Plane Node Reference to noderef
    # noderef is an X-Plane DataRef Object
    def setNodeRef(self, noderef, direction: str) -> None:
        self.noderef[direction] = noderef


class EncoderWorker(threading.Thread):
    def __init__(self, encoder) -> None:
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.stopping = False
        self.encoder = encoder
        self.daemon = True
        self.delta = 0
        self.delay = 0.001
        self.lastSwitchState = False
        self.upEvent = False
        self.downEvent = False
        # print("class Encoder : {}".format(self.encoder.__class__.__name__))

    def run(self) -> None:
        # self.lastSwitchState = self.encoder.get_switchstate()
        while not self.stopping:
            delta = self.encoder.get_cycles()
            with self.lock:
                self.delta += delta
                '''
                self.switchstate = self.encoder.get_switchstate()
                if (not self.lastSwitchState) and (self.switchstate):
                    self.upEvent = True
                if (self.lastSwitchState) and (not self.switchstate):
                    self.downEvent = True
                self.lastSwitchState = self.switchstate
                '''
            time.sleep(self.delay)

    # get_delta, get_upEvent, and get_downEvent return events that occurred on
    # the encoder. As a side effect, the corresponding event will be reset.

    def get_delta(self) -> int:
        with self.lock:
            delta = self.delta
            self.delta = 0
        return delta

    def get_upEvent(self) -> bool:
        with self.lock:
            delta = self.upEvent
            self.upEvent = False
        return delta

    def get_downEvent(self) -> bool:
        with self.lock:
            delta = self.downEvent
            self.downEvent = False
        return delta

    def getValue(self) -> int:
        return self.encoder.getEncoderValue()

    def setValue(self, value) -> None:
        self.encoder.setEncoderValue(value)

    def getMinValue(self) -> int:
        return self.encoder.minvalue

    def getMaxValue(self) -> int:
        return self.encoder.maxvalue

    def getIncrement(self) -> int:
        return self.encoder.increment
