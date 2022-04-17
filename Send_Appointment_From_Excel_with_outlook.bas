Attribute VB_Name = "Módulo3"
Sub CreateAppointment2()

    Set olOutlook = CreateObject("outlook.Application")
    Set Namespace = olOutlook.GetNamespace("MAPI")
    Set oloFolder = Namespace.GetDefaultFolder(9)
    
    ActiveRow = ActiveCell.Row
    LastRowTracker = Worksheets("Tracker").Cells(Rows.Count, 1).End(xlUp).Row
    
    Dim ComboBoxEntregaValue As String
    ComboBoxEntregaValue = Worksheets("Dados").Range("K2").Value + 1
    ComboBoxEntregaValue = "I" & ComboBoxEntregaValue

    Dim ComboBoxDevolucaoValue As String
    ComboBoxDevolucaoValue = Worksheets("Dados").Range("M2").Value + 1
    ComboBoxDevolucaoValue = "I" & ComboBoxDevolucaoValue
    
    HoraEntrega = Worksheets("Dados").Range(ComboBoxEntregaValue)
    HoraEntrega = Format(HoraEntrega, "hh:00")
    
    HoraDevolucao = Worksheets("Dados").Range(ComboBoxDevolucaoValue)
    HoraDevolucao = Format(HoraDevolucao, "hh:mm")
    
    DescriptionEntrega = "Entrega de " & Cells(ActiveRow, 17).Value & ": " & Cells(ActiveRow, 4).Value
    StartDateEntrega = Cells(ActiveRow, 21).Value & " " & HoraEntrega
    
    DescriptionDevolucao = "Devolução de " & Cells(ActiveRow, 17).Value & ": " & Cells(ActiveRow, 4).Value
    StartDateDevolucao = Cells(ActiveRow, 23).Value & " " & HoraDevolucao
    
    Set Appointment = oloFolder.Items.Add
    Set Appointment2 = oloFolder.Items.Add
    
    Emails = Worksheets("Dados").Cells(1, 2).Value
    
    With Appointment
        .MeetingStatus = olMeeting
        .Start = StartDateEntrega
        .Subject = DescriptionEntrega
        .RequiredAttendees = Emails
        .Send
    
    End With
    
    With Appointment2
        .MeetingStatus = olMeeting
        .Start = StartDateDevolucao
        .Subject = DescriptionDevolucao
        .RequiredAttendees = Emails
        .Send
    
    End With
    
End Sub
