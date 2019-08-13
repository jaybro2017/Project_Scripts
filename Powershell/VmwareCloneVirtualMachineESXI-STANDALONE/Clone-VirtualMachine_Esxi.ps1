#========================================================================
# Created with: PowerShell Studio
# Created on:   02/10/2018 22:16
# Created by:   Jason
# Organization: 
# Filename:     
#========================================================================
#

#Import Modules
Add-PsSnapin VMware.VimAutomation.Core -ea "SilentlyContinue"
Import-Module Posh-SSH
Import-Module CimCmdlets

#Remove existing ssh sessions
Get-SSHSession|Remove-SSHSession|out-null

#Functions

#Function to set advanced configuration to vmx file
function ChangeConfig($vmcheck){

New-AdvancedSetting -Entity $vmcheck -name "svga.vramSize" -Value "9216000" -Type Vm -Confirm
New-AdvancedSetting -Entity $vmcheck -name "mks.enable3d" -Value "TRUE" -Type Vm -Confirm


}

#Function to return which guest the virtual machine is.
function GetGuest($image){

$os=get-vm $image
$result=$os.GuestId

return $result.ToString()

}

#Function to write-files from a files array to virtual machine when finished cloning.
Function WriteFilesVM($vmname,$files){

foreach ($file in $files){

$dir="c:\scripts\$file"
write-host $file -ForegroundColor "green"
get-item "C:\files\scripts\$file"|Copy-VMGuestFile -Destination $dir -VM $vmname -LocalToGuest -GuestUser "jason" -GuestPassword "Jimmy2010!" -force
}

}

Function StartClock($vmname){

$timeout = new-timespan -Minutes 10
$sw = [diagnostics.stopwatch]::StartNew()

while($sw.Elapsed -lt $timeout){

if ((Get-VM -Name $vmname).ExtensionData.guest.interactiveGuestOperationsReady -eq $true){
Return Write-Host "Ready"
}
else{
sleep -Seconds 2
Write-Host "Not Ready"
}
}
}

function setDomainConfig($file,$Domain,$vmname,$pwddomain){

Set-Location "C:\file"
$folder="C:\File\esxi\"

[xml]$myXML = Get-Content $file
$myXML.unattend.settings[0].component[0].Identification.Credentials.domain=$domain.toString()
$myXML.unattend.settings[0].component[0].Identification.JoinDomain=$domain.toString()
$myXML.unattend.settings[0].component[0].Identification.Credentials.Password=$pwddomain.toString()
$myXML.unattend.settings[0].component[1].ComputerName=$vmname.ToString()
		
		if($KeyStore)
	{
	$myXML.unattend.settings[0].component[1].ProductKey=$keystore.ToString()
	}
		
$myXML.Save($folder+$vmname+"autojoin.xml") #added here modifications
}

function setStandAloneConfig($file,$vmname){

Set-Location "C:\file"
$folder="C:\File\esxi\"

[xml]$myXML = Get-Content $file
$myXML.unattend.settings[0].component.ComputerName=$vmname.ToString()
		
	if($KeyStore)
	{
	$myXML.unattend.settings[0].component.ProductKey=$keystore.ToString()
	}	
		
		
$myXML.Save($folder+$vmname+"autojoin.xml") #added here new function to add for standalone computer
}

function Get_DiskSize($vmname,$credential,$sessionid1)
{
$answer1=$null	

$result=Invoke-SSHCommand -SessionId $sessionid1 -Command "echo `$(du -hm /vmfs/volumes/Datastore1/$vmname/$vmname-flat.vmdk|cut -f1)"
	$taste=$result.Output|Out-String
	
	$answer1=$taste.Trim() 
	return $answer1
	
	
}

function Get_ImageSize($image,$credential,$sessionid2)
{
$answer2=$null

$result=Invoke-SSHCommand -SessionId $sessionid2 -Command "echo `$(du -hm /vmfs/volumes/Datastore2/$image/$image-flat.vmdk|cut -f1)"
	$taste=$result.Output|Out-String
	$answer2=$taste.Trim() 
    return $answer2

	
	
}








function Create_VM($vmhost,$store1,$folder,$credential,$image)
{
$os=GetGuest($image)
new-vm -name $folder -ResourcePool "192.168.1.106" -Datastore $store1 -DiskPath "[$store1] $folder/$folder.vmdk" -HardwareVersion vmx-10 -NumCPU 1 -MemoryGB 8 -NetworkName "Vlan 13" -GuestId $os -CD -

ChangeConfig($folder)
}

function Check_DiskReady($vmhost,$credential,$folder)
{	
	$strVMName = $folder
$viewVM = Get-View -ViewType VirtualMachine -Property Name, Config.Hardware.Device, LayoutEx -Filter @{"Name" = $strVMName}

$disksize=$viewVM.Config.Hardware.Device | ?{$_ -is [VMware.Vim.VirtualDisk]} | %{
    $oThisVirtualDisk = $_
   
    $oLayoutExDisk = $viewVM.LayoutEx.Disk | ?{$_.Key -eq $oThisVirtualDisk.Key}
    
    $arrLayoutExDiskFileKeys = $oLayoutExDisk.Chain | ?{$_ -is [VMware.Vim.VirtualMachineFileLayoutExDiskUnit]}
    New-Object -TypeName PSObject -Property @{
    
       
        SizeOnDatastoreGB = [Math]::Round(($arrLayoutExDiskFileKeys | %{$_.FileKey} | %{$intFileKey = $_; $viewVM.LayoutEx.File | ?{($_.Key -eq $intFileKey) -and ($_.Type -eq "diskExtent")}} | Measure-Object -Sum Size).Sum / 1GB, 1)
    } 
} 
Write-Host $disksize.SizeOnDatastoreGB -ForegroundColor "green"
return $disksize.SizeOnDatastoreGB
}


function Get-VMDisks($VMName) {            
         
$VMObj = Get-VM -Name $VMName            
$Disks = Get-Harddisk -VM $VMObj            
foreach($disk in $Disks) {            

$DiskName = $Disk.Name            

$DisksizeinGB = ($Disk.CapacityKB * 1024)/1GB            

"{0} : {1}" -f $DiskName, $DisksizeinGB            

}            
}
####End Of Functions Declared#####################

#Variables Declared################################

$files=@("changekeyboard.bat",
"changekeyboard.ps1",
"ChangeKeyboard.xml",
"changemouse.ps1",
"ChangeMouseCursor.xml",
"createmousecursor.bat",
"dhcp.ps1",
"ipchange.ps1"
)



#ImageFile you want to copy
$image="UbuntuImage"
#Storage Location of virtual machine setup
$Store1="Datastore1"
#Storage Location of image stored
$Store2="Datastore2"
#Get the name of the computer you want to create
$folder=Read-Host -Prompt 'Input a computer name'
#Get the Domain Name if this computer is part of a domain
$domain=Read-Host -Prompt 'Input a Domain Name'
#Get the ip address or dns name of the esxi host you want to connect to
$esxihost=Read-Host -Prompt 'Input an Esxi Host'

if ($domain){
$pwdomain=Read-Host -Prompt 'Input a password for the domain'
}
#Guest user credentials to access virtual machine
$guestuser="user"
$guestpwd="password"
#User credentials to connect to the esxi host
$username="root"
$password="password"
$securepassword=$password|ConvertTo-SecureString -AsPlainText -Force
#Folder is not created to False
$foldercreated=$false
#Diskcloned is set to False
$diskcloned=$false
 
 #Create the number of SSH Sessions which we will connect on the Esxi Host
$session0=0
$session1=1
$session2=2
#Create the credential object to connect to the vmware esxi host.
$credential=new-object -type System.Management.Automation.PSCredential -argumentlist $username,$securepassword
#Create 3 Connections to the esxi host which we will perform some tasks during the session
$conhost0=New-SSHSession $esxihost -credential $credential -AcceptKey
$conhost1=New-SSHSession $esxihost -credential $credential -AcceptKey
$conhost2=New-SSHSession $esxihost -credential $credential -AcceptKey

#End of Variables Declared##########


#Create connection to esxi host#######

Connect-Viserver $esxihost -credential $credential

#Create folder location for where we want to store the cloned virtual machine
 $createdir=Invoke-SSHCommand -SessionId $session0 -Command "mkdir /vmfs/volumes/$store1/$folder"

 #Show the output of the request to screen if it was a success then it means 0 or else failed.
 $createdir.Output


#Will check the output of the request to see if it was a success or failure.
#If the status is 0 then we will set the foldercreated to True.
if ($createdir.exitstatus -eq 0)
{
write-host `n "Created Folder Sucessfully" -ForegroundColor 'Green'
	$foldercreated=$true

}
else{
	#If the status is not 0 then we will set the foldercreated to False.
write-host `n "Failed to create folder" -ForegroundColor 'Yellow'
	$foldercreated=$false
	Write-Host "Create Directory exit status:$createdir.exitstatus"
	
	
	
}
#Setting the command to create a clone of the disk of the image file we specified.
$clonedisk=Invoke-SSHCommand -SessionId $session0 -Command "vmkfstools -i /vmfs/volumes/$Store2/$image/$image.vmdk /vmfs/volumes/$Store1/$folder/$folder.vmdk -d thin" -Timeout 30

#Will check the output of the request to see if it was a success or failure.
#If the status is 0 then we will set the diskcloned to True.
if ($clonedisk.exitstatus -eq 0)
{
	Write-host `n "Cloned Disk completed" -ForegroundColor 'Green'
	$diskcloned=$true
	}
else{
	#If the status is not 0 then we will set the diskcloned to False and out put the Error.
	Write-host `n "Cloned Disk failed" -ForegroundColor 'Yellow'
	$diskcloned=$false
	Write-Host "Clone Disk exit status:$createdir.exitstatus"
}
Write-Host "Waiting for hard disk to clone........." -ForegroundColor 'Green'

#If both the folder is created and the disk is clone we can begin to create the virtual machine.
if ($foldercreated -and $diskcloned -eq $true)
{
#We will call the function Create VM to Create The VM and register it on the esxi host.
	Create_VM "192.168.1.106" $Store1 $folder $credential $image
}



#We will then set the image size variable to null and get the disk size of the original image on the esxi host.
$imagesize=$null
$imagesize=Get_ImageSize $image $credential $session2
write-host "Disk Image File $image contains amount $imagesize MB" -ForegroundColor DarkGreen

#We Will then start a timeout clock for the disk to copy the image file and output the size of the copy and imagesize left.
#If the disk file copy matches the orginal size of the disk then we know the file copy is completed.

$timeout = new-timespan -Minutes 10
$sw = [diagnostics.stopwatch]::StartNew()
while ($sw.elapsed -lt $timeout){
    if($(Get_DiskSize $folder $credential $session1) -eq $imagesize)
	
	{
        
$msg=$true
		break
			
        } #We will show that there is still an active SSH sessions running in the background during the copy process.
        Get-SSHSession
 Write-Host "Waiting on disk to copy ... $(Get_DiskSize $folder $credential $session1) MB // $imagesize MB" -ForegroundColor 'Green'
 #We will the check what is the status of the file transfer copy.
    start-sleep -seconds 5

if($(Get_DiskSize $folder $credential $session1) -eq $imagesize){
$msg=$true
break}	
}
 #We will then write a message saying the Disk image is finished copying and we can then proceed.
if ($msg -eq $true){
write-host "Disk Clone is  Ready"}	
else{(write-host "Disk not working")}
Get-SSHsession|Remove-SSHsession|out-null

write-host "This is the test part ended" -ForegroundColor Red

#We will timeout for 2 seconds before heading on to the next stage of the process.
start-sleep -seconds 2

#If the virtual machine is linux we can then exit the script as there is no sysprepping for linux to be done.
if(GetGuest($image) -eq "ubuntu64Guest" -or "ubuntu32Guest")
{
write-host "No Windows Prepping needs to be done"
exit
}

#We will then start a sysprep stage for the windows virtual machine and start it up.
Start-VM -VM $folder

start-sleep -seconds 5
#If there was domain entered in the configuration we will then try to set the xml file for the sysprep configuration of the virtual machine example the computername and domainname.
if ($domain)
{             
setDomainConfig "unattend2012.xml" $domain $folder $pwdomain
}
else{
#If the computer is not part of a domain then the xml configuration will be set to just the computer name.
setStandAloneConfig "standalone2012.xml" $folder
}

#We we will then set a timer to wait for the virtual machine to start and run within windows.
StartClock $folder


Start-Sleep -Seconds 2
#We will then write a list of files which need to be copied to the virtual machine

WriteFilesVM $folder $files

Start-Sleep -Seconds 2

get-item "C:\file\esxi\${folder}autojoin.xml"|Copy-VMGuestFile -Destination "c:\windows\system32\sysprep\autojoin.xml" -VM $folder -LocalToGuest -GuestUser $guestuser -GuestPassword $guestpwd -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

Invoke-VMScript -VM $folder -ScriptText "c:\Windows\System32\sysprep\domainjoin.bat" -HostCredential $credential -GuestUser "jason" -GuestPassword "Jimmy2010!" -ScriptType Bat -ErrorAction SilentlyContinue


Get-SSHSession|Remove-SSHSession