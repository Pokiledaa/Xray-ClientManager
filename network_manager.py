import psutil
import time




class NetworkManager:
    def __init__(
        self,
    ):
        self.i_sent: int
        self.i_recv: int
        self.io = psutil.net_io_counters()

        self.i_recv = self.io.bytes_recv
        self.i_sent = self.io.bytes_sent

        self.standalone_network_check(1)


    def standalone_network_check(self, Interval: float):
        
        while True:
            time.sleep(Interval)

            # Geting The network Information
            self.io = psutil.net_io_counters()

            d_sent = self.io.bytes_sent - self.i_sent
            d_recv = self.io.bytes_recv - self.i_recv

            print(f"Upload : {self._get_size(self.io.bytes_sent)}")
            print(f"Download: {self._get_size(self.io.bytes_recv)}")

            



    def _get_size(self, value: int):
        """
        Returns size of bytes in a nice format
        """
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if value < 1024:
                return f"{value:.2f}{unit}B"
            value /= 1024

    

