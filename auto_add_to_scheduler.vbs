Set WshShell = WScript.CreateObject("WScript.Shell") 
If WScript.Arguments.Length = 0 Then 
  Set ObjShell = CreateObject("Shell.Application") 
  ObjShell.ShellExecute "wscript.exe" _ 
  , """" & WScript.ScriptFullName & """ RunAsAdministrator", , "runas", 1 
  WScript.Quit 
End if 

'------------------------------------------------------------------
' This sample schedules a task to start on a daily basis.
'------------------------------------------------------------------

' A constant that specifies a daily trigger.
const TriggerTypeDaily = 2
const TASK_TRIGGER_BOOT = 8
' A constant that specifies an executable action.
const ActionTypeExec = 0

'********************************************************
' Create the TaskService object.
Set service = CreateObject("Schedule.Service")
call service.Connect()

'********************************************************
' Get a folder to create a task definition in. 
Dim rootFolder
Set rootFolder = service.GetFolder("\")

' The taskDefinition variable is the TaskDefinition object.
Dim taskDefinition
' The flags parameter is 0 because it is not supported.
Set taskDefinition = service.NewTask(0) 

'********************************************************
' Define information about the task.

' Set the registration info for the task by 
' creating the RegistrationInfo object.
Dim regInfo
Set regInfo = taskDefinition.RegistrationInfo
regInfo.Description = "Auto_connect CAU Network"
regInfo.Author = "Scrpion"

' Set the task setting info for the Task Scheduler by
' creating a TaskSettings object.
Dim settings
Set settings = taskDefinition.Settings
settings.Enabled = True
settings.StartWhenAvailable = True
settings.DisallowStartIfOnBatteries = True
settings.StopIfGoingOnBatteries = False
settings.Hidden = False

'********************************************************
' Create a daily trigger. Note that the start boundary 
' specifies the time of day that the task starts and the 
' interval specifies what days the task is run.
Dim triggers
Set triggers = taskDefinition.Triggers

Dim trigger1
Set trigger1 = triggers.Create(TriggerTypeDaily)
Set trigger2 = triggers.Create(TASK_TRIGGER_BOOT)

' Trigger variables that define when the trigger is active 
' and the time of day that the task is run. The format of 
' this time is YYYY-MM-DDTHH:MM:SS
Dim startTime, endTime

Dim time
startTime = "2022-11-25T11:23:49"  'Task runs at 8:00 AM

trigger1.StartBoundary = startTime
' trigger1.EndBoundary = endTime
trigger1.DaysInterval = 1    'Task runs every day.
trigger1.Id = "DailyTriggerId"
trigger1.Enabled = True

' Set the task repetition pattern for the task.
' This will repeat the task 5 times.
Dim repetitionPattern
Set repetitionPattern = trigger1.Repetition
repetitionPattern.Interval = "PT5M"
repetitionPattern.Duration = "P1D"
repetitionPattern.StopAtDurationEnd = True


' Dim ScheduleByDay
' Set ScheduleByDay = trigger1.ScheduleByDay
' ScheduleByDay.DaysInterval = 1
'***********************************************************
' Create the action for the task to execute.

' Add an action to the task to run notepad.exe.
Dim Action
Set Action = taskDefinition.Actions.Create( ActionTypeExec )
set ws=WScript.CreateObject("WScript.Shell")
dir = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
Action.Path = dir&"\run.vbs"
Action.WorkingDirectory = dir

' WScript.Echo "Task definition created. About to submit the task..."

'***********************************************************
' Register (create) the task.

call rootFolder.RegisterTaskDefinition( _
"auto_login_cau", taskDefinition, 6, , , 3)

WScript.Echo "Task submitted."