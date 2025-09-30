const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// const  expressListEndpoints  =  require ( "express-list-endpoints" ) ;

const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

let notes = [];
let nextId = 1;

// GET /notes - вернуть все заметки
app.get('/notes', (req, res) => {
    if (notes.length === 0) return res.status(404).json({ message: 'No notes found' });
    res.status(200).json(notes);
});

// GET /note/:id - вернуть заметку с соответствующим id
app.get('/note/:id', (req, res) => {
    const note = notes.find(n => n.id === parseInt(req.params.id));
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.status(200).json(note);
});

// GET /note/read/:title - вернуть заметку с соответствующим названием
app.get('/note/read/:title', (req, res) => {
    const note = notes.find(n => n.title === req.params.title);
    if (!note) return res.status(404).json({ message: 'Note not found' });
    res.status(200).json(note);
});

// POST /note/ - создать и вернуть заметку
app.post('/note/', (req, res) => {
    const { title, content } = req.body;
    if (!title || !content) return res.status(409).json({ message: 'Title and content are required' });

    const newNote = {
        id: nextId++,
        title,
        content,
        created: new Date(),
        changed: new Date()
    };
    notes.push(newNote);
    res.status(201).json(newNote);
});

// DELETE /note/:id - удалить заметку с соответствующим id
app.delete('/note/:id', (req, res) => {
    const noteIndex = notes.findIndex(n => n.id === parseInt(req.params.id));
    if (noteIndex === -1) return res.status(409).json({ message: 'Note not found' });

    notes.splice(noteIndex, 1);
    res.status(204).send();
});

// PUT /note/:id - изменить заметку с соответствующим id
app.put('/note/:id', (req, res) => {
    const note = notes.find(n => n.id === parseInt(req.params.id));
    if (!note) return res.status(409).json({ message: 'Note not found' });

    const { title, content } = req.body;
    if (title) note.title = title;
    if (content) note.content = content;
    note.changed = new Date();

    res.status(204).send();
});

// const  endpoints  =  expressListEndpoints ( app ) ;
// console.log (endpoints) ;


// Запуск сервера
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});