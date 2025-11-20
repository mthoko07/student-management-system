const API_URL = "http://localhost:5000/api/students";
let editingId = null;

// DOM Elements
const form = {
  name: document.getElementById("name"),
  email: document.getElementById("email"),
  age: document.getElementById("age"),
  course: document.getElementById("course"),
  submitBtn: document.getElementById("submit-btn"),
  cancelBtn: document.getElementById("cancel-btn"),
  title: document.getElementById("form-title"),
};

const alert = document.getElementById("alert");
const tableBody = document.getElementById("table-body");
const count = document.getElementById("count");
const searchInput = document.getElementById("search");

// Show alert message
function showAlert(message, type = "success") {
  alert.textContent = message;
  alert.className = `alert ${type}`;
  alert.style.display = "block";
  setTimeout(() => (alert.style.display = "none"), 3000);
}

// Clear form
function clearForm() {
  form.name.value = "";
  form.email.value = "";
  form.age.value = "";
  form.course.value = "";
}

// Load students
async function loadStudents() {
  try {
    const res = await fetch(API_URL);
    const students = await res.json();
    displayStudents(students);
    count.textContent = students.length;
  } catch (error) {
    showAlert("Failed to load students", "error");
  }
}

// Display students
function displayStudents(students) {
  if (students.length === 0) {
    tableBody.innerHTML =
      '<tr><td colspan="6" class="loading">No students found</td></tr>';
    return;
  }

  tableBody.innerHTML = students
    .map(
      (s) => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.email}</td>
            <td>${s.age}</td>
            <td>${s.course}</td>
            <td class="actions">
                <button class="btn btn-edit" onclick="editStudent(${s.id})">Edit</button>
                <button class="btn btn-delete" onclick="deleteStudent(${s.id})">Delete</button>
            </td>
        </tr>
    `
    )
    .join("");
}

// Submit form
form.submitBtn.onclick = async () => {
  const data = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    age: form.age.value,
    course: form.course.value.trim(),
  };

  if (!data.name || !data.email || !data.age || !data.course) {
    showAlert("Please fill all fields", "error");
    return;
  }

  try {
    const url = editingId ? `${API_URL}/${editingId}` : API_URL;
    const method = editingId ? "PUT" : "POST";

    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await res.json();

    if (res.ok) {
      showAlert(editingId ? "Student updated!" : "Student added!");
      clearForm();
      cancelEdit();
      loadStudents();
    } else {
      showAlert(result.error || "Operation failed", "error");
    }
  } catch (error) {
    showAlert("Network error", "error");
  }
};

// Edit student
async function editStudent(id) {
  try {
    const res = await fetch(`${API_URL}/${id}`);
    const student = await res.json();

    form.name.value = student.name;
    form.email.value = student.email;
    form.age.value = student.age;
    form.course.value = student.course;

    editingId = id;
    form.title.textContent = "Edit Student";
    form.submitBtn.textContent = "Update Student";
    form.cancelBtn.style.display = "inline-block";

    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (error) {
    showAlert("Failed to load student", "error");
  }
}

// Cancel edit
function cancelEdit() {
  editingId = null;
  form.title.textContent = "Add New Student";
  form.submitBtn.textContent = "Add Student";
  form.cancelBtn.style.display = "none";
  clearForm();
}

form.cancelBtn.onclick = cancelEdit;

// Delete student
async function deleteStudent(id) {
  if (!confirm("Delete this student?")) return;

  try {
    const res = await fetch(`${API_URL}/${id}`, { method: "DELETE" });

    if (res.ok) {
      showAlert("Student deleted!");
      loadStudents();
    } else {
      showAlert("Failed to delete", "error");
    }
  } catch (error) {
    showAlert("Network error", "error");
  }
}

// Search students
searchInput.oninput = async (e) => {
  const query = e.target.value.trim();

  if (!query) {
    loadStudents();
    return;
  }

  try {
    const res = await fetch(`${API_URL}/search?q=${query}`);
    const students = await res.json();
    displayStudents(students);
    count.textContent = students.length;
  } catch (error) {
    showAlert("Search failed", "error");
  }
};

// Initialize
loadStudents();
