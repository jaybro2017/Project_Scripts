Set-ExecutionPolicy -Bypass

$RegConnect = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey([Microsoft.Win32.RegistryHive]"CurrentUser","$env:COMPUTERNAME")

$RegCursors = $RegConnect.OpenSubKey("Control Panel\Cursors",$true)

$RegCursors.SetValue("","Windows Inverted (extra large)")

$RegCursors.SetValue("AppStarting","%SystemRoot%\cursors\wait_il.cur")

$RegCursors.SetValue("Arrow","%SystemRoot%\cursors\arrow_il.cur")

$RegCursors.SetValue("Crosshair","%SystemRoot%\cursors\cross_il.cur")

#$RegCursors.SetValue("Hand","")

$RegCursors.SetValue("Help","%SystemRoot%\cursors\help_il.cur")

$RegCursors.SetValue("IBeam","%SystemRoot%\cursors\beam_il.cur")

$RegCursors.SetValue("No","%SystemRoot%\cursors\no_il.cur")

$RegCursors.SetValue("NWPen","%SystemRoot%\cursors\pen_il.cur")

$RegCursors.SetValue("SizeAll","%SystemRoot%\cursors\move_il.cur")

$RegCursors.SetValue("SizeNESW","%SystemRoot%\cursors\size1_il.cur")

$RegCursors.SetValue("SizeNS","%SystemRoot%\cursors\size4_il.cur")

$RegCursors.SetValue("SizeNWSE","%SystemRoot%\cursors\size2_il.cur")

$RegCursors.SetValue("SizeWE","%SystemRoot%\cursors\size3_il.cur")

$RegCursors.SetValue("UpArrow","%SystemRoot%\cursors\up_il.cur")

$RegCursors.SetValue("Wait","%SystemRoot%\cursors\busy_il.cur")

$RegCursors.Close()

$RegConnect.Close()

$CSharpSig = @'

[DllImport("user32.dll", EntryPoint = "SystemParametersInfo")]

public static extern bool SystemParametersInfo(

                 uint uiAction,

                 uint uiParam,

                 uint pvParam,

                 uint fWinIni);

'@

$CursorRefresh = Add-Type -MemberDefinition $CSharpSig -Name WinAPICall -Namespace SystemParamInfo –PassThru

$CursorRefresh::SystemParametersInfo(0x0057,0,$null,0)

