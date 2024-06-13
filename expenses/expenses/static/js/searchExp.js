const searchField = document.getElementById("searchField");
const pag = document.querySelector(".pagination-container");
const output_table = document.querySelector(".output-table");
const app_table = document.querySelector("#expensesTable");
const tbody = document.querySelector(".table-body");
output_table.style.display = "table";
output_table.style.display = "none";


searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value.trim();
    if (searchValue.length > 0) {
        tbody.innerHTML = ``


        fetch("/search-expenses", {
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

                output_table.style.display = "table";
                app_table.style.display = "none";

                if (data.length === 0) {

                    output_table.innerHTML = 'No result found';
                    pag.style.display = "none";




                } else {
                    pag.style.display = "block";
                    data.forEach((expense) => {
                        console.log(data)
                        tbody.innerHTML += `
                        <tr>
                        <td>${expense.amount}</td>
                        <td>${expense.category}</td>
                        <td>${expense.description}</td>
                        <td>${expense.date}</td>              
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
        app_table.style.display = "table";
    }
});