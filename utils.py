import socket

#[Comment]: Gets the IPV4 address of the active network adapter.
def get_network_ip_address():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  #[Comment]: 8.8.8.8 is the primary DNS server for Google DNS. It is assumed that this DNS server will always be up.
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  return ip

get_network_ip_address()