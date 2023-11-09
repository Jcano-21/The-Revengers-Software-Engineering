document.addEventListener("DOMContentLoaded", function () {


    

    // Select the button element by its ID
    const itemSelectionButton = document.getElementById("itemSelection");

     // Select the input elements by their IDs
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");

    // Select the "Submit" button
    const submitButton = document.getElementById("submitDates");

    // Select the choices by their IDs
    const acyChoice = document.getElementById("acyInserts");
    const filterChoice = document.getElementById("filterInserts");
    const foodChoice = document.getElementById("food");
    const foodRSChoice = document.getElementById("foodRS");
    const foodUSChoice = document.getElementById("foodUS");
    const ktoChoice = document.getElementById("kto");
    const ptanksChoice = document.getElementById("pTanks");
    obj = null
    newResult = null


    function captureInputValues() {
        const startDateValue = startDateInput.value;
        const endDateValue = endDateInput.value;
        const categoryValue = itemSelectionButton.textContent;

        if (startDateValue >= endDateValue) {
            alert("Start date must be before the end date and not the same day.");
            return;
        }

        // Define the data to send in the request
        const data = {
            start_date: startDateValue,
            end_date: endDateValue,
            category: categoryValue,
        };

        

        function fetchDataAndCreatePlot(data) {
            fetch('/consumable', {
                headers: {
                    'Content-Type': 'application/json',
                },
                method: 'POST',
                body: JSON.stringify(data),
                // credentials: 'include',  // Include credentials if needed
            })
                .then(response => response.json())
                .then(result => {
                    // Parse the JSON response to an object
                    result = JSON.parse(result);

                    console.log('Print results: ', result);

                    // Access df1, df2, and df3 within the result object
                    const df1Data = JSON.parse(result.df1);
                    const df2Data = JSON.parse(result.df2);
                    const df3Data = JSON.parse(result.df3);
                    const df4Data = JSON.parse(result.df4)
                    console.log('DF1: ', df1Data);
                    console.log('DF2: ', df2Data);
                    console.log('DF3: ', df3Data);
                    console.log('DF4: ', df4Data);

                    // Extract data for plotting
                    const dates = df1Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesCrewUS = df2Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesCrewRS = df3Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesFlights = df4Data.data.map(entry => entry.datedim.split('T')[0]);
                    const flightsCount = Object.keys(datesFlights).length;
                    console.log('flight count: ', flightsCount)                   
                    const nasaCounts = df1Data.data.map(entry => entry.nasa_count);
                    const rsaCounts = df1Data.data.map(entry => entry.rsa00_count);
                    const distinctIdCounts = df1Data.data.map(entry => entry.distinct_id_count_categories);
                    const discardCounts = df1Data.data.map(entry => entry.discard_count);
                    const usCrewCounts = df2Data.data.map(entry => entry.US_crew_count);
                    const rsCrewCounts = df3Data.data.map(entry => entry.RS_crew_count);

                    // Create a Plotly plot using the extracted data
                    const data = [
                        {
                            x: dates,
                            y: nasaCounts,
                            type: 'scatter',
                            name: 'NASA Count',
                        },
                        {
                            x: datesFlights,
                            y: flightsCount,
                            type: 'scatter',
                            name: 'Resupply',
                        },
                        {
                            x: dates,
                            y: rsaCounts,
                            type: 'linear',
                            name: 'RSA00 Count',
                        },
                        {
                            x: dates,
                            y: distinctIdCounts,
                            type: 'linear',
                            name: 'Distinct ID Count',
                        },
                        {
                            x: dates,
                            y: discardCounts,
                            type: 'linear',
                            name: 'Discard Count',
                        },
                        {
                            x: datesCrewUS,
                            y: usCrewCounts,
                            type: 'linear',
                            name: 'US Crew Count',
                        },
                        {
                            x: datesCrewRS,
                            y: rsCrewCounts,
                            type: 'linear',
                            name: 'RS Crew Count',
                        },
                    ];

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 0 },
                    };

                    Plotly.newPlot('tester', data, layout);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }


        fetchDataAndCreatePlot(data);


    }

    



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

    foodChoice.addEventListener("click", function () {
        changeText(foodChoice);
    });

    foodChoice.addEventListener("click", function () {
        changeText(foodChoice);
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

    // Add a click event listener to the "Submit" button
    submitButton.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission
        captureInputValues();
    });
});



TESTER = document.getElementById('tester');

Plotly.plot( TESTER, [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16] }], { 
    margin: { t: 0 } }, {showSendToCloud:true} );

/* Current Plotly.js version */
console.log( Plotly.BUILD );