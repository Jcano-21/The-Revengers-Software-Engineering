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
                    itemRate.textContent = 'A_Rate: ' + df5Data.rate.toFixed(4) + ' C_Rate: ' + df5Data.calculated_rate.toFixed(4) + ' P_Diff: '  + df5Data.Percent_Difference.toFixed(3) 
                    + '\n\n' + 'A_RateTech: ' + df5Data.rateTech.toFixed(4) + ' C_RateTech: ' + df5Data.calculated_rate_tech.toFixed(4) + ' P_Diff: '  + df5Data.Percent_DifferenceTech.toFixed(3) ;
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
                if ((data !== 'US-Water') && (data !== 'RS-Water') && (data !== 'Gases') ) {
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
            else {
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
                itemRate.textContent = 'Category: ' + df1Data + ' Rate_Pot_AVG: ' + df2Data.toFixed(4) + ' P_Diff_Pot: '  + df3Data.toFixed(3) 
                +  'Rate_Tech_AVG: ' + df4Data.toFixed(4) + ' P_Diff_Tech: ' + df5Data.toFixed(4) + ' Usage_Pot: '  + df6Data.toFixed(3) 
                + ' Usage_Tech: ' + df7Data.toFixed(4) + ' Usage_Rod: ' + df12Data.toFixed(4) + ' Resupply_Pot: ' + df8Data.toFixed(4) + ' Resupply_Tech: ' + df9Data.toFixed(4) + ' Resupply_Rod: ' + df10Data.toFixed(5) + ' Days_Between_Resupply_AVG: ' + df11Data.toFixed(4);
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
                result = JSON.parse(result);

                console.log('Print results: ', result);
            
                if (data == 'All')  {
                
                     
                    // Extract data for plotting
                    const dates = result.data.map(entry => entry.index.split('T')[0]);
                    const kto = result.data.map(entry => entry.KTO);
                    const acyInserts = result.data.map(entry => entry['ACY Inserts']);
                    const foodUS = result.data.map(entry => entry['Food-US']);
                    const foodRS = result.data.map(entry => entry['Food-RS']);
                    const pretreat = result.data.map(entry => entry['Pretreat Tanks']);
                    const insertF = result.data.map(entry => entry['Insert Filters']);
                    

                    
                    // Create a Plotly plot using the extracted data
                    const data = [
                        
                        {
                            x: dates,
                            y:  kto,
                            type: 'scatter',
                            name: 'KTO',
                        },

                        {
                            x: dates,
                            y:  foodUS,
                            type: 'scatter',
                            name: 'Food-US',
                        },

                        {
                            x: dates,
                            y:  foodRS,
                            type: 'scatter',
                            name: 'Food-RS',
                        },

                        {
                            x: dates,
                            y:  acyInserts,
                            type: 'scatter',
                            name: 'ACY Filters',
                        },

                        {
                            x: dates,
                            y:  insertF,
                            type: 'scatter',
                            name: 'Insert Filters',
                        },

                        {
                            x: dates,
                            y:  pretreat,
                            type: 'scatter',
                            name: 'Pretreat Tanks',
                        }
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