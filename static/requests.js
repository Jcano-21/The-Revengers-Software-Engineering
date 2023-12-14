// Select the "Submit" button
const submitButton = document.getElementById("submitDates");

// Select Info Screen buttons
const consumptionButton = document.getElementById("consumption");
const makePredictionsButton = document.getElementById("percent_diff");

// selecting loading div
const loader = document.querySelector("#loading");
const loadertwo = document.querySelector("#loadingtwo");
const loaderthree = document.querySelector("#loadingthree");

// showing loading
function displayLoading() {
    loader.classList.add("display");
    // to stop loading after some time
    setTimeout(() => {
        loader.classList.remove("display");
    }, 3000000);

    loadertwo.classList.add("displaytwo");
    // to stop loading after some time
    setTimeout(() => {
        loadertwo.classList.remove("displaytwo");
    }, 3000000);

    loaderthree.classList.add("displaythree");
    // to stop loading after some time
    setTimeout(() => {
        loaderthree.classList.remove("displaythree");
    }, 3000000);
}

// hiding loading 
function hideLoading() {
    loader.classList.remove("display");
    loadertwo.classList.remove("displaytwo");
    loaderthree.classList.remove("displaythree");
}

function captureInputValues(data, itemRate, div) {
    itemRate.textContent = '\n                    \n     ';
    itemRate.innerText = '';
    itemRate.appendChild(div);
    loaderthree.textContent = 'FETCHING DATA, PLEASE WAIT.';
    displayLoading()

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
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                // Parse the JSON response to an object
                result = JSON.parse(result);

                console.log('Print results: ', result);
                dataCheck = data.category;
                if ((data.category !== 'US-Water') && (data.category !== 'RS-Water') && (data.category !== 'Gases') && (data.category !== 'Inventory') ) {
                    const df1Data = JSON.parse(result.df1);
                    const df2Data = JSON.parse(result.df2);
                    const df3Data = JSON.parse(result.df3);
                    const df4Data = JSON.parse(result.df4);
                    df5Data = JSON.parse(result.df5);
                    df6Data = JSON.parse(result.df6);
                    df7Data = JSON.parse(result.df7);
                    console.log('DF5: ', df5Data);
                    console.log('DF1: ', df1Data);
                    console.log('DF2: ', df2Data);
                    console.log('DF3: ', df3Data);
                    console.log('DF4: ', df4Data);

                     if (dataCheck !== 'Food'){
                     //Fill Warning box with assume rate, calculated rate, and percent difference
                     itemRate.textContent = 'A_Rate: ' + df5Data.rate.toFixed(4) + ' C_Rate: ' + df5Data.calculated_rate.toFixed(4) + ' P_Diff: '  + df5Data.Percent_Difference.toFixed(2);
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
                        margin: { t: 20 },
                    };

                    Plotly.newPlot('tester', data, layout);
                }
            else {
                //pars the json strings for water data
                const df1Data = JSON.parse(result.df1);
                const df2Data = JSON.parse(result.df2);
                const df3Data = JSON.parse(result.df3);
                const df4Data = JSON.parse(result.df4);
                //If category is US-Water or RS-Water fill in text box with rate usage data
                if ((data.category === 'US-Water' || data.category === 'RS-Water')) {
                    const df5Data = JSON.parse(result.df5);
                    itemRate.innerHTML = 'A_Rate: ' + df5Data.rate.toFixed(4) + ' C_Rate: ' + df5Data.calculated_rate.toFixed(4) + ' P_Diff: '  + df5Data.Percent_Difference.toFixed(3) 
                    + '<br>' + 'A_RateTech: ' + df5Data.rateTech.toFixed(4) + ' C_RateTech: ' + df5Data.calculated_rate_tech.toFixed(4) + ' P_Diff: '  + df5Data.Percent_DifferenceTech.toFixed(3) ;
                    console.log('DF5: ', df5Data);
                }


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
                    waterCountsTech = df1Data.data.map(entry => entry.technicalL);
                    replenishdCounts = df1Data.data.map(entry => entry.rodnik_potableL);
                    waterName = 'Remain. Potable'
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
                            name: 'Remain. Technical',
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
                        margin: { t: 20 },
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
                                    x: dates,
                                    y: waterCountsTech,
                                    type: 'scatter',
                                    name: 'Remain. Technical',
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
                                    name: 'Rodnik',
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
                                margin: { t: 20 },
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
                            margin: { t: 20 },
                        };

                        Plotly.newPlot('tester', data, layout);
                        }
            }
            })
            .catch(error => {
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                console.error('Error:', error);
            });
    }

    fetchDataAndCreatePlot(data);
}

function captureInputValuesCalc(categoryValue, itemRate, div) {
    itemRate.textContent = '\n                    \n     ';
    itemRate.innerText = '';
    itemRate.appendChild(div);
    loaderthree.textContent = 'FETCHING DATA, PLEASE WAIT.';
     displayLoading()
    // Define the data to send in the request
    const data = categoryValue;

    function fetchDataAndCreatePlot(data) {
        fetch('/consumptionRates', {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                // Parse the JSON response to an object
                console.log('print first results: ', result)
                averages = JSON.parse(result[0]);
                resupply_periods = JSON.parse(result[1]);
                resupply_Dates = JSON.parse(result[2]);
                console.log('Print results: ', averages);
                if ((data !== 'US-Water') && (data !== 'RS-Water') && (data !== 'Gases') && (data !== 'Inventory') ) {
                    const df1Data = averages.Category;
                    const df2Data = averages.RATE_AVERAGE;
                    const df3Data = averages.RATE_DIFF_AVERAGE;
                    const df4Data = averages.DAYS_BETWEEN_RESUPPLY_AVERAGE;
                    const df5Data = averages.USAGE_AVERAGE
                    const df6Data = averages.RESUPPLY_AVERAGE
                    console.log('DF1: ', df1Data);
                    console.log('DF2: ', df2Data);
                    console.log('DF3: ', df3Data);
                    console.log('DF4: ', df4Data);
                    console.log('print periods: ', resupply_periods)
                    console.log('print dates: ', resupply_Dates)

                    //Fill Warning box with assume rate, calculated rate, and percent difference
                    itemRate.innerHTML = 'Category: ' + df1Data + ' Rate_Average: ' + df2Data.toFixed(4) + ' Rate_Diff: ' + df3Data.toFixed(2) + '<br>DBR: '  + df4Data.toFixed(2) + ' Usage_Avg: ' + df5Data.toFixed(2) + ' Ressuply_Avg: ' + df6Data.toFixed(2);
                    
                    const c_rate = resupply_periods.data.map(entry => entry.calculated_rate);
                    const a_rate = resupply_periods.data.map(entry => entry.rate);
                    const p_diff = resupply_periods.data.map(entry => entry.Percent_Difference);
                    const d_diff = resupply_periods.data.map(entry => entry.Diff_days);
                    const q_diff = resupply_periods.data.map(entry => entry.Diff_Quantity);
                    const r_count = resupply_periods.data.map(entry => entry.Resupply_Count);
                    const dates = resupply_periods.data.map(entry => entry.date.split('T')[0]);
                    const data = [
                        {
                            x: dates,
                            y: c_rate,
                            type: 'scatter',
                            name: 'Calculated_Rate',
                        },

                        {
                            x: dates,
                            y: a_rate,
                            type: 'scatter',
                            name: 'Assumed_Rate',
                        },

                        {
                            x: dates,
                            y: p_diff,
                            type: 'scatter',
                            name: 'Rate_Percent_Difference',
                        },
                        
                        {
                            x: dates,
                            y: d_diff,
                            type: 'scatter',
                            name: 'Day\'s since resupply',
                        },

                        {
                            x: dates,
                            y: q_diff,
                            type: 'scatter',
                            name: 'Usage since resupply',
                        },

                        {
                            x: dates,
                            y: r_count,
                            type: 'scatter',
                            name: 'Resupply Amount',
                        },
                    ]

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 20 },
                    };

                    Plotly.newPlot('tester', data, layout);

                    
                }
            else if (data == 'RS-Water') {
                //pars the json strings for water data
                const df1Data = averages.Category;
                const df2Data = averages.RATE_AVERAGE_POT;
                const df3Data = averages.RATE_DIFF_AVERAGE_POT;
                const df4Data = averages.RATE_AVERAGE_TECH;
                const df5Data = averages.RATE_DIFF_AVERAGE_TECH
                const df6Data = averages.USAGE_AVERAGE_POT
                const df7Data = averages.USAGE_AVERAGE_TECH
                const df8Data = averages.RESUPPLY_AVERAGE_POT
                const df9Data = averages.RESUPPLY_AVERAGE_TECH
                const df10Data = averages.RESUPPLY_AVERAGE_ROD
                const df11Data = averages.DAYS_BETWEEN_RESUPPLY_AVERAGE
                const df12Data = averages.USAGE_AVERAGE_ROD


                //If category is US-Water or RS-Water fill in text box with rate usage data
                itemRate.innerHTML = 'Category: ' + df1Data + ' Rate_Pot_AVG: ' + df2Data.toFixed(4) + ' P_Diff_Pot: '  + df3Data.toFixed(2) 
                +  '<br>Rate_Tech_AVG: ' + df4Data.toFixed(4) + ' P_Diff_Tech: ' + df5Data.toFixed(2) + '<br>Usage_Pot: '  + df6Data.toFixed(2) 
                + ' Usage_Tech: ' + df7Data.toFixed(2) + ' Usage_Rod: ' + df12Data.toFixed(2) + '<br> Resupply_Pot: ' + df8Data.toFixed(2) + ' Resupply_Tech: ' + df9Data.toFixed(2) + ' Resupply_Rod: ' + df10Data.toFixed(2) + '<br> Days_Between_Resupply_AVG: ' + df11Data.toFixed(2);
                console.log('DF5: ', df5Data);
                
                //Grab attributes to plot on graph
                const c_rate_pot = resupply_periods.data.map(entry => entry.calculated_rate);
                const a_rate_pot = resupply_periods.data.map(entry => entry.rate);
                const p_diff_pot = resupply_periods.data.map(entry => entry.Percent_Difference);
                const a_rate_tech = resupply_periods.data.map(entry => entry.rateTech);
                const c_rate_tech = resupply_periods.data.map(entry => entry.calculated_rate_tech);
                const p_diff_tech = resupply_periods.data.map(entry => entry.Percent_DifferenceTech);
                const u_pot = resupply_periods.data.map(entry => entry.Usage_Pot);
                const u_tech = resupply_periods.data.map(entry => entry.Usage_Tech);
                const u_rod = resupply_periods.data.map(entry => entry.Usage_Rod);
                const r_pot = resupply_periods.data.map(entry => entry.Resupply_Pot);
                const r_tech = resupply_periods.data.map(entry => entry.Resupply_Tech);
                const r_rod = resupply_periods.data.map(entry => entry.Resupply_Rod);
                const d_diff = resupply_periods.data.map(entry => entry.Diff_in_days);
                const dates = resupply_periods.data.map(entry => entry.date.split('T')[0]);


                console.log('DF1: ', df1Data);
                console.log('DF2: ', df2Data);
                console.log('DF3: ', df3Data);
                console.log('DF4: ', df4Data);

                
                const data = [
                    {
                        x: dates,
                        y: c_rate_pot,
                        type: 'scatter',
                        name: 'Calculated_Rate_Pot',
                    },

                    {
                        x: dates,
                        y: a_rate_pot,
                        type: 'scatter',
                        name: 'Assumed_Rate_Pot',
                    },

                    {
                        x: dates,
                        y: p_diff_pot,
                        type: 'scatter',
                        name: 'Percent_Difference_Pot',
                    },
                    
                    {
                        x: dates,
                        y: a_rate_tech,
                        type: 'scatter',
                        name: 'Assumed_Rate_Tech',
                    },

                    {
                        x: dates,
                        y: c_rate_tech,
                        type: 'scatter',
                        name: 'Calculated_Rate_Tech',
                    },

                    {
                        x: dates,
                        y: p_diff_tech,
                        type: 'scatter',
                        name: 'Percent_Difference_Tech',
                    },

                    {
                        x: dates,
                        y: u_pot,
                        type: 'scatter',
                        name: 'Usage_Pot',
                    },

                    {
                        x: dates,
                        y: u_tech,
                        type: 'scatter',
                        name: 'Usage_Tech',
                    },

                    {
                        x: dates,
                        y: u_rod,
                        type: 'scatter',
                        name: 'Usage_Rod',
                    },

                    {
                        x: dates,
                        y: r_pot,
                        type: 'scatter',
                        name: 'Resupply_Pot',
                    },

                    {
                        x: dates,
                        y: r_tech,
                        type: 'scatter',
                        name: 'Resupply_Tech',
                    },

                    {
                        x: dates,
                        y: r_rod,
                        type: 'scatter',
                        name: 'Resupply_Rod',
                    },

                    {
                        x: dates,
                        y: d_diff,
                        type: 'scatter',
                        name: 'Days Between Resupply',
                    }
                ]

                const layout = {
                    xaxis: {
                        title: 'Date',
                    },
                    yaxis: {
                        title: 'Count',
                    },
                    margin: { t: 20 },
                };

                Plotly.newPlot('tester', data, layout);
            }
                
            else if (data == 'US-Water') {
                //pars the json strings for water data
                const df1Data = averages.Category;
                const df2Data = averages.RATE_AVERAGE_POT;
                const df3Data = averages.RATE_DIFF_AVERAGE_POT;
                const df4Data = averages.RATE_AVERAGE_TECH;
                const df5Data = averages.RATE_DIFF_AVERAGE_TECH
                const df6Data = averages.USAGE_AVERAGE_POT
                const df7Data = averages.USAGE_AVERAGE_TECH
                const df8Data = averages.RESUPPLY_AVERAGE_POT
                const df9Data = averages.RESUPPLY_AVERAGE_TECH
                const df11Data = averages.DAYS_BETWEEN_RESUPPLY_AVERAGE


                //If category is US-Water or RS-Water fill in text box with rate usage data
                itemRate.innerHTML = 'Category: ' + df1Data + ' Rate_Pot_AVG: ' + df2Data.toFixed(4) + ' P_Diff_Pot: '  + df3Data.toFixed(2) 
                +  '<br> Rate_Tech_AVG: ' + df4Data.toFixed(4) + ' P_Diff_Tech: ' + df5Data.toFixed(2) + '<br> Usage_Pot: '  + df6Data.toFixed(2) 
                + ' Usage_Tech: ' + df7Data.toFixed(2) + '<br> Resupply_Pot: ' + df8Data.toFixed(2) + ' Resupply_Tech: ' + df9Data.toFixed(2) +'<br> Days_Between_Resupply_AVG: ' + df11Data.toFixed(2);
                console.log('DF5: ', df5Data);
                
                //Grab attributes to plot on graph
                const c_rate_pot = resupply_periods.data.map(entry => entry.calculated_rate);
                const a_rate_pot = resupply_periods.data.map(entry => entry.rate);
                const p_diff_pot = resupply_periods.data.map(entry => entry.Percent_Difference);
                const a_rate_tech = resupply_periods.data.map(entry => entry.rateTech);
                const c_rate_tech = resupply_periods.data.map(entry => entry.calculated_rate_tech);
                const p_diff_tech = resupply_periods.data.map(entry => entry.Percent_DifferenceTech);
                const u_pot = resupply_periods.data.map(entry => entry.Usage_Pot);
                const u_tech = resupply_periods.data.map(entry => entry.Usage_Tech);
                const r_pot = resupply_periods.data.map(entry => entry.Resupply_Pot);
                const r_tech = resupply_periods.data.map(entry => entry.Resupply_Tech);
                const d_diff = resupply_periods.data.map(entry => entry.Diff_in_days);
                const dates = resupply_periods.data.map(entry => entry.date.split('T')[0]);


                console.log('DF1: ', df1Data);
                console.log('DF2: ', df2Data);
                console.log('DF3: ', df3Data);
                console.log('DF4: ', df4Data);

                
                const data = [
                    {
                        x: dates,
                        y: c_rate_pot,
                        type: 'scatter',
                        name: 'Calculated_Rate_Pot',
                    },

                    {
                        x: dates,
                        y: a_rate_pot,
                        type: 'scatter',
                        name: 'Assumed_Rate_Pot',
                    },

                    {
                        x: dates,
                        y: p_diff_pot,
                        type: 'scatter',
                        name: 'Percent_Difference_Pot',
                    },
                    
                    {
                        x: dates,
                        y: a_rate_tech,
                        type: 'scatter',
                        name: 'Assumed_Rate_Tech',
                    },

                    {
                        x: dates,
                        y: c_rate_tech,
                        type: 'scatter',
                        name: 'Calculated_Rate_Tech',
                    },

                    {
                        x: dates,
                        y: p_diff_tech,
                        type: 'scatter',
                        name: 'Percent_Difference_Tech',
                    },

                    {
                        x: dates,
                        y: u_pot,
                        type: 'scatter',
                        name: 'Usage_Pot',
                    },

                    {
                        x: dates,
                        y: u_tech,
                        type: 'scatter',
                        name: 'Usage_Tech',
                    },

                    {
                        x: dates,
                        y: r_pot,
                        type: 'scatter',
                        name: 'Resupply_Pot',
                    },

                    {
                        x: dates,
                        y: r_tech,
                        type: 'scatter',
                        name: 'Resupply_Tech',
                    },

                    {
                        x: dates,
                        y: d_diff,
                        type: 'scatter',
                        name: 'Days Between Resupply',
                    }
                ]

                const layout = {
                    xaxis: {
                        title: 'Date',
                    },
                    yaxis: {
                        title: 'Count',
                    },
                    margin: { t: 20 },
                };

                Plotly.newPlot('tester', data, layout);
                
            }

            else if (data == 'Gases') {
                //pars the json strings for water data
                const df1Data = averages.Category;
                const df2Data = averages.RATE_AVERAGE_O2;
                const df3Data = averages.RATE_DIFF_AVERAGE_O2;
                const df4Data = averages.RATE_AVERAGE_N2;
                const df5Data = averages.RATE_DIFF_AVERAGE_N2
                const df6Data = averages.USAGE_AVERAGE_O2
                const df7Data = averages.USAGE_AVERAGE_N2
                const df8Data = averages.RESUPPLY_AVERAGE_O2
                const df9Data = averages.RESUPPLY_AVERAGE_N2
                const df11Data = averages.DAYS_BETWEEN_RESUPPLY_AVERAGE


                //If category is US-Water or RS-Water fill in text box with rate usage data
                itemRate.innerHTML = 'Category: ' + df1Data + ' Rate_O2_AVG: ' + df2Data.toFixed(4) + ' P_Diff_O2: '  + df3Data.toFixed(2) 
                +  '<br> Rate_N2_AVG: ' + df4Data.toFixed(4) + ' P_Diff_N2: ' + df5Data.toFixed(2) + '<br> Usage_O2: '  + df6Data.toFixed(2) 
                + ' Usage_N2: ' + df7Data.toFixed(2) + '<br> Resupply_O2: ' + df8Data.toFixed(2) + ' Resupply_N2: ' + df9Data.toFixed(2) +'<br> Days_Between_Resupply_AVG: ' + df11Data.toFixed(2);
                console.log('DF5: ', df5Data);
                
                //Grab attributes to plot on graph
                const c_rate_O2 = resupply_periods.data.map(entry => entry.calculated_rate_O2);
                const a_rate_O2 = resupply_periods.data.map(entry => entry.rate);
                const p_diff_O2 = resupply_periods.data.map(entry => entry.Percent_Difference_O2);
                const a_rate_N2 = resupply_periods.data.map(entry => entry.rateUSN2);
                const c_rate_N2 = resupply_periods.data.map(entry => entry.calculated_rate_N2);
                const p_diff_N2 = resupply_periods.data.map(entry => entry.Percent_DifferenceN2);
                const u_O2 = resupply_periods.data.map(entry => entry.Usage_O2);
                const u_N2 = resupply_periods.data.map(entry => entry.Usage_N2);
                const r_O2 = resupply_periods.data.map(entry => entry.Resupply_O2);
                const r_N2 = resupply_periods.data.map(entry => entry.Resupply_N2);
                const d_diff = resupply_periods.data.map(entry => entry.Diff_in_days);
                const dates = resupply_periods.data.map(entry => entry.date.split('T')[0]);


                console.log('DF1: ', df1Data);
                console.log('DF2: ', df2Data);
                console.log('DF3: ', df3Data);
                console.log('DF4: ', df4Data);

                
                const data = [
                    {
                        x: dates,
                        y: c_rate_O2,
                        type: 'scatter',
                        name: 'Calculated_Rate_O2',
                    },

                    {
                        x: dates,
                        y: a_rate_O2,
                        type: 'scatter',
                        name: 'Assumed_Rate_O2',
                    },

                    {
                        x: dates,
                        y: p_diff_O2,
                        type: 'scatter',
                        name: 'Percent_Difference_O2',
                    },
                    
                    {
                        x: dates,
                        y: a_rate_N2,
                        type: 'scatter',
                        name: 'Assumed_Rate_N2',
                    },

                    {
                        x: dates,
                        y: c_rate_N2,
                        type: 'scatter',
                        name: 'Calculated_Rate_N2',
                    },

                    {
                        x: dates,
                        y: p_diff_N2,
                        type: 'scatter',
                        name: 'Percent_Difference_N2',
                    },

                    {
                        x: dates,
                        y: u_O2,
                        type: 'scatter',
                        name: 'Usage_O2',
                    },

                    {
                        x: dates,
                        y: u_N2,
                        type: 'scatter',
                        name: 'Usage_N2',
                    },

                    {
                        x: dates,
                        y: r_O2,
                        type: 'scatter',
                        name: 'Resupply_O2',
                    },

                    {
                        x: dates,
                        y: r_N2,
                        type: 'scatter',
                        name: 'Resupply_N2',
                    },

                    {
                        x: dates,
                        y: d_diff,
                        type: 'scatter',
                        name: 'Days Between Resupply',
                    }
                ]

                const layout = {
                    xaxis: {
                        title: 'Date',
                    },
                    yaxis: {
                        title: 'Count',
                    },
                    margin: { t: 20 },
                };

                Plotly.newPlot('tester', data, layout);
                
            }
            })
            .catch(error => {
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                console.error('Error:', error);
            });
    }

    fetchDataAndCreatePlot(data)

}

    

function startPredictions(data, itemRate, div) {
    itemRate.textContent = '\n                    \n     ';
    itemRate.innerText = '';
    itemRate.appendChild(div);
    displayLoading()

    function fetchDataAndCreatePlot(data) {
        loaderthree.textContent = 'TRAINING, MAY TAKE SEVERAL MINUTES!';
        displayLoading()
        fetch('/makePredictions', {
            headers: {
                'Content-Type': 'application/json',
            },
            method: 'POST',
            body: JSON.stringify(data),
            // credentials: 'include',  // Include credentials if needed
        })
            .then(response => response.json())
            .then(result => {
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                // Parse the JSON response to an object
                if (data == 'Inventory')  {
                    predict = JSON.parse(result[0]);
                    calcOne = JSON.parse(result[1]);
                    calcTwo = JSON.parse(result[2]);
                    calcThree = JSON.parse(result[3]);
                    calcFour = JSON.parse(result[4]);
                    calcFive = JSON.parse(result[5]);
                    calcSix = JSON.parse(result[6]);

                    // Initialize an object to store the smallest values and dates
                    let smallestValues = {
                        schema: {
                            fields: [
                                { name: 'index', type: 'datetime' },
                                { name: 'value', type: 'number' },
                            ],
                            primaryKey: ['index'],
                            pandas_version: '1.4.0',
                        },
                        data: [],
                    };

                    // Iterate over each field in the predict data
                    for (let field of predict.schema.fields) {
                        const category = field.name;

                        if (category !== 'index') {
                            // Find the minimum value and its date for each category
                            let minEntry = predict.data.reduce((min, entry) => {
                                const value = entry[category]; // Access the correct property
                                if (value < min.value) {
                                    return { value, index: entry.index };
                                } else {
                                    return min;
                                }
                            }, { value: Infinity, index: null });

                            // Add the smallest value and its date to the smallestValues object
                            smallestValues.data.push({ index: minEntry.index, value: minEntry.value });
                        }
                    }
                    // Print the result or use it as needed
                    console.log("Smallest Values and Dates:");
                    console.log(smallestValues);

                    console.log(smallestValues.data[0].value);
                    console.log(smallestValues.data[1].value);
                    console.log(smallestValues.data[2].value);
                    console.log(smallestValues.data[3].value);
                    console.log(smallestValues.data[4].value);
                    console.log(smallestValues.data[5].value);

                    newString = ''
                    alertString = ''
                    const existingDiv = document.getElementById('graph_box');
                    const newContainer = document.createElement("container");
                    newContainer.id = 'container';
                    newContainer.classList = 'newContainer'

                    document.body.appendChild(newContainer);
                 

                    if (smallestValues.data[0].value < 1039){
                        console.log("ALERT ACY INSERTS BELOW MINMUM THRESHOLD");
                        alertString = alertString +  "ALERT ACY INSERTS BELOW MINMUM THRESHOLD ";

                        // Create a new div element
                        const newDivOne = document.createElement('alertOne');
                        // Apply styles to the div
                        newDivOne.classList.add('alert');
                        // Set the text content of the new div
                        newDivOne.innerHTML = alertString;
                        newDivOne.id = 'alertOne'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivOne);
                    }

                    if (smallestValues.data[1].value < 8){
                        console.log("ALERT FILTER INSERTS BELOW MINMUM THRESHOLD");
                        alertString = ''
                        alertString = alertString +  "ALERT FILTER INSERTS BELOW MINMUM THRESHOLD";                        ;
                        // Create a new div element
                        const newDivTwo = document.createElement('alertTwo');
                        // Apply styles to the div
                        newDivTwo.classList.add('alert');
                        // Set the text content of the new div
                        newDivTwo.innerHTML = alertString;
                        newDivTwo.id = 'alertTwo'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivTwo);
                        
                    }
                    if (smallestValues.data[2].value < 21){
                        console.log("ALERT RS-Food BELOW MINMUM THRESHOLD");
                        alertString = ''
                        alertString = alertString +  "ALERT RS-Food BELOW MINMUM THRESHOLD ";
                        // Create a new div element
                        const newDivThree = document.createElement('alertThree');
                        // Apply styles to the div
                        newDivThree.classList.add('alert');
                        // Set the text content of the new div
                        newDivThree.innerHTML = alertString;
                        newDivThree.id = 'alertThree'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivThree);
                    }
                    if (smallestValues.data[3].value < 160){
                        console.log("ALERT US-FOOD BELOW MINMUM THRESHOLD");
                        alertString = ''
                        alertString = alertString +  "ALERT US-FOOD BELOW MINMUM THRESHOLD ";                        ;
                        // Create a new div element
                        const newDivFour = document.createElement('alertFour');
                        // Apply styles to the div
                        newDivFour.classList.add('alert');
                        // Set the text content of the new div
                        newDivFour.innerHTML = alertString;
                        newDivFour.id = 'alertFour'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivFour);
                    }
                    if (smallestValues.data[4].value < 28){
                        console.log("ALERT KTO BELOW MINMUM THRESHOLD");
                        alertString = ''
                        alertString = alertString +  "ALERT KTO BELOW MINMUM THRESHOLD";                        ;
                        // Create a new div element
                        const newDivFive = document.createElement('alertFive');
                        // Apply styles to the div
                        newDivFive.classList.add('alert');
                        // Set the text content of the new div
                        newDivFive.innerHTML = alertString;
                        newDivFive.id = 'alertFive'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivFive);
                        
                    }
                    if (smallestValues.data[5].value < 5){
                        console.log("ALERT PRETREAT TANKS BELOW MINMUM THRESHOLD");
                        alertString = ''
                        alertString = alertString +  "ALERT PRETREAT TANKS BELOW MINMUM THRESHOLD ";                        ;
                        // Create a new div element
                        const newDivSix = document.createElement('alertSix');
                        // Apply styles to the div
                        newDivSix.classList.add('alert');
                        // Set the text content of the new div
                        newDivSix.innerHTML = alertString;
                        newDivSix.id = 'alertSix'


                        // Insert the new div as a child of the pre-existing div
                        newContainer.appendChild(newDivSix);
                        
                    }

                    
                    

                    if (calcOne.USAGE_AVERAGE > calcOne.RESUPPLY_AVERAGE){

                        newString = newString + "ACY Inserts Usage WARNING Usage:" + calcOne.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcOne.RESUPPLY_AVERAGE.toFixed(2);

                    }

                    if (calcTwo.USAGE_AVERAGE > calcTwo.RESUPPLY_AVERAGE){

                        if(newString.length > 0){
                            newString = newString + "<br>Filter Inserts Usage WARNING Usage:" + calcTwo.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcTwo.RESUPPLY_AVERAGE.toFixed(2);
                        }

                        else {
                            newString = newString + "Filter Inserts Usage WARNING Usage:" + calcTwo.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcTwo.RESUPPLY_AVERAGE.toFixed(2);

                        }
    
                    }

                    if (calcThree.USAGE_AVERAGE > calcThree.RESUPPLY_AVERAGE){

                        if(newString.length > 0){
                            newString = newString + "<br>Food-RS Usage WARNING Usage:" + calcThree.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcThree.RESUPPLY_AVERAGE.toFixed(2);
                        }
    
                        else {
                            newString = newString + "Food-RS Usage WARNING Usage:" + calcThree.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcThree.RESUPPLY_AVERAGE.toFixed(2);
    
                        }
        
                    }


                    if (calcFour.USAGE_AVERAGE > calcFour.RESUPPLY_AVERAGE){

                        if(newString.length > 0){
                            newString = newString + "<br>Food-US Usage WARNING Usage:" + calcFour.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcFour.RESUPPLY_AVERAGE.toFixed(2);
                        }
    
                        else {
                            newString = newString + "Food-US Usage WARNING Usage:" + calcFour.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcFour.RESUPPLY_AVERAGE.toFixed(2);
    
                        }    
                    }

                    if (calcFive.USAGE_AVERAGE > calcFive.RESUPPLY_AVERAGE){

                        if(newString.length > 0){
                            newString = newString + "<br>KTO Usage WARNING Usage:" + calcFive.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcFive.RESUPPLY_AVERAGE.toFixed(2);
                        }
    
                        else {
                            newString = newString + "KTO Usage WARNING Usage:" + calcFive.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcFive.RESUPPLY_AVERAGE.toFixed(2);
    
                        }    
                    }

                    if (calcSix.USAGE_AVERAGE > calcSix.RESUPPLY_AVERAGE){

                        if(newString.length > 0){
                            newString = newString + "<br>Pretreat Tanks Usage WARNING Usage:" + calcSix.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcSix.RESUPPLY_AVERAGE.toFixed(2);
                        }
    
                        else {
                            newString = newString + "Pretreat Tanks Usage WARNING Usage:" + calcSix.USAGE_AVERAGE.toFixed(2) + " Resupply:" + calcSix.RESUPPLY_AVERAGE.toFixed(2);
    
                        }    
                    }
                        
        
                        
                    itemRate.innerHTML =   newString

                    console.log('Print results: ', predict);
                    console.log('print calOne: ', calcOne);

                    // Print the result or use it as needed
                    console.log("Smallest Values and Dates:");
                    console.log(smallestValues);
                
                
                
                     
                    // Extract data for plotting
                    const dates = predict.data.map(entry => entry.index.split('T')[0]);
                    const kto = predict.data.map(entry => entry.KTO);
                    const acyInserts = predict.data.map(entry => entry['ACY Inserts']);
                    const foodUS = predict.data.map(entry => entry['Food-US']);
                    const foodRS = predict.data.map(entry => entry['Food-RS']);
                    const pretreat = predict.data.map(entry => entry['Pretreat Tanks']);
                    const insertF = predict.data.map(entry => entry['Filter Inserts']);
                    

                    
                    // Sort the dates array
                    dates.sort((a, b) => new Date(a) - new Date(b));

                    // Create a Plotly plot using the extracted data
                    const data = [
                        {
                            x: dates,
                            y: kto,
                            type: 'scatter',
                            name: 'KTO',
                        },
                        {
                            x: dates,
                            y: foodUS,
                            type: 'scatter',
                            name: 'Food-US',
                        },
                        {
                            x: dates,
                            y: foodRS,
                            type: 'scatter',
                            name: 'Food-RS',
                        },
                        {
                            x: dates,
                            y: acyInserts,
                            type: 'scatter',
                            name: 'ACY Filters',
                        },
                        {
                            x: dates,
                            y: insertF,
                            type: 'scatter',
                            name: 'Insert Filters',
                        },
                        {
                            x: dates,
                            y: pretreat,
                            type: 'scatter',
                            name: 'Pretreat Tanks',
                        },
                    ];

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 20 },

                        shapes: [
                            // Add horizontal lines for thresholds
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 1039, y1: 1039, line: { color: 'red', width: 1, dash: 'dash' } },
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 8, y1: 8, line: { color: 'green', width: 1, dash: 'dash' } },
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 21, y1: 21, line: { color: 'blue', width: 1, dash: 'dash'} },
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 160, y1: 160, line: { color: 'orange', width: 1, dash: 'dash'} },
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 28, y1: 28, line: { color: 'purple', width: 1, dash: 'dash'} },
                            { type: 'line', visible: false, x0: dates[0], x1: dates[dates.length - 1], y0: 5, y1: 5, line: { color: 'brown', width: 1, dash: 'dash'} },
                        ],                 

                    };

                    layout.updatemenus = [
                        {
                            
                            direction: 'down',
                            pad: { r: 5, t: 5 },
                            showactive: true,
                            x: 0.1,
                            xanchor: 'left',
                            y: 1.1,
                            yanchor: 'top',
                            buttons: [
                                {
                                    args: [{ 'shapes[0].visible': layout.shapes[0].visible === false ? true : false }],
                                    label: 'ACY Inserts Threshold',
                                    method: 'relayout',
                                },
                                {
                                    args: [{ 'shapes[1].visible': layout.shapes[1].visible === false ? true : false }],
                                    label: 'Insert Filters Threshold',
                                    method: 'relayout',
                                },
                                { 
                                    args: [{ 'shapes[2].visible': layout.shapes[2].visible === false ? true : false }],
                                    label: 'Food-RS Threshold',
                                    method: 'relayout',
                                },
                                {
                                    args: [{ 'shapes[3].visible': layout.shapes[3].visible === false ? true : false }],
                                    label: 'Food-US Threshold',
                                    method: 'relayout',
                                },
                                {
                                    args: [{ 'shapes[4].visible': layout.shapes[4].visible === false ? true : false }],
                                    label: 'KTO Threshold',
                                    method: 'relayout',
                                },
                                {
                                    args: [{ 'shapes[5].visible': layout.shapes[5].visible === false ? true : false  }],
                                    label: 'Pretreat Tanks Threshold',
                                    method: 'relayout',
                                },

                                {
                                    args: [{ 'shapes[0].visible': false, 'shapes[1].visible': false, 'shapes[2].visible': false, 'shapes[3].visible': false, 'shapes[4].visible': false, 'shapes[5].visible': false   }],
                                    label: 'Toggle Thresholds',
                                    method: 'relayout',
                                },
                            ],
                        },
                    ];

                    Plotly.newPlot('tester', data, layout);

                    console.log('value: ', layout.shapes[0].line.visible);
                }

                else if (data == 'RS-Water')  {
                
                    result = JSON.parse(result);

                    // Extract data for plotting
                    const dates = result.data.map(entry => entry.index.split('T')[0]);
                    const potable = result.data.map(entry => entry.remaining_potableL);
                    const technical = result.data.map(entry => entry.technicalL);
                    const rodnik = result.data.map(entry => entry.rodnik_potableL);
                    

                    
                    // Create a Plotly plot using the extracted data
                    const data = [
                        
                        {
                            x: dates,
                            y:  potable,
                            type: 'scatter',
                            name: 'Potbale',
                        },

                        {
                            x: dates,
                            y:  technical,
                            type: 'scatter',
                            name: 'Technical',
                        },

                        

                        {
                            x: dates,
                            y:  rodnik,
                            type: 'scatter',
                            name: 'Rodnik',
                        },


                    ];

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 20 },
                    }; 

                    Plotly.newPlot('tester', data, layout);
                }

                else if (data == 'US-Water')  {
                    result = JSON.parse(result);

                     
                    // Extract data for plotting
                    const dates = result.data.map(entry => entry.index.split('T')[0]);
                    const potable = result.data.map(entry => entry.corrected_potableL);
                    const technical = result.data.map(entry => entry.corrected_technicalL);
                    

                    
                    // Create a Plotly plot using the extracted data
                    const data = [
                        
                        {
                            x: dates,
                            y:  potable,
                            type: 'scatter',
                            name: 'Potbale',
                        },

                        {
                            x: dates,
                            y:  technical,
                            type: 'scatter',
                            name: 'Technical',
                        },



                    ];

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 20 },
                    }; 

                    Plotly.newPlot('tester', data, layout);
                }
                
                else if (data == 'Gases')  {
                    result = JSON.parse(result);

                     
                    // Extract data for plotting
                    const dates = result.data.map(entry => entry.index.split('T')[0]);
                    const o2 = result.data.map(entry => entry.newO2kg);
                    const n2 = result.data.map(entry => entry.newN2kg);
                    

                    
                    // Create a Plotly plot using the extracted data
                    const data = [
                        
                        {
                            x: dates,
                            y:  o2,
                            type: 'scatter',
                            name: 'O2',
                        },

                        {
                            x: dates,
                            y:  n2,
                            type: 'scatter',
                            name: 'N2',
                        },



                    ];

                    const layout = {
                        xaxis: {
                            title: 'Date',
                        },
                        yaxis: {
                            title: 'Count',
                        },
                        margin: { t: 20 },
                    }; 

                    Plotly.newPlot('tester', data, layout);
                }
                    

                                        
            
            })
            .catch(error => {
                hideLoading()
                submitButton.disabled = false;
                consumptionButton.disabled = false;
                makePredictionsButton.disabled = false;
                console.error('Error:', error);
            });
    }

    fetchDataAndCreatePlot(data);
}