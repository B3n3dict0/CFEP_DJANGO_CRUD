class NotesManager {
    constructor() {
        this.currentSection = null;
        this.notes = this.loadNotes();
        this.initializeEvents();
    }

    initializeEvents() {
        // Evento para botones de agregar nota
        document.querySelectorAll('.add-note-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const section = e.target.dataset.section;
                this.openNotesModal(section);
            });
        });

        // Eventos del modal
        document.getElementById('saveNote').addEventListener('click', () => this.saveNote());
        document.getElementById('clearNote').addEventListener('click', () => this.clearNote());
        document.getElementById('exportNotes').addEventListener('click', () => this.exportToWord());
        document.querySelector('#notesModal .close').addEventListener('click', () => this.closeModal());
    }

    openNotesModal(section) {
        this.currentSection = section;
        const modal = document.getElementById('notesModal');
        document.getElementById('modalSectionName').textContent = section.toUpperCase();
        
        // Cargar notas existentes
        this.displayExistingNotes();
        
        modal.style.display = 'block';
    }

    closeModal() {
        document.getElementById('notesModal').style.display = 'none';
        this.currentSection = null;
    }

    displayExistingNotes() {
        const container = document.getElementById('existing-notes');
        container.innerHTML = '';
        
        const sectionNotes = this.notes[this.currentSection] || [];
        
        if (sectionNotes.length === 0) {
            container.innerHTML = '<p>No hay notas para esta sección.</p>';
            return;
        }
        
        sectionNotes.forEach((note, index) => {
            const noteElement = document.createElement('div');
            noteElement.className = 'note-item';
            noteElement.innerHTML = `
                <p>${note.text}</p>
                <small>${new Date(note.timestamp).toLocaleString()}</small>
                <div class="note-actions">
                    <button class="edit-note" data-index="${index}">Editar</button>
                    <button class="delete-note" data-index="${index}">Eliminar</button>
                </div>
            `;
            container.appendChild(noteElement);
        });
        
        // Agregar eventos a los botones de editar y eliminar
        container.querySelectorAll('.edit-note').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = e.target.dataset.index;
                this.editNote(index);
            });
        });
        
        container.querySelectorAll('.delete-note').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = e.target.dataset.index;
                this.deleteNote(index);
            });
        });
    }

    saveNote() {
        const noteText = document.getElementById('noteText').value.trim();
        if (!noteText) return;
        
        if (!this.notes[this.currentSection]) {
            this.notes[this.currentSection] = [];
        }
        
        this.notes[this.currentSection].push({
            text: noteText,
            timestamp: new Date().toISOString()
        });
        
        this.saveNotes();
        this.displayExistingNotes();
        document.getElementById('noteText').value = '';
        
        // Mostrar mensaje de éxito
        this.showMessage('Nota guardada correctamente');
    }

    editNote(index) {
        const noteText = prompt('Editar nota:', this.notes[this.currentSection][index].text);
        if (noteText !== null) {
            this.notes[this.currentSection][index].text = noteText;
            this.notes[this.currentSection][index].timestamp = new Date().toISOString();
            this.saveNotes();
            this.displayExistingNotes();
            this.showMessage('Nota actualizada correctamente');
        }
    }

    deleteNote(index) {
        if (confirm('¿Estás seguro de que quieres eliminar esta nota?')) {
            this.notes[this.currentSection].splice(index, 1);
            this.saveNotes();
            this.displayExistingNotes();
            this.showMessage('Nota eliminada correctamente');
        }
    }

    clearNote() {
        document.getElementById('noteText').value = '';
    }

    loadNotes() {
        const savedNotes = localStorage.getItem('meeting_notes');
        return savedNotes ? JSON.parse(savedNotes) : {};
    }

    saveNotes() {
        localStorage.setItem('meeting_notes', JSON.stringify(this.notes));
    }

    async exportToWord() {
        try {
            const response = await fetch('/operativo/export-notes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    notes: this.notes,
                    meeting_date: document.getElementById('fecha').textContent
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `acta_reunion_operativa_${new Date().toISOString().split('T')[0]}.docx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showMessage('Documento exportado correctamente');
            } else {
                throw new Error('Error al exportar');
            }
        } catch (error) {
            console.error('Error exporting notes:', error);
            this.showMessage('Error al exportar el documento', 'error');
        }
    }

    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }

    showMessage(message, type = 'success') {
        // Implementar un sistema de mensajes toast
        const messageDiv = document.createElement('div');
        messageDiv.className = `toast-message ${type}`;
        messageDiv.textContent = message;
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.notesManager = new NotesManager();
});