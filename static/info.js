document.addEventListener("DOMContentLoaded", function () {


    

    // Select the button element by its ID
    const itemRate = document.getElementById("top");
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
    const rswaterChoice = document.getElementById("rswater");
    const uswaterChoice = document.getElementById("uswater");
    const gasesChoice = document.getElementById("gases");
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
                    dataCheck = data.category;
                    if ((data.category !== 'US-Water') && (data.category !== 'RS-Water') && (data.category !== 'Gases') ) {
                        const df1Data = JSON.parse(result.df1);
                        const df2Data = JSON.parse(result.df2);
                        const df3Data = JSON.parse(result.df3);
                        const df4Data = JSON.parse(result.df4);
                        if (dataCheck !== 'Food') {
                            df5Data = JSON.parse(result.df5);
                            df6Data = JSON.parse(result.df6);
                            df7Data = JSON.parse(result.df7);
                            console.log('DF5: ', df5Data);

                        }
                        console.log('DF1: ', df1Data);
                        console.log('DF2: ', df2Data);
                        console.log('DF3: ', df3Data);
                        console.log('DF4: ', df4Data);

                        if (dataCheck !== 'Food'){
                        //Fill Warning box with assume rate, calculated rate, and percent difference
                        itemRate.textContent = 'A_Rate: ' + df5Data.rate.toFixed(4) + ' C_Rate: ' + df5Data.calculated_rate.toFixed(4) + ' P_Diff: '  + df5Data.Percent_Difference.toFixed(3);
                        }
                        else {
                            itemRate.textContent = 'Rate not yet calculated.'

                        }
                        // Extract data for plotting
                        const dates = df1Data.data.map(entry => entry.datedim.split('T')[0]);
                        const datesCrewUS = df2Data.data.map(entry => entry.datedim.split('T')[0]);
                        const datesCrewRS = df3Data.data.map(entry => entry.datedim.split('T')[0]);
                        const datesFlights = df4Data.data.map(entry => entry.datedim.split('T')[0]);
                        const flightsCount = Object.keys(datesFlights).length;
                        const eventType = df4Data.data.map(entry => entry.event);
                        const evaType = df4Data.data.map(entry => entry.eva_type);
                        const vehicleName = df4Data.data.map(entry => entry.vehicle_name);
                        console.log('flight count: ', flightsCount)
                        const rsaDates = df6Data.data.map(entry => entry.datedim.split('T')[0]);
                        const nasaDates = df7Data.data.map(entry => entry.datedim.split('T')[0]);                   
                        const nasaCounts = df7Data.data.map(entry => entry.distinct_id_count_categories);
                        const rsaCounts = df6Data.data.map(entry => entry.distinct_id_count_categories);
                        //const distinctIdCounts = df1Data.data.map(entry => entry.distinct_id_count_categories);
                        const totalCounts = df1Data.data.map(entry => entry.distinct_id_count_categories);
                        const totalDiscard = df1Data.data.map(entry => entry.discard_count);
                        const totalDifference = df1Data.data.map(entry => entry.distinct_discard_difference);
                        const rsDiscard = df6Data.data.map(entry => entry.discard_count);
                        const usDiscard = df7Data.data.map(entry => entry.discard_count);
                        const rsDifference = df6Data.data.map(entry => entry.distinct_discard_difference);
                        const usDifference = df7Data.data.map(entry => entry.distinct_discard_difference);
                        const usCrewCounts = df2Data.data.map(entry => entry.US_crew_count);
                        const rsCrewCounts = df3Data.data.map(entry => entry.RS_crew_count);

                        // Create a Plotly plot using the extracted data
                        const data = [
                            
                            {
                                x: datesFlights,
                                y: 6000,
                                name: 'Vehicle Info 3',
                                mode: 'markers',
                                marker: {
                                color: 'yellow',
                                size: 30,
                                },
                                text: vehicleName

                            },

                            {
                                x: datesFlights,
                                y: 6000,
                                name: 'Vehicle Info 2',
                                mode: 'markers',
                                marker: {
                                color: 'red',
                                size: 20,
                                },
                                text: eventType

                            },

                            {
                                x: datesFlights,
                                y: 6000,
                                name: 'Vehicle Info 1',
                                mode: 'markers',
                                marker: {
                                color: 'blue',
                                size: 10,
                                },
                                text: evaType

                            },

                            {
                                x: nasaDates,
                                y: nasaCounts,
                                type: 'scatter',
                                name: 'NASA Count',
                            },

                            {
                                x: rsaDates,
                                y: rsaCounts,
                                type: 'scatter',
                                name: 'RSA00 Count',
                            },
                            {
                                x: dates,
                                y:  totalCounts,
                                type: 'scatter',
                                name: 'Total Count',
                            },
                            {
                                x: rsaDates,
                                y: rsDiscard,
                                type: 'linear',
                                name: 'RS Discard',
                            },
                            {
                                x: nasaDates,
                                y: usDiscard,
                                type: 'linear',
                                name: 'US Discard',
                            },
                            {
                                x: dates,
                                y:  totalDiscard,
                                type: 'scatter',
                                name: 'Total Discard',
                            },

                            {
                                x: rsaDates,
                                y: rsDifference,
                                type: 'scatter',
                                name: 'RS remain.',
                            },

                            {
                                x: nasaDates,
                                y: usDifference,
                                type: 'scatter',
                                name: 'US remain.',
                            },

                            {
                                x: dates,
                                y: totalDifference,
                                type: 'scatter',
                                name: 'Total remain.',
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
                    }
                else {
                    const df1Data = JSON.parse(result.df1);
                    const df2Data = JSON.parse(result.df2);
                    const df3Data = JSON.parse(result.df3);
                    const df4Data = JSON.parse(result.df4);
                    console.log('DF1: ', df1Data);
                    console.log('DF2: ', df2Data);
                    console.log('DF3: ', df3Data);
                    console.log('DF4: ', df4Data);
                    
                    // Extract data for plotting
                    const evaType = df4Data.data.map(entry => entry.eva_type);
                    const dates = df1Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesCrewUS = df2Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesCrewRS = df3Data.data.map(entry => entry.datedim.split('T')[0]);
                    const datesFlights = df4Data.data.map(entry => entry.datedim.split('T')[0]);
                    const flightsCount = Object.keys(datesFlights).length;
                    const eventType = df4Data.data.map(entry => entry.event);
                    const vehicleName = df4Data.data.map(entry => entry.vehicle_name);
                    console.log('flight count: ', flightsCount)
                    console.log('EventType: ', eventType)  
                    if (data.category == 'US-Water') {
                        waterCounts = df1Data.data.map(entry => entry.corrected_potableL);
                        technical = df1Data.data.map(entry => entry.corrected_technicalL);
                        technicalResupply = df1Data.data.map(entry => entry.resupply_technicalL);
                        replenishdCounts = df1Data.data.map(entry => entry.resupply_potableL);
                        waterName = 'US Water'
                    } 
                    
                    else if (data.category == 'RS-Water') {
                        waterCounts = df1Data.data.map(entry => entry.remaining_potableL);
                        replenishdCounts = df1Data.data.map(entry => entry.rodnik_potableL);
                        waterName = 'RS Water'
                    }

                    else if (data.category == 'Gases') {
                        us_o2 = df1Data.data.map(entry => entry.US_O2kg);
                        rs_o2 = df1Data.data.map(entry => entry.RS_O2kg);
                        us_n2 = df1Data.data.map(entry => entry.US_N2kg);
                        rs_n2 = df1Data.data.map(entry => entry.RS_N2kg);
                        adjusted_o2 = df1Data.data.map(entry => entry.adjusted_O2kg);
                        adjusted_n2 = df1Data.data.map(entry => entry.adjusted_N2kg);
                        resupply_o2 = df1Data.data.map(entry => entry.resupply_O2kg);
                        resupply_n2 = df1Data.data.map(entry => entry.resupply_N2kg);
                        resupply_air = df1Data.data.map(entry => entry.resupply_air_kg);
                    }
                    
                    const usCrewCounts = df2Data.data.map(entry => entry.US_crew_count);
                    const rsCrewCounts = df3Data.data.map(entry => entry.RS_crew_count);
                    //Plot for water
                    if (data.category == 'US-Water') {
                        // Create a Plotly plot using the extracted data
                        const data = [
                            {
                                x: dates,
                                y: waterCounts,
                                type: 'scatter',
                                name: waterName,
                            },
                            {
                                x: dates,
                                y: technical,
                                type: 'scatter',
                                name: 'Technical',
                            },

                            {
                                x: datesFlights,
                                y: flightsCount,
                                name: 'Vehicle Info 3',
                                mode: 'markers',
                                marker: {
                                color: 'yellow',
                                size: 30,
                                },
                                text: vehicleName

                            },

                            {
                                x: datesFlights,
                                y: flightsCount,
                                name: 'Vehicle Info 2',
                                mode: 'markers',
                                marker: {
                                color: 'red',
                                size: 20,
                                },
                                text: eventType

                            },

                            {
                                x: datesFlights,
                                y: flightsCount,
                                name: 'Vehicle Info 1',
                                mode: 'markers',
                                marker: {
                                color: 'blue',
                                size: 10,
                                },
                                text: evaType

                            },

                            {
                                x: dates,
                                y: replenishdCounts,
                                type: 'linear',
                                name: 'Replenish',
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
                        }

                        else if (data.category == 'RS-Water') {
                                // Create a Plotly plot using the extracted data
                                const data = [
                                    {
                                        x: dates,
                                        y: waterCounts,
                                        type: 'scatter',
                                        name: waterName,
                                    },

                                    {
                                        x: datesFlights,
                                        y: flightsCount,
                                        name: 'Vehicle Info 3',
                                        mode: 'markers',
                                        marker: {
                                        color: 'yellow',
                                        size: 30,
                                        },
                                        text: vehicleName
        
                                    },
        
                                    {
                                        x: datesFlights,
                                        y: flightsCount,
                                        name: 'Vehicle Info 2',
                                        mode: 'markers',
                                        marker: {
                                        color: 'red',
                                        size: 20,
                                        },
                                        text: eventType
    
                                    },
    
                                    {
                                        x: datesFlights,
                                        y: flightsCount,
                                        name: 'Vehicle Info 1',
                                        mode: 'markers',
                                        marker: {
                                        color: 'blue',
                                        size: 10,
                                        },
                                        text: evaType
    
                                    },
        
                                    {
                                        x: dates,
                                        y: replenishdCounts,
                                        type: 'linear',
                                        name: 'Replenish',
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
                            }
        
                        

                        //Plot for Gases
                        else if (data.category == 'Gases') {
                            // Create a Plotly plot using the extracted data
                            const data = [
                                {
                                    x: dates,
                                    y: us_o2,
                                    type: 'scatter',
                                    name: 'US O2',
                                },

                                {
                                    x: datesFlights,
                                    y: flightsCount,
                                    name: 'Vehicle Info 3',
                                    mode: 'markers',
                                    marker: {
                                    color: 'yellow',
                                    size: 30,
                                    },
                                    text: vehicleName
    
                                },

                                {
                                    x: datesFlights,
                                    y: flightsCount,
                                    name: 'Vehicle Info 2',
                                    mode: 'markers',
                                    marker: {
                                    color: 'red',
                                    size: 20,
                                    },
                                    text: eventType

                                },

                                {
                                    x: datesFlights,
                                    y: flightsCount,
                                    name: 'Vehicle Info 1',
                                    mode: 'markers',
                                    marker: {
                                    color: 'blue',
                                    size: 10,
                                    },
                                    text: evaType

                                },

                                {
                                    x: dates,
                                    y: rs_o2,
                                    type: 'linear',
                                    name: 'RS O2',
                                },

                                {
                                    x: dates,
                                    y: us_n2,
                                    type: 'linear',
                                    name: 'US N2',
                                },

                                {
                                    x: dates,
                                    y: rs_n2,
                                    type: 'linear',
                                    name: 'RS N2',
                                },
                                
                                {
                                    x: dates,
                                    y: adjusted_o2,
                                    type: 'linear',
                                    name: 'Adjusted O2',
                                },

                                {
                                    x: dates,
                                    y: adjusted_n2,
                                    type: 'linear',
                                    name: 'Adjusted N2',
                                },

                                {
                                    x: dates,
                                    y: resupply_o2,
                                    type: 'linear',
                                    name: 'Resupply O2',
                                },
                                
                                {
                                    x: dates,
                                    y: resupply_n2,
                                    type: 'linear',
                                    name: 'Resupply N2',
                                },

                                {
                                    x: dates,
                                    y: resupply_air,
                                    type: 'linear',
                                    name: 'Resupply Air',
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
                            }
                }
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