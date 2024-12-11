const baseUrl = "http://127.0.0.1:8000";

async function fetchData(url, options = {}) {
    try {
        const response = await fetch(`${baseUrl}${url}`, options);
        if (!response.ok) throw new Error(response.statusText);
        return await response.json();
    } catch (error) {
        console.error(`Error en la solicitud a ${url}:`, error);
    }
}

// Cargar Dashboard
async function cargarDashboard() {
    const stats = await fetchData('/dashboard/');
    document.getElementById('totalUsuarios').textContent = stats?.total_usuarios || 0;
    document.getElementById('totalAsistencias').textContent = stats?.total_asistencias || 0;
    document.getElementById('totalMaterias').textContent = stats?.total_materias || 0;
    document.getElementById('porcentajeAsistencia').textContent = `${stats?.porcentaje_asistencia || 0}%`;
}

// Registrar Usuario
document.getElementById('usuarioForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('nombre').value,
        apellido: document.getElementById('apellido').value,
        email: document.getElementById('email').value,
        contraseña: document.getElementById('contraseña').value,
        rol: document.getElementById('rol').value,
        uid: document.getElementById('uid').value,
    };
    
    try {
        const response = await fetchData('/usuarios/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (response) {
            alert('Usuario registrado correctamente');
            e.target.reset(); // Limpiar el formulario
            cargarDashboard();
        } else {
            throw new Error('Error al registrar el usuario');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

// Registrar Asistencia
document.getElementById('asistenciaForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        usuario_id: parseInt(document.getElementById('usuario_id').value, 10),
        estado: document.getElementById('estado').value,
    };
    await fetchData('/asistencias/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    cargarAsistencias();
});

// Cargar Asistencias
async function cargarAsistencias() {
    const asistencias = await fetchData('/asistencias');
    const lista = document.getElementById('listaAsistencias');
    lista.innerHTML = asistencias
        .map(a => `<div class="list-group-item">${a.nombre} ${a.apellido} - ${a.estado}</div>`)
        .join('');
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    cargarDashboard();
    cargarAsistencias();
});