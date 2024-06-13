const today_div = document.getElementById('today');
const sixmonths_div = document.getElementById('sixmonths');
const year_div = document.getElementById('year');
const amount_year = document.getElementById('amount_year');
const amount_month = document.getElementById('amount_month');
const amount_today = document.getElementById('amount_today');

document.addEventListener('DOMContentLoaded', (event) => {
    let categories = [];
    let amounts = [];
    let expensesChart;
    const ctx = document.getElementById('expensesChart').getContext('2d');
    const ctx1 = document.getElementById('expensesChart1').getContext('2d');

    fetch('/expenses-by-category/')
        .then(response => response.json())
        .then(data => {
            console.log(data.amount.total_amount)
            categories = data.data.map(item => item.category);
            amounts = data.data.map(item => item.total_amount);
            amount_year.innerHTML = `${data.year_amount.total_amount}$`
            amount_month.innerHTML = `${data.month_amount.total_amount}$`
            amount_today.innerHTML = `${data.amount.total_amount}$`

            expensesChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: categories,
                    datasets: [{
                        label: 'Expenses by Category',
                        data: amounts,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });

    function update_chart() {
        const new_data = {
            type: 'pie', // Update the chart type if needed
            data: {
                labels: categories,
                datasets: [{
                    label: 'Expenses by Category',
                    data: amounts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
        const new_data_two = {
            type: 'bar', // Update the chart type if needed
            data: {
                labels: categories,
                datasets: [{
                    label: 'Expenses by Category',
                    data: amounts,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };

        expensesChart.destroy();
        expensesChart = new Chart(ctx, new_data);
        expensesChart = new Chart(ctx1, new_data_two);
    }

    sixmonths_div.addEventListener('click', (event) => {
        fetch('expenses-by-category-month/')
            .then(response => response.json())
            .then(new_data_month => {
                categories = new_data_month.map(item => item.category);
                amounts = new_data_month.map(item => item.total_amount);

                update_chart();
            });
    });
    year_div.addEventListener('click', (event) => {
        fetch('expenses-by_category-year/')
            .then(response => response.json())
            .then(new_data_year => {
                console.log(new_data_year)
                categories = new_data_year.map(item => item.category);
                amounts = new_data_year.map(item => item.total_amount);

                update_chart();
            });
    });
    today_div.addEventListener('click', (event) => {
        fetch('expenses-by-category-today/')
            .then(response => response.json())
            .then(new_data => {

                console.log(new_data)
                categories = new_data.map(item => item.category);
                amounts = new_data.map(item => item.total_amount);

                update_chart();
            });
    });
});