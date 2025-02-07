document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // Llenar tarjetas
            document.getElementById('maxSaltos').innerHTML = `<h3>Máximos Saltos</h3><p>${data.max_saltos.registro}:<br> Cantidad: ${data.max_saltos.saltos}</p>`;
            document.getElementById('maxTiempoRespuesta').innerHTML = `<h3>Máxima Espera</h3><p>${data.max_tiempo_respuesta.registro}:<br> Tiempo: ${data.max_tiempo_respuesta.tiempo} ms</p>`;
            document.getElementById('minSaltos').innerHTML = `<h3>Mínimos Saltos</h3><p>${data.min_saltos.registro}:<br> Cantidad: ${data.min_saltos.saltos}</p>`;
            document.getElementById('minTiempoRespuesta').innerHTML = `<h3>Mínima Espera</h3><p>${data.min_tiempo_respuesta.registro}:<br> Tiempo: ${data.min_tiempo_respuesta.tiempo} ms</p>`;

            // Diagrama de dispersión
            const puntosMuertosPorRegistro = {};
            data.puntos_muertos.forEach(punto => {
                if (!puntosMuertosPorRegistro[punto.registro]) {
                    puntosMuertosPorRegistro[punto.registro] = 0;
                }
                puntosMuertosPorRegistro[punto.registro]++;
            });

            const scatterCtx = document.getElementById('scatterChart').getContext('2d');
            new Chart(scatterCtx, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Puntos Muertos por Registro',
                        data: Object.keys(puntosMuertosPorRegistro).map(registro => ({
                            x: registro,
                            y: puntosMuertosPorRegistro[registro]
                        })),
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            type: 'category',
                            title: {
                                display: true,
                                text: 'Registro'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Número de Puntos Muertos'
                            }
                        }
                    }
                }
            });

            // Diagrama de Doughnut
            const doughnutCtx = document.getElementById('doughnutChart').getContext('2d');
            new Chart(doughnutCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(data.puntos_muertos_por_continente),
                    datasets: [{
                        label: 'Puntos Muertos por Continente',
                        data: Object.values(data.puntos_muertos_por_continente),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    plugins: {
                        datalabels: {
                            color: 'rgb(72, 72, 72)',
                            formatter: (value, context) => {
                                return value;
                            }
                        }
                    }
                },
                plugins: [ChartDataLabels]
            });

            // Diagrama de Barras para Saltos por Continente
            const barSaltosCtx = document.getElementById('barChartSaltos').getContext('2d');
            new Chart(barSaltosCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.saltos_por_continente),
                    datasets: [{
                        label: 'Saltos por Continente',
                        data: Object.values(data.saltos_por_continente),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Diagrama de Barras para Tiempo de Respuesta por Continente
            const barTiempoCtx = document.getElementById('barChartTiempo').getContext('2d');
            new Chart(barTiempoCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(data.tiempo_respuesta_por_continente),
                    datasets: [{
                        label: 'Tiempo de Respuesta por Continente (ms)',
                        data: Object.values(data.tiempo_respuesta_por_continente),
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));

    // Exportar a PDF
    document.getElementById('exportPdf').addEventListener('click', function () {
        const element = document.getElementById('main-content'); // Selecciona el contenedor específico
    
        // Configuración de html2canvas para capturar todo el contenido del contenedor
        html2canvas(element, {
            scrollY: -window.scrollY, // Ajusta el scroll para capturar todo el contenido
            windowHeight: element.scrollHeight, // Establece la altura del contenedor
            useCORS: true, // Permite el uso de recursos externos (si es necesario)
            allowTaint: true, // Permite el uso de imágenes externas (si es necesario)
        }).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jspdf.jsPDF('p', 'mm', 'a4');
            const imgWidth = 210; // Ancho de A4 en mm
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
            // Añade la imagen al PDF
            pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
            
            // Guarda el PDF
            pdf.save('informe.pdf');
        });
    });
});