class Packet:
    def __init__(self, packetType, SeqNum, Data, AckNum):
        self.packetType = packetType
        self.SeqNum = SeqNum
        self.Data = data
        self.AckNum
    
    def getPacketType(self):
        return self.packetType
    
    def getSeqNum(self):
        return self.SeqNum
    
    def getData(self):
        return self.packetData
    
    def getAckNum(self):
        return self.AckNum