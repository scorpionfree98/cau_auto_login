set ws=WScript.CreateObject("WScript.Shell")
dir = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
ws.currentdirectory = dir
ws.Run dir & "\run.bat",0