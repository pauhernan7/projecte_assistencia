const baseUrl = "http://127.0.0.1:8000";

// Fetch genérico
async function fetchData(endpoint, options = {}) {
    const url = `${baseUrl}${endpoint}`;
    const response = await fetch(url, options);
    if (!response.ok) throw new Error(`Error en ${endpoint}: ${response.statusText}`);
    return await response.json();
}

export async function getDashboardStats() {
    return await fetchData('/dashboard/');
}

export async function getAsistencias() {
    return await fetchData('/asistencias/');
}

export async function createUsuario(data) {
    return await fetchData('/usuarios/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
}

export async function createAsistencia(data) {
    return await fetchData('/asistencias/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
}