<template>
  <section class="todo-app">
    <h1>Todo List</h1>

    <div class="input-row">
      <input
        v-model="newTodo"
        placeholder="New todo"
        @keydown.enter="addTodo"
      >
      <button @click="addTodo">
        Add
      </button>
    </div>

    <ul
      v-if="todos"
      class="todo-list"
    >
      <li
        v-for="todo in todos"
        :key="todo.id"
        class="todo-item"
      >
        <!-- Edit mode -->
        <template v-if="editingId === todo.id">
          <input
            v-model="editText"
            class="edit-input"
            @keydown.enter="saveEdit(todo)"
            @keydown.esc="cancelEdit"
          >
          <span class="actions">
            <button
              class="btn-save"
              @click="saveEdit(todo)"
            >Save</button>
            <button @click="cancelEdit">Cancel</button>
          </span>
        </template>

        <!-- View mode -->
        <template v-else>
          <span :class="{ done: todo.done }">{{ todo.text }}</span>
          <span class="actions">
            <button @click="toggleDone(todo)">
              {{ todo.done ? "Undo" : "Done" }}
            </button>
            <button @click="startEdit(todo)">Edit</button>
            <button @click="removeTodo(todo)">Delete</button>
          </span>
        </template>
      </li>
    </ul>

    <p
      v-if="loading"
      class="hint"
    >
      Loading…
    </p>
    <p
      v-if="error"
      class="hint"
      style="color: red"
    >
      {{ error }}
    </p>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = 'http://localhost:8000/api'

const newTodo = ref('')
const todos = ref(null)
const loading = ref(true)
const error = ref(null)

// Edit state
const editingId = ref(null)
const editText = ref('')

function startEdit(todo) {
  editingId.value = todo.id
  editText.value = todo.text
}

function cancelEdit() {
  editingId.value = null
  editText.value = ''
}

async function saveEdit(todo) {
  const text = editText.value.trim()
  if (!text) return
  try {
    const res = await fetch(`${API_BASE}/todos/${todo.id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    })
    if (!res.ok) throw new Error(`Update failed: ${res.status}`)
    cancelEdit()
    await loadTodos()
  } catch (e) {
    error.value = e?.message ?? 'Update failed'
  }
}

async function loadTodos() {
  loading.value = true
  error.value = null
  try {
    const res = await fetch(`${API_BASE}/todos/`)
    if (!res.ok) throw new Error(`Failed to load: ${res.status}`)
    todos.value = await res.json()
  } catch (e) {
    error.value = e?.message ?? 'Unknown error'
  } finally {
    loading.value = false
  }
}

async function addTodo() {
  const text = newTodo.value.trim()
  if (!text) return
  try {
    const res = await fetch(`${API_BASE}/todos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, done: false })
    })
    if (!res.ok) throw new Error(`Create failed: ${res.status}`)
    await loadTodos()
    newTodo.value = ''
  } catch (e) {
    error.value = e?.message ?? 'Create failed'
  }
}

async function toggleDone(todo) {
  try {
    const res = await fetch(`${API_BASE}/todos/${todo.id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !todo.done })
    })
    if (!res.ok) throw new Error(`Update failed: ${res.status}`)
    await loadTodos()
  } catch (e) {
    error.value = e?.message ?? 'Update failed'
  }
}

async function removeTodo(todo) {
  try {
    const res = await fetch(`${API_BASE}/todos/${todo.id}/`, {
      method: 'DELETE'
    })
    if (!res.ok) throw new Error(`Delete failed: ${res.status}`)
    await loadTodos()
  } catch (e) {
    error.value = e?.message ?? 'Delete failed'
  }
}

onMounted(loadTodos)
</script>

<style scoped>
.todo-app {
  max-width: 640px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
}

.input-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
}

button {
  padding: 8px 12px;
}

.todo-list {
  list-style: none;
  padding: 0;
  border-top: 1px solid #eee;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.todo-item .done {
  text-decoration: line-through;
  color: #888;
}

.edit-input {
  flex: 1;
  margin-right: 8px;
  padding: 4px 8px;
  font-size: 15px;
}

.actions button {
  margin-left: 6px;
}

.btn-save {
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.hint {
  color: #666;
  font-size: 12px;
}
</style>
