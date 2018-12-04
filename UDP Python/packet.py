class Packet:
    def __init__(self, packetType='', SeqNum=0, Data='', AckNum=0):
        self.packetType = packetType
        self.SeqNum = SeqNum
        self.packetData = Data
        self.AckNum = AckNum

    def toString(self):
        return '{},{},{},{}'.format(self.packetType, self.SeqNum, self.packetData, self.AckNum)

    def decode(self, dString):
        decodeData = dString.split(',')
        self.packetType = decodeData[0]
        self.SeqNum = decodeData[1]
        self.packetData = decodeData[2]
        self.AckNum = decodeData[3]
        return self

    def getPacketType(self):
        return self.packetType

    def getSeqNum(self):
        return self.SeqNum

    def getData(self):
        return self.packetData

    def getAckNum(self):
        return self.AckNum
