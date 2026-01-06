// Blood Stock Chart Component
const BloodStockChart = () => {
    const [stockData, setStockData] = React.useState([]);
    const chartRef = React.useRef(null);
    const chartInstance = React.useRef(null);

    React.useEffect(() => {
        fetchStockData();
        const interval = setInterval(fetchStockData, 30000); // Refresh every 30 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchStockData = async () => {
        try {
            const response = await fetch('/api/blood-stock');
            const data = await response.json();
            setStockData(data.stock);
        } catch (error) {
            console.error('Error fetching stock data:', error);
        }
    };

    React.useEffect(() => {
        if (stockData.length > 0 && chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            
            // Destroy existing chart if it exists
            if (chartInstance.current) {
                chartInstance.current.destroy();
            }

            // Create new chart
            chartInstance.current = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: stockData.map(s => s.blood_group),
                    datasets: [{
                        label: 'Units Available',
                        data: stockData.map(s => s.units),
                        backgroundColor: [
                            'rgba(220, 53, 69, 0.7)',
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(255, 159, 64, 0.7)',
                            'rgba(255, 205, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                            'rgba(201, 203, 207, 0.7)'
                        ],
                        borderColor: [
                            'rgba(220, 53, 69, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255, 205, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(201, 203, 207, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Blood Inventory by Type',
                            font: {
                                size: 16
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }

        return () => {
            if (chartInstance.current) {
                chartInstance.current.destroy();
            }
        };
    }, [stockData]);

    return (
        <div className="card shadow-sm">
            <div className="card-body">
                <div style={{ height: '300px' }}>
                    <canvas ref={chartRef}></canvas>
                </div>
            </div>
        </div>
    );
};

// Live Statistics Component
const LiveStats = () => {
    const [stats, setStats] = React.useState({
        total_donors: 0,
        total_requests: 0,
        pending_requests: 0,
        approved_requests: 0
    });
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 10000); // Refresh every 10 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchStats = async () => {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            setStats(data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching stats:', error);
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="text-center py-4">
                <div className="spinner-border text-danger" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="row g-3 mb-4">
            <div className="col-md-3">
                <div className="card text-white bg-primary shadow-sm">
                    <div className="card-body">
                        <h5 className="card-title">
                            <i className="bi bi-people-fill"></i> Total Donors
                        </h5>
                        <h2 className="mb-0">{stats.total_donors}</h2>
                        <small>Registered in system</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3">
                <div className="card text-white bg-info shadow-sm">
                    <div className="card-body">
                        <h5 className="card-title">
                            <i className="bi bi-file-medical"></i> Total Requests
                        </h5>
                        <h2 className="mb-0">{stats.total_requests}</h2>
                        <small>All time</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3">
                <div className="card text-white bg-warning shadow-sm">
                    <div className="card-body">
                        <h5 className="card-title">
                            <i className="bi bi-clock-history"></i> Pending
                        </h5>
                        <h2 className="mb-0">{stats.pending_requests}</h2>
                        <small>Awaiting approval</small>
                    </div>
                </div>
            </div>
            <div className="col-md-3">
                <div className="card text-white bg-success shadow-sm">
                    <div className="card-body">
                        <h5 className="card-title">
                            <i className="bi bi-check-circle"></i> Approved
                        </h5>
                        <h2 className="mb-0">{stats.approved_requests}</h2>
                        <small>Successfully processed</small>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Recent Donors Component
const RecentDonors = () => {
    const [donors, setDonors] = React.useState([]);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetchDonors();
        const interval = setInterval(fetchDonors, 15000); // Refresh every 15 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchDonors = async () => {
        try {
            const response = await fetch('/api/recent-donors');
            const data = await response.json();
            setDonors(data.donors);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching donors:', error);
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="text-center py-3"><div className="spinner-border text-danger"></div></div>;
    }

    return (
        <div className="card shadow-sm">
            <div className="card-header bg-danger text-white">
                <h5 className="mb-0">
                    <i className="bi bi-heart-pulse"></i> Recent Donors
                </h5>
            </div>
            <div className="card-body p-0">
                <div className="table-responsive">
                    <table className="table table-hover mb-0">
                        <thead className="table-light">
                            <tr>
                                <th>Name</th>
                                <th>Blood Group</th>
                                <th>City</th>
                                <th>Registered</th>
                            </tr>
                        </thead>
                        <tbody>
                            {donors.map(donor => (
                                <tr key={donor.id}>
                                    <td>{donor.full_name}</td>
                                    <td>
                                        <span className="badge bg-danger">{donor.blood_group}</span>
                                    </td>
                                    <td>{donor.city}</td>
                                    <td><small className="text-muted">{donor.created_at}</small></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

// Recent Requests Component
const RecentRequests = () => {
    const [requests, setRequests] = React.useState([]);
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        fetchRequests();
        const interval = setInterval(fetchRequests, 15000); // Refresh every 15 seconds
        return () => clearInterval(interval);
    }, []);

    const fetchRequests = async () => {
        try {
            const response = await fetch('/api/recent-requests');
            const data = await response.json();
            setRequests(data.requests);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching requests:', error);
            setLoading(false);
        }
    };

    const getStatusBadge = (status) => {
        const statusColors = {
            'Pending': 'warning',
            'Approved': 'success',
            'Rejected': 'danger'
        };
        return <span className={`badge bg-${statusColors[status] || 'secondary'}`}>{status}</span>;
    };

    if (loading) {
        return <div className="text-center py-3"><div className="spinner-border text-danger"></div></div>;
    }

    return (
        <div className="card shadow-sm">
            <div className="card-header bg-danger text-white">
                <h5 className="mb-0">
                    <i className="bi bi-file-earmark-medical"></i> Recent Blood Requests
                </h5>
            </div>
            <div className="card-body p-0">
                <div className="table-responsive">
                    <table className="table table-hover mb-0">
                        <thead className="table-light">
                            <tr>
                                <th>Patient</th>
                                <th>Hospital</th>
                                <th>Blood Group</th>
                                <th>Units</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {requests.map(request => (
                                <tr key={request.id}>
                                    <td>{request.patient_name}</td>
                                    <td>{request.hospital_name}</td>
                                    <td><span className="badge bg-danger">{request.blood_group}</span></td>
                                    <td>{request.units}</td>
                                    <td>{getStatusBadge(request.status)}</td>
                                    <td><small className="text-muted">{request.created_at}</small></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

// Main Dashboard App Component
const DashboardApp = () => {
    return (
        <>
            <LiveStats />
            <div className="row g-4 mb-4">
                <div className="col-lg-6">
                    <BloodStockChart />
                </div>
                <div className="col-lg-6">
                    <div className="card shadow-sm">
                        <div className="card-body">
                            <h5 className="card-title">
                                <i className="bi bi-bar-chart-fill text-danger"></i> Quick Stats
                            </h5>
                            <p className="text-muted">Real-time updates every few seconds</p>
                            <div className="alert alert-info">
                                <i className="bi bi-info-circle"></i> Dashboard updates automatically. 
                                No page refresh needed!
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="row g-4">
                <div className="col-lg-6">
                    <RecentDonors />
                </div>
                <div className="col-lg-6">
                    <RecentRequests />
                </div>
            </div>
        </>
    );
};
