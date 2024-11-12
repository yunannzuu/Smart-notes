from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout


import json


app = QApplication([])





'''Application interface'''
#application window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Kasir')
notes_win.resize(900, 600)


#application window widgets
list_notes = QListWidget()
list_notes_label = QLabel('List Pembelian')


button_note_create = QPushButton('Beli') #a window appears with the field "Enter note name"
button_note_del = QPushButton('Hapus pembelian')
button_note_save = QPushButton('Simpan')


field_tag = QLineEdit('')
field_tag.setPlaceholderText('Keterangan tambahan..')
field_text = QTextEdit()
button_add = QPushButton('Tambah keterangan')
button_del = QPushButton('Hapus keterangan')
button_tag_search = QPushButton('Cari keterangan dari pembelian')
list_tags = QListWidget()
list_tags_label = QLabel('Keterangan')


#arranging widgets by layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)


col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)
col_2.addLayout(row_4)


layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


'''Application functionality'''
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name:")
    if ok and note_name != "":
        notes[note_name] = {"text" : "", "tags" : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["tags"])
        print(notes)
def show_note():
    #get the text from the note with the title highlighted and display it in the edit field
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_dat.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_asclii=False)
        print(notes)
    else:
        print("Note to save is not selected")

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Note to delete is not selected")

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Search notes by tag" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Search note by tag")
        print(button_tag_search.text())
    else:
        pass

def add_tag():
    #cek apakah ada note yang dipilih oleh cursor
    if list_notes.selectedItems():
        #cari tau judul note nya
        key = list_notes.selectedItems()[0].text()
        #simpen kalimat yg ada di dalam field tag
        tag = field_tag.text()
        #untuk setiap note yang ada di dalam notes
        for note in notes:
            #jika ada note yang punya judul yg sama
            #dengan tag nya belum ada kalimat tersebut
            if note[note] == key and notes[note]["tags"] != tag:
                notes[note]["tags"] = tag
                #tampilin tag tersebut ke dalam tampilan screen
                list_tags.addItem(note[2])
                field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Pilih keterangan!")


# 6. fungsi untuk del tag
def del_tag():
    #cek dulu, apakah kita pilih note A / note B /dll
    if list_notes.selectedItems():
        #cari tau judul note yg kita pilih
        key = list_notes.selectedItems()[0].text()
        #cari tau tag dari note yg kita pilih
        tag = list_tags.selectedItems()[0].text()
        #setelah tau, baru remove
        for note in notes:
            if notes[note] == key and notes[note]["tags"] == tag:
                list_tags.takeItem(list_tags.currentRow())
                notes.remove(note)
        #kita simpen ke dalam json file
        #json file berisikan semua data
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("note yang tag nya mau di delete, belum dipilih")


'''Run the application'''
#connecting event handling

list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
#run the application 
button_note_create.clicked.connect(add_note)
button_tag_search.clicked.connect(search_tag)
button_add.clicked.connect(add_tag)
button_del.clicked.connect(del_tag)
notes_win.show()


with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


app.exec_()


