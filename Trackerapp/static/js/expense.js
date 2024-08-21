const form = document.getElementById('expense-form');
const submitBtn = document.getElementById('submit');

form.addEventListener('submit',(e) => {
    e.preventDefault();
    const date = document.getElementById('date').value;
    const category = document.getElementById('category').value;
    const price = document.getElementById('price').value;
    const income = document.getElementById('income').value;
    const description = document.getElementById('description').value;

    fetch("/user-expenses/",{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({date,category,price,income,description})
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Expense saved successfully!');
    })
    .catch((error) => console.error(error));
});