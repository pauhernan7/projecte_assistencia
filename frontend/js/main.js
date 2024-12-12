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


// Obtenir usuari per id
document.getElementById('buscarUsuarioForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuarioId = document.getElementById('buscarUsuarioId').value;

    try {
        const usuario = await fetchData(`/usuarios/${usuarioId}`);
        if (usuario) {
            document.getElementById('resultadoUsuario').innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5>${usuario.nombre} ${usuario.apellido}</h5>
                        <p>Email: ${usuario.email}</p>
                        <p>Rol: ${usuario.rol}</p>
                        <p>UID: ${usuario.uid}</p>
                        <p>Fecha de Registro: ${new Date(usuario.fecha_registro).toLocaleDateString()}</p>
                    </div>
                </div>
            `;
        } else {
            document.getElementById('resultadoUsuario').innerHTML = '<p class="text-danger">Usuario no encontrado</p>';
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

document.getElementById('crearMateriaForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('nombreMateria').value,
        grupo_id: parseInt(document.getElementById('grupoId').value, 10),
        profesor_id: parseInt(document.getElementById('profesorId').value, 10),
    };

    try {
        const response = await fetchData('/materias/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (response) {
            alert('Materia creada correctamente');
            e.target.reset();
        } else {
            throw new Error('Error al crear materia');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
});

// Obtener estadísticas del usuario
document.getElementById('estadisticasUsuarioForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuarioId = document.getElementById('usuarioEstadisticasId').value;

    try {
        const estadisticas = await fetchData(`/usuarios/${usuarioId}/estadisticas`);
        if (estadisticas) {
            document.getElementById('resultadoEstadisticasUsuario').innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5>Estadísticas para Usuario ID: ${usuarioId}</h5>
                        <p><strong>Porcentaje de Asistencia:</strong> ${estadisticas.porcentaje_asistencia}%</p>
                        <p><strong>Total Presente:</strong> ${estadisticas.total_presente}</p>
                        <p><strong>Total Ausente:</strong> ${estadisticas.total_ausente}</p>
                        <p><strong>Total Tarde:</strong> ${estadisticas.total_tarde}</p>
                    </div>
                </div>
            `;
        } else {
            document.getElementById('resultadoEstadisticasUsuario').innerHTML = `
                <p class="text-danger">No se encontraron estadísticas para el usuario con ID: ${usuarioId}</p>
            `;
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
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