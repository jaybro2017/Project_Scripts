#Functions
function UpdateIpSettings($ip,$subm,$gw,$dns1,$dns2){
	$folder="c:\file\Config\"
	$file="settings.xml"
	[xml]$xml = (Get-Content $folder$file);
	
	#Modify settings for ip address configuration
	$xml.computer.setattribute("name",$vmname)
	$root=$xml.computer.config
	$root.ipaddress=$ip.ToString()
	$root.submask=$subm.ToString()
	$root.gateway=$gw.ToString()
	$root.dns1=$dns1.ToString()
	$root.dns2=$dns2.ToString()
	$xml.Save($folder+$vmname+"_settings.xml") #added here modifications
	
	Write-Host "IP settings created for "$vmname
}
	



$strComputer ="."
#$colItems = Get-WmiObject Win32_NetworkAdapterConfiguration -Namespace "root\CIMV2" | where{$_.IPEnabled -eq “True”} #{Multiple)
$description="Intel(R) 82579V Gigabit Network Connection"

#Single object - Retrieve ip address configured from dhcp automatic settings
$Networkobj=Get-WmiObject Win32_NetworkAdapterConfiguration -Namespace "root\CIMV2" | where{$_.IPEnabled -eq “True” -and $_.Description -eq $description} 

#store ip address settings into memory variables
$ip1=$Networkobj.ipaddress[0]
$sub1=$Networkobj.ipsubnet[0]
$gw=$Networkobj.defaultipgateway
$dns1=$Networkobj.dnsserversearchorder



#Set the ip address via static configuration
$wmi=Get-WmiObject Win32_NetworkAdapterConfiguration -Filter "ipenabled=true"
$wmi.EnableStatic($ip1,$sub1)
$wmi.SetGateways($gw,1)
$wmi.SetDNSServerSearchOrder($dns1)

#Update settings in settings xml file

UpdateIpSettings $ip1 $sub1 $gw $dns1


#Display results of object
$Networkobj=Get-WmiObject Win32_NetworkAdapterConfiguration -Namespace "root\CIMV2" | where{$_.IPEnabled -eq “True” -and $_.Description -eq $description} 
#foreach($objItem in $colItems) { Used for multiple)
#}
     Write-Host "Adapter:" $Networkobj.Description
     Write-Host "         DNS Domain:" $Networkobj.DNSDomain
     Write-Host "         IPv4 Address:" $Networkobj.IPAddress[0]
     #Write-Host "         IPv6 Address:" $Networkobj.IPAddress[1]
Write-Host "         IP Gateway Address:" $Networkobj.defaultipgateway
Write-Host "         DNS1 Address:" $Networkobj.dnsserversearchorder
     Write-Host " "
     
Write-Host "********************************************" 
Write-Host " "