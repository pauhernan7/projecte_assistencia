fetch("http://127.0.0.1:8000/usuaris/llista")
    .then(response => {
        console.log("Resposta del servidor:", response);
        if (!response.ok) {
            console.error("Error a la resposta del servidor", response.status);
            throw new Error("Error a la resposta del servidor");
        }
        return response.json();
    })
    .then(data => {
        console.log("Dades rebudes:", data);

        if (!Array.isArray(data)) {
            throw new Error("La resposta no és una llista d'usuaris");
        }

        const usuarisTableBody = document.querySelector("#tablaUsuari tbody");
        if (!usuarisTableBody) {
            throw new Error("No s'ha trobat la taula o el tbody a l'HTML");
        }

        usuarisTableBody.innerHTML = "";

        data.forEach(usuarios => {
            console.log("usuarios:", usuarios);

            const row = document.createElement("tr");

            const idUsuariosCell = document.createElement("td");
            idUsuariosCell.textContent = usuarios.usuario_id || 'Desconegut';
            row.appendChild(idUsuariosCell);

            const nomUsuariosCell = document.createElement("td");
            nomUsuariosCell.textContent = usuarios.nombre || 'Desconegut';
            row.appendChild(nomUsuariosCell);

            const apellidoUsuariosCell = document.createElement("td");
            apellidoUsuariosCell.textContent = usuarios.apellido || 'Desconegut';
            row.appendChild(apellidoUsuariosCell);

            const emailUsuariosCell = document.createElement("td");
            emailUsuariosCell.textContent = usuarios.email || 'Desconegut';
            row.appendChild(emailUsuariosCell);

            const rolUsuariosCell = document.createElement("td");
            rolUsuariosCell.textContent = usuarios.rol || 'Desconegut';
            row.appendChild(rolUsuariosCell);



            usuarisTableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error("Error capturat:", error);
        alert("Error al carregar la llista d'usuaris");
    });
