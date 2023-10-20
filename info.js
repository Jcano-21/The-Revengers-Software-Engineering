document.addEventListener("DOMContentLoaded", function () {
    // Select the button element by its ID
    const itemSelectionButton = document.getElementById("itemSelection");

     // Select the input elements by their IDs
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");

    // Select the "Submit" button
    const submitButton = document.getElementById("submitDates");

    // Select the choices by their IDs
    const waterChoice = document.getElementById("water");
    const oxygenChoice = document.getElementById("oxygen");
    const foodChoice = document.getElementById("food");

    function captureInputValues() {
        const startDateValue = startDateInput.value;
        const endDateValue = endDateInput.value;

        if (startDateValue >= endDateValue) {
            alert("Start date must be before the end date and not the same day.");
            return;
        }

        // You can now use startDateValue and endDateValue as needed
        console.log("Start Date: " + startDateValue);
        console.log("End Date: " + endDateValue);
    }

    // Function to change the text
    function changeText(choice) {
        itemSelectionButton.textContent = choice.textContent;
    }

    // Add click event listeners to the choices
    waterChoice.addEventListener("click", function () {
        changeText(waterChoice);
    });

    oxygenChoice.addEventListener("click", function () {
        changeText(oxygenChoice);
    });

    foodChoice.addEventListener("click", function () {
        changeText(foodChoice);
    });

    // Add a click event listener to the "Submit" button
    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission
        captureInputValues();
    });
});