document.addEventListener('DOMContentLoaded', function () {

    /* --- THEME SWITCHER --- */
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    const savedTheme = localStorage.getItem('myopia-theme');
    if (savedTheme) {
        body.className = savedTheme;
        themeToggle.checked = savedTheme === 'light-theme';
    } else {
        // Default to dark theme if nothing is saved
        body.className = 'dark-theme';
        themeToggle.checked = false;
    }

    themeToggle.addEventListener('change', () => {
        if (body.classList.contains('dark-theme')) {
            body.className = 'light-theme';
            localStorage.setItem('myopia-theme', 'light-theme');
        } else {
            body.className = 'dark-theme';
            localStorage.setItem('myopia-theme', 'dark-theme');
        }
        // Redraw charts on theme change to update colors
        myopiaChart.destroy();
        riskFactorChart.destroy();
        initCharts();
    });

    /* --- CHART.JS SETUP & 3D BAR CHART --- */

    // Custom controller for 3D Bar chart
    class Bar3DController extends Chart.controllers.bar {
        draw() {
            const chart = this.chart;
            const { ctx } = chart;
            const vm = this._view;
            let { x, y, base, width } = vm;

            const topHeight = 10; // Height of the 3D top part
            const sideWidth = 10; // Width of the 3D side part

            ctx.save();

            // Front face
            ctx.fillStyle = vm.backgroundColor;
            ctx.fillRect(x - width / 2, y, width, base - y);
            
            // Top face
            ctx.fillStyle = Chart.helpers.color(vm.backgroundColor).lighten(0.15).rgbString();
            ctx.beginPath();
            ctx.moveTo(x - width / 2, y);
            ctx.lineTo(x - width / 2 + sideWidth, y - topHeight);
            ctx.lineTo(x + width / 2 + sideWidth, y - topHeight);
            ctx.lineTo(x + width / 2, y);
            ctx.closePath();
            ctx.fill();

            // Side face
            ctx.fillStyle = Chart.helpers.color(vm.backgroundColor).darken(0.15).rgbString();
            ctx.beginPath();
            ctx.moveTo(x + width / 2, y);
            ctx.lineTo(x + width / 2 + sideWidth, y - topHeight);
            ctx.lineTo(x + width / 2 + sideWidth, base - topHeight);
            ctx.lineTo(x + width / 2, base);
            ctx.closePath();
            ctx.fill();

            ctx.restore();
        }
    }

    Bar3DController.id = 'bar3d';
    Bar3DController.defaults = Chart.controllers.bar.defaults;
    Chart.register(Bar3DController);

    let myopiaChart, riskFactorChart;
    
    function getChartColors() {
        const isLightTheme = body.classList.contains('light-theme');
        return {
            gridColor: isLightTheme ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.05)',
            tickColor: isLightTheme ? '#6e6e73' : '#a1a1a6',
            primaryAccent: isLightTheme ? '#0066CC' : '#0A84FF',
        };
    }

    function initCharts() {
        const colors = getChartColors();
        
        // Myopia Progression Chart - 3D Bar
        const myopiaCtx = document.getElementById('myopiaChart').getContext('2d');
        myopiaChart = new Chart(myopiaCtx, {
            type: 'bar3d',
            data: {
                labels: ['2020', '2021', '2022', '2023', '2024', '2025'],
                datasets: [{
                    label: 'Myopia Progression (D)',
                    data: [-0.5, -0.75, -1.0, -1.25, -1.5, -2.25],
                    backgroundColor: colors.primaryAccent,
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: colors.gridColor },
                        ticks: { color: colors.tickColor, font: { family: 'Inter' } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: colors.tickColor, font: { family: 'Inter' } }
                    }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false } // Disable default tooltip for 3D effect
                }
            }
        });

        // Risk Factor Chart - Doughnut
        const riskFactorCtx = document.getElementById('riskFactorChart').getContext('2d');
        riskFactorChart = new Chart(riskFactorCtx, {
            type: 'doughnut',
            data: {
                labels: ['Genetics', 'Screen Time', 'Outdoor Activity', 'Near Work', 'Lighting'],
                datasets: [{
                    data: [40, 25, 15, 10, 10],
                    backgroundColor: ['#0A84FF', '#FF375F', '#32D74B', '#FF9F0A', '#BF5AF2'],
                    borderColor: body.classList.contains('light-theme') ? '#ffffff' : '#1a1a1a',
                    borderWidth: 4,
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: colors.tickColor,
                            padding: 20,
                            font: { size: 12, family: 'Inter' }
                        }
                    }
                }
            }
        });
    }


    /* --- LIVE DATA SIMULATION --- */
    function updateData() {
        // Update prescription
        let currentPrescription = parseFloat(myopiaChart.data.datasets[0].data.slice(-1)[0]);
        let change = (Math.random() * 0.05 - 0.02).toFixed(2);
        currentPrescription -= change;
        
        myopiaChart.data.datasets[0].data.push(currentPrescription.toFixed(2));
        myopiaChart.data.labels.push(new Date().getFullYear() + 1); 
        // a bit of a hack to extend years, in a real app this logic would be better
        if (myopiaChart.data.datasets[0].data.length > 8) {
             myopiaChart.data.datasets[0].data.shift();
             myopiaChart.data.labels.shift();
        }
        myopiaChart.update();
        document.getElementById('prescription').textContent = `${currentPrescription.toFixed(2)} D`;

        // Update other cards with random data
        let outdoorTime = (Math.random() * 2 + 1).toFixed(1);
        document.getElementById('outdoor-time').textContent = `${outdoorTime}h/day`;
        
        let screenTime = (Math.random() * 3 + 5).toFixed(1);
        document.getElementById('screen-time').textContent = `${screenTime}h/day`;

        // Animate the change
        const changedElements = ['prescription', 'outdoor-time', 'screen-time'];
        changedElements.forEach(id => {
            const el = document.getElementById(id);
            el.style.transition = 'none';
            el.style.transform = 'translateY(5px)';
            el.style.opacity = '0';
            setTimeout(() => {
                el.style.transition = 'all 0.3s ease';
                el.style.transform = 'translateY(0)';
                el.style.opacity = '1';
            }, 50);
        });

    }

    // Initialize charts and start simulation
    initCharts();
    setInterval(updateData, 5000); // Update data every 5 seconds
});
