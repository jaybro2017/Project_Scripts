$dhcp=Get-WmiObject Win32_NetworkAdapterConfiguration -Namespace "root\CIMV2"| where{$_.description -eq “Intel(R) PRO/1000 MT Network Connection”}
$dhcp.EnableDHCP()
$dhcp.SETDNSServerSearchOrder()