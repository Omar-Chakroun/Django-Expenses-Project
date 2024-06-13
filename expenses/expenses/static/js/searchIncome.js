const searchField = document.getElementById("searchField");
const pag = document.querySelector(".pagination-container");
const output_table = document.querySelector(".output-table");
const app_table = document.querySelector("#incomesTable");
const tbody = document.querySelector(".table-body");
output_table.style.display = "block";
output_table.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value.trim();
    if (searchValue.length > 0) {
        tbody.innerHTML = ``


        fetch("/income/search-incomes", {
                body: JSON.stringify({ searchText: searchValue }),
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {

                output_table.style.display = "block";
                app_table.style.display = "none";

                if (data.length === 0) {

                    output_table.innerHTML = 'No result found';
                    pag.style.display = "none";




                } else {
                    pag.style.display = "block";
                    data.forEach((income) => {
                        console.log(data)
                        tbody.innerHTML += `
                        <tr>
                        <td>${income.amount}</td>
                        <td>${income.source}</td>
                        <td>${income.description}</td>
                        <td>${income.date}</td>
                        <td>
                            <a href="/income/edit-inc/${income.id}" class="btn btn-secondary btn-sm">Edit</a>
                        </td>
                        <td>
                            <a href="/income/delete-income/${income.id}" class="btn btn-danger btn-sm">Delete</a>
                        </td>              
                    </tr>
                        `;

                    });
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            });

    } else {
        output_table.style.display = "none";
        app_table.style.display = "block";
    }
});