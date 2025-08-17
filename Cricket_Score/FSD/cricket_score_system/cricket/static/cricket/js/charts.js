// cricket/static/cricket/js/charts.js

let runRateChartInstance; // Variable to hold the Chart.js instance

/**
 * Gets the appropriate color based on the current theme (light/dark).
 * @param {string} lightColor - Color for light mode.
 * @param {string} darkColor - Color for dark mode.
 * @returns {string} The selected color.
 */
function getThemeColor(lightColor, darkColor) {
    const htmlElement = document.documentElement;
    return htmlElement.classList.contains('dark') ? darkColor : lightColor;
}

/**
 * Initializes or updates the run rate chart.
 * @param {object|string} graphData - The data for the chart, typically containing labels and datasets.
 * Can be a JSON string from Django template |safe.
 */
function initializeOrUpdateRunRateChart(graphData) {
    const ctx = document.getElementById('runRateChart');
    if (!ctx) {
        console.error("Canvas element with ID 'runRateChart' not found.");
        return;
    }

    // Parse graphData if it's a string (e.g., from Django template |safe)
    let parsedGraphData = graphData;
    if (typeof graphData === 'string') {
        try {
            parsedGraphData = JSON.parse(graphData);
        } catch (e) {
            console.error("Error parsing graph data for chart:", e);
            return;
        }
    }

    // Ensure parsedGraphData has the expected structure
    // The match_detail view needs to pass graph_data in this format:
    // { labels: [...], datasets: [{ label: "Run Rate", data: [...] }] }
    if (!parsedGraphData || !parsedGraphData.labels || !parsedGraphData.datasets) {
        console.warn("Invalid graph data received for run rate chart. Expected 'labels' and 'datasets'.");
        return;
    }

    // If a chart instance already exists, destroy it before creating a new one
    if (runRateChartInstance) {
        runRateChartInstance.destroy();
    }

    runRateChartInstance = new Chart(ctx, {
        type: 'line', // Line chart for run rate
        data: {
            labels: parsedGraphData.labels,
            datasets: parsedGraphData.datasets.map(dataset => ({
                label: dataset.label,
                data: dataset.data,
                // Apply theme-aware colors
                borderColor: dataset.borderColor || getThemeColor('#3b82f6', '#60a5fa'), // blue-600 / blue-400
                backgroundColor: dataset.backgroundColor || getThemeColor('rgba(59, 130, 246, 0.2)', 'rgba(96, 165, 250, 0.2)'),
                tension: 0.3, // Smoother lines
                fill: true,
                pointBackgroundColor: dataset.pointBackgroundColor || getThemeColor('#1d4ed8', '#93c5fd'), // blue-800 / blue-300
                pointBorderColor: getThemeColor('#fff', '#374151'), // white / gray-700
                pointHoverRadius: 6,
                pointHoverBackgroundColor: getThemeColor('#fff', '#374151'),
                pointHoverBorderColor: dataset.borderColor || getThemeColor('#3b82f6', '#60a5fa'),
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Allows canvas to fill container
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        color: getThemeColor('#333', '#e5e7eb') // Dark gray / Light gray for legend text
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw} runs`;
                        }
                    },
                    backgroundColor: getThemeColor('rgba(0,0,0,0.8)', 'rgba(255,255,255,0.8)'), // Dark/Light background for tooltip
                    titleColor: getThemeColor('#fff', '#1f2937'), // White/Dark text for tooltip title
                    bodyColor: getThemeColor('#fff', '#1f2937'), // White/Dark text for tooltip body
                    padding: 10,
                    borderRadius: 8
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Overs',
                        color: getThemeColor('#555', '#cbd5e1'), // Dark gray / Light gray for axis title
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: false // Hide vertical grid lines
                    },
                    ticks: {
                        color: getThemeColor('#666', '#9ca3af') // Gray / Darker gray for axis ticks
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Run Rate',
                        color: getThemeColor('#555', '#cbd5e1'), // Dark gray / Light gray for axis title
                        font: {
                            size: 16,
                            weight: 'bold'
                        }
                    },
                    beginAtZero: true,
                    grid: {
                        color: getThemeColor('rgba(0, 0, 0, 0.05)', 'rgba(255, 255, 255, 0.1)') // Light/Dark transparent grid lines
                    },
                    ticks: {
                        color: getThemeColor('#666', '#9ca3af') // Gray / Darker gray for axis ticks
                    }
                }
            },
            animation: {
                duration: 1000, // General animation time
                easing: 'easeInOutQuad' // Easing function
            }
        }
    });
}

// Expose the update function globally for use in match_detail.html
// This function will re-initialize the chart with new data, adapting to theme.
window.updateChart = function(newGraphData) {
    initializeOrUpdateRunRateChart(newGraphData);
};

// Initialize chart when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    const chartCanvas = document.getElementById('runRateChart');
    if (chartCanvas) {
        const graphData = chartCanvas.dataset.graphData;
        if (graphData) {
            initializeOrUpdateRunRateChart(graphData);
        }
    }

    // Listen for theme changes (from base.html's script)
    // This will redraw the chart with updated colors if the theme changes
    const htmlElement = document.documentElement;
    const observer = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (runRateChartInstance) {
                    // Update chart colors without destroying and recreating
                    runRateChartInstance.options.plugins.legend.labels.color = getThemeColor('#333', '#e5e7eb');
                    runRateChartInstance.options.scales.x.title.color = getThemeColor('#555', '#cbd5e1');
                    runRateChartInstance.options.scales.x.ticks.color = getThemeColor('#666', '#9ca3af');
                    runRateChartInstance.options.scales.y.title.color = getThemeColor('#555', '#cbd5e1');
                    runRateChartInstance.options.scales.y.ticks.color = getThemeColor('#666', '#9ca3af');
                    runRateChartInstance.options.scales.y.grid.color = getThemeColor('rgba(0, 0, 0, 0.05)', 'rgba(255, 255, 255, 0.1)');

                    runRateChartInstance.data.datasets.forEach(dataset => {
                        dataset.borderColor = getThemeColor('#3b82f6', '#60a5fa');
                        dataset.backgroundColor = getThemeColor('rgba(59, 130, 246, 0.2)', 'rgba(96, 165, 250, 0.2)');
                        dataset.pointBackgroundColor = getThemeColor('#1d4ed8', '#93c5fd');
                        dataset.pointBorderColor = getThemeColor('#fff', '#374151');
                        dataset.pointHoverBorderColor = getThemeColor('#3b82f6', '#60a5fa');
                    });

                    // Tooltip colors need to be updated directly in options.plugins.tooltip
                    runRateChartInstance.options.plugins.tooltip.backgroundColor = getThemeColor('rgba(0,0,0,0.8)', 'rgba(255,255,255,0.8)');
                    runRateChartInstance.options.plugins.tooltip.titleColor = getThemeColor('#fff', '#1f2937');
                    runRateChartInstance.options.plugins.tooltip.bodyColor = getThemeColor('#fff', '#1f2937');


                    runRateChartInstance.update(); // Re-render the chart to apply new colors
                }
            }
        }
    });

    observer.observe(htmlElement, { attributes: true }); // Observe changes to the 'class' attribute on <html>
});
