async function load_users() {
    const response = await fetch("/api/users");
    const users = await response.json();

    const table = document.getElementById("users-table");
    table.innerHTML = "";

    for (const user of users)
    {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <button><a href="/${user.name}">Follow</a></button>
        `;

        table.appendChild(row);
    }
}

load_users();

setInterval(load_users, 5000);