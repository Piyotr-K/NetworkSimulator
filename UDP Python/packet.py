class Packet:
    def __init__(self, packetType, SeqNum, Data, WindowSize, AckNum):
        self.packetType = packetType
        self.SeqNum = SeqNum
        self.packetData = Data
        self.WindowSize = WindowSize
        self.AckNum = AckNum

    def getPacketType(self):
        return self.packetType

    def getSeqNum(self):
        return self.SeqNum

    def getData(self):
        return self.packetData

    def getWindowSize(self):
        return self.WindowSize

    def getAckNum(self):
        return self.AckNum
