leftFrame = Frame(root, bg="red", bd=2, relief=RIDGE)
leftFrame.place(relx=0.01, rely=0.15, relwidth=0.28, relheight=0.8)

addparticipantButton = ttk.Button(leftFrame, text='Add Participant', style='Yellow.TButton', command=add_participant, state=DISABLED)
addparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

searchparticipantButton = ttk.Button(leftFrame, text='Search Participant', style='Yellow.TButton', command=search_participant, state=DISABLED)
searchparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

deleteparticipantButton = ttk.Button(leftFrame, text='Delete Participant', style='Yellow.TButton', command=delete_participant, state=DISABLED)
deleteparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

updateparticipantButton = ttk.Button(leftFrame, text='Update Participant', style='Yellow.TButton', command=update_participant, state=DISABLED)
updateparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

showparticipantButton = ttk.Button(leftFrame, text='Show Participant', style='Yellow.TButton', command=show_participant, state=DISABLED)
showparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

exportdataparticipantButton = ttk.Button(leftFrame, text='Export Data', style='Yellow.TButton', command=export_data_participant, state=DISABLED)
exportdataparticipantButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

downloadpdfButton = ttk.Button(leftFrame, text='Download PDF', style='Yellow.TButton', command=download_pdf, state=DISABLED)
downloadpdfButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally

updatedeptButton = ttk.Button(leftFrame, text='Update Department', style='Yellow.TButton', command=update_dept, state=DISABLED)
updatedeptButton.pack(pady=10, **expand=True, fill=X**)  # Centered horizontally