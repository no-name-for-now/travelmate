// post.js

document.addEventListener("DOMContentLoaded", function () {
    const tableRows = document.querySelectorAll(".clickable-row");

    tableRows.forEach((row) => {
        row.addEventListener("click", function () {
            const form = this.querySelector("form");
            form.submit();
        });
    });
});

// JavaScript code to display the current date
const currentDateElement = document.getElementById("currentDate");
const currentDate = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
const formattedDate = currentDate.toLocaleDateString(undefined, options);
currentDateElement.textContent = formattedDate;