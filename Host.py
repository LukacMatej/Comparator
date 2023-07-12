class Host:
    name = ""
    ipv4 = ""
    ipv6 = ""
    id = ""
    def __init__(self,name):
        self.name = name
    def setIp(self,ipv4):
        self.ipv4 = ipv4
    def setIpv6(self,ipv6):
        self.ipv6 = ipv6
    def setId(self,id):
        self.id = id
    def getName(self):
        return ("{}").format(str(self.name))
    def getIpv4(self):
        return ("{}").format(str(self.ipv4))
    def getIpv6(self):
        return ("{}").format(str(self.ipv6))
    def getId(self):
        return ("{}").format(str(self.id))
    def __str__(self) -> str:
        return ("{}   {}   {}").format(str(self.name),str(self.ipv4),str(self.ipv6))
