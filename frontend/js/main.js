// Configuración global
const baseUrl = "http://127.0.0.1:8000";

// Función mejorada para fetch con manejo de errores
async function fetchData(url, options = {}) {
    try {
        console.log(`Iniciando fetch a ${url}`);
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log(`Datos recibidos de ${url}:`, data);
        return data;
    } catch (error) {
        console.error(`Error en fetch a ${url}:`, error);
        return null;
    }
}

// Actualizar dashboard
async function actualizarDashboard() {
    console.log('Actualizando dashboard...');
    const data = await fetchData(`${baseUrl}/dashboard/`);
    if (!data) {
        console.error('No se pudieron obtener datos del dashboard');
        return;
    }

    const elementos = {
        totalUsuarios: data.total_usuarios || 0,
        totalAsistencias: data.total_asistencias || 0,
        totalMaterias: data.total_materias || 0,
        porcentajeAsistencia: `${data.porcentaje_asistencia || 0}%`
    };

    Object.entries(elementos).forEach(([id, valor]) => {
        const elemento = document.getElementById(id);
        if (elemento) {
            console.log(`Actualizando ${id} con valor ${valor}`);
            elemento.textContent = valor;
        }
    });
}

// Cargar asistencias
async function cargarAsistencias() {
    const container = document.getElementById('asistencias-list');
    if (!container) {
        console.log('Contenedor de asistencias no encontrado');
        return;
    }

    console.log('Cargando asistencias...');
    const asistencias = await fetchData(`${baseUrl}/asistencias`);
    
    if (!asistencias) {
        container.innerHTML = '<p class="text-danger">Error al cargar asistencias</p>';
        return;
    }

    if (asistencias.length === 0) {
        container.innerHTML = '<p class="text-muted">No hay asistencias registradas</p>';
        return;
    }

    container.innerHTML = asistencias.map(a => `
        <div class="card mb-3">
            <div class="card-body">
                <h6 class="card-subtitle mb-2 text-muted">
                    ${a.nombre} ${a.apellido}
                </h6>
                <p class="card-text">
                    <strong>Fecha:</strong> ${new Date(a.fecha).toLocaleDateString()}<br>
                    <strong>Estado:</strong> ${a.estado}<br>
                    <strong>Hora:</strong> ${a.hora_entrada || 'No registrada'}
                </p>
            </div>
        </div>
    `).join('');
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    console.log('Iniciando aplicación');
    actualizarDashboard();
    cargarAsistencias();
    
    // Actualizar cada 2 minutos
    setInterval(() => {
        actualizarDashboard();
        cargarAsistencias();
    }, 120000);
});