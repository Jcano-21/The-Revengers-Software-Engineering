document.addEventListener("DOMContentLoaded", function () {

    // Select the button element by its ID
    const itemRate = document.getElementById("calc_data");
    const div = document.getElementById("loading");
    const itemSelectionButton = document.getElementById("itemSelection");

     // Select the input elements by their IDs
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");

    // Select the "Submit" button
    const submitButton = document.getElementById("submitDates");

    // Select Info Screen buttons
    const consumptionButton = document.getElementById("consumption");
    const makePredictionsButton = document.getElementById("percent_diff");

    // Select the choices by their IDs
    const acyChoice = document.getElementById("acyInserts");
    const filterChoice = document.getElementById("filterInserts");
    const all = document.getElementById("all");
    const foodRSChoice = document.getElementById("foodRS");
    const foodUSChoice = document.getElementById("foodUS");
    const ktoChoice = document.getElementById("kto");
    const ptanksChoice = document.getElementById("pTanks");
    const rswaterChoice = document.getElementById("rswater");
    const uswaterChoice = document.getElementById("uswater");
    const gasesChoice = document.getElementById("gases");
    obj = null
    newResult = null
    
    // Function to change the text
    function changeText(choice) {
        itemSelectionButton.textContent = choice.textContent;
        console.log(itemSelectionButton.textContent)
        
    }

    // Add click event listeners to the choices
    acyChoice.addEventListener("click", function () {
        changeText(acyChoice);
    });

    filterChoice.addEventListener("click", function () {
        changeText(filterChoice);
    });


    all.addEventListener("click", function () {
        changeText(all);
    });

    foodRSChoice.addEventListener("click", function () {
        changeText(foodRSChoice);
    });

    foodUSChoice.addEventListener("click", function () {
        changeText(foodUSChoice);
    });

    ktoChoice.addEventListener("click", function () {
        changeText(ktoChoice);
    });

    ptanksChoice.addEventListener("click", function () {
        changeText(ptanksChoice);
    });
    rswaterChoice.addEventListener("click", function () {
        changeText(rswaterChoice);
    });
    uswaterChoice.addEventListener("click", function () {
        changeText(uswaterChoice);
    });
    gasesChoice.addEventListener("click", function () {
        changeText(gasesChoice);
    });

    // Add a click event listener to the "Submit" button
    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission
        const startDateValue = startDateInput.value;
        const endDateValue = endDateInput.value;
        const categoryValue = itemSelectionButton.textContent;
        submitButton.disabled = true;
        consumptionButton.disabled = true;
        makePredictionsButton.disabled = true;


        if (startDateValue >= endDateValue) {
            alert("Start date must be before the end date and not the same day.");
            submitButton.disabled = false;
            consumptionButton.disabled = false;
            makePredictionsButton.disabled = false;
            return;
        }

        // Define the data to send in the request
        const data = {
            start_date: startDateValue,
            end_date: endDateValue,
            category: categoryValue,
        };
        captureInputValues(data, itemRate, div);
    });

    // Add a click event listener to the "Submit" button
    consumptionButton.addEventListener("click", function (event) {

        submitButton.disabled = true;
        consumptionButton.disabled = true;
        makePredictionsButton.disabled = true;

        
        if (itemSelectionButton.textContent !== 'Select Item' && itemSelectionButton.textContent !== 'All'){ // Prevent the default form submission
            const categoryValue = itemSelectionButton.textContent;
            captureInputValuesCalc(categoryValue, itemRate, div);
        }
        else {
            window.alert("Please select an Item")
            submitButton.disabled = false;
            consumptionButton.disabled = false;
            makePredictionsButton.disabled = false;
        }

        

    });

    makePredictionsButton.addEventListener("click", function (event) {
        
        submitButton.disabled = true;
        consumptionButton.disabled = true;
        makePredictionsButton.disabled = true;

        if (itemSelectionButton.textContent == 'All' || itemSelectionButton.textContent == 'RS-Water'|| itemSelectionButton.textContent == 'US-Water' || itemSelectionButton.textContent == 'Gases'){ // Prevent the default form submission
            const categoryValue = itemSelectionButton.textContent;
            startPredictions(categoryValue, itemRate, div);
            
        }
        else {
            window.alert("Please select All for predictions.")
            submitButton.disabled = false;
            consumptionButton.disabled = false;
            makePredictionsButton.disabled = false;
        }

    });

    

    
});



TESTER = document.getElementById('tester');

Plotly.plot( TESTER, [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16] }], { 
    margin: { t: 20 } }, {showSendToCloud:true} );

/* Current Plotly.js version */
console.log( Plotly.BUILD );