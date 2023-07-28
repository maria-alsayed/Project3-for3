// Function to fetch data from the Flask backend
async function fetchData() {
    const response = await fetch('/static/data.json')
    const data = await response.json();
    console.log('Data:', data);

    // Verify the data structure
    if (!Array.isArray(data) || data.length === 0 || !('team_id' in data[0]) || !('team_data' in data[0])) {
        console.error('Invalid data structure from the Flask backend.');
        return null;
    }

    // Verify data structure for each team_data
    for (const team of data) {
        if (!Array.isArray(team.team_data) || team.team_data.length === 0) {
            console.error('Invalid data structure for team_data.');
            return null;
        }
    }

    return data;
}

// Function to render the bar chart
async function renderChart() {
    const data = await fetchData();

    // Check if data is available
    if (!data) {
        return;
    }

    const options = {
        chart: {
            type: 'bar',
        },
        series: data.map(team => ({
            name: `Team ID: ${team.team_id}`,
            data: team.team_data.map(row => row.three_point_percentage),
        })),
        xaxis: {
            categories: data[0].team_data.map(row => row.year),
        },
    };

    const chart = new ApexCharts(document.querySelector('#chart-container'), options);
    chart.render();
}

renderChart();
